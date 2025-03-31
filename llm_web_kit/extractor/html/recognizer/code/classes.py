from lxml.html import HtmlElement

from llm_web_kit.extractor.html.recognizer.code.common import \
    replace_node_by_cccode
from llm_web_kit.extractor.html.recognizer.recognizer import CCTag


def modify_tree(root: HtmlElement) -> None:
    for maybe_code_root in root.iter(None):
        assert isinstance(maybe_code_root, HtmlElement)

        hit = False
        classes = maybe_code_root.classes
        for class_name in classes:
            if 'code' in class_name:
                hit = True
        if not hit:
            continue

        hit = False
        for _ in maybe_code_root.iter(CCTag.CC_CODE):
            hit = True
            break
        if not hit:
            replace_node_by_cccode(maybe_code_root, 'classname', False, False)


def detect(root: HtmlElement) -> bool:
    for maybe_code_root in root.iter(None):
        assert isinstance(maybe_code_root, HtmlElement)

        hit = False
        classes = maybe_code_root.classes
        for class_name in classes:
            if 'code' in class_name:
                hit = True
        if not hit:
            continue

        hit = False
        for _ in maybe_code_root.iter(CCTag.CC_CODE):
            hit = True
            break
        if not hit:
            return True

    return False
