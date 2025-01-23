import re

from lxml.html import HtmlElement

from llm_web_kit.libs.html_utils import build_cc_element, replace_element
from llm_web_kit.pipeline.extractor.html.recognizer.cc_math.common import (
    CCMATH, CCMATH_INLINE, CCMATH_INTERLINE, EQUATION_INLINE,
    EQUATION_INTERLINE, text_strip)


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
        pattern = r'\\?`[^`]*`'
        if re.search(pattern, text):
            equation_type, math_type = cm.get_equation_type(o_html)
            if equation_type == EQUATION_INLINE:
                new_tag = CCMATH_INLINE
            elif equation_type == EQUATION_INTERLINE:
                new_tag = CCMATH_INTERLINE
            else:
                return
            if text and text_strip(text):
                text = text_strip(text)
                wrapped_asciimath = replace_asciimath(cm,text)
                new_span = build_cc_element(html_tag_name=new_tag, text=cm.wrap_math_md(wrapped_asciimath), tail=text_strip(node.tail), type=math_type, by=math_render, html=o_html)
                replace_element(node, new_span)
        else:
            return
    except Exception as e:
        raise ValueError(f'Error processing asciimath: {e}')


def replace_asciimath(cm: CCMATH,text):
    def process_match(match):
        try:
            if match:
                asciimath_text = match.group(0)
                asciimath_text = text_strip(asciimath_text.replace('`','').replace('\\',''))
                if asciimath_text:
                    # asciimath -> latex
                    wrapped_text = cm.wrap_math(extract_asciimath(asciimath_text))
                else:
                    wrapped_text = ''
                return wrapped_text
        except Exception:
            return ''
    pattern = r'\\?`[^`]*`'
    result = re.sub(pattern, process_match, text)
    return result
