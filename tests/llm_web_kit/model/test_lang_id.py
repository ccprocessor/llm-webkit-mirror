import unittest
from unittest.mock import MagicMock, patch

from llm_web_kit.model.lang_id import CACHE_DIR  # 添加这行导入语句
from llm_web_kit.model.lang_id import (LanguageIdentification,
                                       decide_language_by_prob_v176,
                                       decide_language_func, detect_code_block,
                                       detect_inline_equation,
                                       detect_latex_env, get_max_chinese_lang,
                                       update_language_by_str)


class TestLanguageIdentification(unittest.TestCase):

    @patch('llm_web_kit.model.lang_id.fasttext.load_model')
    @patch('llm_web_kit.model.lang_id.LanguageIdentification.auto_download')
    def test_init(self, mock_auto_download, mock_load_model):
        mock_auto_download.return_value = '/fake/model/path'
        # Test with default model path
        _ = LanguageIdentification()
        mock_load_model.assert_called_once_with('/')

        # Test with custom model path
        mock_load_model.reset_mock()
        _ = LanguageIdentification('custom_model_path')
        mock_load_model.assert_called_once_with('custom_model_path')

    @patch('llm_web_kit.model.lang_id.load_config')
    @patch('llm_web_kit.model.lang_id.download_auto_file')
    @patch('llm_web_kit.model.lang_id.logger')
    @patch('os.path.join')
    @patch('os.makedirs')
    @patch('llm_web_kit.model.lang_id.fasttext.load_model')
    def test_auto_download(self, mock_load_model, mock_os_makedirs, mock_os_path_join, mock_logger, mock_download_auto_file, mock_load_config):
        # 准备测试数据
        mock_load_config.return_value = {
            'resources': {
                'lang-id-176': {'download_path': 'mock_url_176', 'md5': 'mock_md5_176'},
                'lang-id-218': {'download_path': 'mock_url_218', 'sha256': 'mock_sha256_218'}
            }
        }
        mock_os_path_join.side_effect = lambda *args: '/'.join(args)  # 模拟os.path.join的行为
        mock_download_auto_file.return_value = 'mock_downloaded_path'  # 模拟download_auto_file的返回值
        mock_load_model.return_value = None  # 模拟fasttext.load_model的返回值

        # 创建LanguageIdentification实例
        lang_id = LanguageIdentification()

        # 测试场景1：默认参数，下载lang-id-176
        result = lang_id.auto_download()
        assert result == ['mock_downloaded_path']  # 验证返回值
        assert mock_load_config.call_count == 2  # 验证load_config被调用两次（一次在初始化，一次在auto_download）
        mock_logger.info.assert_any_call(f'开始下载模型 lang-id-176 -> {CACHE_DIR}/lang-id-176/model.bin')  # 验证日志输出
        mock_logger.info.assert_any_call('模型 lang-id-176 下载完成')  # 验证日志输出
        assert mock_download_auto_file.call_count == 2  # 验证download_auto_file被调用一次
        assert mock_os_makedirs.call_count == 2

        # 重置mock对象的调用记录，准备下一个测试场景
        mock_load_config.reset_mock()
        mock_logger.reset_mock()
        mock_download_auto_file.reset_mock()
        mock_os_makedirs.reset_mock()

        # 测试场景2：下载lang-id-218
        result = lang_id.auto_download(resource_names='lang-id-218')
        assert result == ['mock_downloaded_path']  # 验证返回值
        mock_download_auto_file.assert_called_once_with(
            resource_path='mock_url_218',
            target_path=f'{CACHE_DIR}/lang-id-218/model.bin',
            sha256_sum='mock_sha256_218'
        )  # 验证download_auto_file的调用参数

        # 重置mock对象的调用记录，准备下一个测试场景
        mock_load_config.reset_mock()
        mock_logger.reset_mock()
        mock_download_auto_file.reset_mock()
        mock_os_makedirs.reset_mock()

        # 测试场景3：下载多个资源
        result = lang_id.auto_download(resource_names=['lang-id-176', 'lang-id-218'])
        assert len(result) == 2  # 验证返回值长度
        assert result[0] == 'mock_downloaded_path'  # 验证第一个资源的下载路径
        assert result[1] == 'mock_downloaded_path'  # 验证第二个资源的下载路径

        # 验证download_auto_file的调用次数和参数
        mock_download_auto_file.assert_any_call(
            resource_path='mock_url_176',
            target_path=f'{CACHE_DIR}/lang-id-176/model.bin',
            md5_sum='mock_md5_176'
        )
        mock_download_auto_file.assert_any_call(
            resource_path='mock_url_218',
            target_path=f'{CACHE_DIR}/lang-id-218/model.bin',
            sha256_sum='mock_sha256_218'
        )

        # 重置mock对象的调用记录，准备下一个测试场景
        mock_load_config.reset_mock()
        mock_logger.reset_mock()
        mock_download_auto_file.reset_mock()
        mock_os_makedirs.reset_mock()

        # 测试场景4：资源未找到的情况
        result = lang_id.auto_download(resource_names='non-existent-resource')
        assert result == []  # 验证返回值
        mock_logger.error.assert_called_once_with("资源 'non-existent-resource' 未在配置中找到，跳过下载。")  # 验证日志输出

        # 打印实际调用参数以调试
        print('Actual call args for download_auto_file:', mock_download_auto_file.call_args)
        print('Actual call args for os.makedirs:', mock_os_makedirs.call_args)

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


class TestDecideLanguageFunc(unittest.TestCase):

    def setUp(self):
        self.lang_detect_supported = MagicMock(version='176.bin')
        self.lang_detect_supported.predict.return_value = (['en'], [0.9])

    def test_empty_string_returns_empty(self):
        result = decide_language_func('   ', self.lang_detect_supported)
        self.assertEqual(result, {'language': 'empty', 'language_details': 'empty'})

    def test_unsupported_version_raises_error(self):
        lang_detect = MagicMock(version='invalid_version')
        with self.assertRaises(ValueError):
            decide_language_func('test', lang_detect)

    @patch('llm_web_kit.model.lang_id.decide_language_by_prob_v176')
    def test_lid_176_pre_en_returns_en(self, mock_decide):
        mock_decide.return_value = 'en'
        result = decide_language_func('test', self.lang_detect_supported)
        self.assertEqual(result, {'language': 'en', 'language_details': ''})

    @patch('llm_web_kit.model.lang_id.decide_language_by_prob_v176')
    @patch('langdetect_zh.detect_langs')
    def test_sim_tra_zh_detect_langs_success(self, mock_detect_langs, mock_decide):
        mock_decide.return_value = 'zh'
        # 创建模拟的Language对象
        mock_lang = MagicMock()
        mock_lang.lang = 'zh-cn'
        mock_lang.prob = 0.8
        mock_detect_langs.return_value = [mock_lang]

        result = decide_language_func('test', self.lang_detect_supported, is_cn_specific=True)
        self.assertEqual(result['language'], 'zh')

    @patch('llm_web_kit.model.lang_id.decide_language_by_prob_v176')
    @patch('langdetect_zh.detect_langs')
    def test_sim_tra_zh_detect_langs_exception(self, mock_detect_langs, mock_decide):
        from langdetect_zh import LangDetectException

        mock_decide.return_value = 'zh'
        mock_detect_langs.side_effect = LangDetectException(code=500, message='test error')

        result = decide_language_func('test', self.lang_detect_supported, is_cn_specific=True)
        self.assertEqual(result, {'language': 'zh', 'language_details': ''})

    @patch('llm_web_kit.model.lang_id.decide_language_by_prob_v176')
    def test_lid_176_pre_other_lang_use_218e_false(self, mock_decide):
        mock_decide.return_value = 'fr'
        result = decide_language_func('test', self.lang_detect_supported, use_218e=False)
        self.assertEqual(result, {'language': 'fr', 'language_details': ''})

    @patch('llm_web_kit.model.lang_id.decide_language_by_prob_v176')
    @patch('llm_web_kit.model.lang_id.get_singleton_lang_detect')
    def test_218_model_lang_in_list(self, mock_get_singleton, mock_decide):
        mock_decide.return_value = 'fr'
        lang_detect_218 = MagicMock()
        lang_detect_218.predict.return_value = (['__label__yue_Hant'], [0.9])
        mock_get_singleton.return_value = lang_detect_218
        result = decide_language_func('test', self.lang_detect_supported, use_218e=True)
        self.assertEqual(result, {'language': 'fr', 'language_details': ''})

    @patch('llm_web_kit.model.lang_id.decide_language_by_prob_v176')
    @patch('llm_web_kit.model.lang_id.get_singleton_lang_detect')
    def test_218_model_lang_not_in_list(self, mock_get_singleton, mock_decide):
        mock_decide.return_value = 'fr'
        lang_detect_218 = MagicMock()
        lang_detect_218.predict.return_value = (['__label__de_DE'], [0.8])
        mock_get_singleton.return_value = lang_detect_218
        result = decide_language_func('test', self.lang_detect_supported, use_218e=True)
        self.assertEqual(result, {'language': 'de', 'language_details': 'de_DE'})


def test_update_language_by_str():
    with patch('llm_web_kit.model.lang_id.get_singleton_lang_detect') as mock_get_singleton_lang_detect, \
         patch('llm_web_kit.model.lang_id.decide_language_func') as mock_decide_language_func:

        # 设置模拟函数的返回值
        mock_get_singleton_lang_detect.return_value = MagicMock()
        mock_decide_language_func.return_value = {'language': 'en'}

        # 调用被测函数
        result = update_language_by_str('test text')

        # 验证返回结果
        expected_result = {
            'language': 'en',
        }
        assert result == expected_result, f'Expected {expected_result}, but got {result}'
        print('Test passed!')


class TestGetMaxChineseLang(unittest.TestCase):

    def test_get_max_chinese_lang_zh_cn_higher(self):
        # 模拟 langs 输入，zh-cn 的概率更高
        lang1 = MagicMock()
        lang1.lang = 'zh-cn'
        lang1.prob = 0.7

        lang2 = MagicMock()
        lang2.lang = 'zh-tw'
        lang2.prob = 0.3

        langs = [lang1, lang2]

        result = get_max_chinese_lang(langs)
        self.assertEqual(result, {'language': 'zh', 'language_details': 'zho_Hans'})

    def test_get_max_chinese_lang_zh_tw_higher(self):
        # 模拟 langs 输入，zh-tw 的概率更高
        lang1 = MagicMock()
        lang1.lang = 'zh-cn'
        lang1.prob = 0.4

        lang2 = MagicMock()
        lang2.lang = 'zh-tw'
        lang2.prob = 0.6

        langs = [lang1, lang2]

        result = get_max_chinese_lang(langs)
        self.assertEqual(result, {'language': 'zh', 'language_details': 'zho_Hant'})
