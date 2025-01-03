from typing import List, Tuple

from lxml import etree
from lxml.etree import _Element as HtmlElement
from overrides import override

from llm_web_kit.pipeline.extractor.html.recognizer.recognizer import (
    BaseHTMLElementRecognizer, CCTag)


class TitleRecognizer(BaseHTMLElementRecognizer):
    """解析多级标题元素."""

    @override
    def to_content_list_node(self, base_url: str, parsed_content: str, raw_html_segment: str) -> dict:
        """将html转换成content_list_node.

        Args:
            base_url: str: 基础url
            parsed_content: str: 解析后的html
            raw_html_segment: str: 原始的html

        Returns:
            dict: content_list_node
        """
        level, text = self.__get_attribute(parsed_content)
        cctitle_content_node = {
            'type': 'title',
            'raw_content': raw_html_segment,
            'content': {
                'title_content': text,
                'level': level
            }
        }
        return cctitle_content_node

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
                new_html_lst.extend(lst)
        return new_html_lst

    def _extract_title(self, raw_html:str) -> List[Tuple[str,str]]:
        """
        提取多级标题元素
        Args:
            raw_html:

        Returns:
            List[Tuple[str,str]]: 多级标题元素, 第一个str是<cctitle>xxx</cctitle>, 第二个str是原始的html内容

        """
        result = []
        tree = self._build_html_tree(raw_html)
        # 遍历这个tree, 找到所有h1, h2, h3, h4, h5, h6标签, 并得到其对应的原始的html片段
        for ele in tree.iter():
            if ele.tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                title_text = self.__extract_title_text(ele)
                title_raw_html = self._element_to_html(ele)
                title_level = str(self.__extract_title_level(ele.tag))
                cctitle_element = self.__build_cc_element(CCTag.CC_TITLE, title_text, level=title_level, html=title_raw_html)
                # 用cctitle_element替换ele
                self.__replace_element(ele, cctitle_element)

        # 最后切割html
        new_html = self._element_to_html(tree)
        lst = self.html_split_by_tags(new_html, CCTag.CC_TITLE)
        result.extend(lst)

        return result

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
        return ''.join(header_el.xpath('.//text()'))

    def __build_cc_element(self, html_tag_name:str, text:str, **kwargs) -> str:
        """构建cctitle的html. 例如：<cctitle level=1>标题1</cctitle>

        Args:
            title_text: str: 标题的文本
            title_level: int: 标题的级别
            raw_html: str: 原始的html

        Returns:
            str: cctitle的html
        """
        attrib = {k:v for k,v in kwargs.items()}
        parser = etree.HTMLParser(collect_ids=False, encoding='utf-8', remove_comments=True, remove_pis=True)
        cc_element = parser.makeelement(html_tag_name, attrib)
        cc_element.text = text
        return cc_element

    def __replace_element(self, element:HtmlElement, cc_element:HtmlElement) -> None:
        """替换element为cc_element."""
        # 清空element的子元素
        if element.getparent():
            element.getparent().replace(element, cc_element)
        else:
            element.tag = cc_element.tag
            element.text = cc_element.text
            element.attrib = cc_element.attrib
            element.tail = cc_element.tail

    def __get_attribute(self, html:str) -> Tuple[int, str]:
        """获取element的属性."""
        ele = self._build_html_tree(html)
        # 找到cctitle标签
        cctitle_ele = ele.find(CCTag.CC_TITLE)
        if cctitle_ele:
            level = cctitle_ele.attrib.get('level')
            text = cctitle_ele.text
            return level, text
        else:
            # TODO 抛出异常
            raise ValueError(f'{html}中没有cctitle标签')
