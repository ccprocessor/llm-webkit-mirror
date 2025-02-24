# flake8: noqa: E402
import os
import sys
import unittest
from unittest.mock import mock_open, patch

current_file_path = os.path.abspath(__file__)
parent_dir_path = os.path.join(current_file_path, *[os.pardir] * 5)
normalized_path = os.path.normpath(parent_dir_path)
sys.path.append(normalized_path)

from llm_web_kit.model.basic_functions.word import (RES_MAP,
                                                    build_stop_word_set,
                                                    filter_stop_word,
                                                    get_stop_word_en_zh_set)


class TestWord(unittest.TestCase):
    def setUp(self) -> None:
        RES_MAP.clear()

    def test_build_stop_word_set_zh_only(self):
        # 模拟文件读取
        mock_file_content = '的\n是\n了\n'
        with patch('builtins.open', mock_open(read_data=mock_file_content)):
            with patch('os.path.join', return_value='dummy_path'):
                stop_words = build_stop_word_set(include_zh=True, include_en=False)
                self.assertIn('的', stop_words)
                self.assertIn('是', stop_words)
                self.assertIn('了', stop_words)
                self.assertEqual(len(stop_words), 3)

    def test_build_stop_word_set_en_only(self):
        stop_words = build_stop_word_set(include_zh=False, include_en=True)
        self.assertIn('and', stop_words)
        self.assertIn('or', stop_words)
        self.assertIn('but', stop_words)
        self.assertEqual(len(stop_words), 198)

    @patch('llm_web_kit.model.basic_functions.word.build_stop_word_set')
    def test_get_stop_word_en_zh_set(self, mock_build):
        mock_build.return_value = {'的', 'is', 'the'}
        result = get_stop_word_en_zh_set()
        self.assertEqual(result, {'的', 'is', 'the'})
        mock_build.assert_called_once_with(include_zh=True, include_en=True)

    def test_filter_stop_word(self):
        tokens = ['hello', 'world', '的']
        stop_words = {'的', '是', '了'}
        # 测试过滤功能
        filtered_tokens = filter_stop_word(tokens, stop_word_set=stop_words)
        self.assertIn('hello', filtered_tokens)
        self.assertIn('world', filtered_tokens)
        self.assertNotIn('的', filtered_tokens)
        self.assertEqual(len(filtered_tokens), 2)


if __name__ == '__main__':
    unittest.main()
