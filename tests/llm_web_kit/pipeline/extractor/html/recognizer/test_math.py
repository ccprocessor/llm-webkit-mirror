import html
import re
import sys
sys.path.append('/nvme/pzx/llm-webkit-mirror')

import unittest
from difflib import SequenceMatcher
from pathlib import Path

from lxml import etree

from llm_web_kit.pipeline.extractor.html.recognizer.cc_math.common import \
    CCMATH
from llm_web_kit.pipeline.extractor.html.recognizer.ccmath import \
    MathRecognizer
from llm_web_kit.pipeline.extractor.html.recognizer.recognizer import CCTag

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
            (
                '<html><body><p>这是p的text</p></body></html>',
                '<html><body><p>这是p的text</p></body></html>'
            ),
            (
                '<html><body><p><ccmath-interline type="latex" by="mathjax" '
                'html="&lt;span class=&quot;mathjax_display&quot;&gt;$$a^2 + b^2 = c^2$$'
                '&lt;/span&gt;&#x8FD9;&#x662F;span&#x7684;tail">$$a^2 + b^2 = c^2$$'
                '</ccmath-interline></p></body></html>',
                '<span class="mathjax_display">$$a^2 + b^2 = c^2$$</span>这是span的tail'
            ),
            (
                '<html><body><p>这是span的tail<b>这是b的text</b>这是b的tail</p></body></html>',
                '<html><body><p>这是span的tail<b>这是b的text</b>这是b的tail</p></body></html>'
            )
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

expected_interline_files = [
    f'/nvme/pzx/llm-webkit-mirror/tests/llm_web_kit/pipeline/extractor/html/recognizer/assets/ccmath/p_gt_interline/{i}.html'
    for i in range(1, 13)
]

expected_inline_files = [
    f'/nvme/pzx/llm-webkit-mirror/tests/llm_web_kit/pipeline/extractor/html/recognizer/assets/ccmath/p_gt_inline/{i}.html'
    for i in range(1, 92)
]

TEST_CASES_HTML = [
    # math-container, latex + mathjax
    # {
    #     'input': ['assets/ccmath/stackexchange_1_span-math-container_latex_mathjax.html'],
    #     'base_url': 'https://worldbuilding.stackexchange.com/questions/162264/is-there-a-safe-but-weird-distance-from-black-hole-merger',
    #     'expected': [
    #         'assets/ccmath/stackexchange_1_interline_1.html',
    #         'assets/ccmath/stackexchange_1_interline_2.html',
    #     ],
    # },
    {
        'input': ['/nvme/pzx/llm-webkit-mirror/tests/llm_web_kit/pipeline/extractor/html/recognizer/assets/ccmath/p_test.html'],
        'base_url': 'https://worldbuilding.stackexchange.com/questions/162264/is-there-a-safe-but-weird-distance-from-black-hole-merger',
        'expected_interline': expected_interline_files,
        'expected_inline': expected_inline_files
    },
    
    # {
    #     'input': [
    #         'assets/ccmath/libretexts_1_p_latex_mathjax.html',
    #     ],
    #     'base_url': 'https://math.libretexts.org/Under_Construction/Purgatory/Remixer_University/Username%3A_pseeburger/MTH_098_Elementary_Algebra/1%3A_Foundations/1.5%3A_Multiply_and_Divide_Integers',
    #     'expected_interline': expected_interline_files,
    #     'expected_inline': expected_inline_files
    # }
]

TEST_EQUATION_TYPE = [
    {
        'input': '$$a^2 + b^2 = c^2$$',
        'expected': 'equation-interline'
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
            '<ccmath-interline type="latex" by="mathjax" html="&lt;span class=&quot;math-container&quot;&gt;$$h$$&lt;/span&gt;">$$h$$</ccmath-interline>',
            '<span class="math-container">$$h$$</span>'
        ),
        'expected': {
            'type': 'equation-interline',
            'raw_content': '<span class="math-container">$$h$$</span>',
            'content': {
                'math_content': '$$h$$',
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

TEST_GET_MATH_RENDER = [
    {
        'input': [
            'assets/ccmath/stackexchange_1_span-math-container_latex_mathjax.html'
        ],
        'base_url': 'https://worldbuilding.stackexchange.com/questions/162264/is-there-a-safe-but-weird-distance-from-black-hole-merger',
        'expected': 'mathjax',
    },
    {
        'input': [
            'assets/ccmath/libretexts_1_p_latex_mathjax.html',
        ],
        'base_url': 'https://math.libretexts.org/Under_Construction/Purgatory/Remixer_University/Username%3A_pseeburger/MTH_098_Elementary_Algebra/1%3A_Foundations/1.5%3A_Multiply_and_Divide_Integers',
        'expected': 'mathjax',
    }
]

base_dir = Path(__file__).parent
cm = CCMATH()

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

    def get_p_gt(self, raw_html):

        html_content = raw_html
        html_content = re.sub(r'&[^;\s]+;', '', html_content)  # 删除无效实体
        html_content = html_content.replace("&nbsp;", " ")  # 将 &nbsp; 替换为空格
        tree = etree.HTML(html_content)
        paragraphs = tree.xpath('//p/text()')
        paragraphs = [p.strip() for p in paragraphs if p.strip()]  # 去除空白内容

        interline_root = '/nvme/pzx/llm-webkit-mirror/tests/llm_web_kit/pipeline/extractor/html/recognizer/assets/ccmath/p_test_gt_interline.html'
        inerline_root = '/nvme/pzx/llm-webkit-mirror/tests/llm_web_kit/pipeline/extractor/html/recognizer/assets/ccmath/p_test_gt_inline.html'
        with open(interline_root, 'w') as f1, open(inerline_root, 'w') as f2:
            for para in paragraphs:
                flag, _ = cm.contains_math(para)
                
                if flag:
                    equation_type = cm.get_equation_type(para)
                    if equation_type == 'equation-inline':
                        f2.write(para + '\n')
                    else:
                        f1.write(para + '\n')

    def assertStringsSimilar(self, expect, actual, threshold=0.5):
        similarity = SequenceMatcher(None, expect, actual).ratio()
        self.assertGreaterEqual(similarity, threshold, f"Expected similarity of at least {threshold*100}%, but got {similarity*100}% between '{expect}' and '{actual}'")

    def test_math_recognizer_html(self):
                
        for test_case in TEST_CASES_HTML:
            raw_html_path = base_dir.joinpath(test_case['input'][0])
            print('base_dir::::::::', base_dir)
            print('raw_html_path::::::::', raw_html_path)
            base_url = test_case['base_url']
            raw_html = raw_html_path.read_text()
            # self.get_p_gt(raw_html)
            # exit(0)

            parts = self.math_recognizer.recognize(base_url, [(raw_html, raw_html)], raw_html)
            print('----------------------------------')
            print('total len(parts):', len(parts))
            print('----------------------------------')
            # for i, part in enumerate(parts):
            #     if CCTag.CC_MATH_INTERLINE in part[0]:
            #         print(part[0])
            #         print(i)
            # exit(0)
            interline_parts = [part[0] for part in parts if CCTag.CC_MATH_INTERLINE in part[0]]
            inline_parts = [part[0] for part in parts if CCTag.CC_MATH_INLINE in part[0]]

            print('post len(interline_parts):', len(interline_parts))
            print('post len(inline_parts):', len(inline_parts))
            # self.assertEqual(len(interline_parts), len(test_case['expected_interline']))
            # self.assertEqual(len(inline_parts), len(test_case['expected_inline']))
            parts = [part[0] for part in parts if CCTag.CC_MATH_INTERLINE in part[0]]
            # self.assertEqual(len(parts), len(test_case['expected']))
            # for expect_path, part in zip(test_case['expected'], parts):
            #     expect = base_dir.joinpath(expect_path).read_text().strip()
            #     a_tree = etree.fromstring(part, None)
            #     a_result = a_tree.xpath(f'.//{CCTag.CC_MATH_INTERLINE}')[0]
            #     answer = a_result.text
            #     print('part::::::::', part)
            #     print('answer::::::::', answer)
            #     # print('expect::::::::', expect)
            #     self.assertEqual(expect, answer)

            for expect_path, part in zip(test_case['expected_interline'], interline_parts):
                expect = base_dir.joinpath(expect_path).read_text().strip()
                tree = etree.fromstring(part)

                interline_answers = tree.xpath('//ccmath-interline/text()')[0].strip()
                inter_tree = etree.HTML(interline_answers)
                interline_answers = ''.join(inter_tree.itertext()).strip() # 去掉最外层p标签

                print('answer::::::::', interline_answers)
                # print('expect::::::::', expect)
                # self.assertStringsSimilar(expect, interline_answers, threshold=0.5)
                # self.assertEqual(expect, answers)

            for expect_path, part in zip(test_case['expected_inline'], inline_parts):
                # print(part)
                # exit(0)
                expect = base_dir.joinpath(expect_path).read_text().strip()
                tree = etree.fromstring(part)

                inline_answers = tree.xpath('//ccmath-inline/text()')[0].strip()
                inner_tree = etree.HTML(inline_answers)
                inline_answers = ''.join(inner_tree.itertext()).strip()

                print('answer::::::::', inline_answers)
                # print('expect::::::::', expect)
                # exit(0)
                # self.assertStringsSimilar(expect, inline_answers, threshold=0.5)
                # self.assertEqual(expect, answers)

    # def test_get_math_render(self):
    #     for test_case in TEST_GET_MATH_RENDER:
    #         raw_html_path = base_dir.joinpath(test_case['input'][0])
    #         raw_html = raw_html_path.read_text()
    #         output_render = self.math_recognizer.get_math_render(raw_html)
    #         self.assertEqual(output_render, test_case['expected'])

    # def test_get_equation_type(self):
    #     for test_case in TEST_EQUATION_TYPE:
    #         with self.subTest(input=test_case['input']):
    #             output_type = self.math_recognizer.get_equation_type(test_case['input'])
    #             self.assertEqual(output_type, test_case['expected'])

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


class TestCCMATH(unittest.TestCase):
    def setUp(self):
        self.ccmath = CCMATH()

    def test_get_equation_type(self):
        for test_case in TEST_EQUATION_TYPE:
            with self.subTest(input=test_case['input']):
                output_type = self.ccmath.get_equation_type(test_case['input'])
                self.assertEqual(output_type, test_case['expected'])

    def test_contains_math(self):
        for test_case in TEST_CONTAINS_MATH:
            with self.subTest(input=test_case['input']):
                output_contains_math = self.ccmath.contains_math(test_case['input'])
                self.assertEqual(output_contains_math, test_case['expected'])

    def test_get_math_render(self):
        for test_case in TEST_GET_MATH_RENDER:
            raw_html_path = base_dir.joinpath(test_case['input'][0])
            raw_html = raw_html_path.read_text()
            output_render = self.ccmath.get_math_render(raw_html)
            self.assertEqual(output_render, test_case['expected'])


if __name__ == '__main__':
    r = TestMathRecognizer()
    r.setUp()
    r.test_math_recognizer_html()
    # r.test_to_content_list_node()
    # html = r'<p class="lt-math-15120">\[\begin{array} {ll} {5 \cdot 3 = 15} &amp;{-5(3) = -15} \\ {5(-3) = -15} &amp;{(-5)(-3) = 15} \end{array}\]</p>'
    # tree = etree.fromstring(html, None)
    # print(tree.text)
