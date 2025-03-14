import unittest
from pathlib import Path

from llm_web_kit.extractor.html.recognizer.cc_math.common import MathType
from llm_web_kit.extractor.html.recognizer.cc_math.render.katex import \
    KaTeXRender
from llm_web_kit.extractor.html.recognizer.cc_math.render.mathjax import \
    MathJaxRender
from llm_web_kit.extractor.html.recognizer.recognizer import CCTag
from llm_web_kit.libs.html_utils import element_to_html, html_to_element

TEST_GET_MATH_RENDER = [
    {
        'input': [
            'assets/ccmath/stackexchange_1_span-math-container_latex_mathjax.html'
        ],
        'base_url': 'https://worldbuilding.stackexchange.com/questions/162264/is-there-a-safe-but-weird-distance-from-black-hole-merger',
        'expected': 'mathjax',
        'is_customized_options': False
    },
    {
        'input': [
            'assets/ccmath/libretexts_1_p_latex_mathjax.html',
        ],
        'base_url': 'https://math.libretexts.org/Under_Construction/Purgatory/Remixer_University/Username%3A_pseeburger/MTH_098_Elementary_Algebra/1%3A_Foundations/1.5%3A_Multiply_and_Divide_Integers',
        'expected': 'mathjax',
        'is_customized_options': False
    },
    {
        'input': [
            'assets/ccmath/math_katex_latex_2.html',
        ],
        'base_url': 'https://www.intmath.com/cg5/katex-mathjax-comparison.php',
        'expected': 'katex',
        'is_customized_options': False
    },
    {
        'input': [
            'assets/ccmath/math_physicsforums.html',
        ],
        'base_url': 'https://www.physicsforums.com/threads/probability-theoretic-inequality.246150/',
        'expected': 'mathjax',
        'is_customized_options': True
    },
    {
        'input': [
            'assets/ccmath/wikipedia_1_math_annotation.html',
        ],
        'base_url': 'https://en.m.wikipedia.org/wiki/Variance',
        'expected': None,
        'is_customized_options': False
    }
]
base_dir = Path(__file__).parent


class TestMathRender(unittest.TestCase):
    """测试数学公式渲染器的各种情况."""

    def setUp(self):
        """设置测试环境."""
        self.mathjax_render = MathJaxRender()
        self.katex_render = KaTeXRender()

    def test_empty_text(self):
        """测试空文本的情况."""
        # 创建一个简单的HTML元素
        parent = html_to_element('<div></div>')

        # 测试空文本
        result = self.mathjax_render._replace_math(parent, '', '$', '$', False)
        self.assertEqual(result, '')

        # 测试None
        result = self.mathjax_render._replace_math(parent, None, '$', '$', False)
        self.assertEqual(result, None)
        self.assertEqual(element_to_html(parent), '<div></div>')

    def test_no_match(self):
        """测试没有匹配的情况."""
        # 创建一个简单的HTML元素
        parent = html_to_element('<div>This is a text without any math formula.</div>')

        # 测试没有匹配的文本
        result = self.mathjax_render._replace_math(parent, parent.text, '$', '$', False)
        self.assertEqual(result, parent.text)
        self.assertEqual(element_to_html(parent), '<div>This is a text without any math formula.</div>')

        # 测试只有一个分隔符的情况
        parent.text = 'This is a text with only one $ delimiter.'
        result = self.mathjax_render._replace_math(parent, parent.text, '$', '$', False)
        self.assertEqual(result, parent.text)
        self.assertEqual(element_to_html(parent), '<div>This is a text with only one $ delimiter.</div>')

    def test_single_inline_formula(self):
        """测试单个行内公式的情况."""
        # 创建一个简单的HTML元素
        parent = html_to_element('<div>This is an inline formula: $a^2 + b^2 = c^2$ in text.</div>')

        # 测试单个行内公式
        self.mathjax_render._replace_math(parent, parent.text, '$', '$', False)

        # 验证结果
        print('single_inline_formula:', element_to_html(parent))
        self.assertEqual(element_to_html(parent), '<div>This is an inline formula: <ccmath-inline type="latex" by="mathjax" html="$a^2 + b^2 = c^2$">a^2 + b^2 = c^2</ccmath-inline> in text.</div>')
        self.assertEqual(parent.text, 'This is an inline formula: ')
        self.assertEqual(len(parent), 1)
        self.assertEqual(parent[0].tag, CCTag.CC_MATH_INLINE)
        self.assertEqual(parent[0].text, 'a^2 + b^2 = c^2')
        self.assertEqual(parent[0].tail, ' in text.')
        self.assertEqual(parent[0].get('type'), MathType.LATEX)
        self.assertEqual(parent[0].get('by'), 'mathjax')
        self.assertEqual(parent[0].get('html'), '$a^2 + b^2 = c^2$')

    def test_single_display_formula(self):
        """测试单个行间公式的情况."""
        # 创建一个简单的HTML元素
        parent = html_to_element('<div>This is a display formula: $$a^2 + b^2 = c^2$$ in text.</div>')

        # 测试单个行间公式
        self.mathjax_render._replace_math(parent, parent.text, '$$', '$$', True)

        # 验证结果
        self.assertEqual(element_to_html(parent), '<div>This is a display formula: <ccmath-interline type="latex" by="mathjax" html="$$a^2 + b^2 = c^2$$">a^2 + b^2 = c^2</ccmath-interline> in text.</div>')
        self.assertEqual(parent.text, 'This is a display formula: ')
        self.assertEqual(len(parent), 1)
        self.assertEqual(parent[0].tag, CCTag.CC_MATH_INTERLINE)
        self.assertEqual(parent[0].text, 'a^2 + b^2 = c^2')
        self.assertEqual(parent[0].tail, ' in text.')
        self.assertEqual(parent[0].get('type'), MathType.LATEX)
        self.assertEqual(parent[0].get('by'), 'mathjax')
        self.assertEqual(parent[0].get('html'), '$$a^2 + b^2 = c^2$$')

    def test_multiple_formulas(self):
        """测试多个公式的情况."""
        # 创建一个简单的HTML元素
        parent = html_to_element('<div>Formula 1: $a^2$ and formula 2: $b^2$ and formula 3: $c^2$.</div>')

        # 测试多个公式
        self.mathjax_render._replace_math(parent, parent.text, '$', '$', False)

        # 验证结果
        print('multiple_formulas:', element_to_html(parent))
        self.assertEqual(element_to_html(parent), '<div>Formula 1: <ccmath-inline type="latex" by="mathjax" html="$a^2$">a^2</ccmath-inline> and formula 2: <ccmath-inline type="latex" by="mathjax" html="$b^2$">b^2</ccmath-inline> and formula 3: <ccmath-inline type="latex" by="mathjax" html="$c^2$">c^2</ccmath-inline>.</div>')
        self.assertEqual(parent.text, 'Formula 1: ')
        self.assertEqual(len(parent), 3)

        # 检查第一个公式
        self.assertEqual(parent[0].tag, CCTag.CC_MATH_INLINE)
        self.assertEqual(parent[0].text, 'a^2')
        self.assertEqual(parent[0].tail, ' and formula 2: ')

        # 检查第二个公式
        self.assertEqual(parent[1].tag, CCTag.CC_MATH_INLINE)
        self.assertEqual(parent[1].text, 'b^2')
        self.assertEqual(parent[1].tail, ' and formula 3: ')

        # 检查第三个公式
        self.assertEqual(parent[2].tag, CCTag.CC_MATH_INLINE)
        self.assertEqual(parent[2].text, 'c^2')
        self.assertEqual(parent[2].tail, '.')

    def test_formula_at_beginning(self):
        """测试公式在文本开头的情况."""
        # 创建一个简单的HTML元素
        parent = html_to_element('<div>$a^2 + b^2 = c^2$ is the Pythagorean theorem.</div>')

        # 测试公式在开头
        self.mathjax_render._replace_math(parent, parent.text, '$', '$', False)

        # 验证结果
        self.assertEqual(element_to_html(parent), '<div><ccmath-inline type="latex" by="mathjax" html="$a^2 + b^2 = c^2$">a^2 + b^2 = c^2</ccmath-inline> is the Pythagorean theorem.</div>')
        self.assertEqual(parent.text, '')
        self.assertEqual(len(parent), 1)
        self.assertEqual(parent[0].tag, CCTag.CC_MATH_INLINE)
        self.assertEqual(parent[0].text, 'a^2 + b^2 = c^2')
        self.assertEqual(parent[0].tail, ' is the Pythagorean theorem.')

    def test_formula_at_end(self):
        """测试公式在文本末尾的情况."""
        # 创建一个简单的HTML元素
        parent = html_to_element('<div>The Pythagorean theorem is $a^2 + b^2 = c^2$</div>')

        # 测试公式在末尾
        self.mathjax_render._replace_math(parent, parent.text, '$', '$', False)

        # 验证结果
        self.assertEqual(element_to_html(parent), '<div>The Pythagorean theorem is <ccmath-inline type="latex" by="mathjax" html="$a^2 + b^2 = c^2$">a^2 + b^2 = c^2</ccmath-inline></div>')
        self.assertEqual(parent.text, 'The Pythagorean theorem is ')
        self.assertEqual(len(parent), 1)
        self.assertEqual(parent[0].tag, CCTag.CC_MATH_INLINE)
        self.assertEqual(parent[0].text, 'a^2 + b^2 = c^2')
        self.assertEqual(parent[0].tail, '')

    def test_only_formula(self):
        """测试只有公式的情况."""
        # 创建一个简单的HTML元素
        parent = html_to_element('<div>$a^2 + b^2 = c^2$</div>')

        # 测试只有公式
        self.mathjax_render._replace_math(parent, parent.text, '$', '$', False)

        # 验证结果
        self.assertEqual(element_to_html(parent), '<div><ccmath-inline type="latex" by="mathjax" html="$a^2 + b^2 = c^2$">a^2 + b^2 = c^2</ccmath-inline></div>')
        self.assertEqual(parent.text, '')
        self.assertEqual(len(parent), 1)
        self.assertEqual(parent[0].tag, CCTag.CC_MATH_INLINE)
        self.assertEqual(parent[0].text, 'a^2 + b^2 = c^2')
        self.assertEqual(parent[0].tail, '')

    def test_tail_text(self):
        """测试处理tail文本的情况."""
        # 创建一个带有子元素的HTML元素
        parent = html_to_element('<div><span>This is a span</span></div>')
        child = parent[0]

        # 设置child.tail包含数学公式
        child.tail = 'This is a tail text with formula: $a^2 + b^2 = c^2$ end.'

        # 使用_replace_math方法处理tail文本中的公式
        self.mathjax_render._replace_math(parent, child.tail, '$', '$', False, child)

        # 验证结果
        self.assertEqual(child.tail, 'This is a tail text with formula: ')
        self.assertEqual(len(parent), 2)
        self.assertEqual(parent[1].tag, CCTag.CC_MATH_INLINE)
        self.assertEqual(parent[1].text, 'a^2 + b^2 = c^2')
        self.assertEqual(parent[1].tail, ' end.')
        self.assertEqual(element_to_html(parent), '<div><span>This is a span</span>This is a tail text with formula: <ccmath-inline type="latex" by="mathjax" html="$a^2 + b^2 = c^2$">a^2 + b^2 = c^2</ccmath-inline> end.</div>')

    def test_multiple_formulas_in_tail(self):
        """测试tail文本中有多个公式的情况."""
        # 创建一个带有子元素的HTML元素
        parent = html_to_element('<div><span>This is a span</span></div>')
        child = parent[0]

        # 设置child.tail包含多个数学公式
        child.tail = 'Formula 1: $a^2$ and formula 2: $b^2$ and formula 3: $c^2$.'

        # 使用_replace_math方法处理tail文本中的公式
        self.mathjax_render._replace_math(parent, child.tail, '$', '$', False, child)

        # 验证结果
        self.assertEqual(child.tail, 'Formula 1: ')
        self.assertEqual(len(parent), 4)  # 原始span + 3个公式节点

        # 检查第一个公式
        self.assertEqual(parent[1].tag, CCTag.CC_MATH_INLINE)
        self.assertEqual(parent[1].text, 'a^2')
        self.assertEqual(parent[1].tail, ' and formula 2: ')

        # 检查第二个公式
        self.assertEqual(parent[2].tag, CCTag.CC_MATH_INLINE)
        self.assertEqual(parent[2].text, 'b^2')
        self.assertEqual(parent[2].tail, ' and formula 3: ')

        # 检查第三个公式
        self.assertEqual(parent[3].tag, CCTag.CC_MATH_INLINE)
        self.assertEqual(parent[3].text, 'c^2')
        self.assertEqual(parent[3].tail, '.')

        # 检查完整HTML
        expected_html = '<div><span>This is a span</span>Formula 1: <ccmath-inline type="latex" by="mathjax" html="$a^2$">a^2</ccmath-inline> and formula 2: <ccmath-inline type="latex" by="mathjax" html="$b^2$">b^2</ccmath-inline> and formula 3: <ccmath-inline type="latex" by="mathjax" html="$c^2$">c^2</ccmath-inline>.</div>'
        self.assertEqual(element_to_html(parent), expected_html)

    def test_different_delimiters(self):
        """测试不同的分隔符."""
        # 创建一个简单的HTML元素
        parent = html_to_element('<div>Inline: \\(a^2 + b^2 = c^2\\) and display: \\[a^2 + b^2 = c^2\\]</div>')

        # 处理行内公式
        self.mathjax_render._replace_math(parent, parent.text, '\\(', '\\)', False)

        # 验证结果
        self.assertEqual(parent.text, 'Inline: ')
        self.assertEqual(len(parent), 1)
        self.assertEqual(parent[0].tag, CCTag.CC_MATH_INLINE)
        self.assertEqual(parent[0].text, 'a^2 + b^2 = c^2')
        self.assertEqual(parent[0].tail, ' and display: \\[a^2 + b^2 = c^2\\]')

        # 检查中间HTML
        mid_html = '<div>Inline: <ccmath-inline type="latex" by="mathjax" html="\\(a^2 + b^2 = c^2\\)">a^2 + b^2 = c^2</ccmath-inline> and display: \\[a^2 + b^2 = c^2\\]</div>'
        self.assertEqual(element_to_html(parent), mid_html)

        # 处理行间公式
        self.mathjax_render._replace_math(parent, parent[0].tail, '\\[', '\\]', True, parent[0])

        # 验证结果
        self.assertEqual(parent[0].tail, ' and display: ')
        self.assertEqual(len(parent), 2)
        self.assertEqual(parent[1].tag, CCTag.CC_MATH_INTERLINE)
        self.assertEqual(parent[1].text, 'a^2 + b^2 = c^2')
        self.assertEqual(parent[1].tail, '')

        # 检查最终HTML
        final_html = '<div>Inline: <ccmath-inline type="latex" by="mathjax" html="\\(a^2 + b^2 = c^2\\)">a^2 + b^2 = c^2</ccmath-inline> and display: <ccmath-interline type="latex" by="mathjax" html="\\[a^2 + b^2 = c^2\\]">a^2 + b^2 = c^2</ccmath-interline></div>'
        self.assertEqual(element_to_html(parent), final_html)

    def test_tex_itex_delimiters(self):
        """测试[tex]和[itex]分隔符."""
        # 创建一个简单的HTML元素
        parent = html_to_element('<div>Display: [tex]a^2 + b^2 = c^2[/tex] and inline: [itex]a^2 + b^2 = c^2[/itex]</div>')

        # 测试[tex]分隔符
        self.mathjax_render._replace_math(parent, parent.text, '[tex]', '[/tex]', True)

        # 验证结果
        self.assertEqual(parent.text, 'Display: ')
        self.assertEqual(len(parent), 1)
        self.assertEqual(parent[0].tag, CCTag.CC_MATH_INTERLINE)
        self.assertEqual(parent[0].text, 'a^2 + b^2 = c^2')
        self.assertEqual(parent[0].tail, ' and inline: [itex]a^2 + b^2 = c^2[/itex]')

        # 检查中间HTML
        mid_html = '<div>Display: <ccmath-interline type="latex" by="mathjax" html="[tex]a^2 + b^2 = c^2[/tex]">a^2 + b^2 = c^2</ccmath-interline> and inline: [itex]a^2 + b^2 = c^2[/itex]</div>'
        self.assertEqual(element_to_html(parent), mid_html)

        # 处理行内公式
        self.mathjax_render._replace_math(parent, parent[0].tail, '[itex]', '[/itex]', False, parent[0])

        # 验证结果
        self.assertEqual(parent[0].tail, ' and inline: ')
        self.assertEqual(len(parent), 2)
        self.assertEqual(parent[1].tag, CCTag.CC_MATH_INLINE)
        self.assertEqual(parent[1].text, 'a^2 + b^2 = c^2')
        self.assertEqual(parent[1].tail, '')

        # 检查最终HTML
        final_html = '<div>Display: <ccmath-interline type="latex" by="mathjax" html="[tex]a^2 + b^2 = c^2[/tex]">a^2 + b^2 = c^2</ccmath-interline> and inline: <ccmath-inline type="latex" by="mathjax" html="[itex]a^2 + b^2 = c^2[/itex]">a^2 + b^2 = c^2</ccmath-inline></div>'
        self.assertEqual(element_to_html(parent), final_html)

    def test_katex_render(self):
        """测试KaTeX渲染器."""
        # 创建一个简单的HTML元素
        parent = html_to_element('<div>This is a KaTeX formula: $a^2 + b^2 = c^2$ in text.</div>')

        # 测试KaTeX渲染器
        self.katex_render._replace_math(parent, parent.text, '$', '$', False)

        # 验证结果
        self.assertEqual(parent.text, 'This is a KaTeX formula: ')
        self.assertEqual(len(parent), 1)
        self.assertEqual(parent[0].tag, CCTag.CC_MATH_INLINE)
        self.assertEqual(parent[0].text, 'a^2 + b^2 = c^2')
        self.assertEqual(parent[0].tail, ' in text.')
        self.assertEqual(parent[0].get('type'), MathType.LATEX)
        self.assertEqual(parent[0].get('by'), 'katex')
        self.assertEqual(parent[0].get('html'), '$a^2 + b^2 = c^2$')

        # 检查HTML
        expected_html = '<div>This is a KaTeX formula: <ccmath-inline type="latex" by="katex" html="$a^2 + b^2 = c^2$">a^2 + b^2 = c^2</ccmath-inline> in text.</div>'
        self.assertEqual(element_to_html(parent), expected_html)

    def test_empty_formula(self):
        """测试空公式的情况."""
        # 创建一个简单的HTML元素
        parent = html_to_element('<div>This is an empty formula: $$ in text.</div>')

        # 测试空公式
        self.mathjax_render._replace_math(parent, parent.text, '$', '$', False)

        # 验证结果 - 应该保持原文本不变
        self.assertEqual(parent.text, 'This is an empty formula: ')
        self.assertEqual(len(parent), 0)

        # 检查HTML - 应该保持原HTML不变
        expected_html = '<div>This is an empty formula: </div>'
        self.assertEqual(element_to_html(parent), expected_html)

    def test_nested_elements(self):
        """测试嵌套元素的情况."""
        # 创建一个嵌套的HTML元素
        parent = html_to_element('<div><p>Paragraph <span>Span</span> text</p></div>')
        p_elem = parent[0]
        span_elem = p_elem[0]

        # 设置文本和tail
        p_elem.text = 'Paragraph with formula: $a^2$ '
        span_elem.tail = ' text with formula: $b^2$ end.'

        # 处理p.text
        self.mathjax_render._replace_math(p_elem, p_elem.text, '$', '$', False)

        # 验证p.text的处理结果
        self.assertEqual(p_elem.text, 'Paragraph with formula: ')
        self.assertEqual(p_elem[0].tag, CCTag.CC_MATH_INLINE)
        self.assertEqual(p_elem[0].text, 'a^2')
        self.assertEqual(p_elem[0].tail, ' ')

        # 检查中间HTML
        mid_html = '<div><p>Paragraph with formula: <ccmath-inline type="latex" by="mathjax" html="$a^2$">a^2</ccmath-inline> <span>Span</span> text with formula: $b^2$ end.</p></div>'
        self.assertEqual(element_to_html(parent), mid_html)

        # span现在是p的第二个子元素
        span_elem = p_elem[1]

        # 处理span.tail
        self.mathjax_render._replace_math(p_elem, span_elem.tail, '$', '$', False, span_elem)

        # 验证span.tail的处理结果
        self.assertEqual(span_elem.tail, ' text with formula: ')
        self.assertEqual(p_elem[2].tag, CCTag.CC_MATH_INLINE)
        self.assertEqual(p_elem[2].text, 'b^2')
        self.assertEqual(p_elem[2].tail, ' end.')

        # 检查最终HTML
        final_html = '<div><p>Paragraph with formula: <ccmath-inline type="latex" by="mathjax" html="$a^2$">a^2</ccmath-inline> <span>Span</span> text with formula: <ccmath-inline type="latex" by="mathjax" html="$b^2$">b^2</ccmath-inline> end.</p></div>'
        self.assertEqual(element_to_html(parent), final_html)

    # def test_find_math_method(self):
    #     """测试find_math方法."""
    #     # 创建一个HTML树
    #     html = """
    #     <div>
    #         <p>Paragraph with inline formula: $a^2 + b^2 = c^2$ and display formula: $$E = mc^2$$</p>
    #         <p>Another paragraph with [tex]\\frac{1}{2}[/tex] formula.</p>
    #     </div>
    #     """
    #     root = html_to_element(html)

    #     # 使用find_math方法处理
    #     self.mathjax_render.find_math(root)

    #     # 验证结果
    #     p1 = root[0]
    #     p2 = root[1]

    #     # 检查第一个段落
    #     self.assertEqual(p1.text, 'Paragraph with inline formula: ')
    #     self.assertEqual(len(p1), 2)
    #     self.assertEqual(p1[0].tag, CCTag.CC_MATH_INLINE)
    #     self.assertEqual(p1[0].text, 'a^2 + b^2 = c^2')
    #     self.assertEqual(p1[0].tail, ' and display formula: ')
    #     self.assertEqual(p1[1].tag, CCTag.CC_MATH_INTERLINE)
    #     self.assertEqual(p1[1].text, 'E = mc^2')
    #     self.assertEqual(p1[1].tail, '')

    #     # 检查第二个段落
    #     self.assertEqual(p2.text, 'Another paragraph with ')
    #     self.assertEqual(len(p2), 1)
    #     self.assertEqual(p2[0].tag, CCTag.CC_MATH_INTERLINE)
    #     self.assertEqual(p2[0].text, '\\frac{1}{2}')
    #     self.assertEqual(p2[0].tail, ' formula.')

    #     # 检查完整HTML
    #     print('test_find_math_method expected_html:', element_to_html(root))
    #     expected_html = """<div>
    #         <p>Paragraph with inline formula: <ccmath-inline type="latex" by="mathjax" html="$a^2 + b^2 = c^2$">a^2 + b^2 = c^2</ccmath-inline> and display formula: <ccmath-interline type="latex" by="mathjax" html="$$E = mc^2$$">E = mc^2</ccmath-interline></p>
    #         <p>Another paragraph with <ccmath-interline type="latex" by="mathjax" html="[tex]\\frac{1}{2}[/tex]">\\frac{1}{2}</ccmath-interline> formula.</p>
    #     </div>"""
    #     self.assertEqual(element_to_html(root), expected_html)

    def test_br_tags(self):
        """测试<br>标签的处理."""
        # 测试带有<br />标签的文本
        html = '<div>Line 1<br>$a^2 + b^2 = c^2$<br>Line 3</div>'

        # 将文本设置为parent的HTML内容
        parent_with_br = html_to_element(html)

        # 使用find_math方法处理
        self.mathjax_render.find_math(parent_with_br)

        # 验证结果 - <br />标签应该被保留
        self.assertEqual(parent_with_br.text, 'Line 1')
        self.assertEqual(len(parent_with_br), 3)
        self.assertEqual(parent_with_br[0].tag, 'br')
        self.assertEqual(parent_with_br[0].tail, '')
        self.assertEqual(parent_with_br[1].tag, CCTag.CC_MATH_INLINE)
        self.assertEqual(parent_with_br[1].text, 'a^2 + b^2 = c^2')
        self.assertEqual(parent_with_br[1].tail, '')
        self.assertEqual(parent_with_br[2].tag, 'br')
        self.assertEqual(parent_with_br[2].tail, 'Line 3')

        # 检查HTML
        expected_html = '<div>Line 1<br><ccmath-inline type="latex" by="mathjax" html="$a^2 + b^2 = c^2$">a^2 + b^2 = c^2</ccmath-inline><br>Line 3</div>'
        self.assertEqual(element_to_html(parent_with_br), expected_html)

    def test_text_preservation(self):
        """测试文本保留问题."""
        # 创建一个简单的HTML元素
        parent = html_to_element('<div>Prefix text $formula$ suffix text.</div>')

        # 测试前缀文本保留
        result = self.mathjax_render._replace_math(parent, parent.text, '$', '$', False)

        # 打印调试信息
        print('text_preservation result:', result)
        print('text_preservation parent.text:', parent.text)
        print('text_preservation HTML:', element_to_html(parent))

        # 验证结果
        self.assertEqual(result, '')
        self.assertEqual(parent.text, 'Prefix text ')
        self.assertEqual(len(parent), 1)
        self.assertEqual(parent[0].tag, CCTag.CC_MATH_INLINE)
        self.assertEqual(parent[0].text, 'formula')
        self.assertEqual(parent[0].tail, ' suffix text.')

        # 检查HTML - 确保前缀和后缀文本都被保留
        expected_html = '<div>Prefix text <ccmath-inline type="latex" by="mathjax" html="$formula$">formula</ccmath-inline> suffix text.</div>'
        self.assertEqual(element_to_html(parent), expected_html)

        # 重置测试环境
        parent = html_to_element('<div>Text1 $formula1$ middle text $formula2$ text3.</div>')

        # 测试多个公式之间的文本保留
        result = self.mathjax_render._replace_math(parent, parent.text, '$', '$', False)

        # 打印调试信息
        print('multiple_formulas_text_preservation result:', result)
        print('multiple_formulas_text_preservation parent.text:', parent.text)
        print('multiple_formulas_text_preservation HTML:', element_to_html(parent))

        # 验证结果
        self.assertEqual(result, '')
        self.assertEqual(parent.text, 'Text1 ')
        self.assertEqual(len(parent), 2)
        self.assertEqual(parent[0].tag, CCTag.CC_MATH_INLINE)
        self.assertEqual(parent[0].text, 'formula1')
        self.assertEqual(parent[0].tail, ' middle text ')
        self.assertEqual(parent[1].tag, CCTag.CC_MATH_INLINE)
        self.assertEqual(parent[1].text, 'formula2')
        self.assertEqual(parent[1].tail, ' text3.')

        # 检查HTML - 确保所有文本段都被保留
        expected_html = '<div>Text1 <ccmath-inline type="latex" by="mathjax" html="$formula1$">formula1</ccmath-inline> middle text <ccmath-inline type="latex" by="mathjax" html="$formula2$">formula2</ccmath-inline> text3.</div>'
        self.assertEqual(element_to_html(parent), expected_html)


if __name__ == '__main__':
    r = TestMathRender()
    r.setUp()
    r.test_multiple_formulas()
