from lxml import etree

from llm_web_kit.pipeline.extractor.html.recognizer.code.common import \
    replace_node_by_cccode


def modify_tree(root: etree._Element) -> None:
    for pre_node in root.iter('pre'):
        assert isinstance(pre_node, etree._Element)
        for code_node in pre_node.iter('code'):
            replace_node_by_cccode(code_node, 'tag_pre_code')


def detect(root: etree._Element) -> bool:
    for pre_node in root.iter('pre'):
        assert isinstance(pre_node, etree._Element)
        for _ in pre_node.iter('code'):
            return True
    return False
