# 在code/__init__.py里了
from typing import List, Tuple

from lxml import etree
from overrides import override

from llm_web_kit.pipeline.extractor.html.recognizer.code import (tag_code,
                                                                 tag_pre_code)
from llm_web_kit.pipeline.extractor.html.recognizer.recognizer import \
    BaseHTMLElementRecognizer


def get_body(html: str) -> etree._Element:
    html_parser = etree.HTMLParser()
    # 有一些代码用 br 换行
    html = html.replace('<br>', '\n')
    html = html.replace('<br/>', '\n')
    root = etree.fromstring(html, html_parser)
    assert isinstance(root, etree._Element)
    bodies = list(root.iter('body'))
    assert len(bodies) == 1
    body = bodies[0]
    assert isinstance(body, etree._Element)
    return body


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

        while True:
            # 最常见:
            # <pre><code></code></pre>
            # 使用 pre 来保证 code 内部格式
            # 所以每一个 code 就是一段代码，只需要切分出code，合并text
            if tag_pre_code.detect(body):
                codes.extend(tag_pre_code.split_code(body))
                break

            # 次常见:
            # 只有 code 没有 pre
            # 网站使用一些 div\span\p\br 来自己控制格式，每个 code 块只有一个单词或者符号。
            # 对 code tag 之间做距离排序，做不完整的最小生成树，挑选出完整的代码块的根节点，再合并内部的 text
            if tag_code.detect(body):
                codes.extend(tag_code.split_code(body))
                break

        # 最后手段：用fasttext看看又没有可能是代码的
        # TODO:

        codes = [
            (code[0].strip(), code[1].strip()) for code in codes if code[1].strip()
        ]

        return codes
