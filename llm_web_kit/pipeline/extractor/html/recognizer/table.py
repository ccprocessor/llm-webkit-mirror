from typing import List, Tuple

from lxml import etree, html
from overrides import override

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
            if self.is_contain_cc_html(cc_html):
                final_result.append(cc_html)
                continue
            tree = html.fromstring(cc_html)
            if not self.is_contain_table(tree):
                final_result.append(cc_html)
            else:
                final_result.extend(self.contain_table_elements(tree))
        merged_cc_html = self.merge_html_fragments(final_result)
        # print(merged_cc_html)
        final_html = BaseHTMLElementRecognizer.html_split_by_tags(merged_cc_html, 'cctable')
        return final_html

    @override
    def to_content_list_node(self, base_url: str, parsed_content: str, raw_html_segment: str) -> dict:
        table_node: etree._Element = etree.fromstring(parsed_content, None)

        d = {
            'type': 'table',
            # "bbox": [],
            'raw_content': raw_html_segment,
            'content': {
                'html': table_node.text,
            },
        }
        if is_complex := table_node.get('is_complex', None):
            d['content']['is_complex'] = is_complex
        return d

    def merge_html_fragments(self, html_list):
        """合并html 片段."""
        merged_html = ''.join(html_list)
        return merged_html

    def is_contain_cc_html(self, cc_html: str) -> bool:
        """判断html片段是否是cc标签."""
        return BaseHTMLElementRecognizer.is_cc_html(cc_html)

    def is_contain_table(self, tree):
        """html中是否包含table标签."""
        # 解析html
        tables = tree.xpath('//table')
        if tables:
            return True
        else:
            return False

    def is_simple_table(self, tree) -> bool:
        """处理table元素，判断是是否复杂：是否包含合并单元格."""
        cells = tree.xpath('//td | //th')
        for cell in cells:
            colspan = cell.get('colspan', '1')
            rowspan = cell.get('rowspan', '1')
            # 如果 colspan 或 rowspan 存在且大于1，则认为是合并单元格
            if (int(colspan) > 1) or (int(rowspan) > 1):
                return False
            else:
                return True

    def is_table_contain_img(self, tree) -> bool:
        """判断table元素是否包含图片."""
        imgs = tree.xpath('//table//img')
        if imgs:
            return False
        else:
            return True

    def is_table_nested(self, tree) -> bool:
        """判断table元素是否嵌套."""
        nested_tables = tree.xpath('//table//table')
        if nested_tables:
            return False
        else:
            return True

    def contain_table_elements(self, tree) -> List[str]:
        """判断html中是否包含table元素并返回修改后的HTML.

        Args:
            tree: HTML树结构

        Returns:
            List[str]: 每个元素是一个列表 (处理后的HTML片段)
        """
        result = list()

        # 解析HTML字符串为树结构
        def process_direct_children(element):
            for child in element.iterchildren():
                if child.tag == 'table':
                    original_table_html = html.tostring(child, encoding='unicode', method='html')
                    if self.is_simple_table(child) and self.is_table_nested(original_table_html) and self.is_table_contain_img(original_table_html):
                        table_type = 'simple'
                    else:
                        table_type = 'complex'
                    # 保留原来的Html
                    new_table_html = ''.join([html.tostring(table_child, encoding='unicode') for table_child in child])
                    cc_table = f"<{CCTag.CC_TABLE} type='{table_type}' html='{original_table_html}'>'{new_table_html}'</{CCTag.CC_TABLE}>"
                    result.append(cc_table)
                else:
                    result.append(html.tostring(child, encoding='unicode'))
                    process_direct_children(child)

        process_direct_children(tree)
        if not tree.find('body') and not tree.body:
            for child in tree:
                process_direct_children(child)

        return result


if __name__ == '__main__':
    recognizer = TableRecognizer()
    base_url = 'https://www.baidu.com'
    main_html_lst = [
        ('<cccode>hello</cccode>',
         '<code>hello</code>'),
        ("""<div><p>段落2</p><table><tr><td rowspan='2'>1</td><td>2</td></tr><tr><td>3</td></tr></table><p>段落2</p><table><tr><td rowspan='2'>1</td><td>2</td></tr><tr><td>3</td></tr></table></div>""",
         """<div><p>段落2</p><table><tr><td rowspan='2'>1</td><td>2</td></tr><tr><td>3</td></tr></table><p>段落2</p><table><tr><td rowspan='2'>1</td><td>2</td></tr><tr><td>3</td></tr></table></div>""",
         )]
    raw_html = (
        """<div><p>段落2</p><table><tr><td rowspan='2'>1</td><td>2</td></tr>"""
        """<tr><td>3</td></tr></table><p>段落2</p><table><tr>"""
        """<td rowspan='2'>1</td><td>2</td></tr><tr><td>3</td></tr></table></div>"""
    )
    print(recognizer.recognize(base_url, main_html_lst, raw_html=''))
