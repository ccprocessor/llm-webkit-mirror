from typing import List, Tuple

from lxml.html import HtmlElement
from overrides import override

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
            raise ValueError(f'table parsed_content{parsed_content}为空')
        table_type, table_body = self.__get_attribute(parsed_content)
        if not table_type or not table_body:
            raise ValueError(f'get table attribute为空,table_body:{table_body},table_type:{table_type}')
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

    def __is_simple_table(self, tree) -> bool:
        """处理table元素，判断是是否复杂：是否包含合并单元格."""
        cells = tree.xpath('//td | //th')
        if len(cells) == 0:
            raise ValueError(f'table节点未通过xpath定位到td或者th标签, cell长度为{len(cells)}')
        for cell in cells:
            colspan_str = cell.get('colspan', 1)
            rowspan_str = cell.get('rowspan', 1)
            try:
                # 尝试将属性值转换为整数
                colspan = int(colspan_str)
                rowspan = int(rowspan_str)
            except ValueError:
                raise ValueError(f'table的合并单元格属性值colspan:{colspan_str}或rowspan:{rowspan_str}不是有效的整数')
            # 如果 colspan 或 rowspan 存在且大于1，则认为是合并单元格, 否则认为是简单格式的单元格
            if (colspan > 1) or (rowspan > 1):
                return False
            elif (colspan == 1) and (rowspan == 1):
                return True
            else:
                raise ValueError(f'table的合并单元格属性值colspan:{colspan}和rowspan:{rowspan}异常')

    def __is_table_contain_img(self, tree) -> bool:
        """判断table元素是否包含图片."""
        imgs = tree.xpath('//table//img')
        if len(imgs) == 0:
            return False
        else:
            return True

    def __is_table_nested(self, tree) -> bool:
        """判断table元素是否嵌套."""
        nested_tables = tree.xpath('//table//table')
        if len(nested_tables) == 0:
            return False
        else:
            return True

    def __extract_tables(self, ele: HtmlElement) -> List[str]:
        """提取html中的table元素."""
        tree = self._build_html_tree(ele)
        self.__do_extract_tables(tree)
        new_html = self._element_to_html(tree)
        lst = self.html_split_by_tags(new_html, CCTag.CC_TABLE)
        return lst

    def __get_table_type(self, child: HtmlElement) -> str:
        """获取table的类型."""
        flag = self.__is_simple_table(child) or self.__is_table_nested(child) or self.__is_table_contain_img(child)
        if flag:
            table_type = 'simple'
        else:
            table_type = 'complex'
        return table_type

    def __extract_table_element(self, ele: HtmlElement) -> str:
        """提取表格的元素."""
        for item in ele.iterchildren():
            return self._element_to_html(item)

    def __do_extract_tables(self, root: HtmlElement) -> None:
        """递归处理所有子标签."""
        if root.tag in ['table']:
            table_raw_html = self._element_to_html(root)
            table_type = self.__get_table_type(root)
            tail_text = root.tail
            table_body = self.__extract_table_element(root)
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
            tale_body = ele.text
            return table_type, tale_body
        else:
            raise ValueError(f'{html}中没有cctable标签')


if __name__ == '__main__':
    recognizer = TableRecognizer()
    base_url = 'https://www.baidu.com'
    main_html_lst = [
        ('<cccode>hello</cccode>',
         '<code>hello</code>'),
        (
            """<div><p>段落2</p><table><tr><td rowspan='2'>1</td><td>2</td></tr><tr><td>3</td></tr></table><p>段落2</p><table><tr><td rowspan='2'>1</td><td>2</td></tr><tr><td>3</td></tr></table></div>""",
            """<div><p>段落2</p><table><tr><td rowspan='2'>1</td><td>2</td></tr><tr><td>3</td></tr></table><p>段落2</p><table><tr><td rowspan='2'>1</td><td>2</td></tr><tr><td>3</td></tr></table></div>""",
        )]
    raw_html = (
        """<div><p>段落2</p><table><tr><td rowspan='2'>1</td><td>2</td></tr>"""
        """<tr><td>3</td></tr></table><p>段落2</p><table><tr>"""
        """<td rowspan='2'>1</td><td>2</td></tr><tr><td>3</td></tr></table></div>"""
    )
    print(recognizer.recognize(base_url, main_html_lst, raw_html=''))
