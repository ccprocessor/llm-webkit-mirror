from lxml.html import HtmlElement

from llm_web_kit.exception.exception import HtmlMathRecognizerException
from llm_web_kit.extractor.html.recognizer.cc_math.common import (CCMATH,
                                                                  MathType,
                                                                  text_strip)
from llm_web_kit.libs.html_utils import replace_element


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
                asciimath_wrap = True if math_type == MathType.ASCIIMATH else False
                new_span = cm.replace_math(new_tag, math_type, math_render, new_span, None,asciimath_wrap)
            new_span.tail = tail
            replace_element(node,new_span)
            # if math_type == MathType.ASCIIMATH:
            #     text = cm.wrap_math_md(text)
            #     text = cm.extract_asciimath(text)
            #     new_span = build_cc_element(html_tag_name=new_tag, text=cm.wrap_math_md(text), tail=text_strip(node.tail), type=math_type, by=math_render, html=o_html)
            #     replace_element(node, new_span)
            # elif math_type == MathType.LATEX:
            #     new_span = build_cc_element(html_tag_name=new_tag, text=cm.wrap_math_md(text), tail=text_strip(node.tail), type=math_type, by=math_render, html=o_html)
            #     replace_element(node, new_span)
    except Exception as e:
        raise HtmlMathRecognizerException(f'Error processing script mathtex: {e}')
