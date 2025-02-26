import os
import sys
import unittest
from unittest import TestCase

current_file_path = os.path.abspath(__file__)
parent_dir_path = os.path.join(current_file_path, *[os.pardir] * 5)
normalized_path = os.path.normpath(parent_dir_path)
sys.path.append(normalized_path)

from llm_web_kit.model.basic_functions.char_norm import (  # noqa: E402
    ar_character_normalize, character_normalize)


class TestCharNorm(TestCase):
    def test_character_normalize(self):
        # 测试普通字符串
        self.assertEqual(character_normalize('Hello, world!'), 'Hello, world!')
        # 测试包含不可见空格和控制字符的字符串
        self.assertEqual(character_normalize('Hello\u200b, world!'), 'Hello, world!')
        # 测试包含私有使用区字符的字符串
        self.assertEqual(character_normalize('Hello\uE000, world!'), 'Hello, world!')
        # 测试包含换行和回车的字符串
        self.assertEqual(character_normalize('Hello\r\nWorld'), 'Hello\nWorld')
        # 测试包含全角空格的字符串
        self.assertEqual(character_normalize('Hello\u3000World'), 'Hello World')
        # 测试只有不可见字符的字符串
        self.assertEqual(character_normalize('\u200b\u2060'), '')

    def test_ar_character_normalize(self):
        # 测试包含普通阿拉伯语文本的字符串
        self.assertEqual(ar_character_normalize('مرحبا، العالم!'), 'مرحبا، العالم!')
        # 测试包含阿拉伯语和特定不可见空格及控制字符的字符串
        self.assertEqual(ar_character_normalize('مرحبا\u2060، العالم!'), 'مرحبا، العالم!')
        # 测试包含私有使用区字符的阿拉伯语字符串
        self.assertEqual(ar_character_normalize('مرحبا\uE000، العالم!'), 'مرحبا، العالم!')
        # 测试包含换行和回车的阿拉伯语字符串
        self.assertEqual(ar_character_normalize('مرحبا\r\nالعالم'), 'مرحبا\nالعالم')
        # 测试包含全角空格的阿拉伯语字符串
        self.assertEqual(ar_character_normalize('مرحبا\u3000العالم'), 'مرحبا العالم')
        # 测试只有不可见字符的阿拉伯语字符串
        self.assertEqual(ar_character_normalize('\u2060\ufeff'), '')


if __name__ == '__main__':
    unittest.main()
