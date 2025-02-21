import re

from lxml import html


def extract_tag_text(element: html.HtmlElement) -> str:
    """Extract text from an html element.

    Args:
        element (html.HtmlElement): The element to extract text from

    Returns:
        str: The text extracted from the element
    """
    # 如果元素是img标签，返回其alt属性
    if element.tag == 'img':
        return element.get('alt', '')

    # 如果元素没有子节点，返回其文本
    if len(element) == 0:
        return element.text if element.text else ''

    # 如果元素有子节点，递归提取每个子节点的文本，并根据元素类型决定是否添加换行符
    newline_tags = ['p', 'br', 'div', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'tr']
    texts = []
    if element.text:  # 添加未被标签包裹的文本
        texts.append(element.text)
    for child in element:
        child_text = extract_tag_text(child)
        if child.tag in newline_tags:
            child_text += '\n'
        texts.append(child_text)
        if child.tail:  # 添加标签后的文本
            texts.append(child.tail)
    # 将只有空格的行变成空行
    texts = [text if text.strip() else '\n' for text in texts]
    # 使用正则表达式将连续的换行符替换为一个
    return re.sub('\n+', '\n', ''.join(texts))


def get_title(root: html.HtmlElement) -> str:
    """Get the title of the html page.

    Args:
        root (html.HtmlElement): The root of the html page

    Returns:
        str: The title of the html page
    """
    title = root.xpath('//title/text()')

    return title[0] if len(title) > 0 else None


def remove_blank_text(root: html.HtmlElement):
    """Remove blank text in html element. Skip <pre> tag and <code> tag and
    there children.

    Args:
        root (html.HtmlElement): The root of the html page

    Returns:
        html.HtmlElement: The root of the html page after removing blank text
    """

    skip_elements = set()
    for element in root.iter():
        if element.tag in ['pre', 'code']:
            skip_elements.add(element)
            skip_elements.update(element.iterdescendants())

    for element in root.iter():
        if element in skip_elements:
            continue
        if element.text and not element.text.strip():
            element.text = None
        if element.tail and not element.tail.strip():
            element.tail = None
    return root


def document_fromstring(html_str: str):
    """Parse html string to lxml.html.HtmlElement default remove blank text,
    comments, processing instructions.

    Args:
        html_str (str): The html string to parse

    Returns:
        html.HtmlElement: The root of the html page
    """
    parser = html.HTMLParser(
        remove_blank_text=True, remove_comments=True, remove_pis=True
    )
    root = html.document_fromstring(html_str, parser=parser)
    root = remove_blank_text(root)
    return root
