import unittest
from pathlib import Path

from llm_web_kit.exception.exception import HtmlMathRecognizerExp
from llm_web_kit.libs.html_utils import html_to_element
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
                '<p>这是p的text<span class="mathjax_display"></span></p>',
                '<p>这是p的text<span class="mathjax_display"></span></p>'
            ),
            (
                '<p><span class="mathjax_display"><ccmath-interline type="latex" by="mathjax" html="a^2 + b^2 = c^2">a^2 + b^2 = c^2</ccmath-interline></span></p>',
                '<p><span class="mathjax_display"><ccmath-interline type="latex" by="mathjax" html="a^2 + b^2 = c^2">a^2 + b^2 = c^2</ccmath-interline></span></p>'
            ),
            (
                '<p><span class="mathjax_display"></span>这是span的tail<b>这是b的text</b>这是b的tail</p>',
                '<p><span class="mathjax_display"></span>这是span的tail<b>这是b的text</b>这是b的tail</p>'
            )
        ]
    },
    {
        'input': [
            ('<p>$x = 5$,$$x=6$$</p>',
             '<p>$x = 5$,$$x=6$$</p>')
        ],
        'raw_html': '<p>$x = 5$,$$x=6$$</p>',
        'expected': [
            ('<p><ccmath-inline type="latex" by="None" html="x = 5">x = 5</ccmath-inline>,</p>',
             '<p><ccmath-inline type="latex" by="None" html="x = 5">x = 5</ccmath-inline>,</p>'),
             ('<p><ccmath-interline type="latex" by="None" html="x=6">x=6</ccmath-interline></p>',
              '<p><ccmath-interline type="latex" by="None" html="x=6">x=6</ccmath-interline></p>')
        ]
    },
    {
        'input': [
            ('<p>By substituting $$x$$ with $$t - \\dfrac{b}{3a}$$, the general</p>',
             '<p>By substituting $$x$$ with $$t - \\dfrac{b}{3a}$$, the general</p>')
        ],
        'raw_html': '<p>By substituting $$x$$ with $$t - \\dfrac{b}{3a}$$, the general</p>',
        'expected': [
            ('<p>By substituting </p>',
             '<p>By substituting </p>'),
            ('<p><ccmath-interline type="latex" by="None" html="x">x</ccmath-interline></p>',
             '<p><ccmath-interline type="latex" by="None" html="x">x</ccmath-interline></p>'),
            ('<p> with </p>',
             '<p> with </p>'),
            ('<p><ccmath-interline type="latex" by="None" html="t - \\dfrac{b}{3a}">t - \\dfrac{b}{3a}</ccmath-interline></p>',
             '<p><ccmath-interline type="latex" by="None" html="t - \\dfrac{b}{3a}">t - \\dfrac{b}{3a}</ccmath-interline></p>'),
            ('<p>, the general</p>',
             '<p>, the general</p>')
        ]
    },
]

TEST_CASES_HTML = [
    # math-container, latex + mathjax
    {
        'input': ['assets/ccmath/stackexchange_1_span-math-container_latex_mathjax.html'],
        'base_url': 'https://worldbuilding.stackexchange.com/questions/162264/is-there-a-safe-but-weird-distance-from-black-hole-merger',
        'expected': 'assets/ccmath/stackexchange_1_span-math-container_latex_mathjax_1.html'
    },
    {
        'input': [
            'assets/ccmath/libretexts_1_p_latex_mathjax.html',
        ],
        'base_url': 'https://math.libretexts.org/Under_Construction/Purgatory/Remixer_University/Username%3A_pseeburger/MTH_098_Elementary_Algebra/1%3A_Foundations/1.5%3A_Multiply_and_Divide_Integers',
        'expected': 'assets/ccmath/libretexts_1_p_latex_mathjax_1.html'
    },
    {
        'input': [
            'assets/ccmath/mathjax_tex_chtml.html',
        ],
        'base_url': 'https://math.libretexts.org/Under_Construction/Purgatory/Remixer_University/Username%3A_pseeburger/MTH_098_Elementary_Algebra/1%3A_Foundations/1.5%3A_Multiply_and_Divide_Integers',
        'expected': 'assets/ccmath/mathjax_tex_chtml_1.html'
    },
    {
        'input': [
            'assets/ccmath/wikipedia_1_math_annotation.html',
        ],
        'base_url': 'https://en.m.wikipedia.org/wiki/Variance',
        'expected': 'assets/ccmath/wikipedia_1_math_annotation_1.html'
    },
    {
        'input': [
            'assets/ccmath/mathjax-mml-chtml.html',
        ],
        'base_url': 'https://mathjax.github.io/MathJax-demos-web/tex-chtml.html',
        'expected': 'assets/ccmath/mathjax-mml-chtml_1.html'
    },
    # img latex.php
    {
        'input': ['assets/ccmath/geoenergymath_img.html'],
        'base_url': 'https://geoenergymath.com/2017/03/04/the-chandler-wobble-challenge/',
        'expected': 'assets/ccmath/geoenergymath_img_1.html'
    },
    # # img codecogs.com
    {
        'input': ['assets/ccmath/img_codecogs_com.html'],
        'base_url': 'https://up-skill.me/math/find-interquartile-range.html',
        'expected': 'assets/ccmath/img_codecogs_com_1.html'
    },
    # img mimetex.cgi
    {
        'input': ['assets/ccmath/img_mimetex_cgi.html'],
        'base_url': 'https://math.eretrandre.org/tetrationforum/showthread.php?tid=965',
        'expected': 'assets/ccmath/img_mimetex_cgi_1.html'
    },
    {
        'input': ['assets/ccmath/katex_mathjax.html'],
        'base_url': 'https://www.intmath.com/cg5/katex-mathjax-comparison.php',
        'expected': 'assets/ccmath/katex_mathjax_1.html'
    },
    {
        'input': ['assets/ccmath/asciimath.html'],
        'base_url': 'https://www.wjagray.co.uk/maths/ASCIIMathTutorial.html',
        'expected': 'assets/ccmath/asciimath_1.html'
    },
    {
        'input': ['assets/ccmath/mathtex_script_type.html'],
        'base_url': 'https://www.intmath.com/cg5/katex-mathjax-comparison.php',
        'expected': 'assets/ccmath/mathtex_script_type_1.html'
    },
    {
        'input': [
            'assets/ccmath/mathjax-mml-chtml_prefix.html',
        ],
        'base_url': 'https://mathjax.github.io/MathJax-demos-web/tex-chtml.html',
        'expected': 'assets/ccmath/mathjax-mml-chtml_prefix_1.html'
    },
]

TEST_EQUATION_TYPE = [
    {
        'input': '<span>$$a^2 + b^2 = c^2$$</span>',
        'expected': [('ccmath-interline', 'latex')]
    },
    {
        'input': '<span>$a^2 + b^2 = c^2$</span>',
        'expected': [('ccmath-inline', 'latex')]
    },
    {
        'input': '<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>a</mi><mo>&#x2260;</mo><mn>0</mn></math>',
        'expected': [('ccmath-inline', 'mathml')]
    },
    {
        'input': '<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mi>a</mi><mo>&#x2260;</mo><mn>0</mn></math>',
        'expected': [('ccmath-interline', 'mathml')]
    },
    {
        'input': '<span>x<sub>1</sub> + x<sup>2</sup></span>',
        'expected': [('ccmath-inline', 'htmlmath')]
    },
    {
        'input': '<p>`x=(-b +- sqrt(b^2 - 4ac))/(2a)`</p>',
        'expected': [('ccmath-interline', 'asciimath')]
    },
    {
        'input': '<p>Matrices: <code>[[a,b],[c,d]]</code> </p>',
        'expected': [(None, None)]
    },
    {
        'input': '<p>这是p的text</p>',
        'expected': [(None, None)]
    },
    {
        'input': r'<p>\begin{align} a^2+b=c\end{align}</p>',
        'expected': [('ccmath-interline', 'latex')]
    },
    {
        'input': r'<p>$$x=5$$,$x=6$</p>',
        'expected': [('ccmath-interline', 'latex'), ('ccmath-inline', 'latex')]
    }
]

TEST_CONTENT_LIST_NODE = [
    {
        'input': (
            'https://www.baidu.com',
            '<html><body><p><ccmath-interline type="latex" by="mathjax" html="&lt;span class=&quot;math-container&quot;&gt;$$h \\approx {{GM} \\over c^2} \\times {1 \\over r} \\times {v^2 \\over c^2}$$&lt;/span&gt;">$$h \\approx {{GM} \\over c^2} \\times {1 \\over r} \\times {v^2 \\over c^2}$$</ccmath-interline></p></body></html>',
            '<span class="math-container">$$h \\approx {{GM} \\over c^2} \\times {1 \\over r} \\times {v^2 \\over c^2}$$</span>'
        ),
        'expected': {
            'type': 'equation-interline',
            'raw_content': '<span class="math-container">$$h \\approx {{GM} \\over c^2} \\times {1 \\over r} \\times {v^2 \\over c^2}$$</span>',
            'content': {
                'math_content': 'h \\approx {{GM} \\over c^2} \\times {1 \\over r} \\times {v^2 \\over c^2}',
                'math_type': 'latex',
                'by': 'mathjax'
            }
        }
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
    },
    {
        'input': [
            'assets/ccmath/math_katex_latex_2.html',
        ],
        'base_url': 'https://www.intmath.com/cg5/katex-mathjax-comparison.php',
        'expected': 'katex',
    }
]

TEST_WRAP_MATH = [
    {
        'input': '$$a^2 + b^2 = c^2$$',
        'display': True,
        'expected': '$$a^2 + b^2 = c^2$$'
    },
    {
        'input': r'{\displaystyle \operatorname {Var} (X)=\operatorname {E} \left[(X-\mu)^{2}\right].}',
        'display': False,
        'expected': r'${\displaystyle \operatorname {Var} (X)=\operatorname {E} \left[(X-\mu)^{2}\right].}$',
    },
    {
        'input': r'\begin{align}a^2 + b^2 = c^2\end{align}',
        'display': True,
        'expected': r'\begin{align}a^2 + b^2 = c^2\end{align}',
    }
]

TEST_WRAP_MATH_MD = [
    {
        'input': r'$$a^2 + b^2 = c^2$$',
        'expected': r'a^2 + b^2 = c^2'
    },
    {
        'input': r'{\displaystyle \operatorname {Var} (X)=\operatorname {E} \left[(X-\mu)^{2}\right].}',
        'expected': r'{\displaystyle \operatorname {Var} (X)=\operatorname {E} \left[(X-\mu)^{2}\right].}'
    },
    {
        'input': r'$a^2 + b^2 = c^2$',
        'expected': r'a^2 + b^2 = c^2'
    },
    {
        'input': r'\(a^2 + b^2 = c^2\)',
        'expected': r'a^2 + b^2 = c^2'
    },
    {
        'input': r'\[a^2 + b^2 = c^2\]',
        'expected': r'a^2 + b^2 = c^2'
    }
]

base_dir = Path(__file__).parent


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
                expect_len = len(test_case['expected'])
                self.assertEqual(len(output_html), len(test_case['expected']), msg=f'result is: {len(output_html)}, expected is: {expect_len}')
                for i in range(len(output_html)):
                    expect = test_case['expected'][i][0]
                    print(output_html[i][0])
                    print(expect)
                    self.assertEqual(output_html[i][0], expect, msg=f'result is: {output_html[i][0]}, expected is: {expect}')

    def test_math_recognizer_html(self):
        for test_case in TEST_CASES_HTML:
            raw_html_path = base_dir.joinpath(test_case['input'][0])
            print('raw_html_path::::::::', raw_html_path)
            base_url = test_case['base_url']
            raw_html = raw_html_path.read_text()
            parts = self.math_recognizer.recognize(base_url, [(raw_html, raw_html)], raw_html)
            # print(parts)
            # 将parts列表中第一个元素拼接保存到文件，带随机数
            # import random
            # with open('parts'+str(random.randint(1, 100))+".html", 'w') as f:
            #     for part in parts:
            #         f.write(str(part[0]))
            parts = [part[0] for part in parts if CCTag.CC_MATH_INTERLINE in part[0]]
            print(len(parts))
            expect_text = base_dir.joinpath(test_case['expected']).read_text().strip()
            expect_formulas = [formula for formula in expect_text.split('\n') if formula]
            self.assertEqual(len(parts), len(expect_formulas))
            # answers = []
            for expect, part in zip(expect_formulas, parts):
                a_tree = html_to_element(part)
                a_result = a_tree.xpath(f'.//{CCTag.CC_MATH_INTERLINE}')[0]
                answer = a_result.text.replace('\n', '').strip()
                # print('part::::::::', part)
                print('expect::::::::', expect)
                print('answer::::::::', answer)
                # answers.append(answer)
                self.assertEqual(expect, answer)
            # self.write_to_html(answers, test_case['input'][0])

    def write_to_html(self, answers, file_name):
        file_name = file_name.split('.')[0]
        with open(base_dir.joinpath(f'{file_name}_1.html'), 'w', encoding='utf-8') as file:
            for formula in answers:
                file.write(formula)
                file.write('\n')

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
        with self.assertRaises(HtmlMathRecognizerExp) as exc_info:
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
                tag_math_type_list = self.ccmath.get_equation_type(test_case['input'])
                print('input::::::::', test_case['input'])
                if tag_math_type_list:
                    for i in range(len(tag_math_type_list)):
                        expect0 = test_case['expected'][i][0]
                        expect1 = test_case['expected'][i][1]
                        self.assertEqual(tag_math_type_list[i][0], expect0, msg=f'result is: {tag_math_type_list[i][0]}, expected is: {expect0}')
                        self.assertEqual(tag_math_type_list[i][1], expect1, msg=f'result is: {tag_math_type_list[i][1]}, expected is: {expect1}')

    def test_get_math_render(self):
        for test_case in TEST_GET_MATH_RENDER:
            raw_html_path = base_dir.joinpath(test_case['input'][0])
            raw_html = raw_html_path.read_text()
            output_render = self.ccmath.get_math_render(raw_html)
            self.assertEqual(output_render, test_case['expected'])

    def test_wrap_math(self):
        for test_case in TEST_WRAP_MATH:
            with self.subTest(input=test_case['input']):
                output_math = self.ccmath.wrap_math(test_case['input'], test_case['display'])
                self.assertEqual(output_math, test_case['expected'])

    def test_wrap_math_md(self):
        for test_case in TEST_WRAP_MATH_MD:
            with self.subTest(input=test_case['input']):
                output_math = self.ccmath.wrap_math_md(test_case['input'])
                self.assertEqual(output_math, test_case['expected'])


if __name__ == '__main__':
    r = TestMathRecognizer()
    r.setUp()
    r.test_math_recognizer()
    r.test_math_recognizer_html()
    # r.test_math_recognizer()
    # r.test_to_content_list_node()
    # html = r'<p class="lt-math-15120">\[\begin{array} {ll} {5 \cdot 3 = 15} &amp;{-5(3) = -15} \\ {5(-3) = -15} &amp;{(-5)(-3) = 15} \end{array}\]</p>'
    # tree = html_to_element(html)
    # print(tree.text)

    # raw_html_path = base_dir.joinpath('assets/ccmath/mathjax-mml-chtml.html')
    # raw_html = raw_html_path.read_text()
    # from llm_web_kit.libs.html_utils import build_html_tree
    # tree = build_html_tree(raw_html)
    # for node in tree.iter():
    #     print(node.tag)

    # c = TestCCMATH()
    # c.setUp()
    # c.test_get_equation_type()
    # c.test_wrap_math()
    # c.test_wrap_math_md()
