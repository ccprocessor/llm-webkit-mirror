import math
import os
import sys
import unittest
from unittest.mock import patch

current_file_path = os.path.abspath(__file__)
parent_dir_path = os.path.join(current_file_path, *[os.pardir] * 5)
normalized_path = os.path.normpath(parent_dir_path)
sys.path.append(normalized_path)

from llm_web_kit.model.basic_functions.utils import content2words  # noqa: E402
from llm_web_kit.model.basic_functions.utils import jieba_lcut  # noqa: E402
from llm_web_kit.model.basic_functions.utils import (  # noqa: E402
    dict_wrapper, div_zero)


class TestUtils(unittest.TestCase):

    def test_div_zero(self):
        self.assertEqual(div_zero(10, 5), 2)
        self.assertTrue(math.isnan(div_zero(0, 0)))
        self.assertEqual(div_zero(10, 0), float('inf'))
        self.assertNotEqual(div_zero(10, 3), 0)

    def test_dict_wrapper(self):
        @dict_wrapper(['result'])
        def sample_function():
            return 42

        self.assertEqual(sample_function(), {'result': 42})
        self.assertEqual(sample_function(as_dict=False), 42)

    @patch('llm_web_kit.model.basic_functions.utils.jieba_fast.lcut')
    def test_jieba_lcut(self, mock_lcut):
        mock_lcut.return_value = ['hello', 'world']
        jieba_lcut.cache_clear()
        self.assertEqual(jieba_lcut('hello world'), ['hello', 'world'])
        mock_lcut.assert_called_with('hello world')

    def test_content2words(self):
        with patch('llm_web_kit.model.basic_functions.utils.jieba_lcut') as mock_lcut:
            mock_lcut.return_value = ['hello', 'world', '123', ' ']
            self.assertEqual(content2words('hello world 123 '), ['hello', 'world', '123'])
            self.assertEqual(content2words('hello world 123 ', alpha=True), ['hello', 'world'])


if __name__ == '__main__':
    unittest.main()
