import re
from copy import deepcopy

from lxml import etree

from llm_web_kit.libs.html_utils import build_cc_element, element_to_html
from llm_web_kit.libs.logger import logger
from llm_web_kit.pipeline.extractor.html.recognizer.cc_math.common import (
    CCMATH, CCMATH_INLINE, CCMATH_INTERLINE, EQUATION_INLINE,
    EQUATION_INTERLINE, MathType, text_strip, wrap_math)


def modify_tree(cm: CCMATH, math_render: str, o_html: str, node: etree._Element, parent: etree._Element):
    try:
        annotation_tags = node.xpath('.//annotation[@encoding="application/x-tex"]')

        if len(annotation_tags) > 0:
            annotation_tag = annotation_tags[0]
            text = annotation_tag.text
            new_tag = CCMATH_INTERLINE  # TODO: 需要判断，先认为mathML都是interline
            contains_math, math_type = cm.contains_math(text)
            if contains_math:
                wrapped_text = wrap_math(text, display=True)
                style_value = parent.get('style')
                if style_value:
                    normalized_style_value = style_value.lower().strip().replace(' ', '').replace(';', '')
                    if 'display: none' in normalized_style_value:
                        parent.style = ''
                new_span = build_cc_element(html_tag_name=new_tag, text=wrapped_text, tail=text_strip(node.tail), type=math_type, by=math_render, html=o_html)
                parent.replace(node, new_span)
        elif text_strip(node.get('alttext')):
            # Get the alttext attribute
            alttext = node.get('alttext')
            new_tag = CCMATH_INTERLINE  # TODO: 需要判断，先认为mathML都是interline
            if text_strip(alttext):
                contains_math, math_type = cm.contains_math(text)
                if contains_math:
                    wrapped_text = wrap_math(alttext, display=True)
                    new_span = build_cc_element(html_tag_name=new_tag, text=wrapped_text, tail=text_strip(node.tail), type=math_type, by=math_render, html=o_html)
                    parent.replace(node, new_span)
        else:
            math_type = MathType.MATHML
            equation_type = cm.get_equation_type(o_html)
            if equation_type == EQUATION_INLINE:
                new_tag = CCMATH_INLINE
            elif equation_type == EQUATION_INTERLINE:
                new_tag = CCMATH_INTERLINE
            else:
                raise ValueError(f'Unknown equation type: {equation_type}')
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
            latex = cm.mml_to_latex(mathml)
            # Set the html of the new span tag to the text
            new_span = build_cc_element(html_tag_name=new_tag, text=latex, tail=text_strip(node.tail), type=math_type, by=math_render, html=o_html)
            parent.replace(node, new_span)
    except Exception as e:
        logger.error(f'Error processing math tag: {e}')
