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
