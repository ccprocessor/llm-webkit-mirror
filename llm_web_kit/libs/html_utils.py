
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
    root = fromstring(html, parser=parser)
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


def html_to_markdown_table(table_html_source: str) -> str:
    """把html代码片段转换成markdown表格.

    Args:
        table_html_source:

    Returns:  如果这个表格内没有任何文字性内容，则返回空字符串
    """
    table_el = html_to_element(table_html_source)
    rows = table_el.xpath('.//tr')
    markdown_table = []

    # 检查第一行是否是表头
    first_row_tags = rows[0].xpath('.//th') or rows[0].xpath('.//td')
    headers = [tag.text_content().strip() for tag in first_row_tags]

    # 添加表头
    markdown_table.append('| ' + ' | '.join(headers) + ' |')
    # 添加表头下的分隔符
    markdown_table.append('|' + '|'.join(['---'] * len(headers)) + '|')

    # 添加表格内容，跳过第一行如果它被当作表头
    for row in rows[1 if first_row_tags[0].tag == 'th' else 0:]:
        columns = [td.text_content().strip() for td in row.xpath('.//td')]
        markdown_table.append('| ' + ' | '.join(columns) + ' |')

    md_str = '\n'.join(markdown_table)
    return md_str.strip()
