from typing import List, Tuple

from lxml.html import HtmlElement
from overrides import override

from llm_web_kit.extractor.html.recognizer.code import (tag_code, tag_pre,
                                                        tag_pre_code)
from llm_web_kit.extractor.html.recognizer.recognizer import (
    BaseHTMLElementRecognizer, CCTag)


class CodeRecognizer(BaseHTMLElementRecognizer):
    """解析代码元素."""
    @override
    def recognize(
        self,
        base_url: str,
        main_html_lst: List[Tuple[HtmlElement, HtmlElement]],
        raw_html: str
    ) -> List[Tuple[HtmlElement, HtmlElement]]:
        """父类，解析代码元素.

        Args:
            base_url: str: 基础url
            main_html_lst: main_html在一层一层的识别过程中，被逐步分解成不同的元素
            raw_html: 原始完整的html

        Returns:
        """

        # assert len(main_html_lst) == 1
        # assert main_html_lst[0][0] == main_html_lst[0][1]

        rtn: List[Tuple[str, str]] = []
        for html, raw_html in main_html_lst:
            if self.is_cc_html(html):
                rtn.append((html, raw_html))
                continue
            # root: HtmlElement = html_to_element(html)
            root = html
            while True:
                # 最常见:
                # <pre><code></code></pre>
                # <code><pre></pre></code>
                # 使用 pre 来保证 code 内部格式
                # 所以每一个 code 就是一段代码，只需要切分出code，合并text
                if tag_pre_code.detect(root):
                    tag_pre_code.modify_tree(root)

                # 次常见:
                # 只有 code 没有 pre
                # 网站使用一些 div\span\p\br 来自己控制格式，每个 code 块只有一个单词或者符号。
                # 对 code tag 之间做距离排序，做不完整的最小生成树，挑选出完整的代码块的根节点，再合并内部的 text
                if tag_code.detect(root):
                    tag_code.modify_tree(root)

                # 只有 pre 没有 code
                if tag_pre.detect(root):
                    tag_pre.modify_tree(root)

                # 最后手段：用fasttext看看又没有可能是代码的
                # TODO:

                # 现在已知两种情况无法处理：
                # 1. 在线代码编辑器里的代码 (react testcase)
                # 2. 使用 table 模拟的代码展示 (telerik testcase)

                break

            def remove_empty_code(r: HtmlElement):
                for x in r:
                    if x.tag == CCTag.CC_CODE or x.tag == CCTag.CC_CODE_INLINE:
                        if not x.text:
                            r.remove(x)
                    else:
                        remove_empty_code(x)

            remove_empty_code(root)
            # html_str: str = element_to_html(root)
            rtn.extend(BaseHTMLElementRecognizer.html_split_by_tags(root, CCTag.CC_CODE))
        return rtn

    @override
    def to_content_list_node(self, base_url:str, parsed_content: HtmlElement, raw_html_segment:str) -> dict:
        """
        把代码元素转换为content list node.
        Args:
            base_url:
            parsed_content: HtmlElement对象
            raw_html_segment:

        Returns:

        """
        d = {
            'type': 'code',
            # "bbox": [],
            'raw_content': raw_html_segment,
            'inline': parsed_content.get('inline', 'false') == 'true',
            'content': {
                'code_content': parsed_content.text,
            },
        }

        if lang := parsed_content.get('language', None):
            d['content']['language'] = lang

        if by := parsed_content.get('by', None):
            d['content']['by'] = by

        return d
