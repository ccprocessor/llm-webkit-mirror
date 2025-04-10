import json
from typing import Any, List, Tuple

from lxml.html import HtmlElement
from overrides import override

from llm_web_kit.exception.exception import HtmlListRecognizerException
from llm_web_kit.extractor.html.recognizer.recognizer import (
    BaseHTMLElementRecognizer, CCTag)
from llm_web_kit.libs.doc_element_type import DocElementType, ParagraphTextType
from llm_web_kit.libs.html_utils import process_sub_sup_tags


class ListRecognizer(BaseHTMLElementRecognizer):
    """解析列表元素."""

    def to_content_list_node(self, base_url: str, parsed_content: HtmlElement, raw_html_segment: str) -> dict:
        """专化为列表元素的解析.

        Args:
            base_url:
            parsed_content:
            raw_html_segment:

        Returns:
        """
        if not isinstance(parsed_content, HtmlElement):
            raise HtmlListRecognizerException(f'parsed_content 必须是 HtmlElement 类型，而不是 {type(parsed_content)}')
        ordered, content_list, _, list_nest_level = self.__get_attribute(parsed_content)
        ele_node = {
            'type': DocElementType.LIST,
            'raw_content': raw_html_segment,
            'content': {
                'items': content_list,
                'ordered': ordered,
                'list_nest_level': list_nest_level
            }
        }

        return ele_node

    @override
    def recognize(self, base_url: str, main_html_lst: List[Tuple[HtmlElement, HtmlElement]], raw_html: str) -> List[Tuple[HtmlElement, HtmlElement]]:
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

    def _extract_list(self, raw_html: HtmlElement) -> List[Tuple[HtmlElement, HtmlElement]]:
        """提取列表元素. 不支持嵌套列表，如果有嵌套的情况，则内部列表将作为一个单独的段落，内部列表的每个列表项作为一个单独的句子，使用句号结尾。
        列表在html中有以下几个标签：

        <ul>, <ol>, <dl>, <menu>, <dir>
        ol, dl是有序列表，ul, menu, dir是无序列表

        Args:
            raw_html:

        Returns:
            List[Tuple[str, str]]: 列表元素, 第一个str是<cc-list>xxx</cc-list>, 第二个str是原始的html内容
        """
        # tree = self._build_html_tree(raw_html)
        tree = raw_html
        self.__do_extract_list(tree)
        # 最后切割html
        # new_html = self._element_to_html(tree)
        new_html = tree
        lst = self.html_split_by_tags(new_html, CCTag.CC_LIST)
        return lst

    def __do_extract_list(self, root: HtmlElement) -> None:
        """提取列表元素.

        Args:
            root:

        Returns:
            Tuple[bool, list, str]: 第一个元素是是否有序; 第二个元素是个python list，内部是文本和行内公式，具体格式参考list的content_list定义。第三个元素是列表原始的html内容
        """
        list_tag_names = ['ul', 'ol', 'dl', 'menu', 'dir']

        if root.tag in list_tag_names:
            list_nest_level, is_ordered, content_list, raw_html, tail_text = self.__extract_list_element(root)
            text = json.dumps(content_list, ensure_ascii=False, indent=4)
            cc_element = self._build_cc_element(CCTag.CC_LIST, text, tail_text, ordered=is_ordered, list_nest_level=list_nest_level, html=raw_html)
            self._replace_element(root, cc_element)  # cc_element 替换掉原来的列表元素
            return

        for child in root.iterchildren():
            self.__do_extract_list(child)

    def __extract_list_element(self, ele: HtmlElement) -> tuple[int, bool, list[list[list]], str, Any]:
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
                    {"c": "爱因斯坦的质量方程公式是", "t": "text", "bbox": [0, 0, 10, 10]},
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
        list_nest_level = self.__get_list_type(ele)
        tail_text = ele.tail
        content_list = []
        raw_html = self._element_to_html(ele)
        # 添加处理ul标签直接文本的逻辑
        if ele.text and ele.text.strip():
            content_list.append([[{'c': ele.text.strip(), 't': ParagraphTextType.TEXT}]])

        for item in ele.iterchildren():
            # 这里 遍历列表的每个直接子元素，每个子元素作为一个段落。 TODO 列表里有列表、图片、表格的情况先不考虑。
            # 获取到每个子元素的全部文本，忽略其他标签
            text_paragraph = self.__extract_list_item_text(item)
            if len(text_paragraph) > 0:
                content_list.append(text_paragraph)

        return list_nest_level, is_ordered, content_list, raw_html, tail_text

    def __get_list_type(self, list_ele: HtmlElement) -> int:
        """获取list嵌套的层级。

        计算一个列表元素的最大嵌套深度，通过递归遍历所有子元素。
        例如：
        - 没有嵌套的列表返回1
        - 有一层嵌套的列表返回2
        - 有两层嵌套的列表返回3

        Args:
            list_ele: 列表HTML元素

        Returns:
            int: 列表的最大嵌套深度
        """
        list_type = ['ul', 'ol', 'dl', 'menu', 'dir']

        def get_max_depth(element):
            max_child_depth = 0
            for child in element.iterchildren():
                if child.tag in list_type:
                    # 找到嵌套列表，其深度至少为1
                    child_depth = 1 + get_max_depth(child)
                    max_child_depth = max(max_child_depth, child_depth)
                else:
                    # 对非列表元素递归检查其子元素
                    child_depth = get_max_depth(child)
                    max_child_depth = max(max_child_depth, child_depth)
            return max_child_depth
        return get_max_depth(list_ele) + 1

    def __extract_list_item_text(self, root: HtmlElement) -> list[list]:
        """提取列表项的文本.
        列表项里的文本的分段策略采用最简单的方式：
        1. 遇到<br/>标签，则认为是一个段落结束。

        Args:
            item: 一个列表项。例如<li>

        Returns:
            list[dict]: 列表项的文本
        """
        text_paragraph = []

        def __extract_list_item_text_recusive(el: HtmlElement) -> list[list]:
            paragraph = []

            # 标记当前元素是否是sub或sup类型
            is_sub_sup = el.tag == 'sub' or el.tag == 'sup'

            if el.tag == CCTag.CC_MATH_INLINE:
                paragraph.append({'c': el.text, 't': ParagraphTextType.EQUATION_INLINE})
            elif el.tag == CCTag.CC_CODE_INLINE:
                paragraph.append({'c': el.text, 't': ParagraphTextType.CODE_INLINE})
            elif el.tag == 'br':
                if len(paragraph) > 0:
                    text_paragraph.append(paragraph)
                    paragraph = []
            elif el.tag == 'sub' or el.tag == 'sup':
                # 处理sub和sup标签，转换为GitHub Flavored Markdown格式
                current_text = ''
                if len(paragraph) > 0 and paragraph[-1]['t'] == ParagraphTextType.TEXT:
                    current_text = paragraph[-1]['c']
                    paragraph.pop()

                processed_text = process_sub_sup_tags(el, current_text, recursive=False)
                if processed_text:
                    paragraph.append({'c': processed_text, 't': ParagraphTextType.TEXT})
            else:
                if el.text and el.text.strip():
                    paragraph.append({'c': el.text, 't': ParagraphTextType.TEXT})
                for child in el.getchildren():
                    p = __extract_list_item_text_recusive(child)
                    if len(p) > 0:
                        paragraph.extend(p)

            # 处理尾部文本
            if el.tag != 'li' and el.tail and el.tail.strip():
                if is_sub_sup:
                    # 如果尾部文本跟在sub/sup后面，直接附加到最后一个文本段落中
                    if len(paragraph) > 0 and paragraph[-1]['t'] == ParagraphTextType.TEXT:
                        paragraph[-1]['c'] += el.tail
                    else:
                        paragraph.append({'c': el.tail, 't': ParagraphTextType.TEXT})
                else:
                    paragraph.append({'c': el.tail, 't': ParagraphTextType.TEXT})

            return paragraph

        if paragraph := __extract_list_item_text_recusive(root):
            if len(paragraph) > 0:
                text_paragraph.append(paragraph)
        return text_paragraph

    def __get_attribute(self, html: HtmlElement) -> Tuple[bool, dict, str]:
        """获取element的属性.

        Args:
            html:

        Returns:
            Tuple[str]: 第一个元素是是否有序; 第二个元素是个python list，内部是文本和行内公式，具体格式参考list的content_list定义。第三个元素是列表原始的html内容
        """
        # ele = self._build_html_tree(html)
        ele = html
        if ele is not None and ele.tag == CCTag.CC_LIST:
            ordered = ele.attrib.get('ordered', 'False') in ['True', 'true']
            content_list = json.loads(ele.text)
            raw_html = ele.attrib.get('html')
            list_nest_level = ele.attrib.get('list_nest_level', 0)
            return ordered, content_list, raw_html, list_nest_level
        else:
            raise HtmlListRecognizerException(f'{html}中没有cclist标签')
