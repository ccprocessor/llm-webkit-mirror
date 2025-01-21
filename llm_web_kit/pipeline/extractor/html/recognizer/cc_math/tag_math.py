import re
from copy import deepcopy

from lxml.html import HtmlElement

from llm_web_kit.exception.exception import HtmlMathRecognizerExp
from llm_web_kit.libs.html_utils import (build_cc_element, element_to_html,
                                         html_to_element, replace_element)
from llm_web_kit.pipeline.extractor.html.recognizer.cc_math.common import (
    CCMATH, CCMATH_INLINE, CCMATH_INTERLINE, EQUATION_INLINE,
    EQUATION_INTERLINE, MathType, text_strip)


def modify_tree(cm: CCMATH, math_render: str, o_html: str, node: HtmlElement, parent: HtmlElement):
    try:
        annotation_tags = node.xpath('.//annotation[@encoding="application/x-tex"]')
        math_type = MathType.MATHML
        equation_type, math_type = cm.get_equation_type(o_html)
        if equation_type == EQUATION_INLINE:
            new_tag = CCMATH_INLINE
        elif equation_type == EQUATION_INTERLINE:
            new_tag = CCMATH_INTERLINE
        else:
            return

        if len(annotation_tags) > 0:
            annotation_tag = annotation_tags[0]
            text = annotation_tag.text
            # wrapped_text = cm.wrap_math(r'{}'.format(text), display=display)
            style_value = parent.get('style')
            if style_value:
                normalized_style_value = style_value.lower().strip().replace(' ', '').replace(';', '')
                if 'display: none' in normalized_style_value:
                    parent.style = ''
            new_span = build_cc_element(html_tag_name=new_tag, text=text, tail=text_strip(node.tail), type=math_type, by=math_render, html=o_html)
            replace_element(node, new_span)
        elif text_strip(node.get('alttext')):
            # Get the alttext attribute
            text = node.get('alttext')
            if text_strip(text):
                # wrapped_text = cm.wrap_math(r'{}'.format(alttext), display=display)
                new_span = build_cc_element(html_tag_name=new_tag, text=text, tail=text_strip(node.tail), type=math_type, by=math_render, html=o_html)
                replace_element(node, new_span)
        else:
            # Try translating to LaTeX
            tmp_node = deepcopy(node)
            tmp_node.tail = None
            mathml = element_to_html(tmp_node)
            # If this includes xmlns:mml, then we need to replace all
            # instances of mml: with nothing
            if 'xmlns:mml' in mathml:
                mathml = mathml.replace('mml:', '')
                # replace xmlns:mml="..." with nothing
                mathml = re.sub(r'xmlns:mml=".*?"', '', mathml)
            # if 'xmlns=' in mathml:
            #     mathml = re.sub(r"xmlns='.*?'", '', mathml)
            # TODO: 这样转换方法有很多错误，见测试用例mathjax-mml-chtml.html，需要优化
            latex = cm.mml_to_latex(mathml)
            latex = cm.wrap_math_md(latex)
            # wrapped_text = cm.wrap_math(r'{}'.format(latex), display=display)
            # Set the html of the new span tag to the text
            new_span = build_cc_element(html_tag_name=new_tag, text=latex, tail=text_strip(node.tail), type=math_type, by=math_render, html=o_html)
            replace_element(node, new_span)
    except Exception as e:
        raise HtmlMathRecognizerExp(f'Error processing math tag: {e}')


if __name__ == '__main__':
    html = '<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>a</mi><mo>&#x2260;</mo><mn>0</mn></math>'
    element = html_to_element(html)
    cm = CCMATH()
    modify_tree(cm, 'mathjax', html, element, element)
