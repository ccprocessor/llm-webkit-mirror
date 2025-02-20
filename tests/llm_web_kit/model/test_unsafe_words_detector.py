from unittest.mock import MagicMock, patch
import unittest

from llm_web_kit.exception.exception import CleanLangTypeExp
from llm_web_kit.input.datajson import DataJson


from llm_web_kit.model.unsafe_words_detector import (
    UnsafeWordChecker,
    decide_unsafe_word_by_data_checker,
    unsafe_words_filter,
    unsafe_words_filter_overall,
    release_unsafe_checker,
    get_unsafe_words_checker,
    *,
)



class TestUnsafeWordChecker(unittest.TestCase):

    @patch('unsafe_words_detector.get_ac')
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

    def test_check_unsafe_words(self):
        checker = UnsafeWordChecker()
        checker.ac = MagicMock()
        checker.ac.iter.return_value = []

        # Test with content containing no unsafe words
        content = "This is a safe content with no unsafe words."
        result = checker.check_unsafe_words(content)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

        # Test with content that may contain unsafe words
        checker.ac.iter.return_value = [ (10, [{'word': 'unsafe', 'level': 'L1', 'count': 1, 'sub_word': 'unsafe', 'sub_words': {'unsafe'}}]) ]
        result = checker.check_unsafe_words("This content contains an unsafe word.")
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    @patch('unsafe_words_detector.get_unsafe_words_checker')
    def test_decide_unsafe_word_by_data_checker(self, mock_get_checker):
        mock_checker = MagicMock()
        mock_checker.check_unsafe_words.return_value = [
            {'word': 'unsafe', 'level': 'L2', 'count': 1}
        ]
        mock_get_checker.return_value = mock_checker

        data_dict = {'content': 'Some content with unsafe elements.'}
        result = decide_unsafe_word_by_data_checker(data_dict, mock_checker)
        self.assertEqual(result, 'L2')

    def test_get_unsafe_words_checker(self):
        release_unsafe_checker()  # Ensure the global detector is clear
        checker1 = get_unsafe_words_checker('zh-en')
        checker2 = get_unsafe_words_checker('zh-en')
        self.assertIs(checker1, checker2)  # Should return the same instance

    def test_release_unsafe_checker(self):
        get_unsafe_words_checker('zh-en')
        release_unsafe_checker()
        self.assertEqual(len(_global_unsafe_words_detect), 0)

    @patch('unsafe_words_detector.get_unsafe_words_checker')
    def test_unsafe_words_filter(self, mock_get_checker):
        mock_checker = MagicMock()
        mock_checker.check_unsafe_words.return_value = [{'level': 'L3'}]
        mock_get_checker.return_value = mock_checker

        data_dict = {'content': 'Test content'}
        result = unsafe_words_filter(data_dict, 'en', 'text')
        self.assertEqual(result, 'L3')

    def test_unsafe_words_filter_with_unsupported_language(self):
        data_dict = {'content': 'Test content'}
        with self.assertRaises(CleanLangTypeExp):
            unsafe_words_filter(data_dict, 'unsupported_language', 'text')

    @patch('unsafe_words_detector.decide_unsafe_word_by_data_checker')
    def test_unsafe_words_filter_overall(self, mock_decide_unsafe_word):
        mock_decide_unsafe_word.return_value = 'L1'

        data_dict = {'content': 'Content with unsafe words.'}
        result = unsafe_words_filter_overall(
            data_dict,
            language='en',
            content_style='text',
            from_safe_source=False,
            from_domestic_source=False
        )
        self.assertIsInstance(result, dict)
        self.assertTrue(result['hit_unsafe_words'])

    @patch('unsafe_words_detector.auto_download')
    def test_auto_download(self, mock_auto_download):
        mock_auto_download.return_value = '/fake/path/unsafe_words.jsonl'
        result = auto_download(language='zh-en')
        self.assertEqual(result, '/fake/path/unsafe_words.jsonl')


if __name__ == '__main__':
    unittest.main()
