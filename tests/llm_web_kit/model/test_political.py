# flake8: noqa: E402
import os
import sys
from unittest.mock import MagicMock, patch

import pytest

current_file_path = os.path.abspath(__file__)
parent_dir_path = os.path.join(current_file_path, *[os.pardir] * 4)
normalized_path = os.path.normpath(parent_dir_path)
sys.path.append(normalized_path)

from llm_web_kit.exception.exception import ModelInputException
from llm_web_kit.model.policical import (PoliticalDetector,
                                         decide_political_by_prob,
                                         decide_political_by_str,
                                         decide_political_func,
                                         political_filter_cpu,
                                         update_political_by_str)


class TestPoliticalDetector:

    @patch('llm_web_kit.model.policical.AutoTokenizer.from_pretrained')
    @patch('llm_web_kit.model.policical.fasttext.load_model')
    @patch('llm_web_kit.model.policical.PoliticalDetector.auto_download')
    def test_init(self, mock_auto_download, mock_load_model, mock_auto_tokenizer):
        mock_auto_download.return_value = '/fake/model/path'
        # Test with default model path
        _ = PoliticalDetector()
        mock_load_model.assert_called_once_with('/fake/model/path/model.bin')
        mock_auto_tokenizer.assert_called_once_with(
            '/fake/model/path/internlm2-chat-20b',
            use_fast=False,
            trust_remote_code=True,
        )

        # Test with custom model path
        mock_load_model.reset_mock()
        mock_auto_tokenizer.reset_mock()
        _ = PoliticalDetector('custom_model_path')
        mock_load_model.assert_called_once_with(os.path.join('custom_model_path', 'model.bin'))
        mock_auto_tokenizer.assert_called_once_with(
            os.path.join('custom_model_path', 'internlm2-chat-20b'),
            use_fast=False,
            trust_remote_code=True,
        )

    @patch('llm_web_kit.model.policical.AutoTokenizer.from_pretrained')
    @patch('llm_web_kit.model.policical.fasttext.load_model')
    @patch('llm_web_kit.model.policical.PoliticalDetector.auto_download')
    def test_predict(self, mock_auto_download, mock_load_model, mock_auto_tokenizer):
        political_detect = PoliticalDetector()
        political_detect.model.predict.return_value = (['label1', 'label2'], [0.9, 0.1])
        predictions, probabilities = political_detect.predict('test text')
        assert predictions == ['label1', 'label2']
        assert probabilities == [0.9, 0.1]


def test_decide_political_by_prob():
    predictions = ['__label__normal', '__label__political']
    probabilities = [0.6, 0.4]
    assert decide_political_by_prob(predictions, probabilities) == 0.6

    predictions = ['__label__political', '__label__normal']
    probabilities = [0.7, 0.3]
    assert decide_political_by_prob(predictions, probabilities) == 0.3


def test_decide_political_func():
    political_detect = MagicMock()
    political_detect.predict.return_value = (
        ['__label__normal', '__label__political'],
        [0.6, 0.4],
    )
    test_str = 'test text'
    assert decide_political_func(test_str, political_detect) == 0.6
    political_detect.predict.assert_called_once_with(test_str)

    test_str = 'test text' * 1000000
    # reset the call count
    political_detect.predict.reset_mock()
    assert decide_political_func(test_str, political_detect) == 0.6
    political_detect.predict.assert_called_once_with(test_str[:2560000])


def test_decide_political_by_str():
    with patch('llm_web_kit.model.policical.get_singleton_political_detect') as mock_get_singleton_political_detect, patch(
            'llm_web_kit.model.policical.decide_political_func') as mock_decide_political_func:
        mock_get_singleton_political_detect.return_value = MagicMock()
        mock_decide_political_func.return_value = 0.6
        assert decide_political_by_str('test text') == 0.6
        mock_get_singleton_political_detect.assert_called_once()


def test_update_political_by_str():
    with patch('llm_web_kit.model.policical.decide_political_by_str') as mock_decide_political_by_str:
        mock_decide_political_by_str.return_value = 0.6
        assert update_political_by_str('test text') == {'political_prob': 0.6}

def test_political_filter_cpu():
    with patch('llm_web_kit.model.policical.decide_political_by_str') as mock_decide_political_by_str:
        with patch('llm_web_kit.model.policical.DataJson') as mock_datajson:
            mock_datajson_instance = MagicMock()
            mock_datajson_instance.get_content_list.return_value.to_txt.return_value = 'This is a test content.'
            mock_datajson.return_value = mock_datajson_instance
            mock_decide_political_by_str.return_value = 0.6
            assert political_filter_cpu({'content': 'This is a test content.'}, 'en') == {'political_prob': 0.6}

    with pytest.raises(ModelInputException) as excinfo:
        political_filter_cpu({'content': 'This is a test content.'}, 'fr')
    assert "Unsupport language 'fr'" in str(excinfo.value)
