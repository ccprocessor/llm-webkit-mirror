import re
from difflib import SequenceMatcher

import numpy as np
from lxml.html import HtmlElement, HTMLParser, fromstring, tostring

from llm_web_kit.extractor.html.magic_html.config import Unique_ID

HTML_PARSER = HTMLParser(
    collect_ids=False,
    default_doctype=False,
    encoding='utf-8',
    remove_comments=True,
    remove_pis=True,
)
DOCTYPE_TAG = re.compile('^< ?! ?DOCTYPE[^>]*/[^<]*>', re.I)
FAULTY_HTML = re.compile(r'(<html.*?)\s*/>', re.I)


def _tostring(string: HtmlElement) -> str:
    return tostring(string, encoding=str, method='html')


def lcs_of_2(a, b):
    match = SequenceMatcher(None, a, b).find_longest_match(0, len(a), 0, len(b))
    return a[match[0]: match[0] + match[2]]


def lcs_of_list(*args):
    if len(args) == 2:
        return lcs_of_2(args[0], args[1])
    first = args[0]
    remains = args[1:]
    return lcs_of_2(first, lcs_of_list(*remains))


def strip_faulty_doctypes(htmlstring: str, beginning: str) -> str:
    if 'doctype' in beginning:
        firstline, _, rest = htmlstring.partition('\n')
        htmlstring = DOCTYPE_TAG.sub('', firstline, count=1) + '\n' + rest
    for i, line in enumerate(iter(htmlstring.splitlines())):
        if '<html' in line and line.endswith('/>'):
            htmlstring = FAULTY_HTML.sub(r'\1>', htmlstring, count=1)
            break
        if i > 2:
            break
    return htmlstring


def ancestor_node_check(node: HtmlElement, tags: list):
    for tag in tags:
        if node.xpath(f'ancestor::{tag}[1]'):
            return True
    return False


def load_html(html_str: str) -> HtmlElement:
    """将html str转为 HtmlElement.

    Args:
        html_str: 网页str

    Returns:
        HtmlElement
    """
    beginning = html_str[:50].lower()
    html_str = strip_faulty_doctypes(html_str, beginning)
    html_bytes = html_str.encode('utf-8')
    tree = fromstring(html_bytes, parser=HTML_PARSER)
    return tree


def iter_node(element: HtmlElement):
    yield element
    for sub_element in element:
        if isinstance(sub_element, HtmlElement):
            yield from iter_node(sub_element)


def img_div_check(tree):
    """如果一个div中只有一张图，且子节点数小于4则保留."""

    if len(tree.xpath('.//img')) == 1 and len(tree.xpath('.//*')) < 4:
        return False
    else:
        return True


def text_len(s):
    s = re.sub(' +', ' ', s)  # 将连续的多个空格替换为一个空格
    s = re.sub('[\n\t\r]+', '\n', s)
    english_words = s.split()
    len_english_words = len(english_words)
    # if len_english_words > 100:
    #     return len_english_words
    chinese_characters = re.findall(r'[\u4e00-\u9fff]', s)
    len_chinese_characters = len(chinese_characters)
    # if len_chinese_characters > 100:
    #     return len_chinese_characters
    japanese_characters = re.findall(r'[\u3040-\u309F\u30A0-\u30FF]', s)
    arabic_characters = re.findall(r'[\u0600-\u06FF]', s)
    th_characters = re.findall(r'[\u0e00-\u0e7f]', s)
    return len_english_words + len_chinese_characters + len(japanese_characters) + len(arabic_characters) + len(th_characters)


def alias(element):
    if element is None:
        return ''
    tag = element.tag
    # skip nth-child
    if tag in ['html', 'body']:
        return tag
    attribs = [tag]
    for k, v in element.attrib.items():
        if k == Unique_ID:
            continue
        k, v = re.sub(r'\s*', '', k), re.sub(r'\s*', '', v)
        v = re.sub(r'-\d+', '', v)
        attribs.append(f'[{k}="{v}"]' if v else f'[{k}]')
    result = ''.join(attribs)

    # 直接将当前子节点属性展示上来
    nth = ''
    for child in element.getchildren():
        if child.tag in ['dt', 'dd', 'li']:
            try:
                # 子节点个数
                nth += str(len(list(child.getchildren())))
            except Exception:
                pass
            continue
        attribs = [child.tag]
        for k, v in child.attrib.items():
            if k == Unique_ID:
                continue
            k, v = re.sub(r'\s*', '', k), re.sub(r'\s*', '', v)
            v = re.sub(r'-\d+', '', v)
            attribs.append(f'[{k}]' if v else f'[{k}]')
        nth += ''.join(attribs)

    result += f':{nth}'
    return result


def similarity2(s1, s2):
    if not s1 or not s2:
        return 0
    s1_set = set(list(s1))
    s2_set = set(list(s2))
    intersection = s1_set.intersection(s2_set)
    union = s1_set.union(s2_set)
    return len(intersection) / len(union)


def similarity_with_element(element1, element2):
    alias1 = alias(element1)
    alias2 = alias(element2)
    return similarity2(alias1, alias2)


def similarity_with_siblings(element, siblings):
    scores = []
    for sibling in siblings:
        scores.append(similarity_with_element(element, sibling))
    if not scores:
        return 0
    # 去掉一个最低值
    min_value = min(scores)
    scores.remove(min_value)
    return np.mean(scores)


def number_of_a_char(ele, xpath='.//a//text()'):
    s = ''.join(ele.xpath(xpath)).strip()
    return text_len(s)


def number_of_char(ele, xpath='.//text()'):
    s = ''.join(ele.xpath(xpath)).strip()
    return text_len(s) + 1


def density_of_a_text(ele, pre=0.7):
    a_char = number_of_a_char(ele)
    t_char = number_of_char(ele)
    if a_char / t_char >= pre:
        return True
    else:
        return False


def uniquify_list(lk):
    return list(dict.fromkeys(lk))


def trim(string):
    """Remove unnecessary spaces within a text string."""
    try:
        return ' '.join(string.split()).strip()
    except (AttributeError, TypeError):
        return ''


def collect_link_info(links_xpath, favor_precision=False):
    shortelems, mylist = 0, []
    threshold = 10 if not favor_precision else 50
    for subelem in links_xpath:
        subelemtext = trim(subelem.text_content())
        if subelemtext:
            mylist.append(subelemtext)
            if len(subelemtext) < threshold:
                shortelems += 1
    lengths = sum(len(text) for text in mylist)
    return lengths, len(mylist), shortelems, mylist


def link_density_test(element, text, favor_precision=False):
    links_xpath, mylist = element.findall('.//a'), []
    if links_xpath:
        if element.tag == 'p':
            if favor_precision is False:
                if element.getnext() is None:
                    limitlen, threshold = 60, 0.8
                else:
                    limitlen, threshold = 30, 0.8
            else:
                limitlen, threshold = 200, 0.8
        else:
            if element.getnext() is None:
                limitlen, threshold = 300, 0.8
            else:
                limitlen, threshold = 100, 0.8
        elemlen = len(text)
        if elemlen < limitlen:
            linklen, elemnum, shortelems, mylist = collect_link_info(
                links_xpath, favor_precision
            )
            if elemnum == 0:
                return True, mylist
            if density_of_a_text(element, 0.5):
                if linklen > threshold * elemlen or (
                        elemnum > 1 and shortelems / elemnum > 0.8
                ):
                    return True, mylist
    return False, mylist
