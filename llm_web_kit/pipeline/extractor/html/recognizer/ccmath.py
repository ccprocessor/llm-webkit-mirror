from typing import List, Tuple

from lxml import etree
from overrides import override

from llm_web_kit.pipeline.extractor.html.recognizer.cc_math import (
    tag_math, tag_span_mathcontainer, tag_span_mathjax)
from llm_web_kit.pipeline.extractor.html.recognizer.cc_math.common import (
    CCMATH, CCMATH_INLINE, CCMATH_INTERLINE, parse_html)
from llm_web_kit.pipeline.extractor.html.recognizer.recognizer import \
    BaseHTMLElementRecognizer

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
        for cc_html, o_html in main_html_lst:
            # 检查是否包含数学公式
            contains_math, math_type = cm.contains_math(cc_html)
            if contains_math and not self.is_cc_html(cc_html):
                # 获取数学公式渲染器
                math_render = cm.get_math_render(raw_html)
                result.extend(self.process_ccmath_html(cc_html, o_html, math_type, math_render))
            else:
                result.append((cc_html, o_html))

        return result

    @override
    def to_content_list_node(self, base_url: str, parsed_content: str, raw_html_segment:str) -> dict:
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
        # tree = parse_html(parsed_content)
        tree: etree._Element = etree.fromstring(parsed_content, None)
        if tree is None:
            raise ValueError(f'Failed to load html: {parsed_content}')

        if tree.tag == CCMATH_INTERLINE or tree.tag == CCMATH_INLINE:
            # 获取math_content
            math_content = tree.text  # TODO: 需要处理math_content两边的$符号

            result = {
                'type': cm.get_equation_type(math_content),
                'raw_content': raw_html_segment,
                'content': {
                    'math_content': tree.text,
                    'math_type': tree.get('type'),
                    'by': tree.get('by')
                }
            }
            return result
        else:
            raise ValueError(f'No ccmath element found in content: {parsed_content}')

    def process_ccmath_html(self, cc_html: str, o_html: str, math_type: str, math_render: str) -> List[Tuple[str, str]]:
        """处理数学公式，将外层标签修改为 ccmath.

        Args:
            cc_html: 处理后的HTML
            o_html: 原始HTML

        Returns:
            List[Tuple[str, str]]: 处理后的HTML对
        """
        # node是从cc_html中解析出来的lxml节点
        tree = parse_html(cc_html)
        if tree is None:
            raise ValueError(f'Failed to load html: {cc_html}')

        for node in tree.iter():
            assert isinstance(node, etree._Element)
            original_html = etree.tostring(node, encoding='utf-8', method='html').decode()
            parent = node.getparent()

            # TODO: 先保留原始latex格式不做格式替换
            # # 1. 文本中有\\begin{align} 或 \\begin{equation}
            # if node.tag not in ['script', 'style'] and text_strip(node.text):
            #     regex = r'\\begin{align}(.*?)\\end{align}'
            #     text = node.text
            #     matches = re.findall(regex, text, re.DOTALL)
            #     if matches:
            #         node.text = text.replace('\\begin{align}', '').replace('\\end{align}', '')

            # if node.tag not in ['script', 'style'] and text_strip(node.text):
            #     regex = r'\\begin{equation}(.*?)\\end{equation}'
            #     text = node.text
            #     matches = re.findall(regex, text, re.DOTALL)
            #     for match in matches:
            #         match = match.replace('\\begin{equation}', '')
            #         match = match.replace('\\end{equation}', '')
            #         wrapped_text = wrap_math(match, display=True)
            #         text = text.replace(match, wrapped_text)
            #     if matches:
            #         # Remove the \begin{equation} and \end{equation} tags
            #         text = text.replace('\\begin{equation}', '').replace('\\end{equation}', '')
            #         node.text = text

            # if node.tag not in ['script', 'style'] and text_strip(node.tail):
            #     regex = r'\\begin{align}(.*?)\\end{align}'
            #     text = node.tail
            #     matches = re.findall(regex, text, re.DOTALL)
            #     if matches:
            #         node.tail = text.replace('\\begin{align}', '').replace('\\end{align}', '')

            # if node.tag not in ['script', 'style'] and text_strip(node.tail):
            #     regex = r'\\begin{equation}(.*?)\\end{equation}'
            #     text = node.tail
            #     matches = re.findall(regex, text, re.DOTALL)
            #     for match in matches:
            #         match = match.replace('\\begin{equation}', '')
            #         match = match.replace('\\end{equation}', '')
            #         wrapped_text = wrap_math(match, display=True)
            #         text = text.replace(match, wrapped_text)
            #     if matches:
            #         # Remove the \begin{equation} and \end{equation} tags
            #         text = text.replace('\\begin{equation}', '').replace('\\end{equation}', '')
            #         node.tail = text

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

        return self.html_split_by_tags(etree.tostring(tree, encoding='utf-8', method='html').decode(), [CCMATH_INTERLINE])


if __name__ == '__main__':
    math_recognizer = MathRecognizer()
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
