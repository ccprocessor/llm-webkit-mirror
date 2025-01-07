import re
from typing import Tuple

from py_asciimath.translator.translator import ASCIIMath2Tex

from llm_web_kit.libs.doc_element_type import DocElementType
from llm_web_kit.libs.html_utils import build_html_tree
from llm_web_kit.pipeline.extractor.html.recognizer.recognizer import CCTag

asciimath2tex = ASCIIMath2Tex(log=False)
color_regex = re.compile(r'\\textcolor\[.*?\]\{.*?\}')


MATH_KEYWORDS = [
    'MathJax',
    'mathjax',
    '<math',
    'math-container',
    'katex.min.css',
    'latex.php',
    'codecogs',
    'tex.cgi',
    'class="tex"',
    "class='tex'",
]

# ccmath标签，区分行内行间公式
CCMATH_INTERLINE = CCTag.CC_MATH_INTERLINE
CCMATH_INLINE = CCTag.CC_MATH_INLINE

# 数学公式的正则表达式模式
LATEX_PATTERNS = [
    r'\$\$(.*?)\$\$',  # 匹配 $$...$$
    r'\$(.*?)\$',      # 匹配 $...$
    r'\\begin{equation}(.*?)\\end{equation}',  # 匹配 equation 环境
    r'\\begin{align}(.*?)\\end{align}',        # 匹配 align 环境
    r'\\[(.*?)\\]',    # 匹配 \[...\]
    r'\\((.*?)\\)',    # 匹配 \(...\)
]

# 数学标记语言
MATH_TYPE_MAP = {
    'LATEX': 'latex',
    'MATHML': 'mathml',
    'ASCIIMATH': 'asciimath',
    'HTMLMATH': 'htmlmath',  # sub, sup, etc.
}

# 数学公式渲染器
MATH_RENDER_MAP = {
    'MATHJAX': 'mathjax',
    'KATEX': 'katex',
}

# 行内行间公式，MathJax中一般也可以通过配置来区分行内行间公式
EQUATION_INLINE = DocElementType.EQUATION_INLINE
EQUATION_INTERLINE = DocElementType.EQUATION_INTERLINE
latex_config = {
    'inlineMath': [
        ['$', '$'],
        ['\\(', '\\)']
    ],
    'displayMath': [
        ['\\[', '\\]'],
        ['$$', '$$'],
        ['\\begin{equation}', '\\end{equation}'],
        ['\\begin{align}', '\\end{align}']
    ],
}

asciimath2tex = ASCIIMath2Tex(log=False)


def text_strip(text):
    return text.strip() if text else text


def wrap_math(s, display=False):
    s = re.sub(r'\s+', ' ', s)
    s = color_regex.sub('', s)
    s = s.replace('$', '')
    s = s.replace('\n', ' ').replace('\\n', '')
    # 只移除开头和结尾的花括号，例如在wikipidia中：{\displaystyle d_{Y}(f(y),f(x))&lt;\epsilon } -> \displaystyle d_{Y}(f(y),f(x))&lt;\epsilon
    s = s.strip()
    if s.startswith('{') and s.endswith('}'):
        s = s[1:-1]
    s = s.strip()
    if len(s) == 0:
        return s
    # Don't wrap if it's already in \align
    if 'align' in s:
        return s
    if display:
        return '$$' + s + '$$'
    return '$' + s + '$'


class CCMATH():
    def extract_asciimath(s: str) -> str:
        parsed = asciimath2tex.translate(s)
        return parsed

    def get_math_render(self, html: str) -> str:
        """获取数学公式渲染器.
        示例:
        MathJax:
            <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/latest.js?config=TeX-MML-AM_CHTML"></script>
        Katex:
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/katex.min.css">
        """
        tree = build_html_tree(html)
        if tree is None:
            return None
        # 查找head标签
        # head = tree.find('head')
        # if head is not None:
        # 检查 MathJax
        for script in tree.iter('script'):
            if script.get('src') and 'mathjax' in script.get('src', '').lower():
                return MATH_RENDER_MAP['MATHJAX']

        # 检查 KaTeX
        for link in tree.iter('link'):
            if link.get('href') and 'katex' in link.get('href', '').lower():
                return MATH_RENDER_MAP['KATEX']

        return None

    def get_equation_type(self, content: str) -> str:
        """根据latex_config判断数学公式是行内还是行间公式.

        Args:
            html: 包含数学公式的HTML文本

        Returns:
            str: EQUATION_INLINE 或 EQUATION_INTERLINE

        Examples:
            >>> get_equation_type("这是行内公式 $x^2$ 测试")
            'equation-inline'
            >>> get_equation_type("这是行间公式 $$y=mx+b$$ 测试")
            'equation-interline'
        """
        def check_delimiters(delims_list):
            for start, end in delims_list:
                pattern = f'{re.escape(start)}.*?{re.escape(end)}'
                if re.search(pattern, content, re.DOTALL):
                    return True
            return False
        # 优先检查行间公式
        if check_delimiters(latex_config['displayMath']):
            return EQUATION_INTERLINE
        if check_delimiters(latex_config['inlineMath']):
            return EQUATION_INLINE

        return None

    def contains_math(self, html: str) -> Tuple[bool, str]:
        """判断html中是否包含数学公式.并根据不同的公式类型返回对应的math_type.

        Args:
            html: 要检查的HTML字符串

        Returns:
            Tuple[bool, str]: (是否包含数学公式, 公式类型)

        示例:
            >>> contains_math('<span>$$x^2$$</span>')
            (True, 'latex')
        """
        # 检查是否包含 LaTeX 格式的公式
        for pattern in LATEX_PATTERNS:
            if re.search(pattern, html, re.DOTALL):
                return True, MATH_TYPE_MAP['LATEX']

        # 检查是否包含 MathML 标签
        tree = build_html_tree(html)
        if tree is not None:
            math_elements = tree.xpath('.//math')
            if math_elements and any(text_strip(elem.text) for elem in math_elements):
                return True, MATH_TYPE_MAP['MATHML']

            # 检查 HTML 数学标记（sub 和 sup）
            sub_elements = tree.xpath('.//sub')
            sup_elements = tree.xpath('.//sup')
            if (sub_elements and any(text_strip(elem.text) for elem in sub_elements)) or \
                (sup_elements and any(text_strip(elem.text) for elem in sup_elements)):
                return True, MATH_TYPE_MAP['HTMLMATH']

        # 检查是否包含 AsciiMath
        # 通常 AsciiMath 被包含在 `...` 中
        if re.search(r'`[^`]+`', html):
            return True, MATH_TYPE_MAP['ASCIIMATH']

        return False, None
