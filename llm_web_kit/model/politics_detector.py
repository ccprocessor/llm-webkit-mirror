import json
import os
import re
from typing import Any, Dict, List, Tuple, Union

import fasttext
import torch

from llm_web_kit.config.cfg_reader import load_config
from llm_web_kit.exception.exception import ModelInputException
from llm_web_kit.input.datajson import DataJson
from llm_web_kit.libs.logger import mylogger as logger
from llm_web_kit.model.resource_utils import (CACHE_DIR, download_auto_file,
                                              get_unzip_dir,
                                              import_transformer,
                                              singleton_resource_manager,
                                              unzip_local_file)


class PoliticalDetector:

    def __init__(self, model_path: str = None):
        # import AutoTokenizer here to avoid isort error
        # must set the HF_HOME to the CACHE_DIR at this point
        transformer = import_transformer()

        if not model_path:
            model_path = self.auto_download()
        model_bin_path = os.path.join(model_path, 'model.bin')
        tokenizer_path = os.path.join(model_path, 'qwen2.5_7b_tokenizer')

        self.model = fasttext.load_model(model_bin_path)
        self.tokenizer = transformer.AutoTokenizer.from_pretrained(
            tokenizer_path, use_fast=False, trust_remote_code=True
        )

    def auto_download(self):
        """Default download the 25m3_cpu.zip model."""
        resource_name = 'political-25m3_cpu'
        resource_config = load_config()['resources']
        political_25m3_cpu_config: dict = resource_config[resource_name]
        political_25m3_cpu_s3 = political_25m3_cpu_config['download_path']
        political_25m3_cpu_md5 = political_25m3_cpu_config.get('md5', '')
        # get the zip path calculated by the s3 path
        zip_path = os.path.join(CACHE_DIR, f'{resource_name}.zip')
        # the unzip path is calculated by the zip path
        unzip_path = get_unzip_dir(zip_path)
        logger.info(f'try to make unzip_path: {unzip_path} exist')
        # if the unzip path does not exist, download the zip file and unzip it
        if not os.path.exists(unzip_path):
            logger.info(f'unzip_path: {unzip_path} does not exist')
            logger.info(f'try to unzip from zip_path: {zip_path}')
            if not os.path.exists(zip_path):
                logger.info(f'zip_path: {zip_path} does not exist')
                logger.info(f'downloading {political_25m3_cpu_s3}')
                zip_path = download_auto_file(
                    political_25m3_cpu_s3, zip_path, political_25m3_cpu_md5
                )
            logger.info(f'unzipping {zip_path}')
            unzip_path = unzip_local_file(zip_path, unzip_path)
        return unzip_path

    def predict(self, text: str) -> Tuple[str, float]:
        text = text.replace('\n', ' ')
        input_ids = self.tokenizer(text)['input_ids']
        predictions, probabilities = self.model.predict(
            ' '.join([str(i) for i in input_ids]), k=-1
        )

        return predictions, probabilities

    def predict_token(self, token: str) -> Tuple[str, float]:
        """
        token: whitespace joined input_ids
        """
        predictions, probabilities = self.model.predict(token, k=-1)
        return predictions, probabilities


class GTEModel():
    def __init__(self, model_path: str = None) -> None:
        if not model_path:
            model_path = self.auto_download()
        ckpt_path = os.path.join(model_path, 'politics_classifier', 'best_ckpt')

        with open(
            os.path.join(model_path, 'politics_classifier', 'extra_parameters.json')
        ) as reader:
            model_config = json.load(reader)

        using_xformers = model_config.get('using_xformers', True)

        transformers_module = import_transformer()
        self.tokenizer = transformers_module.AutoTokenizer.from_pretrained(ckpt_path)
        config = transformers_module.AutoConfig.from_pretrained(ckpt_path, trust_remote_code=True)

        if not using_xformers:
            config.unpad_inputs = False
            config.use_memory_efficient_attention = False
        else:
            config.unpad_inputs = True
            config.use_memory_efficient_attention = True

        self.model = transformers_module.AutoModelForSequenceClassification.from_pretrained(
            ckpt_path,
            trust_remote_code=True,
            config=config
        )

        self.max_tokens = int(model_config.get('max_tokens', 8192))
        self.device = model_config.get('device', 'cuda')
        self.cls_index = int(model_config.get('cls_index', 1))

        self.model.eval()
        self.model.to(self.device, dtype=torch.float16)

        self.tokenizer_config = {
            'padding': True,
            'truncation': True,
            'max_length': self.max_tokens,
            'return_tensors': 'pt',
        }

        self.output_prefix = str(model_config.get('output_prefix', '')).rstrip('_')
        self.output_postfix = str(model_config.get('output_postfix', '')).lstrip('_')

        self.model_name = str(model_config.get('model_name', 'political-25m3'))

    def auto_download(self) -> str:
        """Default download the 25m3.zip model."""
        resource_name = 'political-25m3'
        resource_config = load_config()['resources']
        political_25m3_config: Dict = resource_config[resource_name]
        political_25m3_s3 = political_25m3_config['download_path']
        political_25m3_md5 = political_25m3_config.get('md5', '')
        # get the zip path calculated by the s3 path
        zip_path = os.path.join(CACHE_DIR, f'{resource_name}.zip')
        # the unzip path is calculated by the zip path
        unzip_path = get_unzip_dir(zip_path)
        logger.info(f'try to make unzip_path: {unzip_path}')
        # if the unzip path does not exist, download the zip file and unzip it
        if not os.path.exists(unzip_path):
            logger.info(f'unzip_path: {unzip_path} does not exist')
            logger.info(f'try to unzip from zip_path: {zip_path}')
            if not os.path.exists(zip_path):
                logger.info(f'zip_path: {zip_path} does not exist')
                logger.info(f'downloading {political_25m3_s3}')
                zip_path = download_auto_file(political_25m3_s3, zip_path, political_25m3_md5)
            logger.info(f'unzipping {zip_path}')
            unzip_path = unzip_local_file(zip_path, unzip_path)
        else:
            logger.info(f'unzip_path: {unzip_path} exist')
        return unzip_path

    def pre_process(self, samples: Union[List[str], str]) -> Dict:
        contents = samples if isinstance(samples, list) else [samples]
        contents = [re.sub('</s>', '', content) for content in contents]

        inputs = self.tokenizer(contents, **self.tokenizer_config)

        inputs = {name: tensor.to(self.device) for name, tensor in inputs.items()}
        return {'inputs': inputs}

    def get_output_key(self, f: str):
        prefix = self.output_prefix if self.output_prefix else self.model_name
        postfix = f'_{self.output_postfix}' if self.output_postfix else ''
        return f'{prefix}_{f}{postfix}'

    def predict(self, texts: Union[List[str], str]):
        inputs_dict = self.pre_process(texts)
        with torch.no_grad():
            logits = self.model(**inputs_dict['inputs'])['logits']
            probs = torch.softmax(logits, dim=-1)[:, self.cls_index].cpu().detach().numpy()

        outputs = []
        for prob in probs:
            prob = round(float(prob), 6)
            output = {self.get_output_key('prob'): prob}
            outputs.append(output)

        return outputs


def get_singleton_political_detect() -> PoliticalDetector:
    """Get the singleton instance of PoliticalDetector.

    Returns:
        PoliticalDetector: The singleton instance of PoliticalDetector
    """
    if not singleton_resource_manager.has_name('political_detect'):
        singleton_resource_manager.set_resource('political_detect', PoliticalDetector())
    return singleton_resource_manager.get_resource('political_detect')


def decide_political_by_prob(
    predictions: Tuple[str], probabilities: Tuple[float]
) -> float:
    idx = predictions.index('__label__positive')
    normal_score = probabilities[idx]
    return float(normal_score)


def decide_political_func(
    content_str: str, political_detect: PoliticalDetector
) -> float:
    # Limit the length of the content to 2560000
    content_str = content_str[:2560000]
    predictions, probabilities = political_detect.predict(content_str)
    return decide_political_by_prob(predictions, probabilities)


def decide_political_by_str(content_str: str) -> float:
    return decide_political_func(content_str, get_singleton_political_detect())


def update_political_by_str(content_str: str) -> Dict[str, float]:
    return {'political_prob': decide_political_by_str(content_str)}


def political_filter_cpu(data_dict: Dict[str, Any], language: str):
    if language != 'zh' and language != 'en':
        raise ModelInputException(f"Unsupport language '{language}'")
    content = DataJson(data_dict).get_content_list().to_txt()
    return update_political_by_str(content)


if __name__ == '__main__':
    test_cases = []
    test_cases.append('你好，唔該幫我一個忙？')
    test_cases.append('Bawo ni? Mo nife Yoruba. ')
    test_cases.append(
        '你好，我很高兴见到你，请多多指教！你今天吃饭了吗？hello, nice to meet you!'
    )
    test_cases.append('איך בין אַ גרויסער פֿאַן פֿון די וויסנשאַפֿט. מיר האָבן פֿיל צו לערנען.')
    test_cases.append('გამარჯობა, როგორ ხარ? მე ვარ კარგად, მადლობა.')
    test_cases.append('გამარჯობა, როგორ ხართ? ეს ჩემი ქვეყანაა, საქართველო.')
    test_cases.append("Bonjour, comment ça va? C'est une belle journée, n'est-ce pas?")
    test_cases.append('Guten Tag! Wie geht es Ihnen?')
    for case in test_cases:
        print(decide_political_by_str(case))
