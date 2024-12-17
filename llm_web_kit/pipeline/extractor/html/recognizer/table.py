from typing import List

from overrides import override

from llm_web_kit.pipeline.extractor.html.recognizer.recognizer import \
    BaseHTMLElementRecognizer


class TableRecognizer(BaseHTMLElementRecognizer):
    """解析table元素."""
    @override
    def recognize(self, base_url:str, main_html_lst: List[str], raw_html:str) -> List[str]:
        """父类，解析表格元素.

        Args:
            base_url: str: 基础url
            main_html_lst: main_html在一层一层的识别过程中，被逐步分解成不同的元素
            raw_html: 原始完整的html

        Returns:
        """
        raise NotImplementedError
