import html
import re
from copy import deepcopy

from lxml.html import HtmlElement, HTMLParser, fromstring, tostring


def html_to_element(html:str) -> HtmlElement:
    """构建html树.

    Args:
        html: str: 完整的html源码

    Returns:
        element: lxml.html.HtmlElement: element
    """
    parser = HTMLParser(collect_ids=False, encoding='utf-8', remove_comments=True, remove_pis=True)
    # 将 HTML 字符串编码为字节类型, 兼容html中有 XML 声明（如 <?xml version="1.0" encoding="utf-8"?>）
    html_bytes = html.encode('utf-8')
    root = fromstring(html_bytes, parser=parser)
    standalone = deepcopy(root)  # 通过拷贝才能去掉自动加入的<html><body>等标签， 非常奇怪的表现。
    return standalone


def element_to_html(element : HtmlElement) -> str:
    """将element转换成html字符串.

    Args:
        element: lxml.html.HtmlElement: element

    Returns:
        str: html字符串
    """
    s = tostring(element, encoding='utf-8').decode()
    return s


def element_to_html_unescaped(element : HtmlElement) -> str:
    """将element转换成html字符串并保持标签不被转义.

    Args:
        element: lxml.html.HtmlElement: element

    Returns:
        str: html字符串
    """
    s = element_to_html(element)
    return html.unescape(s)


def build_cc_element(html_tag_name: str, text: str, tail: str, **kwargs) -> HtmlElement:
    """构建cctitle的html. 例如：<cctitle level=1>标题1</cctitle>

    Args:
        html_tag_name: str: html标签名称，例如 'cctitle'
        text: str: 标签的文本内容
        tail: str: 标签后的文本内容
        **kwargs: 标签的其他属性，例如 level='1', html='<h1>标题</h1>' 等

    Returns:
        str: cctitle的html
    """
    attrib = {k:str(v) for k,v in kwargs.items()}
    parser = HTMLParser(collect_ids=False, encoding='utf-8', remove_comments=True, remove_pis=True)
    cc_element = parser.makeelement(html_tag_name, attrib)
    cc_element.text = text
    cc_element.tail = tail
    return cc_element


def get_element_text(element: HtmlElement) -> str:
    """
    获取这个节点下，包括子节点的所有文本.
    Args:
        element:

    Returns:

    """
    text = ''.join(element.itertext())
    return text


def replace_element(old_element: HtmlElement, new_element: HtmlElement) -> None:
    """替换element为cc_element.

    Args:
        old_element: HtmlElement: 要替换的元素
        new_element: HtmlElement: 替换的元素
    """
    if old_element.getparent() is not None:
        old_element.getparent().replace(old_element, new_element)
    else:
        old_element.tag = new_element.tag
        old_element.text = new_element.text
        for k,_ in old_element.attrib.items():
            del old_element.attrib[k]
        for k, v in new_element.attrib.items():
            old_element.attrib[k] = v
        old_element.tail = new_element.tail
        for child in new_element:
            old_element.append(child)


def iter_node(element: HtmlElement):
    """迭代html树.

    Args:
        element: lxml.html.HtmlElement: html树

    Returns:
        generator: 迭代html树
    """
    yield element
    for sub_element in element:
        if isinstance(sub_element, HtmlElement):
            yield from iter_node(sub_element)


def _escape_table_cell(text: str) -> str:
    """转义表格单元格中的特殊字符.

    比如 |、内容中的\n等
    """
    # 首先处理换行符，将其替换为空格
    text = re.sub(r'[\r\n]+', ' ', text)
    # 转义竖线和点号，避免与markdown表格语法冲突
    escaped = text.replace('|', '\\|')
    return escaped


def html_to_markdown_table(table_html_source: str) -> str:
    """把html代码片段转换成markdown表格.

    Args:
        table_html_source: 被<table>标签包裹的html代码片段(含<table>标签)

    Returns: 如果这个表格内没有任何文字性内容，则返回空字符串
    """
    # 解析HTML
    table_el = html_to_element(table_html_source)
    rows = table_el.xpath('.//tr')
    if not rows:
        return ''

    # 确定最大列数
    max_cols = 0
    for row in rows:
        cols = row.xpath('.//th | .//td')
        max_cols = max(max_cols, len(cols))

    if max_cols == 0:
        return ''
    markdown_table = []
    first_row = rows[0]
    # 检查第一行是否是表头并获取表头内容
    first_row_tags = first_row.xpath('.//th | .//td')
    if not first_row_tags:
        # 如果第一行没有td/th，则取整行内容作为表头
        headers = [_escape_table_cell(first_row.text_content().strip())]
    else:
        headers = [_escape_table_cell(tag.text_content().strip()) for tag in first_row_tags]
    # 如果表头存在，添加表头和分隔符，并保证表头与最大列数对齐
    if headers:
        while len(headers) < max_cols:
            headers.append('')  # 补充空白表头
        markdown_table.append('| ' + ' | '.join(headers) + ' |')
        markdown_table.append('|---' * max_cols + '|')
    else:
        # 如果没有明确的表头，创建默认表头
        default_headers = [''] * max_cols
        markdown_table.append('| ' + ' | '.join(default_headers) + ' |')
        markdown_table.append('|---' * max_cols + '|')

    # 添加表格内容，跳过已被用作表头的第一行（如果有的话）
    for row in rows[1:]:
        cells = row.xpath('.//td | .//th')
        if not cells:  # 无td/th时取整行内容，放到第一个单元格
            columns = [_escape_table_cell(row.text_content().strip())]
        else:
            columns = [_escape_table_cell(cell.text_content().strip()) for cell in cells]
        while len(columns) < max_cols:
            columns.append('')
        markdown_table.append('| ' + ' | '.join(columns) + ' |')

    md_str = '\n'.join(markdown_table)
    return md_str.strip()


def table_cells_count(table_html_source: str) -> int:
    """获取表格的单元格数量.
    当只有1个单元格时，这个table就要被当做普通的一个段落处理。
    Args:
        table_html_source: str: 被<table>标签包裹的html代码片段(含<table>标签)

    Returns:
        int: 单元格数量
    """
    table_el = html_to_element(table_html_source)
    # 计算 <table> 中的 <td> 和 <th> 单元格数量
    cells = table_el.xpath('.//td | .//th')
    number_of_cells = len(cells)
    return number_of_cells


def convert_html_to_entity(html_source) -> str:
    """html中的特殊字符转成实体标记."""
    table_entity = html.escape(html_source)
    return table_entity


def convert_html_entity_to_str(html_str):
    """将HTML实体转换回原始字符."""
    result = html.unescape(html_str)
    return result


def remove_element(element: HtmlElement):
    """删除节点.

    删除节点时，保留节点后的tail文本

    Args:
        element: HtmlElement
    """
    parent = element.getparent()
    if parent is None:
        return

    if element.tail:
        previous = element.getprevious()
        if previous is None:
            parent.text = (parent.text or '') + element.tail
        else:
            previous.tail = (previous.tail or '') + element.tail

    parent.remove(element)
