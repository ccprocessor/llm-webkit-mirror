import re
from typing import Any, Dict, List

from llm_web_kit.extractor.html.recognizer.cc_math.render.render import (
    BaseMathRender, MathRenderType)
from llm_web_kit.libs.html_utils import (HtmlElement, element_to_html,
                                         html_to_element)

# 添加MATHJAX_OPTIONS变量定义
MATHJAX_OPTIONS = {
    'inlineMath': [['$', '$'], ['\\(', '\\)']],
    'displayMath': [['$$', '$$'], ['\\[', '\\]']],
    'processEscapes': True,
    'processEnvironments': True,
    'processRefs': True,
    'skipTags': ['script', 'noscript', 'style', 'textarea', 'pre', 'code'],
    'ignoreClass': 'tex2jax_ignore',
    'processClass': 'tex2jax_process',
    'elements': ['body']
}


class MathJaxRender(BaseMathRender):
    """MathJax渲染器实现."""

    def __init__(self):
        """初始化MathJax渲染器."""
        super().__init__()
        self.render_type = MathRenderType.MATHJAX
        self.options = {
            'inlineMath': [],
            'displayMath': [],
            'extensions': [],
            'config': '',
            'version': ''
        }

    def get_options(self, html: str) -> Dict[str, Any]:
        """从HTML中提取MathJax选项.

        Args:
            html: 包含MathJax配置的HTML字符串

        Returns:
            Dict[str, Any]: MathJax选项字典
        """
        tree = html_to_element(html)
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
            self.options['inlineMath'] = self._parse_delimiters(delimiters_str)

        # 提取行间公式分隔符
        display_pattern = (
            r'displayMath:\s*\['
            r'\s*(\[.*?\](?:\s*,\s*\[.*?\])*)\s*\]'
        )
        display_match = re.search(display_pattern, config_text, re.DOTALL)
        if display_match:
            delimiters_str = display_match.group(1)
            self.options['displayMath'] = self._parse_delimiters(delimiters_str)

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

    def _is_list_contained(self, list1: List[List[str]], list2: List[List[str]]) -> bool:
        """判断list1中的元素是否都被list2包含.

        Args:
            list1: 第一个列表
            list2: 第二个列表

        Returns:
            bool: 如果list1中的所有元素都被list2包含，则返回True，否则返回False
        """
        if not list1:
            return True

        # 将list2转换为集合，方便查找
        list2_set = {tuple(item) for item in list2}

        # 检查list1中的每个元素是否都在list2中
        for item in list1:
            if tuple(item) not in list2_set:
                return False

        return True

    def is_customized_options(self) -> bool:
        """是否与默认配置不同."""
        # 如果options中inlineMath和displayMath为空，则认为没有自定义配置
        if self.options.get('inlineMath') == [] and self.options.get('displayMath') == []:
            return False

        # 检查inlineMath是否被默认配置包含
        if not self._is_list_contained(
            self.options.get('inlineMath', []),
            MATHJAX_OPTIONS['inlineMath']
        ):
            return True

        # 检查displayMath是否被默认配置包含
        if not self._is_list_contained(
            self.options.get('displayMath', []),
            MATHJAX_OPTIONS['displayMath']
        ):
            return True

        return False

    def find_math(self, root: HtmlElement) -> None:
        """查找MathJax格式的数学公式，并创建相应的数学公式节点.

        Args:
            root: HTML根节点
        """
        # 获取行内和行间公式分隔符
        inline_delimiters = self.options.get('inlineMath', [])
        if not inline_delimiters:
            # 使用默认分隔符
            inline_delimiters = MATHJAX_OPTIONS.get(
                'inlineMath', [['$', '$'], ['\\(', '\\)']]
            )
        # 打印调试信息
        print(f'行内公式分隔符: {inline_delimiters}')

        display_delimiters = self.options.get('displayMath', [])
        if not display_delimiters:
            # 使用默认分隔符
            display_delimiters = MATHJAX_OPTIONS.get(
                'displayMath', [['$$', '$$'], ['\\[', '\\]']]
            )

        # 打印调试信息
        print(f'行间公式分隔符: {display_delimiters}')

        # 处理所有文本节点
        self._process_text_nodes(
            root, inline_delimiters, display_delimiters
        )


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

    # 测试MathJax
    print('Testing MathJax detection:')
    mathjax_tree = html_to_element(mathjax_html)
    render_type = BaseMathRender.detect_render_type(mathjax_tree)
    print(f'Detected render type: {render_type}')

    mathjax_render = BaseMathRender.create_render(mathjax_tree)
    if mathjax_render:
        options = mathjax_render.get_options(mathjax_html)
        print(f'MathJax options: {options}')
    else:
        print('No renderer detected')

    # 测试find_math方法
    print('\n测试find_math方法 - MathJax:')
    mathjax_html = open('bench/data/origin/math_physicsforums_1.html', 'r').read()
    mathjax_tree = html_to_element(mathjax_html)
    mathjax_render = BaseMathRender.create_render(mathjax_tree)
    print(f'mathjax_render options: {mathjax_render.get_options(mathjax_html)}')
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
