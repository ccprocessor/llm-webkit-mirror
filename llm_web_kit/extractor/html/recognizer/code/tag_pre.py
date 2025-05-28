from lxml.html import HtmlElement

# from llm_web_kit.model.code_detector import decide_code_by_str
from llm_web_kit.extractor.html.recognizer.code.common import \
    replace_node_by_cccode
from llm_web_kit.extractor.html.recognizer.recognizer import CCTag


def modify_tree(root: HtmlElement) -> None:
    for pre_node in root.iter('pre'):
        assert isinstance(pre_node, HtmlElement)
        hit = False
        for _ in pre_node.iter(CCTag.CC_CODE):
            hit = True
            break
        if not hit:
            # if decide_code_by_str(''.join(pre_node.itertext(None))) > 0.6:
            replace_node_by_cccode(pre_node, 'tag_pre')


def detect(root: HtmlElement) -> bool:
    """检测是否存在非全由 <p> 标签构成的 <pre> 标签，并且该 <pre> 中没有 <code> 标签.

    Args:
        root: 根节点

    Returns:
        bool: 是否存在符合条件的 <pre> 标签
    """

    for pre_node in root.iter('pre'):
        # 判断是否所有直接子元素是 <p>
        all_p = True
        for child in pre_node.iterchildren():
            if child.tag.lower() != 'p':
                all_p = False
                break

        if all_p:
            continue  # 跳过全由 <p> 构成的 <pre>

        has_code = False
        for _ in pre_node.iter(CCTag.CC_CODE):
            has_code = True
            break

        if not has_code:
            return True  # 找到一个符合条件的 <pre>

    return False
