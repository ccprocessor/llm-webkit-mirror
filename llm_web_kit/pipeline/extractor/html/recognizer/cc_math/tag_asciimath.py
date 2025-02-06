from lxml.html import HtmlElement

from llm_web_kit.exception.exception import HtmlMathRecognizerExp
from llm_web_kit.libs.html_utils import element_to_html
from llm_web_kit.pipeline.extractor.html.recognizer.cc_math.common import (
    CCMATH, MathRender, text_strip)


def _translator():
    import py_asciimath.translator.translator as _translator
    return _translator


def ASCIIMath2Tex(*args, **kwargs):
    return _translator().ASCIIMath2Tex(*args, **kwargs)


asciimath2tex = ASCIIMath2Tex(log=False)


def extract_asciimath(s):
    parsed = asciimath2tex.translate(s)
    return parsed


def modify_tree(cm: CCMATH, math_render: str, o_html: str, node: HtmlElement, parent: HtmlElement):
    try:
        text = node.text
        equation_type, math_type = cm.get_equation_type(o_html)
        if math_render and math_render == MathRender.ASCIIMath:
            if text and text_strip(text):
                # node.text = cm.replace_math(new_tag, math_type, math_render, r'\\?`[^`]*`', node, extract_asciimath)
                cm.replace_math(math_type, math_render, r'\\?`[^`]*`', node, extract_asciimath)
                print(element_to_html(node))
        else:
            return
    except Exception as e:
        raise HtmlMathRecognizerExp(f'Error processing asciimath: {e}')
