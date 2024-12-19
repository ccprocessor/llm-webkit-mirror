import html

from typing import List, Tuple

from lxml import etree
from overrides import override

from llm_web_kit.pipeline.extractor.html.recognizer.recognizer import (
    BaseHTMLElementRecognizer,
)


# 对 prismjs 和 highlightjs 有效
# 但是如果没写，那没有办法
def detect_language(node: etree._Element) -> str:
    ptr = node
    assert isinstance(ptr, etree._Element)
    while ptr is not None:
        classes: list[str] = [c for c in ptr.attrib.get("class", "").split(" ") if c]
        for c in classes:
            if c.startswith("language-") or c.startswith("lang-"):
                return c.replace("language-", "").replace("lang-", "")
        ptr = ptr.getparent()
    return "unkonwn"


def split_code(root: etree._Element, by: str) -> list[tuple[str, str]]:
    if len(root.getchildren()) == 0:
        html_str: str = etree.tostring(root).decode()
        if root.tag == "code":
            language = detect_language(root)
            full_text = "".join(root.itertext(None))
            full_text: str = html.escape(full_text)
            code_str = (
                f'<cccode language="{language}" by="{by}">\n{full_text}\n</cccode>'
            )
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
            code_str = (
                f'<cccode language="{language}" by="{by}">\n{full_text}\n</cccode>'
            )
            rtn.append((html_str, code_str))
            if node.tail:
                rtn.append((node.tail, node.tail))
            continue

        if len(list(node.iter("code"))) == 0:
            rtn.append((html_str, html_str))
            if node.tail:
                rtn.append((node.tail, node.tail))
            continue

        rtn.extend(split_code(node, by))
        if node.tail:
            rtn.append((node.tail, node.tail))

    return rtn


def get_body(html: str) -> etree._Element:
    html_parser = etree.HTMLParser()
    html = html.replace("<br>", "\n")
    html = html.replace("<br/>", "\n")
    root = etree.fromstring(html, html_parser)
    assert isinstance(root, etree._Element)
    bodies = list(root.iter("body"))
    assert len(bodies) == 1
    body = bodies[0]
    assert isinstance(body, etree._Element)
    return body


def detect_pre_code(raw_html: str) -> bool:
    body = get_body(raw_html)
    for pre_node in body.iter("pre"):
        assert isinstance(pre_node, etree._Element)
        for _ in pre_node.iter("code"):
            return True
    return False


class CodeRecognizer(BaseHTMLElementRecognizer):
    """解析代码元素."""

    @override
    def recognize(
        self,
        base_url: str,
        main_html_lst: List[Tuple[str, str]],
        raw_html: str,
    ) -> List[Tuple[str, str]]:
        """父类，解析代码元素.

        Args:
            base_url: str: 基础url
            main_html_lst: main_html在一层一层的识别过程中，被逐步分解成不同的元素
            raw_html: 原始完整的html

        Returns:
        """

        assert len(main_html_lst) == 1

        main_html = main_html_lst[0][0]
        body = get_body(main_html)
        codes: list[tuple[str, str]] = []

        if detect_pre_code(raw_html):
            for pre_node in body.iter("pre"):
                codes.extend(split_code(pre_node, "pre_code_tag"))

        codes = [(code[0].strip(), code[1].strip()) for code in codes]

        return codes
