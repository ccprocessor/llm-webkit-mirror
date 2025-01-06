import json
from typing import List, Tuple

from lxml.etree import _Element as HtmlElement
from overrides import override

from llm_web_kit.libs.doc_element_type import DocElementType, ParagraphTextType
from llm_web_kit.pipeline.extractor.html.recognizer.recognizer import (
    BaseHTMLElementRecognizer, CCTag)


class ListRecognizer(BaseHTMLElementRecognizer):
    """解析列表元素."""

    def to_content_list_node(self, base_url: str, parsed_content: str, raw_html_segment: str) -> dict:
        """专化为列表元素的解析.

        Args:
            base_url:
            parsed_content:
            raw_html_segment:

        Returns:
        """
        ordered, content_list, _ = self.__get_attribute(parsed_content)
        ele_node = {
            'type': DocElementType.LIST,
            'raw_content': raw_html_segment,
            'content': {
                'items': content_list,
                'ordered': ordered
            }
        }

        return ele_node

    @override
    def recognize(self, base_url: str, main_html_lst: List[Tuple[str, str]], raw_html: str) -> List[Tuple[str, str]]:
        """父类，解析列表元素.

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
                lst = self._extract_list(html)
                new_html_lst.extend(lst)
        return new_html_lst

    def _extract_list(self, raw_html: str) -> List[Tuple[str, str]]:
        """提取列表元素. 不支持嵌套列表，如果有嵌套的情况，则内部列表将作为一个单独的段落，内部列表的每个列表项作为一个单独的句子，使用句号结尾。
        列表在html中有以下几个标签：

        <ul>, <ol>, <dl>, <menu>, <dir>
        ol, dl是有序列表，ul, menu, dir是无序列表

        Args:
            raw_html:

        Returns:
            List[Tuple[str, str]]: 列表元素, 第一个str是<cc-list>xxx</cc-list>, 第二个str是原始的html内容
        """
        tree = self._build_html_tree(raw_html)
        self.__do_extract_list(tree)
        # 最后切割html
        new_html = self._element_to_html(tree)
        lst = self.html_split_by_tags(new_html, CCTag.CC_LIST)

        return lst

    def __do_extract_list(self, root:HtmlElement) -> None:
        """提取列表元素.

        Args:
            root:

        Returns:
            Tuple[bool, list, str]: 第一个元素是是否有序; 第二个元素是个python list，内部是文本和行内公式，具体格式参考list的content_list定义。第三个元素是列表原始的html内容
        """
        list_tag_names = ['ul', 'ol', 'dl', 'menu', 'dir']

        if root.tag in list_tag_names:
            is_ordered, content_list, raw_html = self.__extract_list_element(root)
            text = json.dumps(content_list, ensure_ascii=False, indent=4)
            cc_element = self._build_cc_element(CCTag.CC_LIST, text, ordered=is_ordered, html=raw_html)
            self._replace_element(root, cc_element)  # cc_element 替换掉原来的列表元素
            return

        for child in root.iterchildren():
            self.__do_extract_list(child)

    def __extract_list_element(self, ele: HtmlElement) -> Tuple[bool, list, str]:
        """
        提取列表元素:
        假如有如下列表：
        <ul>
        <li>爱因斯坦的质量方差公式是</li>
        <li>E=mc^2</li>
        <li>，其中E是能量，m是质量，c是光速 </li>
        </ul>
        则提取出的内容为：
        ordered = False
        content_list = [
            [
                {"c": "爱因斯坦的质量方差公式是", "t": "text", "bbox": [0, 0, 10, 10]},
                {"c": "E=mc^2", "t": "equation-inline", "bbox": [10, 0, 10, 10]},
                {"c": "，其中E是能量，m是质量，c是光速 ", "t": "text", "bbox": [20, 0, 10, 10]}
            ]
        ]
        raw_html = "<ul><li>爱因斯坦的质量方差公式是</li><li>E=mc^2</li><li>，其中E是能量，m是质量，c是光速 </li></ul>"
        --------------
        最终拼接的<cclist>为：
        <cclist ordered="False" html="raw_html">
            [
                [
                    {"c": "爱因斯坦的质量方差公式是", "t": "text", "bbox": [0, 0, 10, 10]},
                    {"c": "E=mc^2", "t": "equation-inline", "bbox": [10, 0, 10, 10]},
                    {"c": "，其中E是能量，m是质量，c是光速 ", "t": "text", "bbox": [20, 0, 10, 10]}
                ]
            ]
        </cclist>

        Args:
            ele:

        Returns:
            (bool, str, str): 第一个元素是是否有序; 第二个元素是个python list，内部是文本和行内公式，具体格式参考list的content_list定义。第三个元素是列表原始的html内容
        """
        is_ordered = ele.tag in ['ol', 'dl']
        content_list = []
        raw_html = self._element_to_html(ele)
        for item in ele.iterchildren():
            # 这里 遍历列表的每个直接子元素，每个子元素作为一个段落。 TODO 列表里有列表、图片、表格的情况先不考虑。
            # 获取到每个子元素的全部文本，忽略其他标签
            text_paragraph = self.__extract_list_item_text(item)
            content_list.append(text_paragraph)

        return is_ordered, content_list, raw_html

    def __extract_list_item_text(self, item:HtmlElement) -> list[list]:
        """提取列表项的文本.
        列表项里的文本的分段策略采用最简单的方式：
        1. 遇到<br/>标签，则认为是一个段落结束。

        Args:
            item:

        Returns:
            list[dict]: 列表项的文本
        """
        text_paragraph = []

        paragraph = []
        if item.text:  # li标签的直接文本。
            paragraph.append({'c': item.text, 't': ParagraphTextType.TEXT})

        for child in item.iter():
            if child.tag == CCTag.CC_MATH_INLINE:
                paragraph.append({'c': child.text, 't': ParagraphTextType.EQUATION_INLINE})
            elif child.tag == 'br':
                text_paragraph.append(paragraph)
                paragraph = []
                if child.tail:
                    paragraph.append({'c': child.tail, 't': ParagraphTextType.TEXT})
            else:
                paragraph.append({'c': child.text, 't': ParagraphTextType.TEXT})

        if paragraph:
            text_paragraph.append(paragraph)

        return text_paragraph

    def __get_attribute(self, html:str) -> Tuple[bool, dict, str]:
        """获取element的属性.

        Args:
            html:

        Returns:
            Tuple[str]: 第一个元素是是否有序; 第二个元素是个python list，内部是文本和行内公式，具体格式参考list的content_list定义。第三个元素是列表原始的html内容
        """
        ele = self._build_html_tree(html)
        # 找到cctitle标签
        cclist_eles = ele.find(CCTag.CC_LIST)
        if cclist_eles:
            ordered = bool(cclist_eles.attrib.get('ordered'))
            content_list = json.loads(cclist_eles.text)
            raw_html = cclist_eles.attrib.get('html')
            return ordered, content_list, raw_html
        else:
            # TODO 抛出异常, 需要自定义
            raise ValueError(f'{html}中没有cctitle标签')
