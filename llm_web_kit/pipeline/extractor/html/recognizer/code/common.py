from typing import Optional

from lxml import etree


def get_lang_maybe(node: etree._Element) -> Optional[str]:
    attrib: dict[str, str] = node.attrib
    classes: list[str] = [c for c in attrib.get('class', '').split(' ') if c]
    for c in classes:
        if c.startswith('language-') or c.startswith('lang-'):
            return c.replace('language-', '').replace('lang-', '')
    return None


# 对 prismjs 和 highlightjs 有效
# 但是如果没写，那没有办法
# TODO: guesslang ?
def detect_language(node: etree._Element) -> Optional[str]:
    for cnode in node.iter(None):
        assert isinstance(cnode, etree._Element)
        if lang := get_lang_maybe(cnode):
            return lang

    ptr = node
    while ptr is not None:
        if lang := get_lang_maybe(ptr):
            return lang
        ptr = ptr.getparent()

    return None


def replace_node_by_cccode(node: etree._Element, by: str) -> None:
    origin_html = etree.tostring(node).decode()

    language = detect_language(node)

    # 让使用 br 换行的代码可以正确换行
    for br in node.xpath('*//br'):
        assert isinstance(br, etree._Element)
        br.tail = ('\n' + br.tail) if br.tail else ('\n')  # type: ignore

    full_text = ''.join(node.itertext(None))
    chunks = [sub_text.replace(' ', ' ').rstrip() for sub_text in full_text.split('\n')]

    while not chunks[0]:
        chunks = chunks[1:]
    while not chunks[len(chunks) - 1]:
        chunks = chunks[:-1]

    full_text = '\n'.join(chunks)
    # print(full_text)

    node.clear(keep_tail=True)
    if language:
        node.set('language', language)
    node.set('by', by)
    node.set('html', origin_html)
    node.tag = 'cccode'  # type: ignore
    node.text = full_text  # type: ignore
