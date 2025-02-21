import unittest
from unittest import TestCase
from unittest.mock import MagicMock, patch

from llm_web_kit.model.code_detector import (CodeClassification,
                                             decide_code_by_str,
                                             decide_code_func,
                                             detect_latex_env,
                                             update_code_by_str)


class TestCodeClassification(TestCase):

    @patch('llm_web_kit.model.code_detector.fasttext.load_model')
    @patch('llm_web_kit.model.code_detector.CodeClassification.auto_download')
    def test_init(self, mock_auto_download, mock_load_model):
        mock_auto_download.return_value = '/fake/model/path'
        # Test with default model path
        _ = CodeClassification()
        mock_load_model.assert_called_once_with('/fake/model/path')

        # Test with custom model path
        mock_load_model.reset_mock()
        _ = CodeClassification('custom_model_path')
        mock_load_model.assert_called_once_with('custom_model_path')

    @patch('llm_web_kit.model.code_detector.fasttext.load_model')
    @patch('llm_web_kit.model.code_detector.CodeClassification.auto_download')
    def test_predict(self, mock_auto_download, mock_load_model):
        code_cl = CodeClassification()
        code_cl.model.predict.return_value = (['label1', 'label2'], [0.9, 0.1])
        predictions, probabilities = code_cl.predict('test text')
        assert predictions == ['label1', 'label2']
        assert probabilities == [0.9, 0.1]


def test_detect_latex_env():
    assert detect_latex_env('\\begin{equation}\nx = y\n\\end{equation}')
    assert not detect_latex_env('This is not a latex environment')


def test_decide_code_func():
    code_detect = MagicMock()
    code_detect.version = 'v3_1223'
    code_detect.predict.return_value = (['__label__1', '__label__0'], [0.6, 0.4])
    assert decide_code_func('test text', code_detect) == 0.6


def test_decide_code_by_str():
    with patch('llm_web_kit.model.code_detector.get_singleton_code_detect') as mock_get_singleton_code_detect, patch(
            'llm_web_kit.model.code_detector.decide_code_func') as mock_decide_code_func:
        mock_get_singleton_code_detect.return_value = MagicMock()
        mock_decide_code_func.return_value = 0.6
        assert decide_code_by_str('test text') == 0.6


def test_update_code_by_str():
    with patch('llm_web_kit.model.code_detector.decide_code_by_str') as mock_decide_code_by_str:
        mock_decide_code_by_str.return_value = 0.6
        assert update_code_by_str('test text') == {'code': 0.6}


if __name__ == '__main__':
    unittest.main()
