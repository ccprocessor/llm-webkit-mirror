from lxml import etree

from llm_web_kit.pipeline.extractor.html.recognizer.code.common import detect_language


def modify_tree(root: etree._Element) -> None:
    if len(root.getchildren()) == 0:
        if root.tag == "code":
            language = detect_language(root)
            full_text = "".join(root.itertext(None))

            root.clear(keep_tail=True)
            root.set("language", language)
            root.set("by", "tag_pre_code")
            root.tag = "cccode"  # type: ignore
            root.text = full_text  # type: ignore
        return

    for node in root.iterchildren(None):
        assert isinstance(node, etree._Element)

        if len(list(node.iter("code"))) == 0:
            continue

        modify_tree(node)


def detect(body: etree._Element) -> bool:
    for pre_node in body.iter("pre"):
        assert isinstance(pre_node, etree._Element)
        for _ in pre_node.iter("code"):
            return True
    return False
