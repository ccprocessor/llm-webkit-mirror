from lxml import etree
from lxml.etree import Element

from llm_web_kit.libs.logger import logger
from llm_web_kit.pipeline.extractor.html.recognizer.cc_math.common import (
    CCMATH, CCMATH_INLINE, CCMATH_INTERLINE, EQUATION_INLINE,
    EQUATION_INTERLINE, text_strip)


def modify_tree(cm: CCMATH, math_render: str, o_html: str, node: etree._Element, parent: etree._Element):
    try:
        annotation_tags = node.xpath('.//annotation[@encoding="application/x-tex"]')
        if len(annotation_tags) > 0:
            annotation_tag = annotation_tags[0]
            text = annotation_tag.text
            equation_type = cm.get_equation_type(text)
            contains_math, math_type = cm.contains_math(text)
            if contains_math:
                if equation_type == EQUATION_INLINE:
                    new_span = Element(CCMATH_INLINE)
                elif equation_type == EQUATION_INTERLINE:
                    new_span = Element(CCMATH_INTERLINE)
                else:
                    raise ValueError(f'Unknown equation type: {equation_type}')
                # wrapped_math = wrap_math(text, display=False)
                new_span.text = text
                style_value = parent.get('style')
                if style_value:
                    normalized_style_value = style_value.lower().strip().replace(' ', '').replace(';', '')
                    if 'display:none' in normalized_style_value:
                        parent.style = ''
                if math_type:
                    new_span.set('type', math_type)
                    if math_render:
                        new_span.set('by', math_render)
                    new_span.set('html', o_html)
                    if parent is not None:
                        if text_strip(node.tail):
                            new_span.tail = node.tail
                parent.replace(node, new_span)
    except Exception as e:
        logger.error(f'Error processing math-container class: {e}')