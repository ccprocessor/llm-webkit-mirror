import unittest

from llm_web_kit.model.basic_functions.format_check import (is_en_letter,
                                                            is_pure_en_word,
                                                            is_space)


# 测试类
class TestFunctions(unittest.TestCase):
    def test_is_en_letter(self):
        # 正常情况：英文大小写字母
        self.assertTrue(is_en_letter('a'), "小写字母 'a' 应返回 True")
        self.assertTrue(is_en_letter('z'), "小写字母 'z' 应返回 True")
        self.assertTrue(is_en_letter('A'), "大写字母 'A' 应返回 True")
        self.assertTrue(is_en_letter('Z'), "大写字母 'Z' 应返回 True")

        # 异常情况：非英文字母
        self.assertFalse(is_en_letter('1'), "数字 '1' 应返回 False")
        self.assertFalse(is_en_letter('@'), "特殊字符 '@' 应返回 False")
        self.assertFalse(is_en_letter('ä'), "非英文字符 'ä' 应返回 False")
        self.assertFalse(is_en_letter('中'), "中文字符 '中' 应返回 False")

    def test_is_space(self):
        # 正常情况：空格和制表符
        self.assertTrue(is_space(' '), "空格 ' ' 应返回 True")
        self.assertTrue(is_space('\t'), "制表符 '\t' 应返回 True")

        # 异常情况：非空格字符
        self.assertFalse(is_space('\n'), "换行符 '\n' 应返回 False")
        self.assertFalse(is_space('\r'), "回车符 '\r' 应返回 False")
        self.assertFalse(is_space('a'), "字母 'a' 应返回 False")
        self.assertFalse(is_space('1'), "数字 '1' 应返回 False")

    def test_is_pure_en_word(self):
        # 正常情况：纯英文单词或带空格的短语
        self.assertTrue(is_pure_en_word('hello'), "'hello' 应返回 True")
        self.assertTrue(is_pure_en_word('World'), "'World' 应返回 True")
        self.assertTrue(is_pure_en_word('hello world'), "'hello world' 应返回 True")
        self.assertTrue(is_pure_en_word('Test \t Pass'), "'Test \t Pass' 应返回 True")
        self.assertTrue(is_pure_en_word(' '), "单个空格 ' ' 应返回 True")
        self.assertTrue(is_pure_en_word('\t\t'), "仅制表符 '\t\t' 应返回 True")

        self.assertTrue(is_pure_en_word(''), "空字符串 '' 应返回 True 但需确认需求")

        # 异常情况：包含非英文或非空格字符
        self.assertFalse(is_pure_en_word('hello1'), "'hello1' 应返回 False")
        self.assertFalse(is_pure_en_word('123'), "'123' 应返回 False")
        self.assertFalse(is_pure_en_word('hello!'), "'hello!' 应返回 False")
        self.assertFalse(is_pure_en_word('word#'), "'word#' 应返回 False")
        self.assertFalse(is_pure_en_word('helloä'), "'helloä' 应返回 False")
        self.assertFalse(is_pure_en_word('中文'), "'中文' 应返回 False")


if __name__ == '__main__':
    unittest.main()
