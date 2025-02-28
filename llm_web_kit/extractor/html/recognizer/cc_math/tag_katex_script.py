import re
from typing import Dict

from lxml.html import HtmlElement

from llm_web_kit.exception.exception import HtmlMathRecognizerException
from llm_web_kit.extractor.html.recognizer.cc_math.common import (
    CCMATH, CCMATH_INTERLINE, MathType, text_strip)
from llm_web_kit.libs.html_utils import build_cc_element, element_to_html


def modify_tree(cm: CCMATH, math_render: str, o_html: str, node: HtmlElement, parent: HtmlElement):
    try:
        text = node.text
        if text and text_strip(text):
            if node.tag not in ['script', 'style']:
                node.text = None
                new_span = build_cc_element(html_tag_name=CCMATH_INTERLINE, text=cm.wrap_math_md(text), tail=text_strip(node.tail), type=MathType.LATEX, math_render=math_render, o_html=o_html)
                node.insert(0,new_span)
            else:
                katex_pattern = re.compile(r'katex.render')
                node_text = text_strip(text)
                if katex_pattern.findall(node_text):
                    formulas_dict = extract_katex_formula(node_text)
                    for element_id, formula_content in formulas_dict.items():
                        target_elements = parent.xpath(f"//*[@id='{element_id}']")
                        if target_elements:
                            target_element = target_elements[0]
                            o_html = element_to_html(target_element)
                            target_element.text = None
                            new_span = build_cc_element(html_tag_name=CCMATH_INTERLINE, text=cm.wrap_math_md(formula_content), tail=text_strip(target_element.tail), type=MathType.LATEX, math_render=math_render, o_html=o_html)
                            target_element.insert(0, new_span)
    except Exception as e:
        raise HtmlMathRecognizerException(f'Error processing katex math: {e}')


def extract_katex_formula(text: str) -> Dict[str, str]:
    render_pattern = re.compile(r'katex.render\s*\(\s*"([^"]*)"\s*,\s*(\w+)\s*\)\s*')
    render_matches = render_pattern.findall(text)
    formulas_dict = {element_id: formula_content for formula_content, element_id in render_matches}
    return formulas_dict
