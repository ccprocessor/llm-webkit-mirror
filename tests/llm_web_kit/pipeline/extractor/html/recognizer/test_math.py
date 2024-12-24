import unittest

from llm_web_kit.pipeline.extractor.html.recognizer.ccmath import \
    MathRecognizer

TEST_CASES = [
    # 基本公式测试用例
    {
        'input': [
            ('<span class=mathjax>Some text with a formula $$x = 5$$ in it.</span>',
             '<span class=mathjax>Some text with a formula $$x = 5$$ in it.</span>')
        ],
        'raw_html': '<span class=mathjax>Some text with a formula $$x = 5$$ in it.</span>',
        'expected': [
            ('<ccmath type="latex" by="None">Some text with a formula $$x = 5$$ in it.</ccmath>',
             '<span class=mathjax>Some text with a formula $$x = 5$$ in it.</span>')
        ]
    },
    # html_list包含多个html
    {
        'input': [
            ('<p>This is a test.</p>', '<p>This is a test.</p>'),
            ('<span class=mathjax_display>$$a^2 + b^2 = c^2$$</span>',
             '<span class=mathjax_display>$$a^2 + b^2 = c^2$$</span>')
        ],
        'raw_html': '<p>This is a test.</p> <span class=mathjax_display>$$a^2 + b^2 = c^2$$</span>',
        'expected': [
            ('<p>This is a test.</p>', '<p>This is a test.</p>'),
            ('<ccmath type="latex" by="None">$$a^2 + b^2 = c^2$$</ccmath>',
             '<span class=mathjax_display>$$a^2 + b^2 = c^2$$</span>')
        ]
    },
    # raw_html包含mathjax渲染器定义
    {
        'input': [
            ('<p>This is a test.</p>', '<p>This is a test.</p>'),
            ('<span class=mathjax_display>$$a^2 + b^2 = c^2$$</span>',
             '<span class=mathjax_display>$$a^2 + b^2 = c^2$$</span>')
        ],
        'raw_html': (
            '<head> '
            '<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js'
            '?config=TeX-MML-AM_CHTML"> </script> '
            '</head> '
            '<p>This is a test.</p> '
            '<span class=mathjax_display>$$a^2 + b^2 = c^2$$</span>'
        ),
        'expected': [
            ('<p>This is a test.</p>', '<p>This is a test.</p>'),
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
            with self.subTest(input=test_case['input'], raw_html=test_case['raw_html']):
                output_html = self.math_recognizer.recognize(
                    'https://www.baidu.com',
                    test_case['input'],
                    test_case['raw_html']
                )
                self.assertEqual(output_html, test_case['expected'])
