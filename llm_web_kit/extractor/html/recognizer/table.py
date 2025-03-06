from itertools import chain
from typing import Any, List, Tuple

from lxml.html import HtmlElement
from overrides import override
import json
from llm_web_kit.exception.exception import HtmlTableRecognizerException
from llm_web_kit.extractor.html.recognizer.cccode import CodeRecognizer
from llm_web_kit.extractor.html.recognizer.ccmath import MathRecognizer
from llm_web_kit.extractor.html.recognizer.recognizer import (
    BaseHTMLElementRecognizer, CCTag)
from llm_web_kit.libs.doc_element_type import DocElementType


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
            raise HtmlTableRecognizerException(f'table parsed_content{parsed_content}为空')
        table_type, table_nest_level, table_body = self.__get_attribute(parsed_content)
        d = {
            'type': DocElementType.TABLE,
            # "bbox": [],
            'raw_content': raw_html_segment,
            'content': {
                'html': table_body,
            },
        }
        d['content']['is_complex'] = table_type
        d['content']['table_nest_level'] = table_nest_level
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
                raise HtmlTableRecognizerException(
                    f'table的合并单元格属性值colspan:{colspan_str}或rowspan:{rowspan_str}不是有效的整数') from e
            if (colspan > 1) or (rowspan > 1):
                return False
        return True

    def __is_table_nested(self, element) -> int:
        """计算表格的嵌套层级（非表格返回0）"""
        if element.tag != "table":
            return 0
        # 获取当前表格下所有的表格（包括自身）
        all_tables = [element] + element.xpath('.//table')
        max_level = 1  # 初始层级为1（当前表格）
        # 计算每个表格的层级，取最大值
        for table in all_tables:
            ancestor_count = len(table.xpath('ancestor::table'))
            level = ancestor_count + 1
            max_level = max(max_level, level)
        return max_level

    def __extract_tables(self, ele: str) -> List[Tuple[str, str]]:
        """提取html中的table元素."""
        tree = self._build_html_tree(ele)
        self.__do_extract_tables(tree)
        new_html = self._element_to_html(tree)
        lst = self.html_split_by_tags(new_html, CCTag.CC_TABLE)
        return lst

    def __get_table_type(self, child: HtmlElement) -> str:
        """获取table的类型."""
        empty_flag = self.__is_table_empty(child)
        level = self.__is_table_nested(child)
        if empty_flag:
            return 'empty'
        # 是否跨行跨列
        flag = (self.__is_simple_table(child) and level < 2)
        if flag:
            table_type = 'simple'
        else:
            table_type = 'complex'
        return table_type


    def __check_table_include_math_code(self, raw_html: HtmlElement):
        """检查table中的内容，包括普通文本、数学公式和代码."""
        math_html = self._element_to_html(raw_html)
        # 处理数学公式和代码
        math_recognizer = MathRecognizer()
        math_res_parts = math_recognizer.recognize(base_url='', main_html_lst=[(math_html, math_html)],
                                               raw_html=math_html)
        code_recognizer = CodeRecognizer()
        code_res_parts = code_recognizer.recognize(base_url='', main_html_lst=math_res_parts,
                                               raw_html=math_html)
        
        result = []
        for math_item in code_res_parts:
            ele_item = self._build_html_tree(math_item[0])
            # 处理所有文本内容
            for text_segment in ele_item.itertext():
                cleaned_text = text_segment.strip().replace('\\n', '')
                if cleaned_text:  # 过滤空字符串
                    #print("cleaned_text", cleaned_text)
                    result.append(cleaned_text)
            # 处理行内公式
            ccinline_math_node = ele_item.xpath(f'//{CCTag.CC_MATH_INLINE}')
            if ccinline_math_node:
                formulas = [
                    el.text.strip() for el in ccinline_math_node if el.text and el.text.strip()
                ]
                result.extend(formulas)
            
            # 处理行间公式
            ccinterline_math_node = ele_item.xpath(f'//{CCTag.CC_MATH_INTERLINE}')
            if ccinterline_math_node:
                formulas = [
                    el.text.strip() for el in ccinterline_math_node if el.text and el.text.strip()
                ]
                result.extend(formulas)
            
            # 处理行内代码
            ccinline_code_node = ele_item.xpath(f'//{CCTag.CC_CODE_INLINE}')
            if ccinline_code_node:
                codes = [
                    el.text.strip() for el in ccinline_code_node if el.text and el.text.strip()
                ]
                result.extend(codes)
            
            # 处理行间代码
            ccinterline_code_node = ele_item.xpath(f'//{CCTag.CC_CODE}')
            if ccinterline_code_node:
                codes = [
                    el.text.strip() for el in ccinterline_code_node if el.text and el.text.strip()
                ]
                result.extend(codes)
        
        return result

    def __simplify_td_th_content(self, elem: HtmlElement) -> None:
        """简化 <td> 和 <th> 内容，仅保留文本内容."""
        if elem.tag in ['td', 'th']:
            # 简化单元格中的元素
            parse_res = list()
            math_res = self.__check_table_include_math_code(elem)
            parse_res.extend(math_res)
            for item in list(elem.iterchildren()):
                elem.remove(item)
            if parse_res:
                elem.text = '<br>'.join(parse_res)
            return
        for child in elem.iter('td', 'th'):
            self.__simplify_td_th_content(child)

    def __get_table_body(self, table_type, table_root):
        """获取并处理table body，返回处理后的HTML字符串。"""
        if table_type == 'empty':
            return None
        allowed_attributes = ['colspan', 'rowspan']
        # 清理除了colspan和rowspan之外的属性
        if len(table_root.attrib) > 0:
            cleaned_attrs = {k: v for k, v in table_root.attrib.items() if k in allowed_attributes}
            table_root.attrib.clear()
            table_root.attrib.update(cleaned_attrs)
        # text进行strip操作,tail保留（部分内容留在tail中）
        for elem in chain([table_root], table_root.iterdescendants()):
            if elem.text is not None:
                elem.text = elem.text.strip().replace('\\n', '')
            if elem.tail is not None:
                elem.tail = elem.tail.strip().replace('\\n', '')
        self.__simplify_td_th_content(table_root)
        # 迭代
        for child in table_root.iterchildren():
            if child is not None:
                self.__get_table_body(table_type, child)
        return self._element_to_html(table_root)

    def __do_extract_tables(self, root: HtmlElement) -> None:
        """递归处理所有子标签."""
        if root.tag in ['table']:
            table_raw_html = self._element_to_html(root)
            table_type = self.__get_table_type(root)
            table_nest_level = self.__is_table_nested(root)
            tail_text = root.tail
            table_body = self.__get_table_body(table_type, root)
            cc_element = self._build_cc_element(
                CCTag.CC_TABLE, table_body, tail_text, table_type=table_type, table_nest_level=table_nest_level,
                html=table_raw_html)
            self._replace_element(root, cc_element)
            return
        for child in root.iterchildren():
            self.__do_extract_tables(child)

    def __get_attribute(self, html: str) -> Tuple[bool, Any, Any]:
        """获取element的属性."""
        ele = self._build_html_tree(html)
        if ele is not None and ele.tag == CCTag.CC_TABLE:
            table_type = ele.attrib.get('table_type')
            table_nest_level = ele.attrib.get('table_nest_level')
            table_flag = self.__get_content_list_table_type(table_type)
            table_body = ele.text
            return table_flag, table_nest_level, table_body
        else:
            raise HtmlTableRecognizerException(f'{html}中没有cctable标签')

    def __get_content_list_table_type(self, table_type):
        """complex|simple 转为True|False."""
        is_complex = False
        if table_type == 'simple':
            is_complex = False
        elif table_type == 'complex':
            is_complex = True
        return is_complex
