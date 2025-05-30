import re
from copy import deepcopy

from lxml.html import HtmlElement

from llm_web_kit.exception.exception import HtmlMathRecognizerException
from llm_web_kit.extractor.html.recognizer.cc_math.common import (CCMATH,
                                                                  MathType,
                                                                  text_strip)
from llm_web_kit.libs.html_utils import (build_cc_element, element_to_html,
                                         html_to_element, replace_element)


def modify_tree(cm: CCMATH, math_render: str, o_html: str, node: HtmlElement, parent: HtmlElement):
    """
    这段代码主要用于将 HTML 中的 MathML 数学公式节点，识别并替换为自定义的 cc 数学标签（如 <ccmath-interline>），以便后续结构化处理。
    其核心流程如下：
        1.查找 MathML节点中的 LaTeX 注释：优先查找 annotation 标签（application/x-tex），如果有则提取 LaTeX 公式。
        2.判断数学公式类型：通过 CCMATH.get_equation_type 判断公式类型（如行内/行间、LaTeX/MathML）。
        3.封装为 cc 标签：将提取到的公式内容用 wrap_math_md 包装，并用 build_cc_element 构造自定义 cc 标签节点，替换原有的 MathML 节点。
        4.兼容 alttext 属性：如果节点有 alttext 属性，也会优先用其内容。
        5.MathML 转 LaTeX：如果没有 LaTeX 注释，则尝试将 MathML 转为 LaTeX，再封装为 cc 标签。
        6.异常处理：如有异常，抛出自定义异常。
        这样做的目的是将原始 HTML 里的数学公式统一转换为项目自定义的结构化标签，便于后续内容抽取和处理。
    """
    try:
        annotation_tags = node.xpath('.//*[local-name()="annotation"][@encoding="application/x-tex"]')
        math_type = MathType.MATHML
        tag_math_type_list = cm.get_equation_type(o_html)
        if not tag_math_type_list:
            return
        new_tag = tag_math_type_list[0][0]
        math_type = tag_math_type_list[0][1]
        if len(annotation_tags) > 0:
            annotation_tag = annotation_tags[0]
            text = annotation_tag.text
            # wrapped_text = cm.wrap_math(r'{}'.format(text), display=display)
            style_value = parent.get('style')
            if style_value:
                normalized_style_value = style_value.lower().strip().replace(' ', '').replace(';', '')
                if 'display: none' in normalized_style_value:
                    parent.style = ''
            text = cm.wrap_math_md(text)
            if text:
                new_span = build_cc_element(html_tag_name=new_tag, text=text, tail=text_strip(node.tail), type=math_type, by=math_render, html=o_html)
                replace_element(node, new_span)
        elif text_strip(node.get('alttext')):
            # Get the alttext attribute
            text = node.get('alttext')
            text = cm.wrap_math_md(text)
            if text:
                new_span = build_cc_element(html_tag_name=new_tag, text=text, tail=text_strip(node.tail), type=math_type, by=math_render, html=o_html)
                replace_element(node, new_span)
        else:
            # Try translating to LaTeX
            tmp_node = deepcopy(node)
            tmp_node.tail = None
            mathml = element_to_html(tmp_node)

            if 'xmlns:' in mathml or re.search(r'<\w+:', mathml):
                mathml = re.sub(r'xmlns:\w+="([^"]*)"', r'xmlns="\1"', mathml)  # remove any xmlns:prefix
                mathml = re.sub(r'<(\w+):', '<', mathml)  # remove any prefix:mi
                mathml = re.sub(r'</(\w+):', '</', mathml)  # remove any /prefix:mi
                mathml = re.sub(r'([^\s])\s+([^\s])', r'\1 \2', mathml)  # remove extra spaces

            # print("Before mml_to_latex:", mathml)
            latex = cm.mml_to_latex(mathml)
            # print("After mml_to_latex:", latex)
            text = cm.wrap_math_md(latex)
            if text:
                # Set the html of the new span tag to the text
                new_span = build_cc_element(html_tag_name=new_tag, text=text, tail=text_strip(node.tail), type=math_type, by=math_render, html=o_html)
                replace_element(node, new_span)
    except Exception as e:
        raise HtmlMathRecognizerException(f'Error processing math tag: {e}')


if __name__ == '__main__':
    html = '<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>a</mi><mo>&#x2260;</mo><mn>0</mn></math>'
    element = html_to_element(html)
    cm = CCMATH()
    modify_tree(cm, 'mathjax', html, element, element)