import html

from lxml import etree

from llm_web_kit.pipeline.extractor.html.recognizer.code.common import detect_language


def split_code(root: etree._Element) -> list[tuple[str, str]]:
    if len(root.getchildren()) == 0:
        html_str: str = etree.tostring(root).decode()
        if root.tag == "code":
            language = detect_language(root)
            full_text = "".join(root.itertext(None))
            full_text: str = html.escape(full_text)
            code_str = f'<cccode language="{language}" by="tag_pre_code">\n{full_text}\n</cccode>'
            return [(html_str, code_str)]
        return [(html_str, html_str)]

    rtn: list[tuple[str, str]] = []
    if root.text:
        rtn.append((root.text, root.text))
    for node in root.getchildren():
        assert isinstance(node, etree._Element)

        html_str: str = etree.tostring(node).decode()

        if node.tag == "code":
            language = detect_language(root)
            full_text = "".join(node.itertext(None))
            full_text: str = html.escape(full_text)
            code_str = f'<cccode language="{language}" by="tag_pre_code">\n{full_text}\n</cccode>'
            rtn.append((html_str, code_str))
            if node.tail:
                rtn.append((node.tail, node.tail))
            continue

        if len(list(node.iter("code"))) == 0:
            rtn.append((html_str, html_str))
            if node.tail:
                rtn.append((node.tail, node.tail))
            continue

        rtn.extend(split_code(node))
        if node.tail:
            rtn.append((node.tail, node.tail))

    return rtn


def detect(body: etree._Element) -> bool:
    for pre_node in body.iter("pre"):
        assert isinstance(pre_node, etree._Element)
        for _ in pre_node.iter("code"):
            return True
    return False
