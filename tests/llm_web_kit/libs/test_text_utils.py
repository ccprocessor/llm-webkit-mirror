
import unittest

from llm_web_kit.libs.text_utils import (collapse_dup_newlines,
                                         normalize_text_segment)


class TestTextUtils(unittest.TestCase):
    def test_normalize_text_segment_by_space(self):
        # Test basic space normalization
        self.assertEqual(normalize_text_segment('hello   world'), 'hello world')

        # Test tabs
        self.assertEqual(normalize_text_segment('hello\tworld'), 'hello world')
        self.assertEqual(normalize_text_segment('hello\t\tworld'), 'hello world')
        self.assertEqual(normalize_text_segment('hello		world'), 'hello world')

        # Test newlines
        self.assertEqual(normalize_text_segment('hello\nworld'), 'hello\nworld')
        self.assertEqual(normalize_text_segment('hello\r\nworld'), 'hello\nworld')

        # Test control characters
        self.assertEqual(normalize_text_segment('hello\u0000world'), 'helloworld')
        self.assertEqual(normalize_text_segment('hello\u007fworld'), 'helloworld')

        # Test zero-width spaces
        self.assertEqual(normalize_text_segment('hello\u200bworld'), 'helloworld')
        self.assertEqual(normalize_text_segment('hello\u2408world'), 'helloworld')
        self.assertEqual(normalize_text_segment('hello\ufeffworld'), 'helloworld')

        # Test various width spaces
        self.assertEqual(normalize_text_segment('hello\u2002world'), 'hello world')
        self.assertEqual(normalize_text_segment('hello\u200aworld'), 'hello world')

        # Test other special spaces
        self.assertEqual(normalize_text_segment('hello\u00a0world'), 'hello world')
        self.assertEqual(normalize_text_segment('hello\u3000world'), 'hello world')

        # Test Unicode private area spaces
        self.assertEqual(normalize_text_segment('hello\U0001da7fworld'), 'hello world')
        self.assertEqual(normalize_text_segment('hello\U000e0020world'), 'hello world')

        # Test empty string
        self.assertEqual(normalize_text_segment(''), '')

        # Test string with only spaces
        self.assertEqual(normalize_text_segment('   '), ' ')

    def test_collapse_dup_newlines(self):
        # Test basic newline collapsing
        self.assertEqual(collapse_dup_newlines('hello\n\nworld'), 'hello\nworld')

        # Test multiple consecutive newlines
        self.assertEqual(collapse_dup_newlines('hello\n\n\n\nworld'), 'hello\nworld')

        # Test no duplicate newlines
        self.assertEqual(collapse_dup_newlines('hello\nworld'), 'hello\nworld')

        # Test empty string
        self.assertEqual(collapse_dup_newlines(''), '')

        # Test string with only newlines
        self.assertEqual(collapse_dup_newlines('\n\n\n'), '\n')

        # Test newlines at start and end
        self.assertEqual(collapse_dup_newlines('\n\nhello\n\n'), '\nhello\n')


if __name__ == '__main__':
    unittest.main()
