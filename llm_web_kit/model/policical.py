import os
from typing import Any, Dict, Tuple

import fasttext

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
        tokenizer_path = os.path.join(model_path, 'internlm2-chat-20b')

        self.model = fasttext.load_model(model_bin_path)
        self.tokenizer = transformer.AutoTokenizer.from_pretrained(
            tokenizer_path, use_fast=False, trust_remote_code=True
        )

    def auto_download(self):
        """Default download the 24m7.zip model."""
        resource_name = 'political-24m7'
        resource_config = load_config()['resources']
        political_24m7_config: dict = resource_config[resource_name]
        political_24m7_s3 = political_24m7_config['download_path']
        political_24m7_md5 = political_24m7_config.get('md5', '')
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
                logger.info(f'downloading {political_24m7_s3}')
                zip_path = download_auto_file(
                    political_24m7_s3, zip_path, political_24m7_md5
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
    idx = predictions.index('__label__normal')
    normal_score = probabilities[idx]
    return normal_score


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
    test_cases.append('你好，我很高兴见到你！')
    test_cases.append('hello, nice to meet you!')
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
