from lxml.html import HtmlElement

from llm_web_kit.pipeline.extractor.html.recognizer.code.common import \
    replace_node_by_cccode


def modify_tree(root: HtmlElement) -> None:
    for pre_node in root.iter('pre'):
        assert isinstance(pre_node, HtmlElement)
        hit = False
        for _ in pre_node.iter('cccode'):
            hit = True
            break
        if not hit:
            replace_node_by_cccode(pre_node, 'tag_pre')


def detect(root: HtmlElement) -> bool:
    """检测是否存在 pre 标签.

    Args:
        root: 根节点

    Returns:
        bool: 是否存在 pre 标签
    """
    for pre_node in root.iter('pre'):
        assert isinstance(pre_node, HtmlElement)
        hit = False
        for _ in pre_node.iter('cccode'):
            hit = True
            break
        if not hit:
            return True
    return False
