from typing import List, Tuple

from lxml.html import HtmlElement
from overrides import override

from llm_web_kit.libs.doc_element_type import DocElementType
from llm_web_kit.libs.html_utils import element_to_html
from llm_web_kit.pipeline.extractor.html.recognizer.cc_math import (
    tag_math, tag_span_mathcontainer, tag_span_mathjax)
from llm_web_kit.pipeline.extractor.html.recognizer.cc_math.common import \
    CCMATH
from llm_web_kit.pipeline.extractor.html.recognizer.recognizer import (
    BaseHTMLElementRecognizer, CCTag)

cm = CCMATH()


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
        """
        result = []
        # 获取数学公式渲染器
        math_render = cm.get_math_render(raw_html)
        for cc_html, o_html in main_html_lst:
            if not self.is_cc_html(cc_html):
                result.extend(self.process_ccmath_html(cc_html, o_html, math_render))
            else:
                result.append((cc_html, o_html))

        return result

    @override
    def to_content_list_node(self, base_url: str, parsed_content: str, raw_html_segment: str) -> dict:
        """将content转换成content_list_node.
        每种类型的html元素都有自己的content-list格式：参考 docs/specification/output_format/content_list_spec.md
        例如代码的返回格式：
        ```json
            {
                "type": "equation-inline", # 数学公式类型，一共equation-inline和equation-interline两种
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
        tree = self._build_html_tree(parsed_content)
        if tree is None:
            raise ValueError(f'Failed to load html: {parsed_content}')

        inter_ele = tree.xpath(f'//{CCTag.CC_MATH_INTERLINE}')
        in_els = tree.xpath(f'//{CCTag.CC_MATH_INLINE}')
        if len(inter_ele) > 0:
            # 获取math_content
            math_content = inter_ele[0].text  # TODO: 需要处理math_content两边的$符号

            return {
                'type': DocElementType.EQUATION_INTERLINE,
                'raw_content': raw_html_segment,
                'content': {
                    'math_content': math_content,
                    'math_type': inter_ele[0].get('type'),
                    'by': inter_ele[0].get('by')
                }
            }
        elif len(in_els) > 0:
            math_content = in_els[0].text  # TODO: 需要处理math_content两边的$符号

            return {
                'type': DocElementType.EQUATION_INLINE,
                'raw_content': raw_html_segment,
                'content': {
                    'math_content': math_content,
                    'math_type': in_els[0].get('type'),
                    'by': in_els[0].get('by')
                }
            }
        else:
            raise ValueError(f'No ccmath element found in content: {parsed_content}')

    def process_ccmath_html(self, cc_html: str, o_html: str, math_render: str) -> List[Tuple[str, str]]:
        """处理数学公式，将外层标签修改为 ccmath.

        Args:
            cc_html: 处理后的HTML
            o_html: 原始HTML

        Returns:
            List[Tuple[str, str]]: 处理后的HTML对
        """
        # node是从cc_html中解析出来的lxml节点
        tree = self._build_html_tree(cc_html)
        if tree is None:
            raise ValueError(f'Failed to load html: {cc_html}')

        # 打印遍历node次数
        # count = 0
        for node in tree.iter():
            assert isinstance(node, HtmlElement)
            original_html = element_to_html(node)
            parent = node.getparent()
            # 3. img中的latex
            if node.tag == 'img':
                pass

            # 4. class 为 math-container，默认为latex
            if node.tag == 'span' and node.get('class') and 'math-container' in node.get('class'):
                tag_span_mathcontainer.modify_tree(cm, math_render, original_html, node, parent)

            # 5. class 为 wp-katex-eq
            if node.tag == 'span' and node.get('class') and 'wp-katex-eq' in node.get('class'):
                pass

            # 6. script[type="math/tex"]
            if node.tag == 'script' and node.get('type') and 'math/tex' in node.get('type'):
                pass

            # 7. script[type="math/asciimath"]
            if node.tag == 'script' and node.get('type') and 'math/asciimath' in node.get('type'):
                pass

            # 8. class tex
            if node.tag == 'span' and node.get('class') and 'tex' in node.get('class'):
                pass

            # 9. span.katex
            if node.tag == 'span' and node.get('class') and 'katex' in node.get('class'):
                pass

            # 10. class 为 x-ck12-mathEditor
            if node.tag == 'span' and node.get('class') and 'x-ck12-mathEditor' in node.get('class'):
                pass

            # 11. Remove any .MathJax_Preview spans
            if node.tag == 'span' and node.get('class') and 'MathJax_Preview' in node.get('class'):
                self.remove_node(node)

            # 12. math tags
            if node.tag == 'math':
                tag_math.modify_tree(cm, math_render, original_html, node, parent)

            # 13. class 为 mathjax
            if (node.tag == 'span' and node.get('class') and
               any('mathjax' in cls.lower() for cls in node.get('class').split())):
                tag_span_mathjax.modify_tree(cm, math_render, original_html, node, parent)

        return self.html_split_by_tags(element_to_html(tree), [CCTag.CC_MATH_INTERLINE])


if __name__ == '__main__':
    math_recognizer = MathRecognizer()
    test_html = [
        (
            ('<p>这是p的text<span class="mathjax_display">'
                '$$a^2 + b^2 = c^2$$</span>这是span的tail<b>这是b的text</b>'
                '这是b的tail</p>'),
            ('<p>这是p的text<span class="mathjax_display">'
                '$$a^2 + b^2 = c^2$$</span>这是span的tail<b>这是b的text</b>'
                '这是b的tail</p>')
        )
    ]
    raw_html = (
        '<head> '
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js'
        '?config=TeX-MML-AM_CHTML"> </script> '
        '</head> '
        '<p>这是p的text<span class="mathjax_display">$$a^2 + b^2 = c^2$$</span>这是span的tail<b>这是b的text</b>这是b的tail</p>'
    )
    print(math_recognizer.recognize(
        'https://www.baidu.com',
        test_html,
        raw_html
    ))
    # print(math_recognizer.to_content_list_node(
    #     'https://www.baidu.com',
    #     '<ccmath-interline type="latex" by="mathjax">$u_{x_0}^{in}(x)$</ccmath-interline>',
    #     # raw_html,
    #     raw_html
    # ))
    # print(math_recognizer.html_split_by_tags(
    #     raw_html,
    #     ['ccmath']
    # ))
