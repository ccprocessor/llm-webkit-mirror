from lxml import etree
from lxml.html import HtmlElement

from llm_web_kit.libs.html_utils import build_cc_element
from llm_web_kit.libs.logger import logger
from llm_web_kit.pipeline.extractor.html.recognizer.cc_math.common import (
    CCMATH,
    CCMATH_INLINE,
    CCMATH_INTERLINE,
    EQUATION_INLINE,
    EQUATION_INTERLINE,
    text_strip,
)

def modify_tree(cm: CCMATH, math_render: str, o_html: str, node: etree._Element, parent: etree._Element):
    try:
        text = etree.tostring(node, method='xml', encoding='unicode', pretty_print=False)
        # print(text)
        # exit(0)

        equation_type, math_type = cm.get_equation_type(o_html)
        if equation_type == EQUATION_INLINE:
            new_tag = CCMATH_INLINE
        elif equation_type == EQUATION_INTERLINE:
            new_tag = CCMATH_INTERLINE
        else:
            raise ValueError(f'Unknown equation type: {equation_type}')

        if text and text_strip(text):
            new_span = build_cc_element(html_tag_name=new_tag, text=text, tail=text_strip(node.tail), type=math_type, by=math_render, html=o_html)
            parent.replace(node, new_span)
            print('111111')
        children = parent.getchildren()  # 获取所有子节点

        # 打印子节点
        for child in children:
            print(etree.tostring(child, encoding='unicode'))

    except Exception as e:
        logger.error(f'Error processing p tag: {e}')
