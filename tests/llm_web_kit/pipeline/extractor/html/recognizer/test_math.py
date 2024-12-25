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
            ('<ccmath type="latex">Some text with a formula $$x = 5$$ in it.</ccmath>',
             '<span class=mathjax>Some text with a formula $$x = 5$$ in it.</span>')
        ]
    },
    # 已经包含cccode标签
    {
        'input': [
            ('<cccode class=mathjax>Some text with a formula $$x = 5$$ in it.</cccode>',
             '<cccode class=mathjax>Some text with a formula $$x = 5$$ in it.</cccode>')
        ],
        'raw_html': '<span class=mathjax>Some text with a formula $$x = 5$$ in it.</span>',
        'expected': [
            ('<cccode class=mathjax>Some text with a formula $$x = 5$$ in it.</cccode>',
             '<cccode class=mathjax>Some text with a formula $$x = 5$$ in it.</cccode>')
        ]
    },
    # html_list包含多个html，class=MathJax_Display
    {
        'input': [
            ('<p>This is a test.</p>', '<p>This is a test.</p>'),
            ('<span class=Mathjax_display>$$a^2 + b^2 = c^2$$</span>',
             '<span class=Mathjax_display>$$a^2 + b^2 = c^2$$</span>')
        ],
        'raw_html': '<p>This is a test.</p> <span class=mathjax_display>$$a^2 + b^2 = c^2$$</span>',
        'expected': [
            ('<p>This is a test.</p>', '<p>This is a test.</p>'),
            ('<ccmath type="latex">$$a^2 + b^2 = c^2$$</ccmath>',
             '<span class=Mathjax_display>$$a^2 + b^2 = c^2$$</span>')
        ]
    },
    # raw_html包含mathjax渲染器定义，class=mathjax_display
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

TEST_EQUATION_TYPE = [
    {
        'input': '$$a^2 + b^2 = c^2$$',
        'expected': 'equation-display'
    },
    {
        'input': '$a^2 + b^2 = c^2$',
        'expected': 'equation-inline'
    }
]

TEST_CONTENT_LIST_NODE = [
    {
        'input': '<ccmath type="latex" by="mathjax">$$x = 5$$</ccmath>',
        'expected': {
            'type': 'equation-display',
            'raw_content': "<ccmath type=\"latex\" by=\"mathjax\">$$x = 5$$</ccmath>",
            'content': {
                'math_content': '$$x = 5$$',
                'math_type': 'latex',
                'by': 'mathjax'
            }
        }
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

    def test_get_equation_type(self):
        for test_case in TEST_EQUATION_TYPE:
            with self.subTest(input=test_case['input']):
                output_type = self.math_recognizer.get_equation_type(test_case['input'])
                self.assertEqual(output_type, test_case['expected'])

    def test_to_content_list_node(self):
        for test_case in TEST_CONTENT_LIST_NODE:
            with self.subTest(input=test_case['input']):
                output_node = self.math_recognizer.to_content_list_node(test_case['input'])
                self.assertEqual(output_node, test_case['expected'])

        # 测试没有ccmath标签的情况
        invalid_content = '<div>Some math content</div>'
        with self.assertRaises(ValueError) as exc_info:
            self.math_recognizer.to_content_list_node(invalid_content)
        self.assertIn('No ccmath element found in content', str(exc_info.exception))
