import unittest

from llm_web_kit.pipeline.extractor.html.recognizer.math import MathRecognizer

TEST_CASES = [
    # 基本公式测试用例
    {
        'input': [
            ('<span class=mathjax>Some text with a formula $$x = 5$$ in it.</span>',
             '<span class=mathjax>Some text with a formula $$x = 5$$ in it.</span>')
        ],
        'expected': [
            ('<ccmath type="latex" by="mathjax">Some text with a formula $$x = 5$$ in it.</ccmath>',
             '<span class=mathjax>Some text with a formula $$x = 5$$ in it.</span>')
        ]
    },
    # 多个公式测试用例
    {
        'input': [
            ('<span class=mathjax_display>$$a^2 + b^2 = c^2$$</span>',
             '<span class=mathjax_display>$$a^2 + b^2 = c^2$$</span>')
        ],
        'expected': [
            ('<ccmath type="latex" by="mathjax">$$a^2 + b^2 = c^2$$</ccmath>',
             '<span class=mathjax_display>$$a^2 + b^2 = c^2$$</span>')
        ]
    }
]


class TestMathRecognizer(unittest.TestCase):
    def setUp(self):
        self.math_recognizer = MathRecognizer()

    def test_math_recognizer(self):
        for test_case in TEST_CASES:
            with self.subTest(input=test_case['input']):
                output_html = self.math_recognizer.recognize(
                    'https://www.baidu.com',
                    test_case['input'],
                    ''
                )
                self.assertEqual(output_html, test_case['expected'])
