import re
from abc import abstractmethod
from typing import Any, Dict, List

from lxml.html import HtmlElement

from llm_web_kit.extractor.html.recognizer.cc_math.common import MathType
from llm_web_kit.extractor.html.recognizer.recognizer import CCTag
from llm_web_kit.libs.html_utils import (build_cc_element, element_to_html,
                                         html_to_element)


class MathRenderType:
    """数学公式渲染器类型."""
    MATHJAX = 'mathjax'
    KATEX = 'katex'


MATHJAX_OPTIONS = {
    'inlineMath': [['\\(', '\\)']],
    'displayMath': [['$$', '$$'], ['\\[', '\\]']],
    'processEscapes': True,
    'processEnvironments': True,
    'processRefs': True,
    'skipTags': ['script', 'noscript', 'style', 'textarea', 'pre', 'code'],
        'ignoreClass': 'tex2jax_ignore',
        'processClass': 'tex2jax_process',
        'elements': ['body']
}


class BaseMathRender():
    """数学公式渲染器基类.

    提供了识别和处理不同类型数学公式渲染器的基本功能。 子类需要实现特定渲染器的选项解析和处理逻辑。
    """

    def __init__(self):
        """初始化渲染器基类."""
        self.options = {}
        self.render_type = None

    @abstractmethod
    def get_options(self, tree: HtmlElement) -> Dict[str, Any]:
        """从HTML中提取渲染器选项.

        Args:
            tree: 包含渲染器配置的HTML树

        Returns:
            Dict[str, Any]: 渲染器选项字典
        """
        pass

    @abstractmethod
    def is_customized_options(self) -> bool:
        """是否与默认配置不同."""
        pass

    def find_math(self, root: HtmlElement) -> None:
        """遍历HTML根节点查找数学公式，并创建相应的数学公式节点.

        Args:
            root: HTML根节点
        """
        pass

    def get_math_render(self, html: str) -> 'BaseMathRender':
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
                render = KaTeXRender()
                render.get_options(link)
                return render
        # 查找head标签
        # head = tree.find('head')
        # if head is not None:
        # 检查 MathJax
        for script in tree.iter('script'):
            src = script.get('src', '').lower()
            if src and ('mathjax' in src or 'asciimath' in src):
                render = MathJaxRender()
                render.get_options(script)
                return render
        return None

    def _process_text_nodes(
        self,
        element: HtmlElement,
        inline_delimiters: List[List[str]],
        display_delimiters: List[List[str]]
    ) -> None:
        """处理元素中的文本节点，查找并替换数学公式.

        Args:
            element: 当前元素
            inline_delimiters: 行内公式分隔符列表
            display_delimiters: 行间公式分隔符列表
        """
        if element is None:
            return

        # 跳过特定标签
        skip_tags = MATHJAX_OPTIONS.get(
            'skipTags',
            ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
        )
        if element.tag in skip_tags:
            return

        # 处理当前节点的文本
        if element.text:
            # 处理行间公式（优先处理，因为可能包含行内公式）
            for start, end in display_delimiters:
                element.text = self._replace_math(
                    element, element.text, start, end, True
                )

            # 处理行内公式
            for start, end in inline_delimiters:
                element.text = self._replace_math(
                    element, element.text, start, end, False
                )

        # 递归处理子节点
        for child in list(element):  # 创建副本以避免迭代时修改
            self._process_text_nodes(
                child, inline_delimiters, display_delimiters
            )

            # 处理尾部文本
            if child.tail:
                # 处理行间公式
                for start, end in display_delimiters:
                    child.tail = self._replace_math(
                        element, child.tail, start, end, True, child
                    )

                # 处理行内公式
                for start, end in inline_delimiters:
                    child.tail = self._replace_math(
                        element, child.tail, start, end, False, child
                    )

    def _replace_math(
        self,
        parent: HtmlElement,
        text: str,
        start: str,
        end: str,
        is_display: bool,
        previous_sibling: HtmlElement = None
    ) -> str:
        """替换文本中的数学公式为相应的节点.

        Args:
            parent: 父节点
            text: 文本内容
            start: 起始分隔符
            end: 结束分隔符
            is_display: 是否为行间公式
            previous_sibling: 前一个兄弟节点，用于处理tail文本

        Returns:
            str: 处理后的文本
        """
        if not text or not start or not end:
            return text

        # 转义正则表达式特殊字符
        start_pattern = re.escape(start)
        end_pattern = re.escape(end)

        # 构建正则表达式
        pattern = f'{start_pattern}(.*?){end_pattern}'

        # 查找所有匹配
        matches = list(re.finditer(pattern, text, re.DOTALL))

        # 如果没有匹配，直接返回原文本
        if not matches:
            return text

        # 从后向前处理，以避免位置偏移
        result = text

        # 如果是处理text，需要创建一个新的文本节点列表
        if previous_sibling is None:
            # 处理element.text的情况
            # 创建一个列表来存储所有的节点和文本片段
            nodes = []
            last_end = 0

            for match in matches:
                formula = match.group(1)
                if not formula:
                    continue

                # 获取公式前的文本
                start_pos = match.start()
                end_pos = match.end()

                # 添加公式前的文本
                if start_pos > last_end:
                    prefix = result[last_end:start_pos]
                    if prefix:
                        nodes.append(prefix)

                # 创建数学公式节点
                tag_name = CCTag.CC_MATH_INTERLINE if is_display else CCTag.CC_MATH_INLINE

                # 使用build_cc_element创建节点
                math_node = build_cc_element(
                    html_tag_name=tag_name,
                    text=formula,
                    tail='',
                    type=MathType.LATEX,
                    by=self.render_type,
                    html=f'{start}{formula}{end}'  # 使用完整的原始HTML
                )

                # 添加公式节点
                nodes.append(math_node)

                # 更新last_end
                last_end = end_pos

            # 添加最后一段文本
            if last_end < len(result):
                suffix = result[last_end:]
                if suffix:
                    nodes.append(suffix)

            # 如果没有节点，直接返回原文本
            if not nodes:
                return text

            # 设置parent.text为第一个节点前的文本
            if isinstance(nodes[0], str):
                parent.text = nodes[0]
                nodes.pop(0)
            else:
                parent.text = ''

            # 添加剩余的节点
            for i, node in enumerate(nodes):
                if isinstance(node, str):
                    # 如果是文本，设置为前一个节点的tail
                    if i > 0 and not isinstance(nodes[i - 1], str):
                        nodes[i - 1].tail = node
                    else:
                        # 如果前一个也是文本，或者是第一个节点，创建一个空节点
                        empty_node = HtmlElement()
                        empty_node.tag = 'span'
                        empty_node.tail = node
                        parent.append(empty_node)
                else:
                    # 如果是节点，直接添加
                    parent.append(node)

            # 返回空字符串，因为已经处理完所有文本
            return ''
        else:
            # 处理element.tail的情况
            # 创建一个列表来存储所有的节点和文本片段
            nodes = []
            last_end = 0

            for match in matches:
                formula = match.group(1)
                if not formula:
                    continue

                # 获取公式前的文本
                start_pos = match.start()
                end_pos = match.end()

                # 添加公式前的文本
                if start_pos > last_end:
                    prefix = result[last_end:start_pos]
                    if prefix:
                        nodes.append(prefix)

                # 创建数学公式节点
                tag_name = CCTag.CC_MATH_INTERLINE if is_display else CCTag.CC_MATH_INLINE

                # 使用build_cc_element创建节点
                math_node = build_cc_element(
                    html_tag_name=tag_name,
                    text=formula,
                    tail='',
                    type=MathType.LATEX,
                    by=self.render_type,
                    html=f'{start}{formula}{end}'  # 使用完整的原始HTML
                )

                # 添加公式节点
                nodes.append(math_node)

                # 更新last_end
                last_end = end_pos

            # 添加最后一段文本
            if last_end < len(result):
                suffix = result[last_end:]
                if suffix:
                    nodes.append(suffix)

            # 如果没有节点，直接返回原文本
            if not nodes:
                return text

            # 设置previous_sibling.tail为第一个节点前的文本
            if isinstance(nodes[0], str):
                previous_sibling.tail = nodes[0]
                nodes.pop(0)
            else:
                previous_sibling.tail = ''

            # 获取previous_sibling在parent中的索引
            parent_index = list(parent).index(previous_sibling)

            # 添加剩余的节点
            for i, node in enumerate(nodes):
                if isinstance(node, str):
                    # 如果是文本，设置为前一个节点的tail
                    if i > 0 and not isinstance(nodes[i - 1], str):
                        nodes[i - 1].tail = node
                    else:
                        # 如果前一个也是文本，或者是第一个节点，创建一个空节点
                        empty_node = HtmlElement()
                        empty_node.tag = 'span'
                        empty_node.tail = node
                        parent.insert(parent_index + 1, empty_node)
                        parent_index += 1
                else:
                    # 如果是节点，直接添加
                    parent.insert(parent_index + 1, node)
                    parent_index += 1

            # 返回空字符串，因为已经处理完所有文本
            return ''

    @staticmethod
    def detect_render_type(tree: HtmlElement) -> str:
        """检测HTML中使用的数学公式渲染器类型.

        Args:
            tree: HTML元素树

        Returns:
            str: 渲染器类型，如果未检测到则返回None
        """
        if tree is None:
            return None

        # 检查 KaTeX
        for link in tree.iter('link'):
            if link.get('href') and 'katex' in link.get('href', '').lower():
                return MathRenderType.KATEX

        # 检查 MathJax
        for script in tree.iter('script'):
            src = script.get('src', '').lower()
            if src and ('mathjax' in src or 'asciimath' in src):
                return MathRenderType.MATHJAX

        return None

    @staticmethod
    def create_render(tree: HtmlElement) -> 'BaseMathRender':
        """根据HTML创建合适的渲染器实例.

        Args:
            tree: HTML元素树

        Returns:
            BaseMathRender: 渲染器实例，如果未检测到则返回None
        """
        render_type = BaseMathRender.detect_render_type(tree)

        if render_type == MathRenderType.KATEX:
            return KaTeXRender()

        return MathJaxRender()


class MathJaxRender(BaseMathRender):
    """MathJax渲染器实现."""

    def __init__(self):
        """初始化MathJax渲染器."""
        super().__init__()
        self.render_type = MathRenderType.MATHJAX
        self.options = {
            'inline_delimiters': [],
            'display_delimiters': [],
            'extensions': [],
            'config': '',
            'version': ''
        }

    def get_options(self, tree: HtmlElement) -> Dict[str, Any]:
        """从HTML中提取MathJax选项.

        Args:
            html: 包含MathJax配置的HTML字符串

        Returns:
            Dict[str, Any]: MathJax选项字典
        """
        if tree is None:
            return self.options

        # 查找MathJax配置脚本
        for script in tree.iter('script'):
            if script.get('type') == 'text/x-mathjax-config':
                self._parse_mathjax_config(script.text)

            # 检查MathJax版本
            src = script.get('src', '')
            if 'mathjax' in src.lower():
                self._parse_mathjax_version(src)

                # 检查配置参数
                if '?' in src:
                    config_part = src.split('?', 1)[1]
                    if 'config=' in config_part:
                        config = re.search(r'config=([^&]+)', config_part)
                        if config:
                            self.options['config'] = config.group(1)
        return self.options

    def _parse_mathjax_config(self, config_text: str) -> None:
        """解析MathJax配置脚本.

        Args:
            config_text: MathJax配置脚本内容
        """
        if not config_text:
            return

        # 提取行内公式分隔符
        inline_pattern = (
            r'inlineMath:\s*\['
            r'\s*(\[.*?\](?:\s*,\s*\[.*?\])*)\s*\]'
        )
        inline_match = re.search(inline_pattern, config_text, re.DOTALL)
        if inline_match:
            delimiters_str = inline_match.group(1)
            self.options['inline_delimiters'] = self._parse_delimiters(delimiters_str)

        # 提取行间公式分隔符
        display_pattern = (
            r'displayMath:\s*\['
            r'\s*(\[.*?\](?:\s*,\s*\[.*?\])*)\s*\]'
        )
        display_match = re.search(display_pattern, config_text, re.DOTALL)
        if display_match:
            delimiters_str = display_match.group(1)
            self.options['display_delimiters'] = self._parse_delimiters(delimiters_str)

        # 提取扩展
        extensions_pattern = (
            r'extensions:\s*\['
            r'\s*([\'"].*?[\'"](?:\s*,\s*[\'"].*?[\'"])*)\s*\]'
        )
        extensions_match = re.search(extensions_pattern, config_text, re.DOTALL)
        if extensions_match:
            extensions_str = extensions_match.group(1)
            self.options['extensions'] = [
                ext.strip('\'"')
                for ext in re.findall(r'[\'"].*?[\'"]', extensions_str)
            ]

    def _parse_mathjax_version(self, src: str) -> None:
        """解析MathJax版本.

        Args:
            src: MathJax脚本的src属性
        """
        version_match = re.search(r'mathjax/(\d+\.\d+\.\d+)', src, re.IGNORECASE)
        if version_match:
            self.options['version'] = version_match.group(1)
        elif 'latest.js' in src:
            self.options['version'] = 'latest'

    def _parse_delimiters(self, delimiters_str: str) -> List[List[str]]:
        """解析分隔符字符串.

        Args:
            delimiters_str: 分隔符字符串，如 "['$', '$'], ['\\\\(', '\\\\)']"

        Returns:
            List[List[str]]: 分隔符列表
        """
        delimiters = []
        # 匹配 ['x', 'y'] 形式的分隔符对
        pattern = r'\[\s*[\'"](.+?)[\'"]\s*,\s*[\'"](.+?)[\'"]\s*\]'
        for match in re.finditer(pattern, delimiters_str):
            start, end = match.groups()
            # 处理转义字符
            start = start.replace('\\\\', '\\')
            end = end.replace('\\\\', '\\')
            delimiters.append([start, end])
        return delimiters

    def is_customized_options(self) -> bool:
        """是否与默认配置不同."""
        # 如果options中inlineMath和displayMath为空，则认为没有自定义配置
        if self.options.get('inlineMath') and self.options.get('displayMath'):
            return False
        # 先只判断MATHJAX_OPTIONS的inlineMath和displayMath
        if self.options.get('inlineMath', []) != MATHJAX_OPTIONS['inlineMath']:
            return True
        if self.options.get('displayMath', []) != MATHJAX_OPTIONS['displayMath']:
            return True
        return False

    def find_math(self, root: HtmlElement) -> None:
        """查找MathJax格式的数学公式，并创建相应的数学公式节点.

        Args:
            root: HTML根节点
        """
        # 获取行内和行间公式分隔符
        inline_delimiters = self.options.get('inline_delimiters', [])
        if not inline_delimiters:
            # 使用默认分隔符
            inline_delimiters = MATHJAX_OPTIONS.get(
                'inlineMath', [['$', '$'], ['\\(', '\\)']]
            )

        display_delimiters = self.options.get('display_delimiters', [])
        if not display_delimiters:
            # 使用默认分隔符
            display_delimiters = MATHJAX_OPTIONS.get(
                'displayMath', [['$$', '$$'], ['\\[', '\\]']]
            )

        # 处理所有文本节点
        self._process_text_nodes(
            root, inline_delimiters, display_delimiters
        )


class KaTeXRender(BaseMathRender):
    """KaTeX渲染器实现."""

    def __init__(self):
        """初始化KaTeX渲染器."""
        super().__init__()
        self.render_type = MathRenderType.KATEX
        self.options = {
            'auto_render': False,
            'display_mode': False,
            'throw_on_error': True,
            'error_color': '#cc0000',
            'version': '',
            'delimiters': []
        }

    def get_options(self, tree: HtmlElement) -> Dict[str, Any]:
        """从HTML中提取KaTeX选项.

        Args:
            html: 包含KaTeX配置的HTML字符串

        Returns:
            Dict[str, Any]: KaTeX选项字典
        """
        if tree is None:
            return self.options

        # 查找KaTeX样式表，提取版本
        for link in tree.iter('link'):
            href = link.get('href', '')
            if 'katex' in href.lower():
                version_pattern = r'katex@(\d+\.\d+\.\d+)'
                version_match = re.search(version_pattern, href, re.IGNORECASE)
                if version_match:
                    self.options['version'] = version_match.group(1)

        # 查找KaTeX配置脚本
        for script in tree.iter('script'):
            script_text = script.text or ''
            if 'renderMathInElement' in script_text:
                self._parse_katex_config(script_text)

        return self.options

    def _parse_katex_config(self, config_text: str) -> None:
        """解析KaTeX配置脚本.

        Args:
            config_text: KaTeX配置脚本内容
        """
        if not config_text:
            return

        # 检查自动渲染
        if 'renderMathInElement' in config_text:
            self.options['auto_render'] = True

        # 提取显示模式
        display_pattern = r'displayMode\s*:\s*(true|false)'
        display_match = re.search(display_pattern, config_text, re.IGNORECASE)
        if display_match:
            self.options['display_mode'] = display_match.group(1).lower() == 'true'

        # 提取错误处理选项
        throw_pattern = r'throwOnError\s*:\s*(true|false)'
        throw_on_error_match = re.search(throw_pattern, config_text, re.IGNORECASE)
        if throw_on_error_match:
            self.options['throw_on_error'] = (
                throw_on_error_match.group(1).lower() == 'true'
            )

        # 提取错误颜色
        error_pattern = r'errorColor\s*:\s*[\'"](.+?)[\'"]'
        error_color_match = re.search(error_pattern, config_text)
        if error_color_match:
            self.options['error_color'] = error_color_match.group(1)

        # 提取分隔符
        delimiters_pattern = r'delimiters\s*:\s*\[(.*?)\]'
        delimiters_match = re.search(delimiters_pattern, config_text, re.DOTALL)
        if delimiters_match:
            delimiters_str = delimiters_match.group(1)
            self.options['delimiters'] = self._parse_delimiters(delimiters_str)

    def _parse_delimiters(self, delimiters_str: str) -> List[Dict[str, str]]:
        """解析KaTeX分隔符配置.

        Args:
            delimiters_str: 分隔符配置字符串

        Returns:
            List[Dict[str, str]]: 分隔符配置列表
        """
        delimiters = []
        # 匹配 {left: 'x', right: 'y', display: true/false} 形式的配置
        pattern = (
            r'\{\s*left\s*:\s*[\'"](.+?)[\'"]\s*,'
            r'\s*right\s*:\s*[\'"](.+?)[\'"]\s*'
            r'(?:,\s*display\s*:\s*(true|false))?\s*\}'
        )
        for match in re.finditer(pattern, delimiters_str):
            left, right, display = match.groups()
            delimiter = {
                'left': left.replace('\\\\', '\\'),
                'right': right.replace('\\\\', '\\')
            }
            if display:
                delimiter['display'] = display.lower() == 'true'
            delimiters.append(delimiter)
        return delimiters

    def is_customized_options(self) -> bool:
        """是否与默认配置不同."""
        return False

    def find_math(self, root: HtmlElement) -> None:
        """查找KaTeX格式的数学公式，并创建相应的数学公式节点.

        Args:
            root: HTML根节点
        """
        # 获取分隔符配置
        delimiters = self.options.get('delimiters', [])
        if not delimiters:
            # 使用常见的默认分隔符
            delimiters = [
                {'left': '$$', 'right': '$$', 'display': True},
                {'left': '$', 'right': '$', 'display': False},
                {'left': '\\(', 'right': '\\)', 'display': False},
                {'left': '\\[', 'right': '\\]', 'display': True}
            ]

        # 分离行内和行间分隔符
        inline_delimiters = []
        display_delimiters = []

        for delimiter in delimiters:
            start = delimiter.get('left', '')
            end = delimiter.get('right', '')
            is_display = delimiter.get('display', False)

            if start and end:
                if is_display:
                    display_delimiters.append([start, end])
                else:
                    inline_delimiters.append([start, end])

        # 处理所有文本节点
        self._process_text_nodes(
            root, inline_delimiters, display_delimiters
        )

        # 处理特殊的KaTeX元素
        for elem in root.xpath('.//*[@class="katex"]'):
            math_text = elem.get('data-katex-expression')
            if math_text:
                is_display = 'katex-display' in elem.get('class', '')
                tag_name = 'ccmath-interline' if is_display else 'ccmath-inline'

                # 创建新节点，使用build_cc_element
                math_node = build_cc_element(
                    html_tag_name=tag_name,
                    text=math_text,
                    tail=elem.tail or '',
                    type=MathType.LATEX,  # 使用MathType枚举
                    by=self.render_type,
                    html=element_to_html(elem)  # 使用完整的原始HTML
                )

                # 替换原节点
                parent = elem.getparent()
                if parent is not None:
                    parent.replace(elem, math_node)


# 使用示例
if __name__ == '__main__':
    # MathJax示例
    mathjax_html = '''
    <html>
    <head>
        <script type="text/x-mathjax-config">
            MathJax.Hub.Config({
                tex2jax: {
                    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
                },
                extensions: ["tex2jax.js", "TeX/AMSmath.js", "TeX/AMSsymbols.js"]
            });
        </script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/latest.js?config=TeX-MML-AM_CHTML"></script>
    </head>
    <body>
        <p>Inline math: $E=mc^2$</p>
        <p>Display math: $$F = G\\frac{m_1 m_2}{r^2}$$</p>
    </body>
    </html>
    '''

    # KaTeX示例
    katex_html = '''
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
                        {left: "\\\\(", right: "\\\\)", display: false},
                        {left: "\\\\[", right: "\\\\]", display: true}
                    ],
                    throwOnError: false,
                    errorColor: "#cc0000"
                });
            });
        </script>
    </head>
    <body>
        <p>Inline math: $E=mc^2$</p>
        <p>Display math: $$F = G\\frac{m_1 m_2}{r^2}$$</p>
    </body>
    </html>
    '''

    # 测试MathJax
    print('Testing MathJax detection:')
    mathjax_tree = html_to_element(mathjax_html)
    render_type = BaseMathRender.detect_render_type(mathjax_tree)
    print(f'Detected render type: {render_type}')

    render = BaseMathRender.create_render(mathjax_tree)
    if render:
        options = render.get_options(mathjax_tree)
        print(f'MathJax options: {options}')
    else:
        print('No renderer detected')

    print('\nTesting KaTeX detection:')
    katex_tree = html_to_element(katex_html)
    render_type = BaseMathRender.detect_render_type(katex_tree)
    print(f'Detected render type: {render_type}')

    render = BaseMathRender.create_render(katex_tree)
    if render:
        options = render.get_options(katex_tree)
        print(f'KaTeX options: {options}')
    else:
        print('No renderer detected')

    # 测试find_math方法
    print('\n测试find_math方法 - MathJax:')
    mathjax_html = open('bench/data/origin/math_physicsforums_1.html', 'r').read()
    mathjax_tree = html_to_element(mathjax_html)
    mathjax_render = BaseMathRender.create_render(mathjax_tree)
    print(f'mathjax_render options: {mathjax_render.get_options(mathjax_tree)}')
    if mathjax_render:
        # 处理前的HTML
        print('处理前的HTML:')
        print(element_to_html(mathjax_tree)[:500] + '...')

        # 使用find_math处理数学公式
        mathjax_render.find_math(mathjax_tree)

        # 处理后的HTML
        print('\n处理后的HTML:')
        processed_html = element_to_html(mathjax_tree)
        print(processed_html[:500] + '...')

        # 查找处理后的ccmath节点
        ccmath_nodes = mathjax_tree.xpath('.//*[self::ccmath-inline or self::ccmath-interline]')
        print(f'\n找到 {len(ccmath_nodes)} 个数学公式节点:')
        for i, node in enumerate(ccmath_nodes, 1):
            print(f"{i}. <{node.tag}> {node.text[:30]}{'...' if len(node.text) > 30 else ''}")

    # 测试[tex]...[/tex]格式的数学公式
    print('\n测试[tex]...[/tex]格式的数学公式:')
    tex_html = '''
    <html>
    <body>
        <p>where [tex]d^2(x_1,x_2)[/tex] is the squared distance between [tex]x_1[/tex] and [tex]x_2[/tex] in some metric space [tex]\\Theta[/tex]. All integrals are over [tex]\\Theta[/tex]</p>
    </body>
    </html>
    '''

    tex_tree = html_to_element(tex_html)
    mathjax_render = MathJaxRender()  # 直接创建MathJax渲染器，不需要检测

    # 处理前的HTML
    print('处理前的HTML:')
    print(element_to_html(tex_tree))

    # 使用find_math处理数学公式
    mathjax_render.find_math(tex_tree)

    # 处理后的HTML
    print('\n处理后的HTML:')
    processed_html = element_to_html(tex_tree)
    print(processed_html)

    # 查找处理后的ccmath节点
    ccmath_nodes = tex_tree.xpath('.//*[self::ccmath-inline or self::ccmath-interline]')
    print(f'\n找到 {len(ccmath_nodes)} 个数学公式节点:')
    for i, node in enumerate(ccmath_nodes, 1):
        print(f'{i}. <{node.tag}> {node.text}')

    # 测试真实文本
    print('\n测试真实文本:')
    real_text = '''
    <p>where [tex]d^2(x_1,x_2)[/tex] is the $a=b$ squared distance between [tex]x_1[/tex] and [tex]x_2[/tex] in some metric space [tex]\\Theta[/tex]. All integrals are over [tex]\\Theta[/tex]</p>
    '''

    real_tree = html_to_element(real_text)
    mathjax_render = MathJaxRender()

    # 处理前的HTML
    print('处理前的HTML:')
    print(element_to_html(real_tree))

    # 使用find_math处理数学公式
    mathjax_render.find_math(real_tree)

    # 处理后的HTML
    print('\n处理后的HTML:')
    processed_html = element_to_html(real_tree)
    print(processed_html)

    # 查找处理后的ccmath节点
    ccmath_nodes = real_tree.xpath('.//*[self::ccmath-inline or self::ccmath-interline]')
    print(f'\n找到 {len(ccmath_nodes)} 个数学公式节点:')
    for i, node in enumerate(ccmath_nodes, 1):
        print(f'{i}. <{node.tag}> {node.text}')

    # 测试$$格式的公式
    print('\n专门测试$$格式的公式:')
    dollar_text = '''
    <p>This is a display formula: $$F = G\\frac{m_1 m_2}{r^2}$$</p>
    '''

    dollar_tree = html_to_element(dollar_text)
    mathjax_render = MathJaxRender()

    # 处理前的HTML
    print('处理前的HTML:')
    print(element_to_html(dollar_tree))

    # 使用find_math处理数学公式
    mathjax_render.find_math(dollar_tree)

    # 处理后的HTML
    print('\n处理后的HTML:')
    processed_html = element_to_html(dollar_tree)
    print(processed_html)

    # 查找处理后的ccmath节点
    ccmath_nodes = dollar_tree.xpath('.//*[self::ccmath-inline or self::ccmath-interline]')
    print(f'\n找到 {len(ccmath_nodes)} 个数学公式节点:')
    for i, node in enumerate(ccmath_nodes, 1):
        print(f'{i}. <{node.tag}> {node.text}')
