from lxml import etree

from typing import Optional


def get_lang_maybe(node: etree._Element) -> Optional[str]:
    attrib: dict[str, str] = node.attrib
    classes: list[str] = [c for c in attrib.get("class", "").split(" ") if c]
    for c in classes:
        if c.startswith("language-") or c.startswith("lang-"):
            return c.replace("language-", "").replace("lang-", "")
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
    language = detect_language(node)
    full_text = "".join(node.itertext(None))

    node.clear(keep_tail=True)
    if language:
        node.set("language", language)
    node.set("by", by)
    node.tag = "cccode"  # type: ignore
    node.text = full_text  # type: ignore
