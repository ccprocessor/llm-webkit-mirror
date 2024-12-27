import html
import re
from typing import List, Tuple

from lxml import etree
from lxml.etree import Element
from overrides import override
from py_asciimath.translator.translator import ASCIIMath2Tex

from llm_web_kit.libs.logger import logger
from llm_web_kit.pipeline.extractor.html.magic_html.utils import (iter_node,
                                                                  load_html)
from llm_web_kit.pipeline.extractor.html.recognizer.common import (text_strip,
                                                                   wrap_math)
from llm_web_kit.pipeline.extractor.html.recognizer.recognizer import \
    BaseHTMLElementRecognizer

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
EQUATION_INLINE = 'equation-inline'
EQUATION_DISPLAY = 'equation-display'
latex_config = {
    'inlineMath': [
        ['$', '$'],
        ['\\(', '\\)']
    ],
    'displayMath': [
        ['\\[', '\\]'],
        ['$$', '$$']
    ],
}

asciimath2tex = ASCIIMath2Tex(log=False)


class MathRecognizer(BaseHTMLElementRecognizer):
    """解析数学公式元素."""

    def __init__(self):
        super().__init__()

    @override
    def recognize(self, base_url: str, main_html_lst: List[Tuple[str, str]], raw_html: str) -> List[Tuple[str, str]]:
        """父类，解析数学公式元素.

        Args:
            base_url: str: 基础url
            main_html_lst: main_html在一层一层的识别过程中，被逐步分解成不同的元素，[(cc_html, o_hmtl), (cc_html, o_html)]
            raw_html: 原始完整的html

        Returns: main_html_lst中发现有公式，则返回处理后的元素，标签更新为ccmath，否则原样返回.
        示例：
        main_html_lst = [
            ('<p>This is a test.</p>', '<p>This is a test.</p>'),
            ('<pre>Some text with a formula $$x = 5$$ in it.</pre>',
             '<pre>Some text with a formula $$x = 5$$ in it.</pre>'),
            ('<p>爱因斯坦质能方程的公式是：<math>E=mc^2</math>其中<math>mc^2</math>代表了...E是能量。</p>',
             '<p>爱因斯坦质能方程的公式是：<math>E=mc^2</math>其中<math>mc^2</math>代表了...E是能量。</p>')
        ]
        Returns:
        [
            ('<p>This is a test.</p>', '<p>This is a test.</p>'),
            ('<ccmath type="latex" by="">Some text with a formula $$x = 5$$ in it.</ccmath>',
             '<pre>Some text with a formula $$x = 5$$ in it.</pre>'),
            ('<p>爱因斯坦质能方程的公式是：<ccmath type="mathml" by="mathjax">E=mc^2</ccmath>'
             '其中<ccmath type="mathml" by="mathjax">mc^2</ccmath>代表了...E是能量。</p>',
             '<p>爱因斯坦质能方程的公式是：<math>E=mc^2</math>其中<math>mc^2</math>'
             '代表了...E是能量。</p>')
        ]
        """
        result = []
        for cc_html, o_html in main_html_lst:
            # 检查是否包含数学公式
            contains_math, math_type = self.contains_math(cc_html)
            if contains_math and not self.is_cc_html(cc_html):
                # 获取数学公式渲染器
                math_render = self.get_math_render(raw_html)
                result.extend(self.process_ccmath_html(cc_html, o_html, math_type, math_render))
            else:
                result.append((cc_html, o_html))

        return result

    @override
    def to_content_list_node(self, base_url:str, parsed_content: str, raw_html_segment:str) -> dict:
        """将content转换成content_list_node.
        每种类型的html元素都有自己的content-list格式：参考 docs/specification/output_format/content_list_spec.md
        例如代码的返回格式：
        ```json
            {
                "type": "equation-inline", # 数学公式类型，一共equation-inline和equation-display两种
                "raw_content": "<ccmath type="latex" by="mathjax">$u_{x_0}^{in}(x)$</ccmath>",
                "content": {
                    "math_content": "u_{x_0}^{in}(x)",
                    "math_type": "latex",
                    "by": "mathjax"
                }
            }
            ```

            Args:
                content: str: 要转换的content

        Returns:
            dict: content_list_node
        """
        result = {}
        tree = load_html(parsed_content)
        if tree is None:
            raise ValueError(f'Failed to load html: {parsed_content}')

        if tree.tag != 'ccmath':
            raise ValueError(f'No ccmath element found in content: {parsed_content}')
        else:
            # 获取math_content
            math_content = tree.text  # TODO: 需要处理math_content两边的$符号
            math_type = tree.get('type')
            math_render = tree.get('by')
            equation_type = self.get_equation_type(math_content)

            result = {
                'type': equation_type,
                'raw_content': parsed_content,
                'content': {
                    'math_content': math_content,
                    'math_type': math_type,
                    'by': math_render
                }
            }
        return result

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
        tree = load_html(html)
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

    def process_ccmath_html(self, cc_html: str, o_html: str, math_type: str, math_render: str) -> List[Tuple[str, str]]:
        """处理数学公式，将外层标签修改为 ccmath.

        Args:
            cc_html: 处理后的HTML
            o_html: 原始HTML

        Returns:
            List[Tuple[str, str]]: 处理后的HTML对
        """
        # node是从cc_html中解析出来的lxml节点
        tree = load_html(cc_html)
        if tree is None:
            raise ValueError(f'Failed to load html: {cc_html}')

        for node in iter_node(tree):
            parent = node.getparent()
            node_class = node.get('class')

            # 1. 文本中有\\begin{align} 或 \\begin{equation}
            if node.tag not in ['script', 'style'] and text_strip(node.text):
                regex = r'\\begin{align}(.*?)\\end{align}'
                text = node.text
                matches = re.findall(regex, text, re.DOTALL)
                if matches:
                    node.text = text.replace('\\begin{align}', '').replace('\\end{align}', '')

            if node.tag not in ['script', 'style'] and text_strip(node.text):
                regex = r'\\begin{equation}(.*?)\\end{equation}'
                text = node.text
                matches = re.findall(regex, text, re.DOTALL)
                for match in matches:
                    match = match.replace('\\begin{equation}', '')
                    match = match.replace('\\end{equation}', '')
                    wrapped_text = wrap_math(match, display=True)
                    text = text.replace(match, wrapped_text)
                if matches:
                    # Remove the \begin{equation} and \end{equation} tags
                    text = text.replace('\\begin{equation}', '').replace('\\end{equation}', '')
                    node.text = text

            if node.tag not in ['script', 'style'] and text_strip(node.tail):
                regex = r'\\begin{align}(.*?)\\end{align}'
                text = node.tail
                matches = re.findall(regex, text, re.DOTALL)
                if matches:
                    node.tail = text.replace('\\begin{align}', '').replace('\\end{align}', '')

            if node.tag not in ['script', 'style'] and text_strip(node.tail):
                regex = r'\\begin{equation}(.*?)\\end{equation}'
                text = node.tail
                matches = re.findall(regex, text, re.DOTALL)
                for match in matches:
                    match = match.replace('\\begin{equation}', '')
                    match = match.replace('\\end{equation}', '')
                    wrapped_text = wrap_math(match, display=True)
                    text = text.replace(match, wrapped_text)
                if matches:
                    # Remove the \begin{equation} and \end{equation} tags
                    text = text.replace('\\begin{equation}', '').replace('\\end{equation}', '')
                    node.tail = text

            # 4. class 为 math-container
            if node_class == 'math-container':
                try:
                    text = node.text
                    if text_strip(text):
                        new_span = Element('ccmath')
                        wrapped_math = wrap_math(text, display=True)
                        new_span.text = wrapped_math
                        new_span.set('type', math_type)
                        new_span.set('by', math_render)
                        # 将原始节点转换为HTML字符串并解除转义
                        original_html = etree.tostring(node, encoding='utf-8', method='html').decode()
                        new_span.set('html', original_html)
                        if parent is not None:
                            if text_strip(node.tail):
                                new_span.tail = node.tail
                            parent.replace(node, new_span)
                except Exception as e:
                    logger.error(f'Error processing math-container class: {e}')

            # 5. class 为 mathjax
            if (node.tag == 'span' and node.get('class') and
               any('mathjax' in cls.lower() for cls in node.get('class').split())):
                # 如果节点是span标签，并且class属性包含mathjax，MathJax，mathjax_display，MathJax_Display等
                # 示例：
                # <span class="mathjax">
                #     <span class="math-inline">$\frac{1}{2}$</span>
                #     是一个分数
                # </span>

                try:
                    # Get the inner text of the mathjax tag
                    text = ''.join([
                        (node.text or '') +
                        ''.join([etree.tostring(child, encoding='utf-8', method='text').decode() for child in node])
                    ])
                    if text_strip(text):
                        text = html.unescape(text)
                        # Create a new ccmath tag
                        new_cc_html = Element('ccmath')
                        new_cc_html.text = text
                        new_cc_html.set('type', math_type)
                        new_cc_html.set('by', math_render)
                        # 将原始节点转换为HTML字符串并解除转义
                        original_html = etree.tostring(node, encoding='utf-8', method='html').decode()
                        new_cc_html.set('html', original_html)
                        # 处理节点替换
                        if parent is not None:
                            # 保存原始节点的tail文本
                            if node.tail:
                                new_cc_html.tail = node.tail
                            # 在父节点中替换原始节点
                            parent.replace(node, new_cc_html)
                        else:
                            # 如果是根节点，直接替换整个树
                            if node.tail:
                                new_cc_html.tail = node.tail
                            tree = new_cc_html
                except Exception as e:
                    logger.error(f'Error processing mathjax class: {e}')

        return self.html_split_by_tags(etree.tostring(tree, encoding='utf-8', method='html').decode(), ['ccmath'])

    def get_math_render(self, html: str) -> str:
        """获取数学公式渲染器.
        示例:
        MathJax:
            <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/latest.js?config=TeX-MML-AM_CHTML"></script>
        Katex:
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/katex.min.css">
        """
        tree = load_html(html)
        if tree is None:
            return None
        # 查找head标签
        head = tree.find('head')
        if head is not None:
            # 检查 MathJax
            mathjax_script = head.find('.//script[@src]')
            if mathjax_script is not None and 'mathjax' in mathjax_script.get('src', '').lower():
                return MATH_RENDER_MAP['MATHJAX']

            # 检查 KaTeX
            katex_link = head.find('.//link[@href]')
            if katex_link is not None and 'katex' in katex_link.get('href', '').lower():
                return MATH_RENDER_MAP['KATEX']

        return None

    def get_equation_type(self, content: str) -> str:
        """根据latex_config判断数学公式是行内还是行间公式.

        Args:
            html: 包含数学公式的HTML文本

        Returns:
            str: EQUATION_INLINE 或 EQUATION_DISPLAY

        Examples:
            >>> get_equation_type("这是行内公式 $x^2$ 测试")
            'equation-inline'
            >>> get_equation_type("这是行间公式 $$y=mx+b$$ 测试")
            'equation-display'
        """
        def check_delimiters(delims_list):
            for start, end in delims_list:
                pattern = f'{re.escape(start)}.*?{re.escape(end)}'
                if re.search(pattern, content, re.DOTALL):
                    return True
            return False
        # 优先检查行间公式
        if check_delimiters(latex_config['displayMath']):
            return EQUATION_DISPLAY
        if check_delimiters(latex_config['inlineMath']):
            return EQUATION_INLINE

        return None


if __name__ == '__main__':
    math_recognizer = MathRecognizer()
    # test_html = [
    #         (
    #             ('<p>这是p的text<span class="mathjax_display">'
    #              '$$a^2 + b^2 = c^2$$</span>这是span的tail<b>'
    #              '这是b的text</b>这是b的tail</p>'),
    #             ('<p>这是p的text<span class="mathjax_display">'
    #              '$$a^2 + b^2 = c^2$$</span>这是span的tail<b>'
    #              '这是b的text</b>这是b的tail</p>')
    #         )]
    # test_html = [(('<span class=mathjax>Some text with a formula $$x = 5$$ in it.</span>',
    #                '<span class=mathjax>Some text with a formula $$x = 5$$ in it.</span>'))]
    test_html = [
        (
            (
                '<p>I think I can now answer my own question, having come across some decent '
                'references I hadn\'t found before asking it. I found the equation for the '
                'gravitational strain <span class=\"math-container\">$h$</span> - the proportional '
                'change in length of an object due to gravitational waves from a mass '
                '<span class=\"math-container\">$M$</span>:</p>\n\n'
                '<p><span class=\"math-container\">$$h \\approx {{GM} \\over c^2} \\times '
                '{1 \\over r} \\times {v^2 \\over c^2}$$</span></p>\n\n'
                '<p><a href=\"http://www.tapir.caltech.edu/~teviet/Waves/gwave.html\" '
                'rel=\"nofollow noreferrer\">(Source of formula)</a></p>\n\n<p>'
            ),
            (
                '<p>I think I can now answer my own question, having come across some decent '
                'references I hadn\'t found before asking it. I found the equation for the '
                'gravitational strain <span class=\"math-container\">$h$</span> - the proportional '
                'change in length of an object due to gravitational waves from a mass '
                '<span class=\"math-container\">$M$</span>:</p>\n\n'
                '<p><span class=\"math-container\">$$h \\approx {{GM} \\over c^2} \\times '
                '{1 \\over r} \\times {v^2 \\over c^2}$$</span></p>\n\n'
                '<p><a href=\"http://www.tapir.caltech.edu/~teviet/Waves/gwave.html\" '
                'rel=\"nofollow noreferrer\">(Source of formula)</a></p>\n\n<p>'
            )
        )
    ]
    raw_html = (
        '<head> '
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js'
        '?config=TeX-MML-AM_CHTML"> </script> '
        '</head> '
        '<ccmath type="mathml" by="mathjax">$$a^2 + b^2 = c^2$$</ccmath>'
        '<p>This is a test.</p> '
        '<span class=mathjax_display>$$a^2 + b^2 = c^2$$</span>'
    )
    print(math_recognizer.recognize(
        'https://www.baidu.com',
        test_html,
        raw_html
    ))
    # print(math_recognizer.to_content_list_node(
    #     'https://www.baidu.com',
    #     '<ccmath type="latex" by="mathjax">$u_{x_0}^{in}(x)$</ccmath>',
    #     raw_html
    # ))
    # print(math_recognizer.html_split_by_tags(
    #     raw_html,
    #     ['ccmath']
    # ))
