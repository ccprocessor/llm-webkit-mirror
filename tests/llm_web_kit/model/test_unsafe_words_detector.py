import unittest
from unittest.mock import MagicMock, Mock, mock_open, patch

from llm_web_kit.exception.exception import SafeModelException
from llm_web_kit.model.unsafe_words_detector import (
    UnsafeWordChecker, auto_download, decide_unsafe_word_by_data_checker,
    get_ac, get_unsafe_words, get_unsafe_words_checker, unsafe_words_filter,
    unsafe_words_filter_overall)


class TestUnsafeWordChecker(unittest.TestCase):

    @patch('llm_web_kit.model.unsafe_words_detector.get_ac')
    def test_init(self, mock_get_ac):
        mock_get_ac.return_value = MagicMock()
        # Test default language initialization
        checker = UnsafeWordChecker()
        mock_get_ac.assert_called_once_with('zh-en')
        self.assertIsNotNone(checker.ac)

        # Test custom language initialization
        mock_get_ac.reset_mock()
        checker = UnsafeWordChecker(language='xyz')
        mock_get_ac.assert_called_once_with('xyz')

    @patch('llm_web_kit.model.unsafe_words_detector.get_ac')
    def test_check_unsafe_words(self, mock_get_ac):
        mock_get_ac.return_value = MagicMock()

        checker = UnsafeWordChecker()
        checker.ac = MagicMock()
        checker.ac.iter.return_value = []

        # Test with content containing no unsafe words
        content = 'This is a safe content with no unsafe words.'
        result = checker.check_unsafe_words(content)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    @patch('llm_web_kit.model.unsafe_words_detector.get_unsafe_words_checker')
    def test_decide_unsafe_word_by_data_checker(self, mock_get_checker):
        mock_checker = MagicMock()
        mock_checker.check_unsafe_words.return_value = [
            {'word': 'unsafe', 'level': 'L2', 'count': 1}
        ]
        mock_get_checker.return_value = mock_checker

        data_dict = {'content': 'Some content with unsafe elements.'}
        result = decide_unsafe_word_by_data_checker(data_dict, mock_checker)
        self.assertEqual(result, 'L2')

    def test_standalone_word_detection(self):
        """测试独立存在的子词能被正确识别[2,6](@ref)"""
        ac = Mock()
        ac.iter = Mock()
        # 配置AC自动机返回数据（子词"unsafe"在位置10）
        ac.iter.return_value = [
            (10, [{
                'sub_word': 'unsafe',
                'word': 'unsafe',
                'sub_words': {'unsafe'},
                'type': 'security',
                'level': 'high',
                'language': 'en'
            }])
        ]
        # 测试字符串包含独立单词"unsafe"
        result = get_unsafe_words(ac, 'This is unsafe.')
        print('result:', result)
        self.assertEqual(len(result), 0)

        result = get_unsafe_words(ac, 'Contains unsafesword')
        self.assertEqual(len(result), 0)

        result = get_unsafe_words(ac, 'Contains realunsafe')
        self.assertEqual(len(result), 0)

    @patch('llm_web_kit.model.unsafe_words_detector.get_ac')
    def test_get_unsafe_words_checker(self, mock_get_ac):
        mock_get_ac.return_value = MagicMock()
        checker1 = get_unsafe_words_checker('zh-en')
        checker2 = get_unsafe_words_checker('zh-en')
        self.assertIs(checker1, checker2)  # Should return the same instance

    @patch('llm_web_kit.model.unsafe_words_detector.get_unsafe_words_checker')
    def test_unsafe_words_filter(self, mock_get_checker):
        mock_checker = MagicMock()
        mock_checker.check_unsafe_words.return_value = [
            {'word': '', 'level': 'L3', 'count': 1}
        ]
        mock_get_checker.return_value = mock_checker

        data_dict = {'content': 'Test content'}
        result = unsafe_words_filter(data_dict, 'en', 'text')
        self.assertEqual(result, 'L3')
        result = unsafe_words_filter(data_dict, 'ko', 'text')
        self.assertEqual(result, 'L3')
        with self.assertRaises(SafeModelException):
            unsafe_words_filter(data_dict, 'unk', 'text')

    def test_unsafe_words_filter_with_unsupported_language(self):
        data_dict = {'content': 'Test content'}
        with self.assertRaises(SafeModelException):
            unsafe_words_filter(data_dict, 'unsupported_language', 'text')

    @patch('llm_web_kit.model.unsafe_words_detector.unsafe_words_filter')
    def test_unsafe_words_filter_overall(self, mock_filter):
        mock_filter.return_value = 'L1'

        data_dict = {'content': 'Content with unsafe words.'}

        result = unsafe_words_filter_overall(
            data_dict,
            language='en',
            content_style='text',
            from_safe_source=False,
            from_domestic_source=False,
        )
        self.assertIsInstance(result, dict)
        self.assertTrue(result['hit_unsafe_words'])

        result = unsafe_words_filter_overall(
            data_dict,
            language='en',
            content_style='text',
            from_safe_source=False,
            from_domestic_source=True,
        )
        self.assertIsInstance(result, dict)
        self.assertTrue(result['hit_unsafe_words'])

        result = unsafe_words_filter_overall(
            data_dict,
            language='en',
            content_style='text',
            from_safe_source=True,
            from_domestic_source=True,
        )
        self.assertIsInstance(result, dict)
        self.assertFalse(result['hit_unsafe_words'])

        result = unsafe_words_filter_overall(
            data_dict,
            language='en',
            content_style='text',
            from_safe_source=True,
            from_domestic_source=False,
        )
        self.assertIsInstance(result, dict)
        self.assertFalse(result['hit_unsafe_words'])

        result = unsafe_words_filter_overall(
            data_dict,
            language='ru',
            content_style='text',
            from_safe_source=False,
            from_domestic_source=False,
        )
        self.assertIsInstance(result, dict)
        self.assertTrue(result['hit_unsafe_words'])

        with self.assertRaises(SafeModelException):
            result = unsafe_words_filter_overall(
                data_dict,
                language='unknown',
                content_style='text',
                from_safe_source=False,
                from_domestic_source=False,
            )

    @patch('llm_web_kit.model.unsafe_words_detector.load_config')
    @patch('llm_web_kit.model.unsafe_words_detector.download_auto_file')
    def test_auto_download(self, mock_download_auto_file, mock_load_config):
        mock_load_config.return_value = {
            'resources': {
                'common': {
                    'cache_path': '/fake/path',
                },
                'unsafe_words': {
                    'download_path': 'http://fake.url/unsafe_words.jsonl',
                    'md5': 'fake_md5',
                },
                'xyz_internal_unsafe_words': {
                    'download_path': 'http://fake.url/xyz_internal_unsafe_words.jsonl',
                    'md5': 'fake_md5',
                },
            }
        }
        # download_auto_file 无返回值，仅负责下载文件到指定路径
        mock_download_auto_file.return_value = '/fake/path/unsafe_words'

        # 调用被测试函数
        with self.assertRaises(SafeModelException):
            auto_download(language='unknown')
        mock_load_config.assert_called_once()
        auto_download(language='xyz')
        result = auto_download(language='zh-en')
        # 预期的返回路径
        expected_local_path = '/fake/path/unsafe_words'

        # 验证返回值
        self.assertEqual(result, expected_local_path)

    @patch('llm_web_kit.model.unsafe_words_detector.auto_download')
    @patch('builtins.open', new_callable=mock_open, read_data='{"word": "test", "type": "涉政", "level": "L3", "language": "zh"}\n{"word": "unsafe&&&word", "type": "敏感", "level": "L2", "language": "en"}\n{"word": "123", "type": "数字", "level": "L1", "language": "zh"}\n{"word": "abcd", "type": "短词", "level": "L1", "language": "en"}\n{"word": "", "type": "空", "level": "L1", "language": "zh"}\n')
    def test_get_ac_success(self, mock_file, mock_auto_download):
        # 模拟 auto_download 返回假路径
        mock_auto_download.return_value = '/fake/path/unsafe_words.jsonl'

        # 调用 get_ac
        ac = get_ac(language='zh-en')
        mock_file.assert_called_once_with('/fake/path/unsafe_words.jsonl','r')
        handle = mock_file()
        lines = handle.readlines()
        self.assertEqual(len(lines), 5)
        print('lines:',lines)

        # 查看ac内容
        for word, w_info_lst in ac.items():
            print('单词:', word)
            print('关联信息:', w_info_lst)

        # 验证 AC 自动机包含预期的词条
        self.assertFalse('test' in ac)          # 'test' 应包含
        self.assertTrue('unsafe' in ac)        # 'unsafe&&&word' 的子词
        self.assertTrue('word' in ac)          # 'unsafe&&&word' 的子词
        self.assertTrue('123' in ac)          # 非纯英文词，保留但需验证逻辑
        self.assertFalse('abcd' in ac)         # 纯英文且 <= 4，应跳过
        self.assertFalse('' in ac)             # 空词，应跳过


if __name__ == '__main__':
    unittest.main()
