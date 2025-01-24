import unittest
from unittest.mock import MagicMock, patch

from llm_web_kit.model.lang_id import (LanguageIdentification,
                                       decide_lang_by_str,
                                       decide_lang_by_str_v218,
                                       decide_language_by_prob_v176,
                                       decide_language_func, detect_code_block,
                                       detect_inline_equation,
                                       detect_latex_env,
                                       get_singleton_lang_detect,
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

    @patch('llm_web_kit.model.lang_id.load_config', return_value={'resources': {'lang-id-218': {'download_path': 'mock_download_path', 'sha256': 'mock_sha256'}}})
    @patch('llm_web_kit.model.lang_id.LanguageIdentification.auto_download', return_value='mock_model_path')
    @patch('llm_web_kit.model.lang_id.logger')
    @patch('os.path.join', return_value='mock_target_path')
    def test_auto_download(self, mock_os_path_join, mock_logger, mock_download_auto_file, mock_load_config):
        mock_download_auto_file.assert_called_with('mock_download_path', 'mock_target_path', 'mock_sha256')
        mock_load_config.assert_called_once()

    @patch('llm_web_kit.model.lang_id.fasttext.load_model')
    @patch('llm_web_kit.model.lang_id.LanguageIdentification.auto_download')
    def test_predict(self, mock_auto_download, mock_load_model):
        lang_id = LanguageIdentification()
        lang_id.model.predict.return_value = (['label1', 'label2'], [0.9, 0.1])
        predictions, probabilities = lang_id.predict('test text')
        assert predictions == ['label1', 'label2']
        assert probabilities == [0.9, 0.1]


class TestGetSingletonLangDetect(unittest.TestCase):

    @patch('llm_web_kit.model.lang_id.singleton_resource_manager.has_name', return_value=False)
    @patch('llm_web_kit.model.lang_id.singleton_resource_manager.set_resource')
    def test_get_singleton_lang_detect_new_instance(self, mock_set_resource, mock_has_name):
        lang_id_instance = MagicMock()
        with patch('llm_web_kit.model.lang_id.LanguageIdentification', return_value=lang_id_instance):
            result = get_singleton_lang_detect('model_path')
            mock_set_resource.assert_called_once_with('lang_detect_model_path', lang_id_instance)
            self.assertEqual(result, lang_id_instance)

    @patch('llm_web_kit.model.lang_id.singleton_resource_manager.has_name', return_value=True)
    @patch('llm_web_kit.model.lang_id.singleton_resource_manager.get_resource', return_value='mock_lang_id_instance')
    def test_get_singleton_lang_detect_existing_instance(self, mock_get_resource, mock_has_name):
        result = get_singleton_lang_detect('model_path')
        mock_get_resource.assert_called_once_with('lang_detect_model_path')
        self.assertEqual(result, 'mock_lang_id_instance')


class TestDecideLanguageByProbV176(unittest.TestCase):

    def test_decide_language_by_prob_v176(self):
        predictions = ('__label__en', '__label__zh', '__label__es')
        probabilities = (0.6, 0.3, 0.1)
        result = decide_language_by_prob_v176(predictions, probabilities)
        self.assertEqual(result, 'en')

    def test_decide_language_by_prob_v176_mix(self):
        predictions = ('__label__en', '__label__zh', '__label__es')
        probabilities = (0.2, 0.3, 0.5)
        result = decide_language_by_prob_v176(predictions, probabilities)
        self.assertEqual(result, 'mix')

    def test_decide_language_by_prob_v176_sr(self):
        predictions = ('__label__sr', '__label__hr', '__label__es')
        probabilities = (0.7, 0.2, 0.1)
        result = decide_language_by_prob_v176(predictions, probabilities)
        self.assertEqual(result, 'sr')


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
    # 模拟 decide_lang_by_str 和 decide_lang_by_str_v218 的行为
    with patch('llm_web_kit.model.lang_id.decide_lang_by_str') as mock_decide_lang_by_str, \
         patch('llm_web_kit.model.lang_id.decide_lang_by_str_v218') as mock_decide_lang_by_str_v218:

        # 设置模拟函数的返回值
        mock_decide_lang_by_str.return_value = 'en'
        mock_decide_lang_by_str_v218.return_value = 'en_v218'

        # 调用被测函数
        result = update_language_by_str('test text')

        # 验证返回结果
        expected_result = {
            'language': 'en',
            'language_details': 'en_v218'
        }
        assert result == expected_result, f"Expected {expected_result}, but got {result}"
        print('Test passed!')


class TestDecideLangByStrV218(unittest.TestCase):

    @patch('llm_web_kit.model.lang_id.get_singleton_lang_detect')
    def test_decide_lang_by_str_v218(self, mock_get_singleton_lang_detect):
        mock_lang_detect = MagicMock()
        mock_lang_detect.predict.return_value = [('__label__en', 0.8), ('__label__fr', 0.2)]
        mock_get_singleton_lang_detect.return_value = mock_lang_detect

        content_str = 'This is an English text.'
        result = decide_lang_by_str_v218(content_str, 'model_path')
        self.assertEqual(result, 'en')

    @patch('llm_web_kit.model.lang_id.get_singleton_lang_detect')
    def test_decide_lang_by_str_v218_custom_model_path(self, mock_get_singleton_lang_detect):
        mock_lang_detect = MagicMock()
        mock_lang_detect.predict.return_value = [('__label__es', 0.9), ('__label__de', 0.1)]
        mock_get_singleton_lang_detect.return_value = mock_lang_detect

        content_str = 'Este es un texto en español.'
        result = decide_lang_by_str_v218(content_str, 'custom_model_path')
        self.assertEqual(result, 'es')
