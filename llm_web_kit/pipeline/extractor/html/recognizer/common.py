import re

from lxml import etree
from lxml.html import HtmlElement
from py_asciimath.translator.translator import ASCIIMath2Tex

asciimath2tex = ASCIIMath2Tex(log=False)
color_regex = re.compile(r'\\textcolor\[.*?\]\{.*?\}')


def extract_asciimath(s: str) -> str:
    parsed = asciimath2tex.translate(s)
    return parsed


def text_strip(text):
    return text.strip() if text else text


def wrap_math(s, display=False):
    s = re.sub(r'\s+', ' ', s)
    s = color_regex.sub('', s)
    s = s.replace('$', '')
    s = s.replace('\n', ' ').replace('\\n', '')
    s = s.strip()
    if len(s) == 0:
        return s
    # Don't wrap if it's already in \align
    if 'align' in s:
        return s
    if display:
        return '$$' + s + '$$'
    return '$' + s + '$'


def parse_html(html_str: str) -> HtmlElement:
    """将html str转为 HtmlElement.

    Args:
        html_str: 网页str

    Returns:
        HtmlElement
    """
    parser = etree.HTMLParser(collect_ids=False, encoding='utf-8', remove_comments=True, remove_pis=True)
    tree = etree.HTML(html_str, parser)
    return tree
