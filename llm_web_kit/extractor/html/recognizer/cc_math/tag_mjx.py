from lxml.html import HtmlElement

from llm_web_kit.extractor.html.recognizer.cc_math.common import (CCMATH,
                                                                  CCTag,
                                                                  MathType,
                                                                  text_strip)
from llm_web_kit.extractor.html.recognizer.recognizer import \
    BaseHTMLElementRecognizer
from llm_web_kit.libs.html_utils import build_cc_element, replace_element


# <mjx-container display="true" jax="CHTML">
# 	<formula  id="mathJaxEqu" class="mathJaxEqu">\vec{F} = m\vec{a}</formula>
# </mjx-container>
def modify_tree(cm: CCMATH, math_render: str, o_html: str, node: HtmlElement):
    """修改HTML树中的数学公式节点.

    Args:
        cm: CCMATH实例
        math_render: 数学公式渲染器类型
        o_html: 原始HTML
        node: 当前节点
    """
    # 处理mjx-container标签
    if node.tag == 'mjx-container':
        # 查找formula标签
        formula = node.find('.//formula')
        if formula is not None and formula.text:
            # 如果已经包含指定的ccmath标签，不进行替换
            if BaseHTMLElementRecognizer.is_cc_html(formula, [CCTag.CC_MATH_INTERLINE, CCTag.CC_MATH_INLINE]):
                return
        display = node.get('display', 'false').lower() == 'true'
        if display:
            new_tag = CCTag.CC_MATH_INTERLINE
        else:
            new_tag = CCTag.CC_MATH_INLINE

        # 获取jax类型
        jax_type = node.get('jax', '')
        if jax_type == 'CHTML':
            math_type = MathType.LATEX
        elif jax_type == 'AsciiMath':
            math_type = MathType.ASCIIMATH
        else:
            math_type = MathType.LATEX  # 先默认是latex

        # 查找formula标签
        formula = node.find('.//formula')
        if formula is not None and formula.text:
            new_span = build_cc_element(
                html_tag_name=new_tag,
                text=formula.text,
                tail=text_strip(formula.tail),
                type=math_type,
                by=math_render,
                html=o_html
            )
            replace_element(formula, new_span)
        return
