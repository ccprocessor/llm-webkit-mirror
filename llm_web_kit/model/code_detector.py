import os
import re
from typing import Dict

import fasttext
import jieba_fast as jieba

from llm_web_kit.config.cfg_reader import load_config
from llm_web_kit.libs.logger import mylogger as logger
from llm_web_kit.model.resource_utils import (CACHE_DIR, download_auto_file,
                                              singleton_resource_manager)


class CodeClassification:
    """Code classification using fasttext model with jieba preprocessing."""

    # Constants for text preprocessing
    MAX_WORD_NUM = 20480

    def __init__(self, model_path: str = None, resource_name=None):
        """Initialize CodeClassification model.

        Args:
            model_path (str, optional): Path to the model. Defaults to None.
        """
        if not model_path:
            model_path = self.auto_download(resource_name)
        self.model = fasttext.load_model(model_path)

    def auto_download(self, resource_name: str = None) -> str:
        if resource_name is None:
            resource_name = 'code_detect_v4_0409'

        resource_config = load_config()['resources']
        code_cl_v4_config: dict = resource_config[resource_name]
        model_download_path = code_cl_v4_config['download_path']
        model_md5 = code_cl_v4_config.get('md5', '')

        target_dir = os.path.join(CACHE_DIR, resource_name)
        os.makedirs(target_dir, exist_ok=True)
        target_path = os.path.join(target_dir, f'{resource_name}.bin')

        logger.info(f'开始下载模型 {resource_name} -> {target_path}')
        return download_auto_file(resource_path=model_download_path, target_path=target_path, md5_sum=model_md5)

    @property
    def version(self) -> str:
        """Get the version of the model.

        Returns:
            str: The version of the model
        """
        if not hasattr(self, '_version'):
            self._version = 'v4_0409'
        return self._version

    def jieba_cut(self, text: str) -> str:
        """Preprocess text using jieba segmentation and cleaning.
        Args:
            text (str): Input text to preprocess

        Returns:
            str: Processed text string
        """
        # Define stop words including the specified ones
        stop_words = {'\r', '\n', ' ', '', '\r\n'}

        words = jieba.lcut(text)
        filtered_words = [word for word in words if word not in stop_words and word.strip()]
        if len(filtered_words) > self.MAX_WORD_NUM:
            filtered_words = filtered_words[: self.MAX_WORD_NUM]

        seg_text = ' '.join(filtered_words)
        seg_text = re.sub(r'([.\!?,\'/()\"\n])', '', seg_text)
        seg_text = re.sub(r'\s+', ' ', seg_text)
        seg_text = seg_text.lower()
        seg_text = seg_text.strip()

        return seg_text

    def predict(self, text: str) -> Dict[str, float]:
        """Predict code classification.

        Args:
            text (str): Input text to classify

        Returns:
            Dict[str, float]: Dictionary with key "has_code_prob_0409" and prediction value
        """
        seg_text = self.jieba_cut(text)
        predictions, probabilities = self.model.predict(seg_text)

        if len(predictions) > 0 and len(probabilities) > 0:
            label = predictions[0]
            confidence = probabilities[0]

            label = label.replace('__label__', '')
            confidence = min(confidence, 1.0)
            if label == '1':
                prediction_value = confidence
            else:
                prediction_value = 1.0 - confidence
        else:
            prediction_value = 0.0

        return {'has_code_prob_0409': prediction_value}


def get_singleton_code_detect() -> CodeClassification:
    """Get the singleton code classification v2 model.

    Returns:
        CodeClassification: The code classification model
    """
    if not singleton_resource_manager.has_name('code_detect_v4_0409'):
        singleton_resource_manager.set_resource('code_detect_v4_0409', CodeClassification())
    return singleton_resource_manager.get_resource('code_detect_v4_0409')


def update_code_prob_by_str(content_str: str) -> Dict[str, float]:
    """Predict code classification using model with detailed output.

    Args:
        content_str (str): The content string to classify

    Returns:
        Dict[str, float]: Dictionary with key "has_code_prob_0409" and prediction value
    """
    code_detect = get_singleton_code_detect()
    return code_detect.predict(content_str)
