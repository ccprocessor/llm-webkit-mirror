from lxml import etree


# 对 prismjs 和 highlightjs 有效
# 但是如果没写，那没有办法
def detect_language(node: etree._Element) -> str:
    ptr = node
    while ptr is not None:
        classes: list[str] = [c for c in ptr.attrib.get("class", "").split(" ") if c]
        for c in classes:
            if c.startswith("language-") or c.startswith("lang-"):
                return c.replace("language-", "").replace("lang-", "")
        ptr = ptr.getparent()
    return "unkonwn"
