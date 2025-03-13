import re
from abc import abstractmethod
from typing import Any, Dict, List

from lxml.html import HtmlElement

from llm_web_kit.extractor.html.recognizer.cc_math.common import MathType
from llm_web_kit.extractor.html.recognizer.recognizer import CCTag
from llm_web_kit.libs.html_utils import build_cc_element, html_to_element


class MathRenderType:
    """数学公式渲染器类型."""
    MATHJAX = 'mathjax'
    KATEX = 'katex'


class BaseMathRender():
    """数学公式渲染器基类.

    提供了识别和处理不同类型数学公式渲染器的基本功能。 子类需要实现特定渲染器的选项解析和处理逻辑。
    """

    def __init__(self):
        """初始化渲染器基类."""
        self.options = {}
        self.render_type = None

    @abstractmethod
    def get_options(self, html: str) -> Dict[str, Any]:
        """从HTML中提取渲染器选项.

        Args:
            html: 包含渲染器配置的HTML字符串

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
        # 在方法内部导入，避免循环导入
        from llm_web_kit.extractor.html.recognizer.cc_math.render.katex import \
            KaTeXRender
        from llm_web_kit.extractor.html.recognizer.cc_math.render.mathjax import \
            MathJaxRender

        tree = html_to_element(html)
        if tree is None:
            return None
        # 检查 KaTeX
        for link in tree.iter('link'):
            if link.get('href') and 'katex' in link.get('href', '').lower():
                render = KaTeXRender()
                render.get_options(html)
                return render
        # 查找head标签
        # head = tree.find('head')
        # if head is not None:
        # 检查 MathJax
        for script in tree.iter('script'):
            src = script.get('src', '').lower()
            if src and ('mathjax' in src or 'asciimath' in src):
                render = MathJaxRender()
                render.get_options(html)
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
        skip_tags = ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
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

        # 打印原始分隔符
        print(f"原始分隔符: start='{start}', end='{end}'")

        # 转义正则表达式特殊字符
        start_pattern = re.escape(start)
        end_pattern = re.escape(end)

        # 打印转义后的分隔符
        print(f"转义后分隔符: start_pattern='{start_pattern}', end_pattern='{end_pattern}'")

        # 构建正则表达式
        pattern = f'{start_pattern}(.*?){end_pattern}'

        # 打印调试信息
        print(f"正则表达式模式: '{pattern}'")
        print(f"文本内容: '{text}'")

        # 查找所有匹配
        matches = list(re.finditer(pattern, text, re.DOTALL))

        # 打印匹配结果
        print(f'找到 {len(matches)} 个匹配')
        for i, match in enumerate(matches):
            print(f"匹配 {i+1}: 位置={match.start()}-{match.end()}, 内容='{match.group(0)}', 公式='{match.group(1)}'")

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
                        print(f"添加前缀文本: '{prefix}'")

                # 创建数学公式节点
                tag_name = CCTag.CC_MATH_INTERLINE if is_display else CCTag.CC_MATH_INLINE
                print(f'创建公式节点: <{tag_name}>{formula}</{tag_name}>')

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
                    print(f"添加后缀文本: '{suffix}'")

            # 如果没有节点，直接返回原文本
            if not nodes:
                return text

            # 设置parent.text为第一个节点前的文本
            if isinstance(nodes[0], str):
                parent.text = nodes[0]
                print(f"设置parent.text = '{nodes[0]}'")
                nodes.pop(0)
            else:
                parent.text = ''
                print("设置parent.text = ''")

            # 添加剩余的节点
            for i, node in enumerate(nodes):
                if isinstance(node, str):
                    # 如果是文本，设置为前一个节点的tail
                    if i > 0 and not isinstance(nodes[i - 1], str):
                        nodes[i - 1].tail = node
                        print(f"设置nodes[{i-1}].tail = '{node}'")
                    else:
                        # 如果前一个也是文本，或者是第一个节点，创建一个空节点
                        empty_node = HtmlElement()
                        empty_node.tag = 'span'
                        empty_node.tail = node
                        print(f"创建空节点，设置tail = '{node}'")
                        parent.append(empty_node)
                else:
                    # 如果是节点，直接添加
                    print(f'添加节点: <{node.tag}>')
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
                        print(f"添加前缀文本(tail): '{prefix}'")

                # 创建数学公式节点
                tag_name = CCTag.CC_MATH_INTERLINE if is_display else CCTag.CC_MATH_INLINE
                print(f'创建公式节点(tail): <{tag_name}>{formula}</{tag_name}>')

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
                    print(f"添加后缀文本(tail): '{suffix}'")

            # 如果没有节点，直接返回原文本
            if not nodes:
                return text

            # 设置previous_sibling.tail为第一个节点前的文本
            if isinstance(nodes[0], str):
                previous_sibling.tail = nodes[0]
                print(f"设置previous_sibling.tail = '{nodes[0]}'")
                nodes.pop(0)
            else:
                previous_sibling.tail = ''
                print("设置previous_sibling.tail = ''")

            # 获取previous_sibling在parent中的索引
            parent_index = list(parent).index(previous_sibling)

            # 添加剩余的节点
            for i, node in enumerate(nodes):
                if isinstance(node, str):
                    # 如果是文本，设置为前一个节点的tail
                    if i > 0 and not isinstance(nodes[i - 1], str):
                        nodes[i - 1].tail = node
                        print(f"设置nodes[{i-1}].tail(tail) = '{node}'")
                    else:
                        # 如果前一个也是文本，或者是第一个节点，创建一个空节点
                        empty_node = HtmlElement()
                        empty_node.tag = 'span'
                        empty_node.tail = node
                        print(f"创建空节点(tail)，设置tail = '{node}'")
                        parent.insert(parent_index + 1, empty_node)
                        parent_index += 1
                else:
                    # 如果是节点，直接添加
                    print(f'添加节点(tail): <{node.tag}>')
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
        # 在方法内部导入，避免循环导入
        from llm_web_kit.extractor.html.recognizer.cc_math.render.katex import \
            KaTeXRender
        from llm_web_kit.extractor.html.recognizer.cc_math.render.mathjax import \
            MathJaxRender

        render_type = BaseMathRender.detect_render_type(tree)

        if render_type == MathRenderType.MATHJAX:
            return MathJaxRender()
        elif render_type == MathRenderType.KATEX:
            return KaTeXRender()

        return None
