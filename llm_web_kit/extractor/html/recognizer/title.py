from typing import List, Tuple

# from lxml.etree import _Element as HtmlElement
from lxml.html import HtmlElement
from overrides import override

from llm_web_kit.exception.exception import HtmlTitleRecognizerException
from llm_web_kit.extractor.html.recognizer.recognizer import (
    BaseHTMLElementRecognizer, CCTag)
from llm_web_kit.libs.doc_element_type import DocElementType


class TitleRecognizer(BaseHTMLElementRecognizer):
    """解析多级标题元素."""

    @override
    def to_content_list_node(self, base_url: str, parsed_content: HtmlElement, raw_html_segment: str) -> dict:
        """将html转换成content_list_node.

        Args:
            base_url: str: 基础url
            parsed_content: str: 解析后的html
            raw_html_segment: str: 原始的html

        Returns:
            dict: content_list_node
        """
        level, text = self.__get_attribute(parsed_content)
        if not text or len(text.strip()) == 0:  # 如果有的空标题存在
            return None
        cctitle_content_node = {
            'type': DocElementType.TITLE,
            'raw_content': raw_html_segment,
            'content': {
                'title_content': text,
                'level': level
            }
        }
        return cctitle_content_node

    @override
    def recognize(self, base_url: str, main_html_lst: List[Tuple[HtmlElement, HtmlElement]], raw_html: str) -> List[Tuple[HtmlElement, HtmlElement]]:
        """父类，解析标题元素.

        Args:
            base_url: str: 基础url
            main_html_lst: main_html在一层一层的识别过程中，被逐步分解成不同的元素
            raw_html: 原始完整的html

        Returns:
            List[Tuple[HtmlElement, HtmlElement]]: 处理后的HTML元素列表
        """
        new_html_lst = []
        for html, raw_html in main_html_lst:
            if isinstance(html, str):
                html = self._build_html_tree(html)
            if self.is_cc_html(html):
                new_html_lst.append((html, raw_html))
            else:
                lst = self._extract_title(html)
                new_html_lst.extend(lst)
        return new_html_lst

    def _extract_title(self, raw_html: HtmlElement) -> List[Tuple[HtmlElement, HtmlElement]]:
        """提取多级标题元素
        Args:
            raw_html: HtmlElement对象

        Returns:
            List[Tuple[HtmlElement, HtmlElement]]: 多级标题元素列表
        """
        tree = raw_html
        self.__do_extract_title(tree)  # 遍历这个tree, 找到所有h1, h2, h3, h4, h5, h6标签
        # 最后切割html
        new_html = tree
        lst = self.html_split_by_tags(new_html, CCTag.CC_TITLE)
        return lst

    def __do_extract_title(self, root:HtmlElement) -> None:
        """递归处理所有子标签.

        Args:
            root: HtmlElement: 标签元素

        Returns:
        """
        # 匹配需要替换的标签
        if root.tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            title_text = self.__extract_title_text(root)
            title_raw_html = self._element_to_html(root)
            title_level = str(self.__extract_title_level(root.tag))
            tail_text = root.tail
            cc_element = self._build_cc_element(CCTag.CC_TITLE, title_text, tail_text, level=title_level, html=title_raw_html)
            self._replace_element(root, cc_element)
            return

        # 递归处理所有子标签必须放到最后。这样能保证对于嵌套的表格、list等元素，能够只处理最外层的标签。（也就是默认不处理嵌套的标签，留给处理者自行决策如何组织）
        for child in root.getchildren():
            self.__do_extract_title(child)  # 递归处理所有子标签

    def __extract_title_level(self, header_tag:str) -> int:
        """提取标题的级别.

        Args:
            header_tag: str: 标题的标签, 例如：h1, h2, h3, h4, h5, h6

        Returns:
            int: 标题的级别
        """
        return int(header_tag[1])

    def __extract_title_text(self, header_el:HtmlElement) -> str:
        """提取标题的文本.

        Args:
            header_el: HtmlElement: 标题的元素

        Returns:
            str: 标题的文本
        """
        def __extract_title_text_recusive(el: HtmlElement, with_tail: bool = True) -> list[str]:
            blks = []

            if el.tag == CCTag.CC_CODE_INLINE:
                blks.append(f'`{el.text}`')
            else:
                blks.append((el.text or '').strip())

            for child in el.getchildren():
                blks.extend(__extract_title_text_recusive(child))

            if with_tail:
                blks.append((el.tail or '').strip())

            return blks

        # 根元素不保留结尾
        blks = __extract_title_text_recusive(header_el, False)

        return ' '.join(blk for blk in blks if blk)

    def __get_attribute(self, html:HtmlElement) -> Tuple[int, str]:
        """获取element的属性."""
        # ele = self._build_html_tree(html)
        ele = html
        # 找到cctitle标签
        if ele is not None:
            level = ele.attrib.get('level')
            text = ele.text
            return level, text
        else:
            raise HtmlTitleRecognizerException(f'{html}中没有cctitle标签')
