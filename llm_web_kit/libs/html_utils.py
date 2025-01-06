from lxml import etree


def build_html_tree(html:str) -> etree._Element:
    """构建html树.

    Args:
        html: str: html字符串

    Returns:
        etree._Element: html树
    """
    parser = etree.HTMLParser(collect_ids=False, encoding='utf-8', remove_comments=True, remove_pis=True)
    root = etree.HTML(html, parser)
    return root


def element_to_html(element : etree._Element) -> str:
    """将element转换成html字符串.

    Args:
        element: etree._Element: element

    Returns:
        str: html字符串
    """
    return etree.tostring(element, encoding='utf-8').decode()
