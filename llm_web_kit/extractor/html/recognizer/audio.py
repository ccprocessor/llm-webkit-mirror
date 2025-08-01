from typing import List, Tuple

from lxml.html import HtmlElement
from overrides import override

from llm_web_kit.extractor.html.recognizer.recognizer import \
    BaseHTMLElementRecognizer


class AudioRecognizer(BaseHTMLElementRecognizer):
    """解析音频元素."""
    @override
    def recognize(self, base_url:str, main_html_lst: List[Tuple[HtmlElement,HtmlElement]], raw_html:str, language:str = 'en') -> List[Tuple[HtmlElement,HtmlElement]]:
        """父类，解析音频元素.

        Args:
            base_url: str: 基础url
            main_html_lst: main_html在一层一层的识别过程中，被逐步分解成不同的元素
            raw_html: 原始完整的html

        Returns:
        """
        raise NotImplementedError

    @override
    def to_content_list_node(self, base_url: str, parsed_content: HtmlElement, raw_html_segment: str) -> dict:
        """
        把音频元素转换为content list node.
        Args:
            base_url:
            parsed_content:
            raw_html_segment:

        Returns:

        """
        raise NotImplementedError
