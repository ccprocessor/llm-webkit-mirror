import re
from typing import List, Tuple

from bs4 import BeautifulSoup
from overrides import override

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

    def contains_math(self, html: str) -> Tuple[bool, str]:
        """判断html中是否包含数学公式."""
        if self.contains_mathjax(html):  # 先认为mathjax公式就是latex公式
            return True, MATH_TYPE_MAP['LATEX']

        return False, None

    def is_cc_html(self, html: str) -> bool:
        """判断html片段是否是cc标签."""  # 这里需要判断是否包含自定义cc标签，应该需要一个全局通用方法
        return html.startswith('<cc')

    def process_ccmath_html(self, cc_html: str, o_html: str, math_type: str, math_render: str) -> List[Tuple[str, str]]:
        """处理数学公式，将外层标签修改为 ccmath.

        Args:
            cc_html: 处理后的HTML
            o_html: 原始HTML

        Returns:
            List[Tuple[str, str]]: 处理后的HTML对
        """
        soup = BeautifulSoup(cc_html, 'html.parser')
        content = soup.get_text(strip=True)

        # 确定数学公式的类型和处理器

        # 创建新的 ccmath 标签
        new_cc_html = f'<ccmath type="{math_type}" by="{math_render}">{content}</ccmath>'

        return [(new_cc_html, o_html)]

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
        soup = BeautifulSoup(html, 'html.parser')
        head = soup.head

        if head:
            # Check for MathJax
            mathjax_script = head.find('script', {'src': lambda x: x and 'mathjax' in x.lower()})
            if mathjax_script:
                return MATH_RENDER_MAP['MATHJAX']

            # Check for KaTeX
            katex_link = head.find('link', {'href': lambda x: x and 'katex' in x.lower()})
            if katex_link:
                return MATH_RENDER_MAP['KATEX']

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
