import unittest
from unittest.mock import MagicMock, patch

from llm_web_kit.exception.exception import CleanLangTypeExp
from llm_web_kit.model.unsafe_words_detector import (
    UnsafeWordChecker, auto_download, decide_unsafe_word_by_data_checker,
    get_unsafe_words_checker, unsafe_words_filter, unsafe_words_filter_overall)


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

    def test_unsafe_words_filter_with_unsupported_language(self):
        data_dict = {'content': 'Test content'}
        with self.assertRaises(CleanLangTypeExp):
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

    @patch('llm_web_kit.config.cfg_reader.load_config')
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
        result = auto_download(language='zh-en')
        mock_load_config.assert_called_once()
        # 预期的返回路径
        expected_local_path = '/fake/path/unsafe_words'

        # 验证返回值
        self.assertEqual(result, expected_local_path)


if __name__ == '__main__':
    unittest.main()
