from lxml.html import HtmlElement

from llm_web_kit.exception.exception import HtmlMathRecognizerExp
from llm_web_kit.libs.html_utils import replace_element
from llm_web_kit.pipeline.extractor.html.recognizer.cc_math.common import (
    CCMATH, MathRender, text_strip)


def modify_tree(cm: CCMATH, math_render: str, o_html: str, node: HtmlElement, parent: HtmlElement):
    try:
        text = node.text
        equation_type, math_type = cm.get_equation_type(o_html)
        if math_render and math_render == MathRender.ASCIIMath:
            if text and text_strip(text):
                # node.text = cm.replace_math(new_tag, math_type, math_render, r'\\?`[^`]*`', node, extract_asciimath)
                new_span = cm.replace_math(math_type, math_render, r'(\\?`[^`]*`)', node, None,True)
                replace_element(node,new_span)
        else:
            return
    except Exception as e:
        raise HtmlMathRecognizerExp(f'Error processing asciimath: {e}')
