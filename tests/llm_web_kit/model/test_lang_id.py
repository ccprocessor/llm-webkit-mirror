import unittest
from unittest.mock import MagicMock, patch

from llm_web_kit.model.lang_id import (LanguageIdentification,
                                       decide_language_by_prob_v176,
                                       decide_language_func, detect_code_block,
                                       detect_inline_equation,
                                       detect_latex_env,
                                       update_language_by_str)


class TestLanguageIdentification(unittest.TestCase):

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
    @patch('llm_web_kit.model.lang_id.fasttext.load_model')
    def test_auto_download(self, mock_load_model, mock_os_path_join, mock_logger, mock_auto_download, mock_load_config):
        # 创建实例，触发auto_download调用
        _ = LanguageIdentification()

        # 打印实际调用参数以调试
        print('Actual call args:', mock_auto_download.call_args)

        # 断言mock_download_auto_file被调用且参数正确
        mock_auto_download.assert_called_once()

    @patch('llm_web_kit.model.lang_id.fasttext.load_model')
    @patch('llm_web_kit.model.lang_id.LanguageIdentification.auto_download')
    def test_predict(self, mock_auto_download, mock_load_model):
        lang_id = LanguageIdentification()
        lang_id.model.predict.return_value = (['label1', 'label2'], [0.9, 0.1])
        predictions, probabilities = lang_id.predict('test text')
        assert predictions == ['label1', 'label2']
        assert probabilities == [0.9, 0.1]


language_dict = {
    'eng': 'en',
    'zho': 'zh',
    'hrv': 'hr',
    'srp': 'sr',
    'eng__Latn': 'en',  # 添加对 __label__eng__Latn 的支持
    # 添加其他映射
}


class TestDecideLanguageByProbV176(unittest.TestCase):
    def test_pattern_218(self):
        # 使用符合 pattern_218 的输入
        predictions = ('__label__eng_Latn', '__label__zho_Hans')
        probabilities = (0.7, 0.3)
        self.assertEqual(decide_language_by_prob_v176(predictions, probabilities), 'en')

    def test_unsupported_prediction_format(self):
        # 测试不符合任何模式的输入
        predictions = ('__label__invalid___format', '__label_____en')
        probabilities = (0.5, 0.5)
        with self.assertRaises(ValueError):
            decide_language_by_prob_v176(predictions, probabilities)

    def test_lang_prob_dict_accumulation(self):
        # 测试概率累加逻辑
        predictions = ('__label__en', '__label__en')
        probabilities = (0.3, 0.4)
        self.assertEqual(decide_language_by_prob_v176(predictions, probabilities), 'en')

    def test_zh_en_prob_logic(self):
        # 测试 zh 和 en 的概率逻辑
        predictions = ('__label__zh', '__label__en')
        probabilities = (0.6, 0.4)
        self.assertEqual(decide_language_by_prob_v176(predictions, probabilities), 'zh')

        predictions = ('__label__zh', '__label__en')
        probabilities = (0.3, 0.7)
        self.assertEqual(decide_language_by_prob_v176(predictions, probabilities), 'en')

    def test_max_prob_logic(self):
        # 测试 hr 和 sr 的逻辑
        predictions = ('__label__hr', '__label__sr')
        probabilities = (0.7, 0.3)
        self.assertEqual(decide_language_by_prob_v176(predictions, probabilities), 'sr')

        predictions = ('__label__hr', '__label__sr')
        probabilities = (0.3, 0.7)
        self.assertEqual(decide_language_by_prob_v176(predictions, probabilities), 'sr')

        # 测试 mix 的逻辑
        predictions = ('__label__de', '__label__fr')
        probabilities = (0.4, 0.4)
        self.assertEqual(decide_language_by_prob_v176(predictions, probabilities), 'mix')


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
    result = decide_language_func('test text', lang_detect)
    assert result == {'language': 'en', 'language_details': 'not_defined'}

    # Test for 218.bin version
    lang_detect.version = '218.bin'
    lang_detect.predict.return_value = (['__label__eng_Latn', '__label__zho_Hans'], [0.6, 0.4])
    result = decide_language_func('test text', lang_detect)
    assert result == {'language': 'en', 'language_details': 'eng_Latn'}

    # Test for empty string
    result = decide_language_func('', lang_detect)
    assert result == {'language': 'empty', 'language_details': 'empty'}


def test_update_language_by_str():
    with patch('llm_web_kit.model.lang_id.get_singleton_lang_detect') as mock_get_singleton_lang_detect, \
         patch('llm_web_kit.model.lang_id.decide_language_func') as mock_decide_language_func:

        # 设置模拟函数的返回值
        mock_get_singleton_lang_detect.return_value = MagicMock()
        mock_decide_language_func.return_value = {'language': 'en', 'language_details': 'eng_Latn'}

        # 调用被测函数
        result = update_language_by_str('test text')

        # 验证返回结果
        expected_result = {
            'language': 'en',
            'language_details': 'eng_Latn'
        }
        assert result == expected_result, f'Expected {expected_result}, but got {result}'
        print('Test passed!')
