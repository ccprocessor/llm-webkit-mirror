import os
import re
from pathlib import Path
from typing import List, Tuple

from lxml import etree
from lxml.html import HtmlElement
from py_asciimath.translator.translator import ASCIIMath2Tex

from llm_web_kit.extractor.html.recognizer.recognizer import CCTag
from llm_web_kit.libs.doc_element_type import DocElementType
from llm_web_kit.libs.html_utils import (build_cc_element, element_to_html,
                                         element_to_html_unescaped,
                                         html_to_element)

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

LATEX_IMAGE_CLASS_NAMES = [
    'latexcenter',
    'latex',
    'tex',
    'latexdisplay',
    'latexblock',
    'latexblockcenter',
]

LATEX_IMAGE_SRC_NAMES = [
    'codecogs.com',
    'latex.php',
    '/images/math/codecogs',
    'mimetex.cgi',
    'mathtex.cgi',
]

# ccmath标签，区分行内行间公式
CCMATH_INTERLINE = CCTag.CC_MATH_INTERLINE
CCMATH_INLINE = CCTag.CC_MATH_INLINE
CCMATH_HANDLE_FAILED = 'ccmath-failed'


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


# node.text匹配结果：
class MathMatchRes:
    ALLMATCH = 'all_match'
    PARTIALMATCH = 'partial_match'
    NOMATCH = 'no_match'


class MATH_TYPE_PATTERN:
    INLINEMATH = 'inlineMath'
    DISPLAYMATH = 'displayMath'


# 行内行间公式，MathJax中一般也可以通过配置来区分行内行间公式
EQUATION_INLINE = DocElementType.EQUATION_INLINE
EQUATION_INTERLINE = DocElementType.EQUATION_INTERLINE
latex_config = {
    MATH_TYPE_PATTERN.INLINEMATH: [
        ['$', '$'],
        ['\\(', '\\)']
    ],
    MATH_TYPE_PATTERN.DISPLAYMATH: [
        ['\\[', '\\]'],
        ['$$', '$$'],
        ['\\begin{equation}', '\\end{equation}'],
        ['\\begin{align}', '\\end{align}'],
        ['\\begin{alignat}', '\\end{alignat}'],
        ['\\begin{array}', '\\end{array}'],
        # 添加通用的begin/end匹配
        ['\\begin{.*?}', '\\end{.*?}'],
    ],
}

asciiMath_config = {
    MATH_TYPE_PATTERN.INLINEMATH: [
        [r'`', r'`'],
    ],
    MATH_TYPE_PATTERN.DISPLAYMATH: [
        [r'`', r'`'],
    ],
}

MATH_TYPE_TO_DISPLAY = {
    MathType.LATEX: latex_config,
    MathType.ASCIIMATH: asciiMath_config
}


asciimath2tex = ASCIIMath2Tex(log=False)


def text_strip(text):
    return text.strip() if text else text


xsl_path = os.path.join(Path(__file__).parent, 'mmltex/mmltex.xsl')
xslt = etree.parse(xsl_path)
transform = etree.XSLT(xslt)


class CCMATH():
    def wrap_math(self, s, display=False):
        """根据行间行内公式加上$$或$"""
        s = re.sub(r'\s+', ' ', s)
        s = color_regex.sub('', s)
        s = s.replace('$', '')
        s = s.replace('\n', ' ').replace('\\n', '')
        s = s.strip()
        if len(s) == 0:
            return s
        # Don't wrap if it's already in \align
        if '\\begin' in s:
            return s
        if display:
            return '$$' + s + '$$'
        return '$' + s + '$'

    def wrap_math_md(self, s):
        """去掉latex公式头尾的$$或$或\\(\\)或\\[\\]"""
        s = s.strip()
        if s.startswith('$$') and s.endswith('$$'):
            return s.replace('$$', '')
        if s.startswith('$') and s.endswith('$'):
            return s.replace('$', '')
        if s.startswith('\\(') and s.endswith('\\)'):
            return s.replace('\\(', '').replace('\\)', '')
        if s.startswith('\\[') and s.endswith('\\]'):
            return s.replace('\\[', '').replace('\\]', '')
        if s.startswith('`') and s.endswith('`'):
            return s.replace('`', '')
        return s

    def wrap_math_space(self, s):
        """转义空格."""
        s = s.strip()
        return s.replace('&space;', ' ')

    def extract_asciimath(self, s: str) -> str:
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
        # 检查 KaTeX
        for link in tree.iter('link'):
            if link.get('href') and 'katex' in link.get('href', '').lower():
                return MathRender.KATEX
        # 查找head标签
        # head = tree.find('head')
        # if head is not None:
        # 检查 MathJax
        for script in tree.iter('script'):
            src = script.get('src', '').lower()
            if src and ('mathjax' in src or 'asciimath' in src):
                return MathRender.MATHJAX
        return None

    def get_equation_type(self, html: str) -> List[Tuple[str, str]]:
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
        def check_delimiters(delims_list, s):
            for start, end in delims_list:
                escaped_start = re.escape(start)
                if start == '$':
                    escaped_start = r'(?<!\$)' + escaped_start + r'(?!\$)'
                # 处理end的特殊情况：如果是$，同样添加环视断言
                escaped_end = re.escape(end)
                if end == '$':
                    escaped_end = r'(?<!\$)' + escaped_end + r'(?!\$)'
                all_pattern = f'^{escaped_start}.*?{escaped_end}$'.replace(r'\.\*\?', '.*?')
                partial_pattern = f'{escaped_start}.*?{escaped_end}'.replace(r'\.\*\?', '.*?')
                if re.search(all_pattern, s, re.DOTALL):
                    return MathMatchRes.ALLMATCH
                if re.search(partial_pattern, s, re.DOTALL):
                    return MathMatchRes.PARTIALMATCH
            return MathMatchRes.NOMATCH

        tree = html_to_element(html)
        if tree is None:
            raise ValueError(f'Failed to load html: {html}')
        result = []
        for node in tree.iter():
            # 先检查mathml
            math_elements = node.xpath('//math | //*[contains(local-name(), ":math")]')
            if len(math_elements) > 0:
                # 检查math标签是否有display属性且值为block，https://developer.mozilla.org/en-US/docs/Web/MathML/Element/math
                if math_elements[0].get('display') == 'block':
                    result.append((EQUATION_INTERLINE, MathType.MATHML))
                else:
                    # 检查math下的mstyle标签，https://developer.mozilla.org/en-US/docs/Web/MathML/Element/mstyle
                    # math_mstyle_element = math_elements[0].xpath('.//mstyle')
                    # if math_mstyle_element and math_mstyle_element[0].get('displaystyle') == 'true':
                    #     return EQUATION_INTERLINE, MathType.MATHML
                    result.append((EQUATION_INLINE, MathType.MATHML))

            # 再检查latex
            if text := text_strip(node.text):
                # 优先检查行间公式
                if check_delimiters(latex_config[MATH_TYPE_PATTERN.DISPLAYMATH], text) != MathMatchRes.NOMATCH:
                    result.append((EQUATION_INTERLINE, MathType.LATEX))
                if check_delimiters(latex_config[MATH_TYPE_PATTERN.INLINEMATH], text) != MathMatchRes.NOMATCH:
                    result.append((EQUATION_INLINE, MathType.LATEX))

                # 再检查asciimath，通常被包含在`...`中，TODO：先只支持行间公式
                if check_delimiters(asciiMath_config[MATH_TYPE_PATTERN.DISPLAYMATH], text) == MathMatchRes.ALLMATCH:
                    result.append((EQUATION_INTERLINE, MathType.ASCIIMATH))
                if check_delimiters(asciiMath_config[MATH_TYPE_PATTERN.DISPLAYMATH], text) == MathMatchRes.PARTIALMATCH:
                    result.append((EQUATION_INLINE, MathType.ASCIIMATH))

            # 检查script标签
            script_elements = tree.xpath('//script')
            if script_elements and any(text_strip(elem.text) for elem in script_elements):
                # 判断type属性，如有包含 mode=display 则认为是行间公式
                for script in script_elements:
                    if 'mode=display' in script.get('type', ''):
                        result.append((EQUATION_INTERLINE, MathType.LATEX))
                    else:
                        result.append((EQUATION_INLINE, MathType.LATEX))

            # 检查 HTML 数学标记（sub 和 sup）
            sub_elements = tree.xpath('//sub')
            sup_elements = tree.xpath('//sup')
            if (sub_elements and any(text_strip(elem.text) for elem in sub_elements)) or \
                (sup_elements and any(text_strip(elem.text) for elem in sup_elements)):
                result.append((EQUATION_INLINE, MathType.HTMLMATH))
        return self.equation_type_to_tag(result)

    def equation_type_to_tag(self, type_math_type: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        return list({
            (eq_type, math_type): (
                CCMATH_INLINE if eq_type == EQUATION_INLINE else CCMATH_INTERLINE,
                math_type
            )
            for eq_type, math_type in type_math_type
            if eq_type in {EQUATION_INLINE, EQUATION_INTERLINE}
        }.values())

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
        mml_ns = re.sub(r'<mspace[^>]*>.*?</mspace>', '', mml_ns, flags=re.DOTALL)
        mml_ns = self.fix_mathml_superscript(mml_ns)
        mml_dom = etree.fromstring(mml_ns)
        mmldom = transform(mml_dom)
        latex_code = str(mmldom)
        return latex_code

    def fix_mathml_superscript(self, mathml_str):
        # 解析输入的MathML字符串
        root = etree.fromstring(mathml_str)
        namespace = {'m': 'http://www.w3.org/1998/Math/MathML'}
        mathml_ns = namespace['m']
        for msup in root.xpath('//m:msup', namespaces=namespace):
            if len(msup) < 1:
                continue
            base = msup[0]
            if base.tag != f'{{{mathml_ns}}}mo' or base.text != ')':
                continue
            parent = msup.getparent()
            if parent is None:
                continue
            siblings = list(parent)
            msup_index = siblings.index(msup)
            left_paren = None
            for i in range(msup_index - 1, -1, -1):
                node = siblings[i]
                if node.tag == f'{{{mathml_ns}}}mo' and node.text == '(':
                    left_paren = i
                    break
            if left_paren is None:
                continue
            content_nodes = siblings[left_paren:msup_index]
            mrow = etree.Element(f'{{{mathml_ns}}}mrow')
            for node in content_nodes:
                parent.remove(node)
                mrow.append(node)
            new_msup = etree.Element(f'{{{mathml_ns}}}msup')
            new_msup.append(mrow)
            if len(msup) >= 2:
                new_msup.extend(msup[1:])
            mrow.append(base)
            parent.insert(left_paren, new_msup)
            parent.remove(msup)

        return etree.tostring(root, encoding='unicode', pretty_print=True)

    def replace_math(self, new_tag: str, math_type: str, math_render: str, node: HtmlElement, func, asciimath_wrap: bool = False) -> HtmlElement:
        # pattern re数学公式匹配 func 公式预处理 默认不处理
        pattern_type = MATH_TYPE_PATTERN.DISPLAYMATH if new_tag == CCMATH_INTERLINE else MATH_TYPE_PATTERN.INLINEMATH
        original_text = node.text or ''

        def is_ccmath_wrapped(match_text, original_text: str) -> bool:
            if not match_text or not original_text:
                return False
            start_idx = match_text.start()
            end_idx = match_text.end()
            before_match = original_text[:start_idx].strip()
            after_match = original_text[end_idx:].strip()
            if 'ccmath' in before_match and 'ccmath' in after_match:
                return True
            if pattern_type == MATH_TYPE_PATTERN.DISPLAYMATH:
                for start, end in MATH_TYPE_TO_DISPLAY[MathType.LATEX][MATH_TYPE_PATTERN.INLINEMATH]:
                    if start in before_match and end in after_match:
                        return True
            return False

        def process(match_text):
            try:
                match = match_text.group(0)
                if is_ccmath_wrapped(match_text, original_text):
                    return match
                math_text = self.extract_asciimath(match.strip('`').replace('\\','')) if asciimath_wrap else match
                wrapped_text = func(math_text) if func else math_text
                wrapped_text = self.wrap_math_md(wrapped_text)
                if not wrapped_text:
                    return match
                new_span = build_cc_element(
                    html_tag_name=new_tag,
                    text=wrapped_text,
                    tail='',
                    type=math_type,
                    by=math_render,
                    html=wrapped_text
                )
            except Exception:
                return match
            return element_to_html(new_span)
        try:
            for start, end in MATH_TYPE_TO_DISPLAY[math_type][pattern_type]:
                pattern = f'{re.escape(start)}.*?{re.escape(end)}'.replace(r'\.\*\?', '.*?')
                regex = re.compile(pattern, re.DOTALL)
                original_text = re.sub(regex, process, original_text)
        except Exception:
            node.text = self.build_cc_exception_tag(original_text, math_type, math_render)
            return node
        node.text = original_text
        return html_to_element(element_to_html_unescaped(node))

    def build_cc_exception_tag(self, text, math_type, math_render) -> str:
        return element_to_html(build_cc_element(
            html_tag_name=CCMATH_HANDLE_FAILED,
            text=text,
            tail='',
            type=math_type,
            by=math_render,
            html=text
        ))


if __name__ == '__main__':
    cm = CCMATH()
    print(cm.get_equation_type('<span>$$a^2 + b^2 = c^2$$</span>'))
    print(cm.get_equation_type('<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mi>a</mi><mo>&#x2260;</mo><mn>0</mn></math>'))
    print(cm.get_equation_type('<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>a</mi><mo>&#x2260;</mo><mn>0</mn></math>'))
    print(cm.get_equation_type('<p>这是p的text</p>'))
    print(cm.get_equation_type(r'<p>\begin{align} a^2+b=c\end{align}</p>'))
    print(cm.get_equation_type(r'<p>\begin{abc} a^2+b=c\end{abc}</p>'))
    print(cm.wrap_math(r'{\displaystyle \operatorname {Var} (X)=\operatorname {E} \left[(X-\mu)^{2}\right].}'))
    print(cm.wrap_math(r'$$a^2 + b^2 = c^2$$'))
    print(cm.wrap_math_md(r'{\displaystyle \operatorname {Var} (X)=\operatorname {E} \left[(X-\mu)^{2}\right].}'))
    print(cm.wrap_math_md(r'$$a^2 + b^2 = c^2$$'))
    print(cm.wrap_math_md(r'\(a^2 + b^2 = c^2\)'))
    print(cm.extract_asciimath('x=(-b +- sqrt(b^2 - 4ac))/(2a)'))
    print(cm.replace_math('ccmath-interline','asciimath','',html_to_element(r'<p>`x=(-b +- sqrt(b^2 - 4ac))/(2a)`</p>'),None,True))
    print(cm.replace_math('ccmath-interline','asciimath','',html_to_element(r'<p>like this: \`E=mc^2\`</p>'),None,True))
    print(cm.replace_math('ccmath-interline','asciimath','',html_to_element(r'<p>A `3xx3` matrix,`((1,2,3),(4,5,6),(7,8,9))`, and a `2xx1` matrix, or vector, `((1),(0))`.</p>'),None,True))
    print(cm.replace_math('ccmath-interline','asciimath','',html_to_element(r'<p>`(x+1)/x^2``1/3245`</p>'),None,True))
    print(cm.replace_math('ccmath-interline','latex','',html_to_element(r'<p>start $$f(a,b,c) = (a^2+b^2+c^2)^3$$end</p>'),None,False))
    print(cm.replace_math('ccmath-inline','latex','',html_to_element(r'<p>\( \newcommand{\norm}[1]{\| #1 \|}\)</p>'),None,False))
