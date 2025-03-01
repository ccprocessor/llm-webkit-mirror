from lxml.html import HtmlElement

from llm_web_kit.exception.exception import HtmlMathRecognizerException
from llm_web_kit.extractor.html.recognizer.cc_math.common import (CCMATH,
                                                                  text_strip)
from llm_web_kit.libs.html_utils import build_cc_element, replace_element


def modify_tree(cm: CCMATH, math_render: str, o_html: str, node: HtmlElement, parent: HtmlElement):
    try:
        text = node.text
        if text and text_strip(text):
            tag_math_type_list = cm.get_equation_type(o_html)
            if not tag_math_type_list:
                return
            node.text = None
            new_span = build_cc_element(html_tag_name=tag_math_type_list[0][0], text=cm.wrap_math_md(text), tail=text_strip(node.tail), type=tag_math_type_list[0][1], by=math_render, html=o_html)
            replace_element(node, new_span)
    except Exception as e:
        raise HtmlMathRecognizerException(f'Error processing math script: {e}')
