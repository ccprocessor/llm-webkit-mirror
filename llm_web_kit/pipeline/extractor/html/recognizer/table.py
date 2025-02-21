from typing import List, Tuple

from lxml.html import HtmlElement
from overrides import override

from llm_web_kit.exception.exception import HtmlTableRecognizerExp
from llm_web_kit.libs.doc_element_type import DocElementType
from llm_web_kit.pipeline.extractor.html.recognizer.recognizer import (
    BaseHTMLElementRecognizer, CCTag)


class TableRecognizer(BaseHTMLElementRecognizer):
    """解析table元素."""

    def __init__(self):
        super().__init__()

    @override
    def recognize(self,
                  base_url: str,
                  main_html_lst: List[Tuple[str, str]],
                  raw_html: str) -> List[Tuple[str, str]]:
        """父类，解析表格元素.

        Args:
            base_url: str: 基础url
            main_html_lst: main_html在一层一层的识别过程中，被逐步分解成不同的元素
            raw_html: 原始完整的html

        Returns:
        """
        final_result = list()
        for cc_html, o_html in main_html_lst:
            if self.__is_contain_cc_html(cc_html):
                final_result.append((cc_html, o_html))
            else:
                lst = self.__extract_tables(cc_html)
                final_result.extend(lst)
        return final_result

    @override
    def to_content_list_node(self, base_url: str, parsed_content: str, raw_html_segment: str) -> dict:
        if not parsed_content:
            raise HtmlTableRecognizerExp(f'table parsed_content{parsed_content}为空')
        table_type, table_body = self.__get_attribute(parsed_content)
        d = {
            'type': DocElementType.TABLE,
            # "bbox": [],
            'raw_content': raw_html_segment,
            'content': {
                'html': table_body,
            },
        }
        d['content']['is_complex'] = table_type
        return d

    def __is_contain_cc_html(self, cc_html: str) -> bool:
        """判断html片段是否是cc标签."""
        return BaseHTMLElementRecognizer.is_cc_html(cc_html)

    def __is_table_empty(self, table) -> bool:
        """检查表格是否为空（递归检查嵌套元素）

        :param table: lxml.html.HtmlElement 对象，表示一个 <table> 元素
        :return: 如果表格为空，返回 True；否则返回 False
        """
        def is_element_empty(elem):
            # 检查元素本身的文本内容
            if elem.text and elem.text.strip():
                return False
            # 检查所有子元素
            for child in elem.iterchildren():
                # 如果是嵌套表格，递归检查表格是否为空
                if child.tag == 'table':
                    if not self.__is_table_empty(child):
                        return False
                # 其他元素需要递归检查
                elif not is_element_empty(child):
                    return False
            # 检查尾部文本（如 </div> 后的文本）
            if elem.tail and elem.tail.strip():
                return False
            return True
        # 检查所有单元格
        for cell in table.xpath('.//td | .//th'):
            # 检查单元格内容
            if cell.text and cell.text.strip():
                return False
            # 递归检查子元素
            if not is_element_empty(cell):
                return False
        return True

    def __is_simple_table(self, tree) -> bool:
        """处理table元素，判断是是否复杂：是否包含合并单元格."""
        cells = tree.xpath('.//td') + tree.xpath('.//th')
        for cell in cells:
            colspan_str = cell.get('colspan', '1')
            rowspan_str = cell.get('rowspan', '1')
            try:
                colspan = int(colspan_str)
                rowspan = int(rowspan_str)
            except ValueError as e:
                raise HtmlTableRecognizerExp(f'table的合并单元格属性值colspan:{colspan_str}或rowspan:{rowspan_str}不是有效的整数') from e
            if (colspan > 1) or (rowspan > 1):
                return False
        return True

    def __is_table_contain_img(self, tree) -> bool:
        """判断table元素是否包含图片."""
        imgs = tree.xpath('//table//img')
        if len(imgs) == 0:
            return True
        else:
            return False

    def __is_table_nested(self, tree) -> bool:
        """判断table元素是否嵌套."""
        nested_tables = tree.xpath('//table//table')
        if len(nested_tables) == 0:
            return True
        else:
            return False

    def __extract_tables(self, ele: HtmlElement) -> List[str]:
        """提取html中的table元素."""
        tree = self._build_html_tree(ele)
        self.__do_extract_tables(tree)
        new_html = self._element_to_html(tree)
        lst = self.html_split_by_tags(new_html, CCTag.CC_TABLE)
        return lst

    def __get_table_type(self, child: HtmlElement) -> str:
        """获取table的类型."""
        empty_flag = self.__is_table_empty(child)
        if empty_flag:
            return 'empty'
        flag = self.__is_simple_table(child) and self.__is_table_nested(child)
        if flag:
            table_type = 'simple'
        else:
            table_type = 'complex'
        return table_type

    def __extract_table_element(self, ele: HtmlElement) -> str:
        """提取表格的元素."""
        for item in ele.iterchildren():
            return self._element_to_html(item)

    def __simplify_td_th_content(self, elem):
        """简化 <td> 和 <th> 内容，仅保留文本内容."""
        if elem.tag in ['td', 'th'] and len(elem.xpath('.//table')) == 0:
            result = '<br>'.join([text for text in elem.itertext() if text.strip()])
            for child in list(elem):
                elem.remove(child)
            elem.text = result
        elif elem.tag in ['td', 'th'] and len(elem.xpath('.//table')) > 0:
            for item in elem.iterchildren():
                self.__simplify_td_th_content(item)

    def __get_table_body(self, table_type, table_root):
        """获取并处理table body，返回处理后的HTML字符串。"""
        if table_type == 'empty':
            return None
        allowed_attributes = ['colspan', 'rowspan']
        for child in list(table_root.iterchildren()):
            if child.tag is not None:
                self.__get_table_body(table_type, child)
        for ele in table_root.iter('td', 'th'):
            self.__simplify_td_th_content(ele)
        if len(table_root.attrib) > 0:
            cleaned_attrs = {k: v for k, v in table_root.attrib.items() if k in allowed_attributes}
            table_root.attrib.clear()
            table_root.attrib.update(cleaned_attrs)
        if table_root.text is not None:
            table_root.text = table_root.text.strip()
        for elem in table_root.iter():
            if elem.tail is not None:
                elem.tail = elem.tail.strip()
        return self._element_to_html(table_root)

    def __do_extract_tables(self, root: HtmlElement) -> None:
        """递归处理所有子标签."""
        if root.tag in ['table']:
            table_raw_html = self._element_to_html(root)
            table_type = self.__get_table_type(root)
            tail_text = root.tail
            table_body = self.__get_table_body(table_type, root)
            cc_element = self._build_cc_element(
                CCTag.CC_TABLE, table_body, tail_text, table_type=table_type, html=table_raw_html)
            self._replace_element(root, cc_element)
            return
        for child in root.iterchildren():
            self.__do_extract_tables(child)

    def __get_attribute(self, html: str) -> Tuple[int, str]:
        """获取element的属性."""
        ele = self._build_html_tree(html)
        if ele is not None and ele.tag == CCTag.CC_TABLE:
            table_type = ele.attrib.get('table_type')
            table_flag = self.__get_content_list_table_type(table_type)
            table_body = ele.text
            return table_flag, table_body
        else:
            raise HtmlTableRecognizerExp(f'{html}中没有cctable标签')

    def __get_content_list_table_type(self, table_type):
        """complex|simple 转为True|False."""
        is_complex = False
        if table_type == 'simple':
            is_complex = False
        elif table_type == 'complex':
            is_complex = True
        return is_complex
