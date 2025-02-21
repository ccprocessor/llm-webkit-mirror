import re
from typing import Dict

from lxml.html import HtmlElement

from llm_web_kit.exception.exception import HtmlMathRecognizerExp
from llm_web_kit.libs.html_utils import (build_cc_element, element_to_html,
                                         replace_element)
from llm_web_kit.pipeline.extractor.html.recognizer.cc_math.common import (
    CCMATH, CCMATH_INTERLINE, MathType, text_strip)


def modify_tree(cm: CCMATH, math_render: str, o_html: str, node: HtmlElement, parent: HtmlElement):
    try:
        text = node.text
        if text and text_strip(text):
            if node.tag not in ['script', 'style']:
                node.text = None
                new_span = create_new_span([(CCMATH_INTERLINE,MathType.LATEX)], cm.wrap_math_md(text), node, math_render, o_html)
                node.addnext(new_span)
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
                            new_span = create_new_span([(CCMATH_INTERLINE,MathType.LATEX)], cm.wrap_math_md(formula_content), target_element, math_render, o_html)
                            target_element.insert(0, new_span)
                elif node.get('type') and 'math/tex' in node.get('type'):
                    tag_math_type_list = cm.get_equation_type(o_html)
                    if not tag_math_type_list:
                        return
                    node.text = None
                    new_span = create_new_span(tag_math_type_list, cm.wrap_math_md(node_text), node, math_render, o_html)
                    replace_element(node, new_span)
    except Exception as e:
        raise HtmlMathRecognizerExp(f'Error processing katex math: {e}')


def create_new_span(tag_math_type_list, text_content, node, math_render, o_html):
    return build_cc_element(
        html_tag_name=tag_math_type_list[0][0],
        text=text_content,
        tail=text_strip(node.tail),
        type=tag_math_type_list[0][1],
        by=math_render,
        html=o_html
    )


def extract_katex_formula(text: str) -> Dict[str, str]:
    render_pattern = re.compile(r'katex.render\s*\(\s*"([^"]*)"\s*,\s*(\w+)\s*\)\s*')
    render_matches = render_pattern.findall(text)
    formulas_dict = {element_id: formula_content for formula_content, element_id in render_matches}
    return formulas_dict
