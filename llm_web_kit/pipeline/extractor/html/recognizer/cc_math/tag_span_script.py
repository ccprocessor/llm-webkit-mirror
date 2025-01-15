import re
from copy import deepcopy

from lxml.html import HtmlElement

from llm_web_kit.libs.html_utils import (build_cc_element, element_to_html,
                                         replace_element)
from llm_web_kit.libs.logger import logger
from llm_web_kit.pipeline.extractor.html.recognizer.cc_math.common import (
    CCMATH, CCMATH_INLINE, CCMATH_INTERLINE, EQUATION_INLINE,
    EQUATION_INTERLINE, text_strip)


def modify_tree(cm: CCMATH, math_render: str, o_html: str, node: HtmlElement, parent: HtmlElement):
    try:
        annotation_tags = node.xpath('.//annotation[@encoding="application/x-tex"]')
        equation_type, math_type = cm.get_equation_type(o_html)
        if equation_type == EQUATION_INLINE:
            new_tag = CCMATH_INLINE
            display = False
        elif equation_type == EQUATION_INTERLINE:
            new_tag = CCMATH_INTERLINE
            display = True
        else:
            raise ValueError(f'Unknown equation type: {equation_type}')
        if len(annotation_tags) > 0:
            annotation_tag = annotation_tags[0]
            text = annotation_tag.text
            wrapped_text = cm.wrap_math(r'{}'.format(text), display=display)
            style_value = parent.get('style')
            if style_value:
                normalized_style_value = style_value.lower().strip().replace(' ', '').replace(';', '')
                if 'display: none' in normalized_style_value:
                    parent.style = ''
            new_span = build_cc_element(html_tag_name=new_tag, text=wrapped_text, tail=text_strip(node.tail), type=math_type, by=math_render, html=o_html)
            replace_element(node, new_span)
        elif text_strip(get_render_content(node,parent)):
            # TODO 需要寻找测试案例 测试
            wrapped_text = get_render_content(node,parent)
            if text_strip(wrapped_text):
                wrapped_text = cm.wrap_math(r'{}'.format(wrapped_text), display=display)
                new_span = build_cc_element(html_tag_name=new_tag, text=wrapped_text, tail=text_strip(node.tail), type=math_type, by=math_render, html=o_html)
                replace_element(node, new_span)
        else:
            # Try translating to LaTeX
            tmp_node = deepcopy(node)
            tmp_node.tail = None
            mathml = element_to_html(tmp_node)
            # If this includes xmlns:mml, then we need to replace all
            # instances of mml: with nothing
            if 'xmlns:mml' in mathml:
                mathml = mathml.replace('mml:', '')
                # replace xmlns:mml="..." with nothing
                mathml = re.sub(r'xmlns:mml=".*?"', '', mathml)
            # if 'xmlns=' in mathml:
            #     mathml = re.sub(r"xmlns='.*?'", '', mathml)
            # TODO: 这样转换方法有很多错误，见测试用例mathjax-mml-chtml.html，需要优化
            latex = cm.mml_to_latex(mathml)
            wrapped_text = cm.wrap_math(r'{}'.format(latex), display=display)
            # Set the html of the new span tag to the text
            new_span = build_cc_element(html_tag_name=new_tag, text=wrapped_text, tail=text_strip(node.tail), type=math_type, by=math_render, html=o_html)
            replace_element(node, new_span)
    except Exception as e:
        logger.error(f'Error processing katex class: {e}')


def get_render_content(node: HtmlElement, parent: HtmlElement) -> str:
    """根据node节点及其父节点，查找对应的script脚本中与该span节点id匹配的渲染内容并返回。 如果未找到则返回空字符串。"""
    id_value = node.get('id')
    if id_value:
        script_elements = parent.xpath('.//script')
        if not script_elements:
            return ''
        for script in script_elements:
            text = script.text_content()
            if not text:
                continue
            text = text.replace("\'", '')
            get_element_pattern = re.compile(r'var\s+(\w+)\s*=\s*document\.getElementById\s*\(\s*{}\s*\)\s*'.format(id_value))
            render_pattern = re.compile(r'katex.render\s*\(\s*"([^"]*)"\s*,\s*(\w+)\s*\)\s*')
            get_element_matches = get_element_pattern.findall(text)
            replacement_id = get_element_matches[0] if get_element_matches else id_value
            render_matches = render_pattern.findall(text)
            for formula_content, element_id in render_matches:
                if element_id == replacement_id:
                    return formula_content
        return ''
    return ''
