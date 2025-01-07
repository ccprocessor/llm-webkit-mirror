from unittest.mock import MagicMock, patch

from llm_web_kit.model.lang_id import (LanguageIdentification,
                                       decide_lang_by_str,
                                       decide_language_by_prob_v176,
                                       decide_language_func, detect_code_block,
                                       detect_inline_equation,
                                       detect_latex_env,
                                       update_language_by_str)


class TestLanguageIdentification:

    @patch('llm_web_kit.model.lang_id.fasttext.load_model')
    @patch('llm_web_kit.model.lang_id.LanguageIdentification.auto_download')
    def test_init(self, mock_auto_download, mock_load_model):
        mock_auto_download.return_value = '/fake/model/path'
        # Test with default model path
        _ = LanguageIdentification()
        mock_load_model.assert_called_once_with('/fake/model/path')

        # Test with custom model path
        mock_load_model.reset_mock()
        _ = LanguageIdentification('custom_model_path')
        mock_load_model.assert_called_once_with('custom_model_path')

    @patch('llm_web_kit.model.lang_id.fasttext.load_model')
    @patch('llm_web_kit.model.lang_id.LanguageIdentification.auto_download')
    def test_predict(self, mock_auto_download, mock_load_model):
        lang_id = LanguageIdentification()
        lang_id.model.predict.return_value = (['label1', 'label2'], [0.9, 0.1])
        predictions, probabilities = lang_id.predict('test text')
        assert predictions == ['label1', 'label2']
        assert probabilities == [0.9, 0.1]


def test_decide_language_by_prob_v176():
    predictions = ['__label__en', '__label__zh']
    probabilities = [0.6, 0.4]
    assert decide_language_by_prob_v176(predictions, probabilities) == 'en'


def test_detect_code_block():
    assert detect_code_block('```python\nprint("Hello, world!")\n```')
    assert not detect_code_block('Hello, world!')


def test_detect_inline_equation():
    assert detect_inline_equation('This is an inline equation: $x = y$')
    assert not detect_inline_equation('This is not an inline equation')


def test_detect_latex_env():
    assert detect_latex_env('\\begin{equation}\nx = y\n\\end{equation}')
    assert not detect_latex_env('This is not a latex environment')


def test_decide_language_func():
    lang_detect = MagicMock()
    lang_detect.version = '176.bin'
    lang_detect.predict.return_value = (['__label__en', '__label__zh'], [0.6, 0.4])
    assert decide_language_func('test text', lang_detect) == 'en'


def test_decide_lang_by_str():
    with patch('llm_web_kit.model.lang_id.get_singleton_lang_detect') as mock_get_singleton_lang_detect, patch(
            'llm_web_kit.model.lang_id.decide_language_func') as mock_decide_language_func:
        mock_get_singleton_lang_detect.return_value = MagicMock()
        mock_decide_language_func.return_value = 'en'
        assert decide_lang_by_str('test text') == 'en'


def test_update_language_by_str():
    with patch('llm_web_kit.model.lang_id.decide_lang_by_str') as mock_decide_lang_by_str:
        mock_decide_lang_by_str.return_value = 'en'
        assert update_language_by_str('test text') == {'language': 'en'}
