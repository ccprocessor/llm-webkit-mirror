from abc import abstractmethod
from typing import Any, Dict

from lxml.html import HtmlElement

from llm_web_kit.exception.exception import \
    HtmlMathMathjaxRenderRecognizerException
from llm_web_kit.libs.html_utils import html_to_element


class MathRenderType:
    """数学公式渲染器类型."""
    MATHJAX = 'mathjax'
    MATHJAX_MOCK = 'mathjax_mock'  # 虚拟的mathjax渲染器
    MATHJAX_CUSTOMIZED = 'mathjax_customized'  # 临时增加这个type，未来区分走自定义解析的数据
    KATEX = 'katex'


class BaseMathRender():
    """数学公式渲染器基类.

    提供了识别和处理不同类型数学公式渲染器的基本功能。 子类需要实现特定渲染器的选项解析和处理逻辑。
    """

    def __init__(self):
        """初始化渲染器基类."""
        self.options = {}
        self.render_type = None
        self.url = ''  # 添加url属性的正确方式

    @abstractmethod
    def get_render_type(self) -> str:
        """获取渲染器类型."""
        return self.render_type

    @abstractmethod
    def get_options(self, html: str) -> Dict[str, Any]:
        """从HTML中提取渲染器选项.

        Args:
            html: 包含渲染器配置的HTML字符串

        Returns:
            Dict[str, Any]: 渲染器选项字典
        """
        return self.options

    @abstractmethod
    def is_customized_options(self) -> bool:
        """是否与默认配置不同."""
        return False

    def find_math(self, root: HtmlElement) -> None:
        """遍历HTML根节点查找数学公式，并创建相应的数学公式节点.

        Args:
            root: HTML根节点
        """
        pass

    def get_math_render(self, html: str) -> 'BaseMathRender':
        """获取数学公式渲染器.

        根据HTML内容检测使用的数学公式渲染器类型（MathJax或KaTeX）。

        Args:
            html: 包含可能的数学公式渲染器的HTML字符串

        Returns:
            BaseMathRender: 返回对应类型的渲染器实例。
                - 如果检测到KaTeX，返回KaTeXRender实例
                - 如果检测到MathJax，返回MathJaxRender实例
                - 如果未检测到任何渲染器或发生异常，返回BaseMathRender实例
                - 如果输入为None或空字符串，返回None

        示例:
            MathJax:
                <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/latest.js?config=TeX-MML-AM_CHTML"></script>
            KaTeX:
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/katex.min.css">
        """
        # 在方法内部导入，避免循环导入
        from llm_web_kit.extractor.html.recognizer.cc_math.render.katex import \
            KaTeXRender
        from llm_web_kit.extractor.html.recognizer.cc_math.render.mathjax import \
            MathJaxRender

        # 处理无效输入
        if html is None or not isinstance(html, str) or not html.strip():
            return None

        try:
            # 解析HTML
            tree = html_to_element(html)
            if tree is None:
                return None
            # 首先检查 KaTeX（优先级更高）
            katex_detected = False
            for link in tree.iter('link'):
                href = link.get('href', '').lower()
                if href and 'katex' in href:
                    katex_detected = True
                    break

            if not katex_detected:
                # 检查脚本中是否包含KaTeX关键字
                for script in tree.iter('script'):
                    src = script.get('src', '').lower()
                    if src and 'katex' in src:
                        katex_detected = True
                        break
                    # 检查脚本内容
                    if script.text and ('katex' in script.text.lower() or 'rendermathinelem' in script.text.lower()):
                        katex_detected = True
                        break

            if katex_detected:
                render = KaTeXRender()
                render.get_options(html)
                return render

            # 检查 MathJax
            mathjax_detected = False
            for script in tree.iter('script'):
                src = script.get('src', '').lower()
                if src and ('mathjax' in src or 'asciimath' in src):
                    mathjax_detected = True
                    break
                # 检查脚本内容
                if script.text and ('mathjax' in script.text.lower() or 'tex2jax' in script.text.lower()):
                    mathjax_detected = True
                    break

            if mathjax_detected:
                render = MathJaxRender()
                render.get_options(html)
                return render
            # 如果没有检测到任何渲染器，返回基础渲染器
            return BaseMathRender()

        except Exception as e:
            # 记录异常，但不抛出
            raise HtmlMathMathjaxRenderRecognizerException(f'获取数学公式渲染器失败: {e}')

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

        return BaseMathRender()
