from lxml.html import HtmlElement

from llm_web_kit.pipeline.extractor.html.recognizer.code.common import \
    replace_node_by_cccode


def modify_tree(root: HtmlElement) -> None:
    for pre_node in root.iter('pre'):
        assert isinstance(pre_node, HtmlElement)
        for code_node in pre_node.iter('code'):
            replace_node_by_cccode(code_node, 'tag_pre_code')


def detect(root: HtmlElement) -> bool:
    """检测是否存在 pre 标签，并且 pre 标签内存在 code 标签.

    Args:
        root: 根节点

    Returns:
        bool: 是否存在 pre 标签，且 pre 标签内存在 code 标签
    """
    for pre_node in root.iter('pre'):
        assert isinstance(pre_node, HtmlElement)
        for _ in pre_node.iter('code'):
            return True
    return False
