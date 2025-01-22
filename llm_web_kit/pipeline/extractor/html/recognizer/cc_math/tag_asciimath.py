import re

from lxml.html import HtmlElement

from llm_web_kit.exception.exception import HtmlMathRecognizerExp
from llm_web_kit.libs.html_utils import build_cc_element, element_to_html
from llm_web_kit.pipeline.extractor.html.recognizer.cc_math.common import (
    CCMATH, CCMATH_INLINE, CCMATH_INTERLINE, EQUATION_INLINE,
    EQUATION_INTERLINE, MathRender, MathType, text_strip)


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
        if math_type == MathType.ASCIIMATH and math_render and math_render == MathRender.ASCIIMath:
            if equation_type == EQUATION_INLINE:
                new_tag = CCMATH_INLINE
            elif equation_type == EQUATION_INTERLINE:
                new_tag = CCMATH_INTERLINE
            else:
                return
            if text and text_strip(text):
                node.text = replace_asciimath(new_tag,math_type,math_render,node)

                print(element_to_html(node))
        else:
            return
    except Exception as e:
        raise HtmlMathRecognizerExp(f'Error processing asciimath: {e}')


def replace_asciimath(new_tag: str,math_type: str,math_render: str,node: HtmlElement):
    def process_match(match):
        try:
            if match:
                asciimath_text = match.group(0)
                asciimath_text = text_strip(asciimath_text.replace('`','').replace('\\',''))
                if asciimath_text:
                    # asciimath -> latex
                    wrapped_text = extract_asciimath(asciimath_text)
                    new_span = build_cc_element(html_tag_name=new_tag, text=wrapped_text, tail='', type=math_type, by=math_render, html=wrapped_text)
                    node.append(new_span)
                return ''
        except Exception:
            return
    pattern = r'\\?`[^`]*`'
    result = re.sub(pattern, process_match, node.text)
    return result
