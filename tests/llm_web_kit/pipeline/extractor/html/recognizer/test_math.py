import unittest

from llm_web_kit.pipeline.extractor.html.recognizer.ccmath import \
    MathRecognizer

TEST_CASES = [
    # 基本公式测试用例
    {
        'input': [
            (
                ('<p>这是p的text<span class="mathjax_display">'
                 '$$a^2 + b^2 = c^2$$</span>这是span的tail<b>这是b的text</b>'
                 '这是b的tail</p>'),
                ('<p>这是p的text<span class="mathjax_display">'
                 '$$a^2 + b^2 = c^2$$</span>这是span的tail<b>这是b的text</b>'
                 '这是b的tail</p>')
            )
        ],
        'raw_html': (
            '<head> '
            '<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js'
            '?config=TeX-MML-AM_CHTML"> </script> '
            '</head> '
            '<p>这是p的text<span class="mathjax_display">$$a^2 + b^2 = c^2$$</span>这是span的tail<b>这是b的text</b>这是b的tail</p>'
        ),
        'expected': [
            ['这是p的text', '这是p的text'],
            ('<ccmath type="latex" by="mathjax" '
             'html="&lt;span class=&quot;mathjax_display&quot;&gt;'
             '$$a^2 + b^2 = c^2$$&lt;/span&gt;&#x8FD9;&#x662F;span&#x7684;tail">'
             '$$a^2 + b^2 = c^2$$</ccmath>',
             '<span class="mathjax_display">$$a^2 + b^2 = c^2$$</span>这是span的tail'),
            ['这是span的tail', '这是span的tail'],
            ('<b>这是b的text</b>这是b的tail', '<b>这是b的text</b>这是b的tail')
        ]
    },
    # 已经包含cccode标签
    # {
    #     'input': [
    #         ('<cccode class=mathjax>Some text with a formula $$x = 5$$ in it.</cccode>',
    #          '<cccode class=mathjax>Some text with a formula $$x = 5$$ in it.</cccode>')
    #     ],
    #     'raw_html': '<span class=mathjax>Some text with a formula $$x = 5$$ in it.</span>',
    #     'expected': [
    #         ('<cccode class=mathjax>Some text with a formula $$x = 5$$ in it.</cccode>',
    #          '<cccode class=mathjax>Some text with a formula $$x = 5$$ in it.</cccode>')
    #     ]
    # },
    # html_list包含多个html，class=MathJax_Display
    # {
    #     'input': [
    #         ('<p>This is a test.</p>', '<p>This is a test.</p>'),
    #         ('<span class=Mathjax_display>$$a^2 + b^2 = c^2$$</span>',
    #          '<span class=Mathjax_display>$$a^2 + b^2 = c^2$$</span>')
    #     ],
    #     'raw_html': '<p>This is a test.</p> <span class=mathjax_display>$$a^2 + b^2 = c^2$$</span>',
    #     'expected': [
    #         ('<p>This is a test.</p>', '<p>This is a test.</p>'),
    #         ('<ccmath type="latex">$$a^2 + b^2 = c^2$$</ccmath>',
    #          '<span class=Mathjax_display>$$a^2 + b^2 = c^2$$</span>')
    #     ]
    # },
    # raw_html包含mathjax渲染器定义，class=mathjax_display
    # {
    #     'input': [
    #         ('<p>这是p的text<span class=mathjax_display>$$a^2 + b^2 = c^2$$</span>这是span的tail<b>这是b的text</b>这是b的tail</p>'),
    #         ('<p>这是p的text<span class=mathjax_display>$$a^2 + b^2 = c^2$$</span>这是span的tail<b>这是b的text</b>这是b的tail</p>')
    #     ],
    #     'raw_html': (
    #         '<head> '
    #         '<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js'
    #         '?config=TeX-MML-AM_CHTML"> </script> '
    #         '</head> '
    #         '<p>这是p的text<span class=mathjax_display>$$a^2 + b^2 = c^2$$</span>这是span的tail<b>这是b的text</b>这是b的tail</p>'
    #     ),
    #     'expected': [
    #         ('<p>这是p的text<ccmath type="latex" by="mathjax">$$a^2 + b^2 = c^2$$</ccmath>这是span的tail<b>这是b的text</b>这是b的tail</p>',
    #          '<p>这是p的text<span class=mathjax_display>$$a^2 + b^2 = c^2$$</span>这是span的tail<b>这是b的text</b>这是b的tail</p>')
    #     ]
    # }
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
        'input': (
            'https://www.baidu.com',
            '<ccmath type="latex" by="mathjax">$$x = 5$$</ccmath>',
            '<span class=mathjax_display>$$a^2 + b^2 = c^2$$</span>'
        ),
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

TEST_CONTAINS_MATH = [
    {
        'input': '<span>$$x^2$$</span>',
        'expected': (True, 'latex')
    },
    {
        'input': '<span>x<sub>1</sub> + x<sup>2</sup></span>',
        'expected': (True, 'htmlmath')
    },
    # {
    #     'input': '<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mi>x</mi><mn>2</mn></msup></math>',
    #     'expected': (True, 'mathml')
    # },
    {
        'input': '<p>Matrices: <code>[[a,b],[c,d]]</code> yields to `[[a,b],[c,d]]`</p>',
        'expected': (True, 'asciimath')
    },
    {
        'input': '<p>Matrices: <code>[[a,b],[c,d]]</code> </p>',
        'expected': (False, None)
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
                print(output_html)
                self.assertEqual(len(output_html), len(test_case['expected']))
                for i in range(len(output_html)):
                    self.assertEqual(output_html[i], test_case['expected'][i])

    def test_get_equation_type(self):
        for test_case in TEST_EQUATION_TYPE:
            with self.subTest(input=test_case['input']):
                output_type = self.math_recognizer.get_equation_type(test_case['input'])
                self.assertEqual(output_type, test_case['expected'])

    def test_to_content_list_node(self):
        for test_case in TEST_CONTENT_LIST_NODE:
            with self.subTest(input=test_case['input']):
                output_node = self.math_recognizer.to_content_list_node(
                    test_case['input'][0],
                    test_case['input'][1],
                    test_case['input'][2]
                )
                self.assertEqual(output_node, test_case['expected'])

        # 测试没有ccmath标签的情况
        invalid_content = (
            'https://www.baidu.com',
            '<div>Some math content</div>',
            '<div>Some math content</div>'
        )
        with self.assertRaises(ValueError) as exc_info:
            self.math_recognizer.to_content_list_node(
                invalid_content[0],
                invalid_content[1],
                invalid_content[2]
            )
        self.assertIn('No ccmath element found in content', str(exc_info.exception))

    def test_contains_math(self):
        for test_case in TEST_CONTAINS_MATH:
            with self.subTest(input=test_case['input']):
                print(test_case['input'])
                output_contains, output_type = self.math_recognizer.contains_math(test_case['input'])
                self.assertEqual(output_contains, test_case['expected'][0])
                self.assertEqual(output_type, test_case['expected'][1])
