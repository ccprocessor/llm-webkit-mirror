from typing import List, Tuple

from lxml import etree
from overrides import override

from llm_web_kit.pipeline.extractor.html.recognizer.code import (tag_code,
                                                                 tag_pre_code)
from llm_web_kit.pipeline.extractor.html.recognizer.recognizer import \
    BaseHTMLElementRecognizer


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
        assert main_html_lst[0][0] == main_html_lst[0][1]

        main_html = main_html_lst[0][0]
        root: etree._Element = etree.fromstring(main_html, etree.HTMLParser())

        while True:
            # 最常见:
            # <pre><code></code></pre>
            # 使用 pre 来保证 code 内部格式
            # 所以每一个 code 就是一段代码，只需要切分出code，合并text
            if tag_pre_code.detect(root):
                tag_pre_code.modify_tree(root)
                break

            # 次常见:
            # 只有 code 没有 pre
            # 网站使用一些 div\span\p\br 来自己控制格式，每个 code 块只有一个单词或者符号。
            # 对 code tag 之间做距离排序，做不完整的最小生成树，挑选出完整的代码块的根节点，再合并内部的 text
            if tag_code.detect(root):
                tag_code.modify_tree(root)
                break

            # 最后手段：用fasttext看看又没有可能是代码的
            # TODO:

            # 现在已知两种情况无法处理：
            # 1. 在线代码编辑器里的代码 (react testcase)
            # 2. 使用 table 模拟的代码展示 (telerik testcase)

            break

        html_str: str = etree.tostring(root).decode()

        return BaseHTMLElementRecognizer.html_split_by_tags(html_str, 'cccode', True)

    @override
    def to_content_list_node(self, base_url:str, parsed_content: str, raw_html_segment:str) -> dict:
        code_node: etree._Element = etree.fromstring(parsed_content, None)

        d = {
            'type': 'code',
            # "bbox": [],
            'raw_content': raw_html_segment,
            'content': {
                'code_content': code_node.text,
            },
        }

        if lang := code_node.get('language', None):
            d['content']['language'] = lang

        if by := code_node.get('by', None):
            d['content']['by'] = by

        return d
