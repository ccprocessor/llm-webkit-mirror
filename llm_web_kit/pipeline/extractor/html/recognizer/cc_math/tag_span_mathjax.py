from lxml import etree

from llm_web_kit.libs.html_utils import build_cc_element
from llm_web_kit.libs.logger import logger
from llm_web_kit.pipeline.extractor.html.recognizer.cc_math.common import (
    CCMATH, CCMATH_INLINE, CCMATH_INTERLINE, EQUATION_INLINE,
    EQUATION_INTERLINE, text_strip)


def modify_tree(cm: CCMATH, math_render: str, o_html: str, node: etree._Element, parent: etree._Element):
    # 如果节点是span标签，并且class属性包含mathjax，MathJax，mathjax_display，MathJax_Display等
    # 示例：
    # <span class="mathjax">
    #     <span class="math-inline">$\frac{1}{2}$</span>
    #     是一个分数
    # </span>

    try:
        # Get the inner text of the mathjax tag
        # text = ''.join([
        #     (node.text or '') +
        #     ''.join([etree.tostring(child, encoding='utf-8', method='text').decode() for child in node])
        # ])
        text = node.text
        equation_type = cm.get_equation_type(o_html)

        if text and text_strip(text):
            equation_type = cm.get_equation_type(text)
            contains_math, math_type = cm.contains_math(text)
            if contains_math:
                if equation_type == EQUATION_INLINE:
                    new_tag = CCMATH_INLINE
                elif equation_type == EQUATION_INTERLINE:
                    new_tag = CCMATH_INTERLINE
                else:
                    raise ValueError(f'Unknown equation type: {equation_type}')
                new_span = build_cc_element(html_tag_name=new_tag, text=text, tail=text_strip(node.tail), type=math_type, by=math_render, html=o_html)
                parent.replace(node, new_span)
    except Exception as e:
        logger.error(f'Error processing mathjax class: {e}')
