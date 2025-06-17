from lxml.html import HtmlElement

from llm_web_kit.extractor.html.recognizer.code.common import \
    replace_node_by_cccode
from llm_web_kit.extractor.html.recognizer.recognizer import CCTag

no_code_tags = ['audio', 'td', 'span','ul', 'li', 'body', 'p', 'h1', 'h2', 'figcaption', 'figure', 'section', 'figure', 'a', 'picture', 'iframe', 'aside']


def modify_tree(root: HtmlElement) -> None:

    for maybe_code_root in root.xpath('.//*[@class]'):
        assert isinstance(maybe_code_root, HtmlElement)

        if not any(['code' in class_name for class_name in maybe_code_root.classes]):
            continue
        # 应对list或者audio被识别为code的情况
        if maybe_code_root.tag in no_code_tags:
            continue
        if maybe_code_root.tag == 'div' and (any([child.tag in no_code_tags for child in maybe_code_root.iterchildren()]) or len([child for child in maybe_code_root.iterchildren()]) == 0):
            continue
        if len(maybe_code_root.xpath(f'.//{CCTag.CC_CODE}')) > 0:
            continue

        replace_node_by_cccode(maybe_code_root, 'classname', False, False)


def detect(root: HtmlElement) -> bool:
    for maybe_code_root in root.xpath('.//*[@class]'):
        assert isinstance(maybe_code_root, HtmlElement)

        if not any(['code' in class_name for class_name in maybe_code_root.classes]):
            continue
        if maybe_code_root.tag in no_code_tags:
            continue
        if maybe_code_root.tag == 'div' and any([child.tag in no_code_tags for child in maybe_code_root.iterchildren()]):
            continue
        if len(maybe_code_root.xpath(f'.//{CCTag.CC_CODE}')) > 0:
            continue
        return True

    return False
