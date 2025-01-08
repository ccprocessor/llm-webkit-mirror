from lxml import etree
from lxml import html as lhtml
from lxml.etree import _Element as Element


def build_html_tree(html:str) -> Element:
    """构建html树.

    Args:
        html: str: 完整的html源码

    Returns:
        etree._Element: html树
    """
    parser = etree.HTMLParser(collect_ids=False, encoding='utf-8', remove_comments=True, remove_pis=True)
    root = etree.HTML(html, parser)
    return root


def build_html_element_from_string(html:str) -> Element:
    """构建html元素.

    Args:
        html: str: html字符串

    Returns:
        etree._Element: html元素
    """
    return lhtml.fromstring(html)


def element_to_html(element : Element) -> str:
    """将element转换成html字符串.

    Args:
        element: etree._Element: element

    Returns:
        str: html字符串
    """
    return etree.tostring(element, encoding='utf-8').decode()


def build_cc_element(html_tag_name: str, text: str, tail: str, **kwargs) -> Element:
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
    parser = etree.HTMLParser(collect_ids=False, encoding='utf-8', remove_comments=True, remove_pis=True)
    cc_element = parser.makeelement(html_tag_name, attrib)
    cc_element.text = text
    cc_element.tail = tail
    return cc_element
