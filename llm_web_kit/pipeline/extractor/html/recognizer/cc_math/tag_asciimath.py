from lxml.html import HtmlElement

from llm_web_kit.exception.exception import HtmlMathRecognizerExp
from llm_web_kit.libs.html_utils import replace_element
from llm_web_kit.pipeline.extractor.html.recognizer.cc_math.common import (
    CCMATH, text_strip)


def modify_tree(cm: CCMATH, math_render: str, o_html: str, node: HtmlElement, parent: HtmlElement):
    try:
        text = node.text
        tag_math_type_list = cm.get_equation_type(o_html)
        if not tag_math_type_list:
            return
        if text and text_strip(text):
            new_span = node
            tail = node.tail
            new_span.tail = None
            for new_tag, math_type in tag_math_type_list:
                new_span = cm.replace_math(new_tag, math_type, math_render, new_span, None,True)
            replace_element(node,new_span)
            new_span.tail = tail
    except Exception as e:
        raise HtmlMathRecognizerExp(f'Error processing asciimath: {e}')
