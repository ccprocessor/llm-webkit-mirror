from urllib.parse import unquote

from lxml.html import HtmlElement

from llm_web_kit.exception.exception import HtmlMathRecognizerExp
from llm_web_kit.libs.html_utils import build_cc_element, replace_element
from llm_web_kit.pipeline.extractor.html.recognizer.cc_math.common import (
    CCMATH, CCMATH_INTERLINE, LATEX_IMAGE_CLASS_NAMES, LATEX_IMAGE_SRC_NAMES,
    MathType, text_strip)


def modify_tree(cm: CCMATH, math_render: str, o_html: str, node: HtmlElement, parent: HtmlElement):
    try:
        new_tag = CCMATH_INTERLINE
        math_type = MathType.LATEX

        class_name = node.get('class')
        if class_name and class_name in LATEX_IMAGE_CLASS_NAMES:
            text = node.get('alt')
            if text and text_strip(text):
                text = cm.wrap_math_md(text)
                new_span = build_cc_element(html_tag_name=new_tag, text=text, tail=text_strip(node.tail), type=math_type, by=math_render, html=o_html)
                replace_element(node, new_span)

        if class_name and 'x-ck12' in class_name:
            if text_strip(text):
                text = unquote(text)
                text = cm.wrap_math_md(text)
                new_span = build_cc_element(html_tag_name=new_tag, text=text, tail=text_strip(node.tail), type=math_type, by=math_render, html=o_html)
                replace_element(node, new_span)

        src_name = node.get('src')
        if src_name:
            if any(s in src_name for s in LATEX_IMAGE_SRC_NAMES):
                if any(src in src_name for src in ['latex.php', '/images/math/codecogs']):
                    text = node.get('alt')
                    if text and text_strip(text):
                        text = unquote(text)
                        text = cm.wrap_math_md(text)
                        new_span = build_cc_element(html_tag_name=new_tag, text=text, tail=text_strip(node.tail), type=math_type, by=math_render, html=o_html)
                        replace_element(node, new_span)
                else:
                    text = src_name.split('?')[1:]
                    text = '?'.join(text)
                    text = unquote(text)
                    text = cm.wrap_math_md(text)
                    new_span = build_cc_element(html_tag_name=new_tag, text=text, tail=text_strip(node.tail), type=math_type, by=math_render, html=o_html)
                    replace_element(node, new_span)

    except Exception as e:
        raise HtmlMathRecognizerExp(f'Error processing img tag: {e}')
