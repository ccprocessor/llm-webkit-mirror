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


__total__ = 0


def replace_node_by_cccode(node: etree._Element, by: str) -> None:
    language = detect_language(node)

    # 让使用 br 换行的代码可以正确换行
    for br in node.xpath("*//br"):
        assert isinstance(br, etree._Element)
        br.tail = ("\n" + br.tail) if br.tail else ("\n")  # type: ignore

    full_text = "".join(node.itertext(None))
    full_text = "\n".join(
        [
            sub_text.replace(" ", " ").rstrip()
            for sub_text in full_text.strip().split("\n")
        ]
    )  # 去除每行的结尾空白符

    node.clear(keep_tail=True)
    if language:
        node.set("language", language)
    node.set("by", by)
    node.tag = "cccode"  # type: ignore
    node.text = full_text  # type: ignore

    global __total__
    # with open(
    #     f"/home/SENSETIME/wuziming/llm-webkit-mirror/tests/llm_web_kit/pipeline/extractor/html/recognizer/assets/cccode/{__total__}",
    #     "wt",
    # ) as f:
    #     f.write(full_text)
    print(__total__)
    __total__ += 1
