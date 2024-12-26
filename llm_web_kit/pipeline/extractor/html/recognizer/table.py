from typing import List, Tuple

from bs4 import BeautifulSoup, Tag
from overrides import override

from llm_web_kit.pipeline.extractor.html.recognizer.recognizer import \
    BaseHTMLElementRecognizer


class TableRecognizer(BaseHTMLElementRecognizer):
    """解析table元素."""

    def __init__(self):
        super().__init__()

    @override
    def recognize(self,
                  base_url: str,
                  main_html_lst: List[Tuple[str,
                                            str]],
                  raw_html: str) -> List[Tuple[str,
                                               str]]:
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
                final_result.append((cc_html, o_html))
                continue
            for has_table, cc_table, o_table in self.contain_table_elements(
                    cc_html):
                final_result.append((cc_table, o_table))
        return final_result

    def is_contain_cc_html(self, html: str) -> bool:
        """判断html片段是否是cc标签."""
        return html.startswith('<cc')

    def contain_table_elements(
            self, raw_html: str) -> List[Tuple[bool, str, str]]:
        """判断html中是否包含table元素并返回修改后的HTML.

        Args:
            raw_html (str): 原始html

        Returns:
            List[Tuple[bool, str, str]]: 每个元素是一个三元组 (是否是表格, 处理后的HTML片段, 原始HTML片段)
        """
        soup = BeautifulSoup(raw_html, 'html.parser')
        result = list()

        def process_direct_children(element):
            for child in element.children:
                if isinstance(child, Tag):
                    if child.name == 'table':
                        table_type = 'simple'
                        for td in child.find_all('td', recursive=True):
                            if int(td.get('rowspan', 1)) > 1 or int(td.get('colspan', 1)) > 1:
                                table_type = 'complex'
                                break
                        cc_table = f'<cctable type="{table_type}">{child.decode()}</cctable>'
                        o_table = str(child)
                        result.append((True, cc_table, o_table))
                    else:
                        process_direct_children(child)
                elif str(element).strip():
                    result.append((False, str(element), str(element)))
        for child in soup.body.children if soup.body else soup.children:
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
    print(recognizer.recognize(base_url, main_html_lst, raw_html=''))
