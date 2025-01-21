import re
from typing import Dict

from lxml.html import HtmlElement

from llm_web_kit.exception.exception import HtmlMathRecognizerExp
from llm_web_kit.libs.html_utils import (build_cc_element, element_to_html,
                                         replace_element)
from llm_web_kit.pipeline.extractor.html.recognizer.cc_math.common import (
    CCMATH, CCMATH_INLINE, CCMATH_INTERLINE, EQUATION_INLINE,
    EQUATION_INTERLINE, text_strip)


def modify_tree(cm: CCMATH, math_render: str, o_html: str, node: HtmlElement, parent: HtmlElement):
    try:
        if node.tag == 'script':
            katex_pattern = re.compile(r'katex.render')
            node_text = text_strip(o_html)
            if katex_pattern.findall(node_text):
                formulas_dict = extract_katex_formula(text=node_text)
                for element_id, formula_content in formulas_dict.items():
                    target_elements = parent.xpath(f"//*[@id='{element_id}']")
                    if target_elements:
                        target_element = target_elements[0]
                        target_element.text = formula_content
                        o_html = element_to_html(target_element)
                        equation_type, math_type = cm.get_equation_type(o_html)
                        equation_type = EQUATION_INTERLINE
                        if equation_type == EQUATION_INLINE:
                            new_tag = CCMATH_INLINE
                        elif equation_type == EQUATION_INTERLINE:
                            new_tag = CCMATH_INTERLINE
                        else:
                            return
                        new_span = build_cc_element(html_tag_name=new_tag, text=formula_content, tail=text_strip(target_element.tail), type=math_type, by=math_render, html=o_html)
                        replace_element(target_element, new_span)
        else:
            text = node.text
            text = re.sub(r'\\displaystyle', '', text)
            text = f'$${text}$$'
            equation_type, math_type = cm.get_equation_type(o_html)
            equation_type = EQUATION_INTERLINE
            if equation_type == EQUATION_INLINE:
                new_tag = CCMATH_INLINE
            elif equation_type == EQUATION_INTERLINE:
                new_tag = CCMATH_INTERLINE
            else:
                return

            if text and text_strip(text):
                new_span = build_cc_element(html_tag_name=new_tag, text=text, tail=text_strip(node.tail), type=math_type, by=math_render, html=o_html)
                replace_element(node, new_span)
    except Exception as e:
        raise HtmlMathRecognizerExp(f'Error processing katex class: {e}')


def extract_katex_formula(text: str) -> Dict[str, str]:
    render_pattern = re.compile(r'katex.render\s*\(\s*"([^"]*)"\s*,\s*(\w+)\s*\)\s*')
    render_matches = render_pattern.findall(text)
    formulas_dict = {element_id: formula_content for formula_content, element_id in render_matches}
    return formulas_dict
