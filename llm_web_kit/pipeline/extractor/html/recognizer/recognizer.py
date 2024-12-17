"""基本的元素解析类."""

from abc import ABC, abstractmethod
from typing import List, Tuple


class BaseHTMLElementRecognizer(ABC):
    """基本的元素解析类."""
    @abstractmethod
    def recognize(self, base_url:str, main_html_lst: List[Tuple[str,str]], raw_html:str) -> List[Tuple[str,str]]:
        """父类，解析html中的元素.

        Args:
            base_url: str: 基础url
            main_html_lst: main_html在一层一层的识别过程中，被逐步分解成不同的元素
            raw_html: 原始完整的html

        Returns:
        """
        raise NotImplementedError
