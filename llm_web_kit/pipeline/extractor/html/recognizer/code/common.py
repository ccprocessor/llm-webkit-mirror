from typing import Optional

from lxml.html import HtmlElement

from llm_web_kit.libs.html_utils import element_to_html


def __get_lang_maybe(node: HtmlElement) -> Optional[str]:
    attrib: dict[str, str] = node.attrib
    classes: list[str] = [c for c in attrib.get('class', '').split(' ') if c]
    for c in classes:
        if c.startswith('language-') or c.startswith('lang-'):
            return c.replace('language-', '').replace('lang-', '')
    return None


# 对 prismjs 和 highlightjs 有效
# 但是如果没写，那没有办法
# TODO: guesslang ?
def __detect_language(node: HtmlElement) -> Optional[str]:
    for cnode in node.iter(None):
        assert isinstance(cnode, HtmlElement)
        if lang := __get_lang_maybe(cnode):
            return lang

    ptr = node
    while ptr is not None:
        if lang := __get_lang_maybe(ptr):
            return lang
        ptr = ptr.getparent()

    return None


def replace_node_by_cccode(node: HtmlElement, by: str) -> None:
    """将 node 替换为 cccode 标签.

    Args:
        node: 要替换的节点
        by: 替换后的标签
    """
    origin_html = element_to_html(node)

    language = __detect_language(node)

    # 让使用 br 换行的代码可以正确换行
    for br in node.xpath('*//br'):
        assert isinstance(br, HtmlElement)
        br.tail = ('\n' + br.tail) if br.tail else ('\n')  # type: ignore

    full_text = ''.join(node.itertext(None))
    chunks = [sub_text.replace(' ', ' ').rstrip() for sub_text in full_text.split('\n')]

    while not chunks[0]:
        chunks = chunks[1:]
    while not chunks[len(chunks) - 1]:
        chunks = chunks[:-1]

    full_text = '\n'.join(chunks)

    node.clear(keep_tail=True)
    if language:
        node.set('language', language)
    node.set('by', by)
    node.set('html', origin_html)
    node.tag = 'cccode'  # type: ignore
    node.text = full_text  # type: ignore
