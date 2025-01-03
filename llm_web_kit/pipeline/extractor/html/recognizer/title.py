from typing import List, Tuple

from overrides import override

from llm_web_kit.pipeline.extractor.html.recognizer.recognizer import \
    BaseHTMLElementRecognizer


class TitleRecognizer(BaseHTMLElementRecognizer):
    """解析多级标题元素."""

    @override
    def to_content_list_node(self, base_url: str, parsed_content: str, raw_html_segment: str) -> dict:
        pass

    @override
    def recognize(self, base_url:str, main_html_lst: List[Tuple[str,str]], raw_html:str) -> List[Tuple[str,str]]:
        """父类，解析多级标题元素.

        Args:
            base_url: str: 基础url
            main_html_lst: main_html在一层一层的识别过程中，被逐步分解成不同的元素
            raw_html: 原始完整的html

        Returns:
        """
        new_html_lst = []
        for html, raw_html in main_html_lst:
            if self.is_cc_html(html):
                new_html_lst.append((html, raw_html))
            else:
                lst = self._extract_title(html)
                new_html_lst.extend([(title, raw_html) for title in lst])
        return new_html_lst

    def _extract_title(self, raw_html:str) -> List[Tuple[str,str]]:
        """
        提取多级标题元素
        Args:
            raw_html:

        Returns:
            List[Tuple[str,str]]: 多级标题元素, 第一个str是<cctitle>xxx</cctitle>, 第二个str是原始的html内容

        """
        pass
