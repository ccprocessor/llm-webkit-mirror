import json
import os
from typing import Dict, List, Union

import torch

from llm_web_kit.config.cfg_reader import load_config
from llm_web_kit.libs.logger import mylogger as logger
from llm_web_kit.model.resource_utils import (CACHE_DIR, download_auto_file,
                                              get_unzip_dir,
                                              import_transformer,
                                              unzip_local_file)

# from transformers import AutoModelForSequenceClassification, AutoTokenizer


class BertModel:
    def __init__(self, model_path: str = None) -> None:
        if not model_path:
            model_path = self.auto_download()
        transformers_module = import_transformer()
        self.model = transformers_module.AutoModelForSequenceClassification.from_pretrained(
            os.path.join(model_path, 'porn_classifier/classifier_hf')
        )
        with open(
            os.path.join(model_path, 'porn_classifier/extra_parameters.json')
        ) as reader:
            model_config = json.load(reader)

        self.cls_index = int(model_config.get('cls_index', 1))
        self.use_sigmoid = bool(model_config.get('use_sigmoid', False))
        self.max_tokens = int(model_config.get('max_tokens', 512))
        self.remain_tail = min(
            self.max_tokens - 1, int(model_config.get('remain_tail', -1))
        )
        self.device = model_config.get('device', 'cpu')

        self.model.eval()
        self.model.to(self.device, dtype=torch.float16)

        if hasattr(self.model, 'to_bettertransformer'):
            self.model = self.model.to_bettertransformer()

        self.tokenizer = transformers_module.AutoTokenizer.from_pretrained(
            os.path.join(model_path, 'porn_classifier/classifier_hf')
        )
        self.tokenizer_config = {
            'padding': True,
            'truncation': self.remain_tail <= 0,
            'max_length': self.max_tokens if self.remain_tail <= 0 else None,
            'return_tensors': 'pt' if self.remain_tail <= 0 else None,
        }

        self.output_prefix = str(model_config.get('output_prefix', '')).rstrip('_')
        self.output_postfix = str(model_config.get('output_postfix', '')).lstrip('_')

        self.model_name = str(model_config.get('model_name', 'porn-23w44'))

    def auto_download(self) -> str:
        """Default download the 23w44.zip model."""
        resource_name = 'porn-23w44'
        resource_config = load_config()['resources']
        porn_23w44_config: Dict = resource_config[resource_name]
        porn_23w44_s3 = porn_23w44_config['download_path']
        porn_23w44_md5 = porn_23w44_config.get('md5', '')
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
                logger.info(f'downloading {porn_23w44_s3}')
                zip_path = download_auto_file(porn_23w44_s3, zip_path, porn_23w44_md5)
            logger.info(f'unzipping {zip_path}')
            unzip_path = unzip_local_file(zip_path, unzip_path)
        else:
            logger.info(f'unzip_path: {unzip_path} exist')
        return unzip_path

    def pre_process(self, samples: Union[List[str], str]) -> Dict:
        contents = samples if isinstance(samples, list) else [samples]

        inputs = self.tokenizer(contents, **self.tokenizer_config)
        # self.remain_tail>0时，才需要对输入进行额外处理
        if self.remain_tail > 0:
            processed_inputs = []

            # 对每个输入进行处理
            for tokens_id in inputs['input_ids']:
                # 通过sep_token_id找到tokens的长度
                length = tokens_id.index(self.tokenizer.sep_token_id) + 1
                # 如果tokens的长度小于等于max_tokens，则直接在尾部补0，不需要截断
                if length <= self.max_tokens:
                    tokens = tokens_id[:length] + [self.tokenizer.pad_token_id] * (
                        self.max_tokens - length
                    )
                    attn = [1] * length + [0] * (self.max_tokens - length)
                # 如果tokens的长度大于max_tokens，则需要取头部max_tokens-remain_tail个tokens和尾部remain_tail个tokens
                else:
                    head_length = self.max_tokens - self.remain_tail
                    tail_length = self.remain_tail
                    tokens = (
                        tokens_id[:head_length]
                        + tokens_id[length - tail_length : length]
                    )
                    attn = [1] * self.max_tokens

                # 将处理后的tokens添加到新的inputs列表中
                processed_inputs.append(
                    {
                        'input_ids': torch.tensor(tokens),
                        'attention_mask': torch.tensor(attn),
                    }
                )

            # 将所有inputs整合成一个batch
            inputs = {
                'input_ids': torch.cat(
                    [inp['input_ids'].unsqueeze(0) for inp in processed_inputs]
                ),
                'attention_mask': torch.cat(
                    [inp['attention_mask'].unsqueeze(0) for inp in processed_inputs]
                ),
            }
        inputs = {name: tensor.to(self.device) for name, tensor in inputs.items()}
        return {'inputs': inputs}

    def get_output_key(self, f: str):
        prefix = self.output_prefix if self.output_prefix else self.model_name
        postfix = f'_{self.output_postfix}' if self.output_postfix else ''
        return f'{prefix}_{f}{postfix}'

    def predict(self, texts: Union[List[str], str]):
        inputs_dict = self.pre_process(texts)
        with torch.no_grad():
            logits = self.model(**inputs_dict['inputs']).logits

            if self.use_sigmoid:
                probs = torch.sigmoid(logits)
            else:
                probs = torch.softmax(logits, dim=-1)

            pos_prob = probs[:, self.cls_index].cpu().numpy()

        outputs = []
        for prob in pos_prob:
            prob = round(float(prob), 6)
            output = {self.get_output_key('prob'): prob}
            outputs.append(output)

        return outputs


class XlmrModel(BertModel):
    def __init__(self, model_path: str = None) -> None:
        if not model_path:
            model_path = self.auto_download()

        transformers_module = import_transformer()

        self.model = transformers_module.AutoModelForSequenceClassification.from_pretrained(
            os.path.join(model_path, 'porn_classifier/classifier_hf')
        )
        with open(
            os.path.join(model_path, 'porn_classifier/extra_parameters.json')
        ) as reader:
            model_config = json.load(reader)
        self.cls_index = int(model_config.get('cls_index', 1))
        self.use_sigmoid = bool(model_config.get('use_sigmoid', False))
        self.max_tokens = int(model_config.get('max_tokens', 512))
        self.remain_tail = min(
            self.max_tokens - 1, int(model_config.get('remain_tail', -1))
        )
        self.device = model_config.get('device', 'cpu')

        self.model.eval()
        self.model.to(self.device, dtype=torch.float16)

        self.tokenizer = transformers_module.AutoTokenizer.from_pretrained(
            os.path.join(model_path, 'porn_classifier/classifier_hf')
        )
        self.tokenizer_config = {
            'padding': True,
            'truncation': self.remain_tail <= 0,
            'max_length': self.max_tokens if self.remain_tail <= 0 else None,
            'return_tensors': 'pt' if self.remain_tail <= 0 else None,
        }

        self.output_prefix = str(model_config.get('output_prefix', '')).rstrip('_')
        self.output_postfix = str(model_config.get('output_postfix', '')).lstrip('_')

        self.model_name = str(model_config.get('model_name', 'porn-24m5'))

    def auto_download(self) -> str:
        """Default download the 24m5.zip model."""
        resource_name = 'porn-24m5'
        resource_config = load_config()['resources']
        porn_24m5_config: Dict = resource_config[resource_name]
        porn_24m5_s3 = porn_24m5_config['download_path']
        porn_24m5_md5 = porn_24m5_config.get('md5', '')
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
                logger.info(f'downloading {porn_24m5_s3}')
                zip_path = download_auto_file(porn_24m5_s3, zip_path, porn_24m5_md5)
            logger.info(f'unzipping {zip_path}')
            unzip_path = unzip_local_file(zip_path, unzip_path)
        else:
            logger.info(f'unzip_path: {unzip_path} exist')
        return unzip_path
