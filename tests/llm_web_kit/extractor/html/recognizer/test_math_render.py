import re
import unittest
import warnings
from pathlib import Path

from llm_web_kit.extractor.html.recognizer.cc_math.common import MathType
from llm_web_kit.extractor.html.recognizer.cc_math.render.katex import \
    KaTeXRender
from llm_web_kit.extractor.html.recognizer.cc_math.render.mathjax import \
    MathJaxRender
from llm_web_kit.extractor.html.recognizer.cc_math.render.render import (
    BaseMathRender, MathRenderType)
from llm_web_kit.extractor.html.recognizer.recognizer import CCTag
from llm_web_kit.libs.html_utils import element_to_html, html_to_element

# 忽略来自 lark 库的废弃警告
warnings.filterwarnings('ignore', category=DeprecationWarning, module='lark.utils')

display_pattern = re.compile('\\$\\$(.*?)\\$\\$|\\\\\\[(.*?)\\\\\\]|\\\\\\\\\\[(.*?)\\\\\\\\\\]', re.DOTALL)
inline_pattern = re.compile('\\$(.*?)\\$|\\\\\\((.*?)\\\\\\)|\\\\\\\\\\((.*?)\\\\\\\\\\)', re.DOTALL)
base_dir = Path(__file__).parent

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
        result = self.mathjax_render._process_math_in_text(parent, parent.text, re.compile('\\$(.*?)\\$', re.DOTALL), False, False)
        self.assertEqual(result, None)

        # 测试None
        result = self.mathjax_render._process_math_in_text(parent, None, re.compile('\\$(.*?)\\$', re.DOTALL), False, False)
        self.assertEqual(result, None)
        self.assertEqual(element_to_html(parent), '<div></div>')

    def test_no_match(self):
        """测试没有匹配的情况."""
        # 创建一个简单的HTML元素
        parent = html_to_element('<div>This is a text without any math formula.</div>')

        # 测试没有匹配的文本
        result = self.mathjax_render._process_math_in_text(parent, parent.text, re.compile('\\$(.*?)\\$', re.DOTALL), False, False)
        self.assertEqual(result, parent.text)
        self.assertEqual(element_to_html(parent), '<div>This is a text without any math formula.</div>')

        # 测试只有一个分隔符的情况
        parent.text = 'This is a text with only one $ delimiter.'
        result = self.mathjax_render._process_math_in_text(parent, parent.text, re.compile('\\$(.*?)\\$', re.DOTALL), False, False)
        self.assertEqual(result, parent.text)
        self.assertEqual(element_to_html(parent), '<div>This is a text with only one $ delimiter.</div>')

    def test_single_inline_formula(self):
        """测试单个行内公式的情况."""
        # 创建一个简单的HTML元素
        parent = html_to_element('<div>This is an inline formula: $a^2 + b^2 = c^2$ in text.</div>')

        # 测试单个行内公式
        self.mathjax_render._process_math_in_text(parent, parent.text, re.compile('\\$(.*?)\\$', re.DOTALL), False, False)

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
        self.mathjax_render._process_math_in_text(parent, parent.text, re.compile('\\$\\$(.*?)\\$\\$', re.DOTALL), True, False)

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
        self.mathjax_render._process_math_in_text(parent, parent.text, re.compile('\\$(.*?)\\$', re.DOTALL), False, False)

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
        self.mathjax_render._process_math_in_text(parent, parent.text, re.compile('\\$(.*?)\\$', re.DOTALL), False, False)

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
        self.mathjax_render._process_math_in_text(parent, parent.text, re.compile('\\$(.*?)\\$', re.DOTALL), False, False)

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
        self.mathjax_render._process_math_in_text(parent, parent.text, re.compile('\\$(.*?)\\$', re.DOTALL), False, False)

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

        # 使用_process_math_in_text方法处理tail文本中的公式
        self.mathjax_render._process_math_in_text(child, child.tail, inline_pattern, False, True)

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

        # 使用_find_math_in_element方法处理tail文本中的公式
        self.mathjax_render._find_math_in_element(child, inline_pattern, display_pattern)

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
        self.mathjax_render._process_math_in_text(parent, parent.text, inline_pattern, False, False)

        # 验证结果
        self.assertEqual(parent.text, 'Inline: ')
        self.assertEqual(len(parent), 1)
        self.assertEqual(parent[0].tag, CCTag.CC_MATH_INLINE)
        self.assertEqual(parent[0].text, 'a^2 + b^2 = c^2')
        self.assertEqual(parent[0].tail, ' and display: \\[a^2 + b^2 = c^2\\]')

        # 检查中间HTML
        mid_html = '<div>Inline: <ccmath-inline type="latex" by="mathjax" html="\\(a^2 + b^2 = c^2\\)">a^2 + b^2 = c^2</ccmath-inline> and display: \\[a^2 + b^2 = c^2\\]</div>'
        self.assertEqual(element_to_html(parent), mid_html)

        # 处理tail的行间公式
        self.mathjax_render._process_math_in_text(parent[0], parent[0].tail, display_pattern, True, True)

        # 验证结果
        self.assertEqual(parent[0].tail, ' and display: ')
        self.assertEqual(len(parent), 2)
        self.assertEqual(parent[1].tag, CCTag.CC_MATH_INTERLINE)
        self.assertEqual(parent[1].text, 'a^2 + b^2 = c^2')
        self.assertEqual(parent[1].tail, '')

        # 检查最终HTML
        final_html = '<div>Inline: <ccmath-inline type="latex" by="mathjax" html="\\(a^2 + b^2 = c^2\\)">a^2 + b^2 = c^2</ccmath-inline> and display: <ccmath-interline type="latex" by="mathjax" html="\\[a^2 + b^2 = c^2\\]">a^2 + b^2 = c^2</ccmath-interline></div>'
        self.assertEqual(element_to_html(parent), final_html)

    def test_different_delimiters_element(self):
        parent = html_to_element('<div>Inline: \\(a^2 + b^2 = c^2\\) and display: \\[a^2 + b^2 = c^2\\]</div>')
        self.mathjax_render._find_math_in_element(parent, inline_pattern, display_pattern)

        # 检查最终HTML
        final_html = '<div>Inline: <ccmath-inline type="latex" by="mathjax" html="\\(a^2 + b^2 = c^2\\)">a^2 + b^2 = c^2</ccmath-inline> and display: <ccmath-interline type="latex" by="mathjax" html="\\[a^2 + b^2 = c^2\\]">a^2 + b^2 = c^2</ccmath-interline></div>'
        self.assertEqual(element_to_html(parent), final_html)

    def test_tex_itex_delimiters(self):
        """测试[tex]和[itex]分隔符."""
        # 创建一个简单的HTML元素
        parent = html_to_element('<div>Display: [tex]a^2 + b^2 = c^2[/tex] and inline: [itex]a^2 + b^2 = c^2[/itex]</div>')

        # 测试[tex]分隔符
        inline_pattern = re.compile('\\[itex\\](.*?)\\[\\/itex\\]', re.DOTALL)
        display_pattern = re.compile('\\[tex\\](.*?)\\[\\/tex\\]', re.DOTALL)

        self.mathjax_render._find_math_in_element(parent, inline_pattern, display_pattern)

        # 检查最终HTML
        final_html = '<div>Display: <ccmath-interline type="latex" by="mathjax" html="[tex]a^2 + b^2 = c^2[/tex]">a^2 + b^2 = c^2</ccmath-interline> and inline: <ccmath-inline type="latex" by="mathjax" html="[itex]a^2 + b^2 = c^2[/itex]">a^2 + b^2 = c^2</ccmath-inline></div>'
        self.assertEqual(element_to_html(parent), final_html)

    # def test_katex_render(self):
    #     """测试KaTeX渲染器."""
    #     # 创建一个简单的HTML元素
    #     parent = html_to_element('<div>This is a KaTeX formula: $a^2 + b^2 = c^2$ in text.</div>')

    #     # 测试KaTeX渲染器
    #     self.katex_render._process_math_in_text(parent, parent.text, inline_pattern, False, False)

    #     # 验证结果
    #     self.assertEqual(parent.text, 'This is a KaTeX formula: ')
    #     self.assertEqual(len(parent), 1)
    #     self.assertEqual(parent[0].tag, CCTag.CC_MATH_INLINE)
    #     self.assertEqual(parent[0].text, 'a^2 + b^2 = c^2')
    #     self.assertEqual(parent[0].tail, ' in text.')
    #     self.assertEqual(parent[0].get('type'), MathType.LATEX)
    #     self.assertEqual(parent[0].get('by'), 'katex')
    #     self.assertEqual(parent[0].get('html'), '$a^2 + b^2 = c^2$')

    #     # 检查HTML
    #     expected_html = '<div>This is a KaTeX formula: <ccmath-inline type="latex" by="katex" html="$a^2 + b^2 = c^2$">a^2 + b^2 = c^2</ccmath-inline> in text.</div>'
    #     self.assertEqual(element_to_html(parent), expected_html)

    def test_empty_formula(self):
        """测试空公式的情况."""
        # 创建一个简单的HTML元素
        parent = html_to_element('<div>This is an empty formula: $$ in text.</div>')

        # 测试空公式
        self.mathjax_render._process_math_in_text(parent, parent.text, inline_pattern, False, False)

        # 验证结果 - 应该保持原文本不变
        self.assertEqual(parent.text, 'This is an empty formula: $$ in text.')
        self.assertEqual(len(parent), 0)

        # 检查HTML - 应该保持原HTML不变
        expected_html = '<div>This is an empty formula: $$ in text.</div>'
        self.assertEqual(element_to_html(parent), expected_html)

    def test_nested_elements(self):
        """测试嵌套元素的情况."""
        # 创建一个嵌套的HTML元素
        parent = html_to_element('<div><p>Paragraph with formula: $a^2$ <span>Span</span> text with formula: $b^2$ end.</p></div>')

        # 处理p.text
        self.mathjax_render._find_math_in_element(parent, inline_pattern, display_pattern)

        # 检查最终HTML
        final_html = '<div><p>Paragraph with formula: <ccmath-inline type="latex" by="mathjax" html="$a^2$">a^2</ccmath-inline> <span>Span</span> text with formula: <ccmath-inline type="latex" by="mathjax" html="$b^2$">b^2</ccmath-inline> end.</p></div>'
        self.assertEqual(element_to_html(parent), final_html)

    def test_find_math_method(self):
        """测试find_math方法."""
        # 创建一个HTML树
        html = """
        <div>
            <p>Paragraph with inline formula: $a^2 + b^2 = c^2$ and display formula: $$E = mc^2$$</p>
            <p>Another paragraph with [textex]\\frac{1}{2}[/textex] formula.</p>
        </div>
        """
        root = html_to_element(html)

        # 使用find_math方法处理
        self.mathjax_render.find_math(root)

        # 验证结果
        p1 = root[0]
        p2 = root[1]

        # 检查第一个段落
        self.assertEqual(p1.text, 'Paragraph with inline formula: ')
        self.assertEqual(len(p1), 2)
        self.assertEqual(p1[0].tag, CCTag.CC_MATH_INLINE)
        self.assertEqual(p1[0].text, 'a^2 + b^2 = c^2')
        self.assertEqual(p1[0].tail, ' and display formula: ')
        self.assertEqual(p1[1].tag, CCTag.CC_MATH_INTERLINE)
        self.assertEqual(p1[1].text, 'E = mc^2')
        self.assertEqual(p1[1].tail, '')

        # 检查第二个段落
        self.assertEqual(p2.text, 'Another paragraph with [textex]\\frac{1}{2}[/textex] formula.')
        self.assertEqual(len(p2), 0)

        # 检查完整HTML
        print('test_find_math_method expected_html:', element_to_html(root))
        expected_html = """<div>
            <p>Paragraph with inline formula: <ccmath-inline type="latex" by="mathjax" html="$a^2 + b^2 = c^2$">a^2 + b^2 = c^2</ccmath-inline> and display formula: <ccmath-interline type="latex" by="mathjax" html="$$E = mc^2$$">E = mc^2</ccmath-interline></p>
            <p>Another paragraph with [textex]\\frac{1}{2}[/textex] formula.</p>
        </div>
        """
        self.assertEqual(element_to_html(root), expected_html)

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
        result = self.mathjax_render._process_math_in_text(parent, parent.text, inline_pattern, False, False)

        # 打印调试信息
        print('text_preservation result:', result)
        print('text_preservation parent.text:', parent.text)
        print('text_preservation HTML:', element_to_html(parent))

        # 验证结果
        self.assertEqual(result, 'Prefix text ')
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
        result = self.mathjax_render._process_math_in_text(parent, parent.text, inline_pattern, False, False)

        # 打印调试信息
        print('multiple_formulas_text_preservation result:', result)
        print('multiple_formulas_text_preservation parent.text:', parent.text)
        print('multiple_formulas_text_preservation HTML:', element_to_html(parent))

        # 验证结果
        self.assertEqual(result, 'Text1 ')
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

    def test_mathjax_get_options(self):
        """测试 MathJax 渲染器的 get_options 方法."""
        # 测试默认配置
        html_default = """
        <html>
        <head>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js"></script>
        </head>
        <body>
            <p>Some math: $E=mc^2$</p>
        </body>
        </html>
        """
        options_default = self.mathjax_render.get_options(html_default)
        self.assertEqual(options_default['inlineMath'], [])
        self.assertEqual(options_default['displayMath'], [])
        self.assertEqual(options_default['version'], '2.7.5')
        self.assertEqual(options_default['config'], '')

        # 测试带有配置的 MathJax
        html_with_config = """
        <html>
        <head>
            <script type="text/x-mathjax-config">
                MathJax.Hub.Config({
                    tex2jax: {
                        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
                    },
                    extensions: ["tex2jax.js", "TeX/AMSmath.js"]
                });
            </script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML"></script>
        </head>
        <body>
            <p>Some math: $E=mc^2$</p>
        </body>
        </html>
        """
        options_with_config = self.mathjax_render.get_options(html_with_config)
        self.assertEqual(len(options_with_config['inlineMath']), 2)
        self.assertEqual(options_with_config['inlineMath'][0], ['$', '$'])
        self.assertEqual(options_with_config['inlineMath'][1], ['\\(', '\\)'])
        self.assertEqual(len(options_with_config['displayMath']), 2)
        self.assertEqual(options_with_config['displayMath'][0], ['$$', '$$'])
        self.assertEqual(options_with_config['displayMath'][1], ['\\[', '\\]'])
        self.assertEqual(options_with_config['version'], '2.7.5')
        self.assertEqual(options_with_config['config'], 'TeX-MML-AM_CHTML')
        self.assertEqual(len(options_with_config['extensions']), 2)
        self.assertEqual(options_with_config['extensions'][0], 'tex2jax.js')
        self.assertEqual(options_with_config['extensions'][1], 'TeX/AMSmath.js')

        # 测试最新版本的 MathJax
        html_latest = """
        <html>
        <head>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/latest.js"></script>
        </head>
        <body>
            <p>Some math: $E=mc^2$</p>
        </body>
        </html>
        """
        options_latest = self.mathjax_render.get_options(html_latest)
        self.assertEqual(options_latest['version'], 'latest')

        # 测试自定义配置
        html_custom = """
        <html>
        <head>
            <script type="text/x-mathjax-config">
                MathJax.Hub.Config({
                    tex2jax: {
                        inlineMath: [['[itexitex]', '[/itexitex]']],
                        displayMath: [['[textex]', '[/textex]']]
                    }
                });
            </script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js"></script>
        </head>
        <body>
            <p>Some math: [itexitex]E=mc^2[/itexitex]</p>
        </body>
        </html>
        """
        options_custom = self.mathjax_render.get_options(html_custom)
        self.assertEqual(len(options_custom['inlineMath']), 1)
        self.assertEqual(options_custom['inlineMath'][0], ['[itexitex]', '[/itexitex]'])
        self.assertEqual(len(options_custom['displayMath']), 1)
        self.assertEqual(options_custom['displayMath'][0], ['[textex]', '[/textex]'])
        self.assertTrue(self.mathjax_render.is_customized_options())

    def test_katex_get_options(self):
        """测试 KaTeX 渲染器的 get_options 方法."""
        # 测试默认配置
        html_default = """
        <html>
        <head>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/katex.min.css">
            <script src="https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/katex.min.js"></script>
        </head>
        <body>
            <p>Some math: $E=mc^2$</p>
        </body>
        </html>
        """
        options_default = self.katex_render.get_options(html_default)
        self.assertEqual(options_default['version'], '0.13.11')
        self.assertEqual(options_default['auto_render'], False)
        self.assertEqual(options_default['delimiters'], [])

        # 测试带有自动渲染的 KaTeX
        html_auto_render = """
        <html>
        <head>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/katex.min.css">
            <script src="https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/katex.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/contrib/auto-render.min.js"></script>
            <script>
                document.addEventListener("DOMContentLoaded", function() {
                    renderMathInElement(document.body, {
                        delimiters: [
                            {left: "$$", right: "$$", display: true},
                            {left: "$", right: "$", display: false},
                            {left: "\\\\(", right: "\\\\)", display: false}
                        ],
                        throwOnError: false,
                        errorColor: "#CC0000",
                        displayMode: false
                    });
                });
            </script>
        </head>
        <body>
            <p>Some math: $E=mc^2$</p>
        </body>
        </html>
        """
        options_auto_render = self.katex_render.get_options(html_auto_render)
        self.assertEqual(options_auto_render['version'], '0.13.11')
        self.assertEqual(options_auto_render['auto_render'], True)
        self.assertEqual(options_auto_render['throw_on_error'], False)
        self.assertEqual(options_auto_render['error_color'], '#CC0000')
        self.assertEqual(options_auto_render['display_mode'], False)
        self.assertEqual(len(options_auto_render['delimiters']), 3)
        self.assertEqual(options_auto_render['delimiters'][0]['left'], '$$')
        self.assertEqual(options_auto_render['delimiters'][0]['right'], '$$')
        self.assertEqual(options_auto_render['delimiters'][0]['display'], True)
        self.assertEqual(options_auto_render['delimiters'][1]['left'], '$')
        self.assertEqual(options_auto_render['delimiters'][1]['right'], '$')
        self.assertEqual(options_auto_render['delimiters'][1]['display'], False)

        # # 测试自定义配置
        # html_custom = """
        # <html>
        # <head>
        #     <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/katex.min.css">
        #     <script src="https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/katex.min.js"></script>
        #     <script src="https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/contrib/auto-render.min.js"></script>
        #     <script>
        #         document.addEventListener("DOMContentLoaded", function() {
        #             renderMathInElement(document.body, {
        #                 delimiters: [
        #                     {left: "[math]", right: "[/math]", display: true}
        #                 ],
        #                 throwOnError: true,
        #                 displayMode: true
        #             });
        #         });
        #     </script>
        # </head>
        # <body>
        #     <p>Some math: [math]E=mc^2[/math]</p>
        # </body>
        # </html>
        # """
        # options_custom = self.katex_render.get_options(html_custom)
        # self.assertEqual(options_custom['auto_render'], True)
        # self.assertEqual(options_custom['throw_on_error'], True)
        # self.assertEqual(options_custom['display_mode'], True)
        # self.assertEqual(len(options_custom['delimiters']), 1)
        # self.assertEqual(options_custom['delimiters'][0]['left'], '[math]')
        # self.assertEqual(options_custom['delimiters'][0]['right'], '[/math]')
        # self.assertEqual(options_custom['delimiters'][0]['display'], True)

    def test_mathjax_should_ignore_element(self):
        """测试 _should_ignore_element 方法."""
        # 测试带有忽略类的元素
        ignore_element = html_to_element('<div class="tex2jax_ignore">$a^2 + b^2 = c^2$</div>')
        self.assertTrue(self.mathjax_render._should_ignore_element(ignore_element))

        # 测试带有处理类的元素
        process_element = html_to_element('<div class="tex2jax_process">$a^2 + b^2 = c^2$</div>')
        self.assertFalse(self.mathjax_render._should_ignore_element(process_element))

        # 测试普通元素
        normal_element = html_to_element('<div>$a^2 + b^2 = c^2$</div>')
        self.assertFalse(self.mathjax_render._should_ignore_element(normal_element))

        # 测试嵌套元素 - 父元素带有忽略类
        parent_ignore_html = """
        <div class="tex2jax_ignore">
            <p>This formula should be ignored: $a^2 + b^2 = c^2$</p>
        </div>
        """
        parent_ignore_tree = html_to_element(parent_ignore_html)
        child_element = parent_ignore_tree[0]  # 获取 p 元素
        self.assertTrue(self.mathjax_render._should_ignore_element(child_element))

        # 测试嵌套元素 - 子元素带有处理类，父元素带有忽略类
        mixed_html = """
        <div class="tex2jax_ignore">
            <p class="tex2jax_process">This formula should be processed: $a^2 + b^2 = c^2$</p>
        </div>
        """
        mixed_tree = html_to_element(mixed_html)
        mixed_child = mixed_tree[0]  # 获取 p 元素
        self.assertFalse(self.mathjax_render._should_ignore_element(mixed_child))

        # 测试多级嵌套 - 祖父元素带有忽略类
        nested_html = """
        <div class="tex2jax_ignore">
            <section>
                <p>This formula should be ignored: $a^2 + b^2 = c^2$</p>
            </section>
        </div>
        """
        nested_tree = html_to_element(nested_html)
        section_element = nested_tree[0]  # 获取 section 元素
        p_element = section_element[0]  # 获取 p 元素
        self.assertTrue(self.mathjax_render._should_ignore_element(p_element))

        # 测试带有多个类的元素
        multi_class_element = html_to_element('<div class="container main-content tex2jax_ignore">$a^2 + b^2 = c^2$</div>')
        self.assertTrue(self.mathjax_render._should_ignore_element(multi_class_element))

        # 测试带有多个类的元素，包括处理类
        multi_class_process = html_to_element('<div class="container tex2jax_process main-content">$a^2 + b^2 = c^2$</div>')
        self.assertFalse(self.mathjax_render._should_ignore_element(multi_class_process))

    def test_mathjax_find_math_with_ignore(self):
        """测试带有忽略类的元素的 find_math 方法."""
        # 创建一个带有忽略类的 HTML
        ignore_html = """
        <div>
            <p>This formula should be processed: $a^2 + b^2 = c^2$</p>
            <p class="tex2jax_ignore">This formula should be ignored: $x^2 + y^2 = z^2$</p>
            <section class="tex2jax_ignore">
                <p>This formula should also be ignored: $E = mc^2$</p>
            </section>
            <section>
                <p>This formula should be processed: $F = ma$</p>
                <p class="tex2jax_process">This formula should be processed even if parent is ignored: $P = IV$</p>
            </section>
        </div>
        """
        root = html_to_element(ignore_html)

        # 使用 find_math 方法处理
        self.mathjax_render.find_math(root)

        # 验证结果
        # 第一个段落应该被处理
        p1 = root[0]
        self.assertEqual(p1.text, 'This formula should be processed: ')
        self.assertEqual(len(p1), 1)
        self.assertEqual(p1[0].tag, CCTag.CC_MATH_INLINE)
        self.assertEqual(p1[0].text, 'a^2 + b^2 = c^2')

        # 第二个段落（带有忽略类）不应该被处理
        p2 = root[1]
        self.assertEqual(p2.text, 'This formula should be ignored: $x^2 + y^2 = z^2$')
        self.assertEqual(len(p2), 0)

        # 第三个部分（带有忽略类）不应该被处理
        section1 = root[2]
        p3 = section1[0]
        self.assertEqual(p3.text, 'This formula should also be ignored: $E = mc^2$')
        self.assertEqual(len(p3), 0)

        # 第四个部分的第一个段落应该被处理
        section2 = root[3]
        p4 = section2[0]
        self.assertEqual(p4.text, 'This formula should be processed: ')
        self.assertEqual(len(p4), 1)
        self.assertEqual(p4[0].tag, CCTag.CC_MATH_INLINE)
        self.assertEqual(p4[0].text, 'F = ma')

        # 第四个部分的第二个段落（带有处理类）应该被处理
        p5 = section2[1]
        self.assertEqual(p5.text, 'This formula should be processed even if parent is ignored: ')
        self.assertEqual(len(p5), 1)
        self.assertEqual(p5[0].tag, CCTag.CC_MATH_INLINE)
        self.assertEqual(p5[0].text, 'P = IV')

        # 检查HTML - 确保所有文本段都被保留
        excepted_html = """<div>
            <p>This formula should be processed: <ccmath-inline type="latex" by="mathjax" html="$a^2 + b^2 = c^2$">a^2 + b^2 = c^2</ccmath-inline></p>
            <p class="tex2jax_ignore">This formula should be ignored: $x^2 + y^2 = z^2$</p>
            <section class="tex2jax_ignore">
                <p>This formula should also be ignored: $E = mc^2$</p>
            </section>
            <section>
                <p>This formula should be processed: <ccmath-inline type="latex" by="mathjax" html="$F = ma$">F = ma</ccmath-inline></p>
                <p class="tex2jax_process">This formula should be processed even if parent is ignored: <ccmath-inline type="latex" by="mathjax" html="$P = IV$">P = IV</ccmath-inline></p>
            </section>
        </div>
        """
        self.assertEqual(element_to_html(root), excepted_html)

    def test_detect_render_type(self):
        """测试检测渲染器类型的方法."""
        from llm_web_kit.extractor.html.recognizer.cc_math.render.render import \
            BaseMathRender

        # 测试 MathJax 渲染器检测
        mathjax_html = """
        <html>
        <head>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML"></script>
        </head>
        <body>
            <p>Some math: $E=mc^2$</p>
        </body>
        </html>
        """
        base_render = BaseMathRender()
        mathjax_render = base_render.get_math_render(mathjax_html)
        self.assertIsNotNone(mathjax_render)
        self.assertEqual(mathjax_render.get_render_type(), 'mathjax')

        # 测试 KaTeX 渲染器检测
        katex_html = """
        <html>
        <head>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/katex.min.css">
            <script src="https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/katex.min.js"></script>
        </head>
        <body>
            <p>Some math: $E=mc^2$</p>
        </body>
        </html>
        """
        katex_render = base_render.get_math_render(katex_html)
        self.assertIsNotNone(katex_render)
        self.assertEqual(katex_render.get_render_type(), 'katex')

        # 测试同时包含 MathJax 和 KaTeX 的情况（应该优先检测 KaTeX）
        mixed_html = """
        <html>
        <head>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/katex.min.css">
            <script src="https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/katex.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML"></script>
        </head>
        <body>
            <p>Some math: $E=mc^2$</p>
        </body>
        </html>
        """
        mixed_render = base_render.get_math_render(mixed_html)
        self.assertIsNotNone(mixed_render)
        self.assertEqual(mixed_render.get_render_type(), 'katex')

        # 测试没有渲染器的情况
        no_render_html = """
        <html>
        <head>
            <title>No Math Renderer</title>
        </head>
        <body>
            <p>Some text without math</p>
        </body>
        </html>
        """
        no_render = base_render.get_math_render(no_render_html)
        self.assertIsInstance(no_render, BaseMathRender)
        self.assertIsNone(no_render.get_render_type())

        # 测试不同版本的 MathJax
        mathjax3_html = """
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/mathjax@3.0.0/es5/tex-mml-chtml.js"></script>
        </head>
        <body>
            <p>Some math: $E=mc^2$</p>
        </body>
        </html>
        """
        mathjax3_render = base_render.get_math_render(mathjax3_html)
        self.assertIsNotNone(mathjax3_render)
        self.assertEqual(mathjax3_render.get_render_type(), 'mathjax')

        # 测试 MathJax 的 CDN 变体
        mathjax_cdn_html = """
        <html>
        <head>
            <script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
        </head>
        <body>
            <p>Some math: $E=mc^2$</p>
        </body>
        </html>
        """
        mathjax_cdn_render = base_render.get_math_render(mathjax_cdn_html)
        self.assertIsNotNone(mathjax_cdn_render)
        self.assertEqual(mathjax_cdn_render.get_render_type(), 'mathjax')

        # 测试 KaTeX 的自动渲染扩展
        katex_auto_html = """
        <html>
        <head>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/katex.min.css">
            <script src="https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/katex.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/contrib/auto-render.min.js"></script>
        </head>
        <body>
            <p>Some math: $E=mc^2$</p>
        </body>
        </html>
        """
        katex_auto_render = base_render.get_math_render(katex_auto_html)
        self.assertIsNotNone(katex_auto_render)
        self.assertEqual(katex_auto_render.get_render_type(), 'katex')

        # 测试无效的 HTML
        invalid_html = 'This is not valid HTML'
        invalid_render = base_render.get_math_render(invalid_html)
        self.assertIsInstance(invalid_render, BaseMathRender)

        # 测试空 HTML
        empty_html = ''
        empty_render = base_render.get_math_render(empty_html)
        self.assertIsNone(empty_render)

    def test_detect_render_type_from_files(self):
        """测试从文件中检测渲染器类型."""
        from llm_web_kit.extractor.html.recognizer.cc_math.render.render import \
            BaseMathRender

        # 使用 TEST_GET_MATH_RENDER 中的测试用例
        for test_case in TEST_GET_MATH_RENDER:
            input_files = test_case['input']
            expected_type = test_case['expected']

            # 跳过不存在的文件
            if not all(base_dir.joinpath(file).exists() for file in input_files):
                continue

            # 读取文件内容
            html_content = ''
            for file in input_files:
                file_path = base_dir.joinpath(file)
                if file_path.exists():
                    with open(file_path, 'r', encoding='utf-8') as f:
                        html_content += f.read()

            # 检测渲染器类型
            base_render = BaseMathRender()
            render = base_render.get_math_render(html_content)

            # 验证结果
            if expected_type is None:
                self.assertIsInstance(render, BaseMathRender)
                self.assertIsNone(render.get_render_type())
            else:
                self.assertIsNotNone(render)
                self.assertEqual(render.get_render_type(), expected_type)

                # 检查是否为自定义选项
                is_customized = test_case['is_customized_options']
                if expected_type == 'mathjax':
                    self.assertEqual(render.is_customized_options(), is_customized)

    def test_detect_render_type_none(self):
        """测试检测空HTML树."""
        self.assertIsNone(BaseMathRender.detect_render_type(None))

    def test_detect_render_type_empty(self):
        """测试检测空内容的HTML."""
        tree = html_to_element('<html><body></body></html>')
        self.assertIsNone(BaseMathRender.detect_render_type(tree))

    def test_detect_render_type_katex(self):
        """测试检测KaTeX渲染器."""
        # 测试常规KaTeX链接
        html = """
        <html>
            <head>
                <link rel="stylesheet"
                    href="https://cdn.jsdelivr.net/npm/katex/dist/katex.min.css">
            </head>
            <body></body>
        </html>
        """
        tree = html_to_element(html)
        self.assertEqual(
            BaseMathRender.detect_render_type(tree),
            MathRenderType.KATEX
        )

        # 测试自定义KaTeX链接
        html = """
        <html>
            <head>
                <link rel="stylesheet" href="/static/katex/katex.css">
            </head>
            <body></body>
        </html>
        """
        tree = html_to_element(html)
        self.assertEqual(
            BaseMathRender.detect_render_type(tree),
            MathRenderType.KATEX
        )

    def test_detect_render_type_mathjax(self):
        """测试检测MathJax渲染器."""
        # 测试常规MathJax脚本
        html = """
        <html>
            <head>
                <script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js">
                </script>
            </head>
            <body></body>
        </html>
        """
        tree = html_to_element(html)
        self.assertEqual(
            BaseMathRender.detect_render_type(tree),
            MathRenderType.MATHJAX
        )

        # 测试AsciiMath脚本
        html = """
        <html>
            <head>
                <script src="/static/asciimath/asciimath.js"></script>
            </head>
            <body></body>
        </html>
        """
        tree = html_to_element(html)
        self.assertEqual(
            BaseMathRender.detect_render_type(tree),
            MathRenderType.MATHJAX
        )

    def test_detect_render_type_mixed(self):
        """测试同时存在多个渲染器的情况."""
        html = """
        <html>
            <head>
                <link rel="stylesheet" href="katex.min.css">
                <script src="mathjax.js"></script>
            </head>
            <body></body>
        </html>
        """
        tree = html_to_element(html)
        # 应该返回第一个检测到的渲染器类型
        self.assertEqual(
            BaseMathRender.detect_render_type(tree),
            MathRenderType.KATEX
        )

    def test_create_render_none(self):
        """测试创建渲染器（无渲染器类型）."""
        tree = html_to_element('<html><body></body></html>')
        render = BaseMathRender.create_render(tree)
        self.assertIsInstance(render, BaseMathRender)

    def test_create_render_katex(self):
        """测试创建KaTeX渲染器."""
        html = """
        <html>
            <head>
                <link rel="stylesheet" href="katex.min.css">
            </head>
            <body></body>
        </html>
        """
        tree = html_to_element(html)
        render = BaseMathRender.create_render(tree)
        self.assertIsInstance(render, KaTeXRender)

    def test_create_render_mathjax(self):
        """测试创建MathJax渲染器."""
        html = """
        <html>
            <head>
                <script src="mathjax.js"></script>
            </head>
            <body></body>
        </html>
        """
        tree = html_to_element(html)
        render = BaseMathRender.create_render(tree)
        self.assertIsInstance(render, MathJaxRender)


if __name__ == '__main__':
    unittest.main()
