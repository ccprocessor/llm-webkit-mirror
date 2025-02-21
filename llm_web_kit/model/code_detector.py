# Copyright (c) Opendatalab. All rights reserved.
import os
import re
from typing import Dict, Tuple

import fasttext

from llm_web_kit.config.cfg_reader import load_config
from llm_web_kit.libs.logger import mylogger as logger
from llm_web_kit.model.resource_utils.download_assets import (
    CACHE_DIR, download_auto_file)
from llm_web_kit.model.resource_utils.singleton_resource_manager import \
    singleton_resource_manager
from llm_web_kit.model.resource_utils.unzip_ext import (get_unzip_dir,
                                                        unzip_local_file)


class CodeClassification:
    """code classification using fasttext model."""

    def __init__(self, model_path: str = None):
        """Initialize CodeClassification model Will download the v3_1223.bin
        model if model_path is not provided.

        Args:
            model_path (str, optional): Path to the model. Defaults to None.
        """

        if not model_path:
            model_path = self.auto_download()
        self.model = fasttext.load_model(model_path)

    def auto_download(self):
        """Default download the v3_1223.bin model."""
        resource_name = 'code_fasttext_models_v3_1223'
        resource_config = load_config()['resources']
        code_cl_v3_config: dict = resource_config[resource_name]
        code_cl_v3_path = code_cl_v3_config['download_path']
        code_cl_v3_md5 = code_cl_v3_config.get('md5', '')
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
                logger.info(f'downloading {code_cl_v3_path}')
                zip_path = download_auto_file(code_cl_v3_path, zip_path, code_cl_v3_md5)
            logger.info(f'unzipping {zip_path}')
            unzip_path = unzip_local_file(zip_path, unzip_path)
        else:
            logger.info(f'unzip_path: {unzip_path} exist')
        return os.path.join(unzip_path, f'{resource_name}.bin')

    @property
    def version(self) -> str:
        """
        Get the version of the model
        The version is determined by the update of model
        now have v3 version from : s3://web-parse-huawei/shared_resource/code/code_fasttext_models_v3_1223.zip

        Returns:
            str: The version of the model
        """
        if not hasattr(self, '_version'):
            self._version = 'v3_1223'
        return self._version

    def predict(self, text: str, k: int = 2) -> Tuple[Tuple[str], Tuple[float]]:
        """Predict code of the given text Return all predictions. Default k is
        2.

        Args:
            text (str): Text to predict code
            k (int, optional): Number of predictions to return. Defaults to 2.

        Returns:
            Tuple[Tuple[str], Tuple[float]]: Tuple of predictions and probabilities return top k predictions
        """
        assert k > 0, 'k should be greater than 0'

        # remove new lines
        text = text.replace('\n', ' ')

        # returns top k predictions
        predictions, probabilities = self.model.predict(text, k=k)

        return predictions, probabilities


def get_singleton_code_detect() -> CodeClassification:
    """Get the singleton code classification model.

    returns:
        CodeClassification: The code classification model
    """
    if not singleton_resource_manager.has_name('code_detect'):
        singleton_resource_manager.set_resource('code_detect', CodeClassification())
    return singleton_resource_manager.get_resource('code_detect')


def detect_latex_env(content_str: str) -> bool:
    """Detect if the content string contains latex environment."""
    latex_env_pattern = re.compile(r'\\begin\{.*?\}.*\\end\{.*\}', re.DOTALL)
    return latex_env_pattern.search(content_str) is not None


CODE_CL_SUPPORTED_VERSIONS = ['v3_1223']


def decide_code_func(content_str: str, code_detect: CodeClassification) -> float:
    """Decide code based on the content string. This function will truncate the
    content string if it is too long.

    Raises:
        ValueError: Unsupported version.
            The prediction str is different for different versions of fasttext model.
            So the version should be specified.
            Now only support version "v3_1223"

    Warning:
        The too long content string may be truncated.
        Some text with latex code block may be misclassified.

    Args:
        content_str (str): The content string to decide code
        code_detect (CodeClassification): The code classification model

    Returns:
        float: the probability of code text
    """

    # truncate the content string if it is too long
    str_len = len(content_str)
    if str_len > 10000:
        logger.warning('Content string is too long, truncate to 10000 characters')
        start_idx = (str_len - 10000) // 2
        content_str = content_str[start_idx:start_idx + 10000]

    # check if the content string contains latex environment
    if detect_latex_env(content_str):
        logger.warning('Content string contains latex environment, may be misclassified')

    def decide_code_by_prob_v3(predictions: Tuple[str], probabilities: Tuple[float]) -> float:
        idx = predictions.index('__label__1')
        true_prob = probabilities[idx]
        return true_prob

    if code_detect.version == 'v3_1223':
        predictions, probabilities = code_detect.predict(content_str)
        result = decide_code_by_prob_v3(predictions, probabilities)
    else:
        raise ValueError(f'Unsupported version: {code_detect.version}. Supported versions: {[CODE_CL_SUPPORTED_VERSIONS]}')
    return result


def decide_code_by_str(content_str: str) -> float:
    """Decide code based on the content string, based on decide_code_func."""
    lang_detect = get_singleton_code_detect()

    return decide_code_func(content_str, lang_detect)


def update_code_by_str(content_str: str) -> Dict[str, float]:
    """Decide code based on the content string, based on decide_code_func."""
    return {'code': decide_code_by_str(content_str)}


if __name__ == '__main__':
    cclass = CodeClassification()
    text = '示例文本'
    predictions, probabilities = cclass.predict(text)
    print(predictions, probabilities)
    print(update_code_by_str(text))

    text = 'import pandas as pd'
    print(update_code_by_str(text))

    text = "# 这是一个代码测试模块\nimport pandas as pd\ndf=pd.read_csv('file.csv')"
    predictions, probabilities = cclass.predict(text)
    print(update_code_by_str(text))
