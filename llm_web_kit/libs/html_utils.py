
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
    return root


def element_to_html(element : HtmlElement) -> str:
    """将element转换成html字符串.

    Args:
        element: lxml.html.HtmlElement: element

    Returns:
        str: html字符串
    """
    return tostring(element, encoding='utf-8').decode()


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


def replace_element(element: HtmlElement, cc_element: HtmlElement) -> None:
    """替换element为cc_element.

    Args:
        element: lxml.html.HtmlElement: 要替换的元素
        cc_element: lxml.html.HtmlElement: 替换后的元素
    """
    # 清空element的子元素
    if element.getparent() is not None:
        element.getparent().replace(element, cc_element)
    else:
        element.tag = cc_element.tag
        element.text = cc_element.text
        element.attrib = cc_element.attrib
        element.tail = cc_element.tail
