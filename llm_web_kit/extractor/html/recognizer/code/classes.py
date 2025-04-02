from lxml.html import HtmlElement

from llm_web_kit.extractor.html.recognizer.code.common import \
    replace_node_by_cccode
from llm_web_kit.extractor.html.recognizer.recognizer import CCTag


def modify_tree(root: HtmlElement) -> None:
    for maybe_code_root in root.xpath('.//*[@class]'):
        assert isinstance(maybe_code_root, HtmlElement)
        if not any(['code' in class_name for class_name in maybe_code_root.classes]):
            continue

        if len(maybe_code_root.xpath(f'.//{CCTag.CC_CODE}')) > 0:
            continue

        replace_node_by_cccode(maybe_code_root, 'classname', False, False)


def detect(root: HtmlElement) -> bool:
    for maybe_code_root in root.xpath('.//*[@class]'):
        assert isinstance(maybe_code_root, HtmlElement)
        if not any(['code' in class_name for class_name in maybe_code_root.classes]):
            continue

        if len(maybe_code_root.xpath(f'.//{CCTag.CC_CODE}')) > 0:
            continue

        return True

    return False
