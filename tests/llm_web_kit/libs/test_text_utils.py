import unittest

from llm_web_kit.libs.text_utils import (collapse_dup_newlines,
                                         normalize_ctl_text,
                                         normalize_math_delimiters,
                                         normalize_text_segment)


class TestTextUtils(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

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
        self.assertEqual(collapse_dup_newlines('hello\n\nworld'), 'hello\n\nworld')

        # Test multiple consecutive newlines
        self.assertEqual(collapse_dup_newlines('hello\n\n\n\nworld'), 'hello\n\nworld')

        # Test no duplicate newlines
        self.assertEqual(collapse_dup_newlines('hello\nworld'), 'hello\nworld')

        # Test empty string
        self.assertEqual(collapse_dup_newlines(''), '')

        # Test string with only newlines
        self.assertEqual(collapse_dup_newlines('\n\n\n'), '\n\n')

        # Test newlines at start and end
        self.assertEqual(collapse_dup_newlines('\n\nhello\n\n'), '\n\nhello\n\n')

    def test_normalize_ctl_text(self):
        """测试控制字符和空白字符的规范化处理."""
        # 测试Unicode空白字符
        self.assertEqual(normalize_ctl_text(r'1+\frac{{q}^{2}}{\left(1-q\right)}+\frac{{q}^{6}}{\left(1-q\right)\left(1-{q}^{2}\right)}+\cdots =\prod _{j=0}^{\mathrm{\infty }}\frac{1}{\left(1-{q}^{5j+2}\right)\left(1-{q}^{5j+3}\right)},\text{for }|q|<1.'), r'1+\frac{{q}^{2}}{\left(1-q\right)}+\frac{{q}^{6}}{\left(1-q\right)\left(1-{q}^{2}\right)}+\cdots =\prod _{j=0}^{\mathrm{\infty }}\frac{1}{\left(1-{q}^{5j+2}\right)\left(1-{q}^{5j+3}\right)},\text{for }|q|<1.')  # Non-breaking space

    def test_normalize_math_delimiters(self):
        # 测试用例1: 基本行间公式
        test1 = r'[tex]f(x) = x^2 + y^2[/tex]'
        expected1 = r"""$$f(x) = x^2 + y^2$$"""
        result1 = normalize_math_delimiters(test1)
        self.assertEqual(result1, expected1, '测试用例1失败')

        # 测试用例2: 基本行内公式
        test2 = r'这是一个行内公式: [itex]E = mc^2[/itex]'
        expected2 = r'这是一个行内公式: $E = mc^2$'
        result2 = normalize_math_delimiters(test2)
        self.assertEqual(result2, expected2, '测试用例2失败')

        # 测试用例3: 多行公式
        test3 = r"""[tex]
        \Delta K = (dd^{\dagger} + d^{\dagger}d)K
        [/tex]"""
        # 注意：我们需要匹配实际的输出格式，包括空格处理
        expected3 = r"""$$\Delta K = (dd^{\dagger} + d^{\dagger}d)K$$"""
        result3 = normalize_math_delimiters(test3)
        self.assertEqual(result3, expected3, '测试用例3失败')

        # 测试用例4: 混合多个公式
        test4 = r"""这是一个段落，包含行间公式：
        [tex]f(x) = \int_{a}^{b} g(x) dx[/tex]
        以及行内公式 [itex]y = mx + b[/itex] 和另一个行内公式 [itex]\alpha + \beta = \gamma[/itex]。
        还有一个行间公式：
        [tex]
        A = \begin{pmatrix}
        a_{11} & a_{12} & a_{13} \\
        a_{21} & a_{22} & a_{23}
        \end{pmatrix}
        [/tex]"""
        expected4 = r"""这是一个段落，包含行间公式：
        $$f(x) = \int_{a}^{b} g(x) dx$$
        以及行内公式 $y = mx + b$ 和另一个行内公式 $\alpha + \beta = \gamma$。
        还有一个行间公式：
        $$A = \begin{pmatrix}
        a_{11} & a_{12} & a_{13} \\
        a_{21} & a_{22} & a_{23}
        \end{pmatrix}$$"""
        result4 = normalize_math_delimiters(test4)
        self.assertEqual(result4, expected4, '测试用例4失败')

        # 测试用例5: 空math
        test5 = r'[tex][/tex]'
        expected5 = r"""$$$$"""
        result5 = normalize_math_delimiters(test5)
        self.assertEqual(result5, expected5, '测试用例5失败')

        # 测试用例6: 只有[tex]
        test6 = r'[tex] just [tex]'
        expected6 = r"""[tex] just [tex]"""
        result6 = normalize_math_delimiters(test6)
        self.assertEqual(result6, expected6, '测试用例6失败')


if __name__ == '__main__':
    unittest.main()
