import re
from copy import deepcopy

from lxml.html import HtmlElement

from llm_web_kit.libs.html_utils import build_cc_element, element_to_html,html_to_element
from llm_web_kit.libs.logger import logger
from llm_web_kit.pipeline.extractor.html.recognizer.cc_math.common import (
    CCMATH, CCMATH_INTERLINE, text_strip)


def modify_tree(cm: CCMATH, math_render: str, o_html: str, node: HtmlElement, parent: HtmlElement):
    formula_content = get_render_content(node,parent)
    print(formula_content)
    o_html = f'<span class="katex">{formula_content}</span>'
    new_tag = CCMATH_INTERLINE
    math_type = 'latex' #TODO 修改get_equation_type
    if formula_content and text_strip(formula_content):
            new_span = build_cc_element(html_tag_name=new_tag, text=formula_content, tail='', type=math_type, by=math_render, html=o_html)
            parent.replace(node, new_span)


def get_render_content(node: HtmlElement, parent: HtmlElement) -> str:
    """
    根据node节点及其父节点，查找对应的script脚本中与该span节点id匹配的渲染内容并返回。
    如果未找到则返回空字符串。
    """
    id_value = node.get('id')
    if id_value:
        script_elements = parent.xpath('.//script')
        if not script_elements:
            return ""
        for script in script_elements:
            text = script.text_content()
            if not text:
                continue
            get_element_pattern = re.compile(r'var\s+(\w+)\s*=\s*document\.getElementById\s*\(\s*"{}"\s*\)\s*'.format(id_value))
            render_pattern = re.compile(r'katex.render\s*\(\s*"([^"]*)"\s*,\s*(\w+)\s*\)\s*')
            get_element_matches = get_element_pattern.findall(text)
            replacement_id = get_element_matches[0] if get_element_matches else id_value
            render_matches = render_pattern.findall(text)
            for formula_content, element_id in render_matches:
                if element_id == replacement_id:
                    return formula_content
        return ""
    return ""
