import os
import re
from pathlib import Path
from typing import Tuple

from lxml import etree
from py_asciimath.translator.translator import ASCIIMath2Tex

from llm_web_kit.libs.doc_element_type import DocElementType
from llm_web_kit.libs.html_utils import html_to_element
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
class MathType:
    LATEX = 'latex'
    MATHML = 'mathml'
    ASCIIMATH = 'asciimath'
    HTMLMATH = 'htmlmath'  # sub, sup, etc.


# 数学公式渲染器
class MathRender:
    MATHJAX = 'mathjax'
    KATEX = 'katex'


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


xsl_path = os.path.join(Path(__file__).parent, 'mmltex/mmltex.xsl')
xslt = etree.parse(xsl_path)
transform = etree.XSLT(xslt)


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
        tree = html_to_element(html)
        if tree is None:
            return None
        # 查找head标签
        # head = tree.find('head')
        # if head is not None:
        # 检查 MathJax
        for script in tree.iter('script'):
            if script.get('src') and 'mathjax' in script.get('src', '').lower():
                return MathRender.MATHJAX

        # 检查 KaTeX
        for link in tree.iter('link'):
            if link.get('href') and 'katex' in link.get('href', '').lower():
                return MathRender.KATEX

        return None

    def get_equation_type(self, html: str) -> Tuple[str, str]:
        """根据latex_config判断数学公式是行内还是行间公式.

        Args:
            html: 包含数学公式的HTML文本

        Returns:
            Tuple[str, str]: (EQUATION_INLINE 或 EQUATION_INTERLINE, 公式类型)

        Examples:
            >>> get_equation_type("<span>这是行内公式 $x^2$ 测试</span>")
            ('equation-inline', 'latex')
            >>> get_equation_type("<span>这是行间公式 $$y=mx+b$$ 测试</span>")
            ('equation-interline', 'latex')
        """
        tree = html_to_element(html)
        if tree is None:
            raise ValueError(f'Failed to load html: {html}')

        for node in tree.iter():
            # 先检查mathml
            math_elements = node.xpath('//math')
            if len(math_elements) > 0:
                if math_elements[0].get('display') == 'block':
                    return EQUATION_INTERLINE, MathType.MATHML
                else:
                    return EQUATION_INLINE, MathType.MATHML

            # 再检查latex
            if text := text_strip(node.text):
                def check_delimiters(delims_list):
                    for start, end in delims_list:
                        pattern = f'{re.escape(start)}.*?{re.escape(end)}'
                        if re.search(pattern, text, re.DOTALL):
                            return True
                    return False
                # 优先检查行间公式
                if check_delimiters(latex_config['displayMath']):
                    return EQUATION_INTERLINE, MathType.LATEX
                if check_delimiters(latex_config['inlineMath']):
                    return EQUATION_INLINE, MathType.LATEX

                # 再检查asciimath，通常被包含在`...`中，TODO：行间和行内如何区分
                if re.search(r'`[^`]+`', text):
                    return EQUATION_INLINE, MathType.ASCIIMATH

            # 检查 HTML 数学标记（sub 和 sup）
            sub_elements = tree.xpath('//sub')
            sup_elements = tree.xpath('//sup')
            if (sub_elements and any(text_strip(elem.text) for elem in sub_elements)) or \
                (sup_elements and any(text_strip(elem.text) for elem in sup_elements)):
                return EQUATION_INLINE, MathType.HTMLMATH

        return None, None

    def mml_to_latex(self, mml_code):
        # Remove any attributes from the math tag
        mml_code = re.sub(r'(<math.*?>)', r'\1', mml_code)
        mml_ns = mml_code.replace('<math>', '<math xmlns="http://www.w3.org/1998/Math/MathML">')  # Required.

        mml_ns = mml_ns.replace('&quot;', '"')
        mml_ns = mml_ns.replace("'\\\"", '"').replace("\\\"'", '"')

        # 很多网页中标签内容就是错误
        # pattern = r"(<[^<>]*?\s)(mathbackground|mathsize|mathvariant|mathfamily|class|separators|style|id|rowalign|columnspacing|rowlines|columnlines|frame|framespacing|equalrows|equalcolumns|align|linethickness|lspace|rspace|mathcolor|rowspacing|displaystyle|style|columnalign|open|close|right|left)(?=\s|>)(?![\"'][^<>]*?>)"
        # def replace_attr(match):
        #     tag_start = match.group(1)  # 标签开始部分和空格
        #     attr_name = match.group(2)  # 属性名
        #     return f'{tag_start}{attr_name}=\"\" '
        # # 替换文本
        # mml_ns = re.sub(pattern, replace_attr, mml_ns, re.S)
        # mml_ns = re.sub(pattern, replace_attr, mml_ns, re.S)
        # mml_ns = re.sub(pattern, replace_attr, mml_ns, re.S)

        pattern = r'"([^"]+?)\''
        mml_ns = re.sub(pattern, r'"\1"', mml_ns)
        mml_dom = html_to_element(mml_ns)
        mmldom = transform(mml_dom)
        latex_code = str(mmldom)
        return latex_code


if __name__ == '__main__':
    cm = CCMATH()
    print(cm.get_equation_type('<span>$$a^2 + b^2 = c^2$$</span>'))
    print(cm.get_equation_type('<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mi>a</mi><mo>&#x2260;</mo><mn>0</mn></math>'))
    print(cm.get_equation_type('<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>a</mi><mo>&#x2260;</mo><mn>0</mn></math>'))
