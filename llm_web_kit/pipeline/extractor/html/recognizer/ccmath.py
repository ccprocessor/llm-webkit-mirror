import html
import re
from typing import List, Tuple

import lxml.etree
from bs4 import BeautifulSoup
from lxml.etree import Element
from overrides import override
from py_asciimath.translator.translator import ASCIIMath2Tex

from llm_web_kit.libs.logger import logger
from llm_web_kit.pipeline.extractor.html.magic_html.utils import (iter_node,
                                                                  load_html)
from llm_web_kit.pipeline.extractor.html.recognizer.common import text_strip
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
    'ASCIIMATH': 'AsciiMath',
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
    def to_content_list_node(self, content: str) -> dict:
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
        tree = load_html(content)
        if tree is None:
            raise ValueError(f'Failed to load html: {content}')

        if tree.tag != 'ccmath':
            raise ValueError(f'No ccmath element found in content: {content}')
        else:
            # 获取math_content
            math_content = tree.text  # TODO: 需要处理math_content两边的$符号
            math_type = tree.get('type')
            math_render = tree.get('by')
            equation_type = self.get_equation_type(math_content)

            result = {
                'type': equation_type,
                'raw_content': content,
                'content': {
                    'math_content': math_content,
                    'math_type': math_type,
                    'by': math_render
                }
            }
        return result

    def contains_math(self, html: str) -> Tuple[bool, str]:
        """判断html中是否包含数学公式."""
        if self.contains_mathjax(html):  # 先认为mathjax公式就是latex公式
            return True, MATH_TYPE_MAP['LATEX']

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
            # 如果节点是span标签，并且class属性包含mathjax，MathJax，mathjax_display，MathJax_Display等
            if (node.tag == 'span' and node.get('class') and
               any('mathjax' in cls.lower() for cls in node.get('class').split())):
                parent = node.getparent()

                try:
                    # Get the inner text of the mathjax tag
                    text = node.text
                    if text_strip(text):
                        text = html.unescape(text)
                        # Create a new ccmath tag
                        new_cc_html = Element('ccmath')
                        new_cc_html.text = text
                        new_cc_html.set('type', math_type)
                        new_cc_html.set('by', math_render)
                        # Then, we need to replace the mathjax tag with the new span tag
                        if parent is not None:
                            if text_strip(node.tail):
                                new_cc_html.tail = node.tail
                                parent.replace(node, new_cc_html)
                    else:
                        logger.info(f'Processing mathjax tag: {node.text}')
                        new_cc_html = node
                except Exception as e:
                    logger.error(f'Error processing mathjax tag: {e}')

        return [(lxml.etree.tostring(new_cc_html, encoding='unicode'), o_html)]

    # def contains_mathml(self, html: str) -> bool:
    #     """检查html中是否包含mathml标签."""
    #     soup = BeautifulSoup(html, 'html.parser')
    #     return bool(soup.find("math") and soup.find("math").get_text(strip=True))

    # def contains_latex(self, html: str) -> bool:
    #     """检查html中是否包含latex公式."""
    #     return bool(re.search(r'\$.*\$', html)) or \
    #         bool(re.search(r'\\(.*\\)', html))

    def contains_mathjax(self, html: str) -> bool:
        """检查html中是否包含mathjax公式.
        示例:
            <span class="MathJax">x^2 + y^2 = z^2</span>
            <div class="MathJax_Display">E = mc^2</div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        mathjax_pattern = re.compile(r'mathjax', re.IGNORECASE)
        display_pattern = re.compile(r'mathjax_display', re.IGNORECASE)
        mathjax_tags = (
            soup.find_all('span', {'class': mathjax_pattern}) +
            soup.find_all('div', {'class': display_pattern})
        )
        for tag in mathjax_tags:
            if tag.get_text(strip=True):  # 如果标签内有非空文本内容，则认为包含mathjax公式
                return True
        return False

    def contains_katex(self, html: str) -> bool:
        """检查html中是否包含katex公式."""
        soup = BeautifulSoup(html, 'html.parser')
        katex_pattern = re.compile(r'katex', re.IGNORECASE)
        katex_display = re.compile(r'katex_display', re.IGNORECASE)
        katex_tags = (
            soup.find_all('span', {'class': katex_pattern}) +
            soup.find_all('span', {'class': katex_display})
        )
        for tag in katex_tags:
            if tag.get_text(strip=True):
                return True
        return False

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
    test_html = [(
        '<span class=mathjax>Some text with a formula $$x = 5$$ in it.</span>',
        '<span class=mathjax>Some text with a formula $$x = 5$$ in it.</span>'
    )]
    raw_html = (
        '<head> '
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js'
        '?config=TeX-MML-AM_CHTML"> </script> '
        '</head> '
        '<p>This is a test.</p> '
        '<span class=mathjax_display>$$a^2 + b^2 = c^2$$</span>'
    )
    print(math_recognizer.recognize(
        'https://www.baidu.com',
        test_html,
        raw_html
    ))
    print(math_recognizer.to_content_list_node(
        '<ccmath type="latex" by="mathjax">$u_{x_0}^{in}(x)$</ccmath>'
    ))
