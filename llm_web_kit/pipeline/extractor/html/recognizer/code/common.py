import re
from typing import Optional

from lxml.html import HtmlElement

from llm_web_kit.libs.html_utils import element_to_html
from llm_web_kit.pipeline.extractor.html.recognizer.recognizer import CCTag

_RE_NUMBER = re.compile(r'^\s*([0-9]+)\s*')
_RE_COMBINE_WHITESPACE = re.compile(r' +')
_BLOCK_ELES = [
    'br',
    'address',
    'article',
    'aside',
    'blockquote',
    'canvas',
    'dd',
    'div',
    'dl',
    'dt',
    'fieldset',
    'figcaption',
    'figure',
    'footer',
    'form',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'header',
    'hr',
    'li',
    'main',
    'nav',
    'noscript',
    'ol',
    'p',
    'pre',
    'section',
    'table',
    'tfoot',
    'ul',
    'video',
]


def __get_lang_maybe(node: HtmlElement) -> Optional[str]:
    attrib: dict[str, str] = node.attrib
    classes: list[str] = [c for c in attrib.get('class', '').split(' ') if c]
    for c in classes:
        if c.startswith('language-') or c.startswith('lang-'):
            return c.replace('language-', '').replace('lang-', '')
    return None


# 对 prismjs 和 highlightjs 有效
# 但是如果没写，那没有办法
# TODO: guesslang ?
def __detect_language(node: HtmlElement) -> Optional[str]:
    for cnode in node.iter(None):
        assert isinstance(cnode, HtmlElement)
        if lang := __get_lang_maybe(cnode):
            return lang

    ptr = node
    while ptr is not None:
        if lang := __get_lang_maybe(ptr):
            return lang
        ptr = ptr.getparent()

    return None


def remove_html_newline_and_spaces(s: str) -> str:
    if not s:
        return s
    return _RE_COMBINE_WHITESPACE.sub(' ', s.replace('\n', '').replace('\r', ''))


def hit_last_leaf(ele: HtmlElement) -> bool:
    children = ele.getchildren()
    if len(children) == 0:
        return False
    if children[-1].tag in _BLOCK_ELES:
        return True
    return hit_last_leaf(children[-1])


def _detect_lineno(s: str) -> tuple[bool, list[int]]:
    lines = s.split('\n')
    maybe_linenos: list[tuple[int, int | None]] = []
    for line in lines:
        if match := _RE_NUMBER.match(line):
            maybe_linenos.append((match.span()[1],int(match.groups()[0])))
        else:
            maybe_linenos.append((0, None))

    linenos = [maybe_lineno for _, maybe_lineno in maybe_linenos if maybe_lineno]
    last = None
    idx = 0
    count = 0
    max_count = 0
    while idx < len(linenos):
        if last is not None and last + 1 == linenos[idx]:
            last += 1
            count += 1
        else:
            last = linenos[idx]
            count = 0 if last is None else 1
        max_count = max(max_count, count)
        idx += 1

    return max_count > 2, [pos for pos, _ in maybe_linenos]


def _remove_linenos(s: str, line_indents: list[int]) -> str:
    lines = s.split('\n')
    new_lines = []
    for line, pos in zip(lines, line_indents):
        if pos:
            new_lines.append(line[pos:])
        else:
            new_lines.append(line)
    return '\n'.join(new_lines)


def _detect_and_remove_subling_lineno(node: HtmlElement, depth: int = 4):
    if depth == 0 or node is None or node.getparent() is None:
        return

    found = False
    # 认为只有代码元素左侧的元素可能是行号
    ele_before = None
    for child in node.getparent():
        if child == node:
            if ele_before is None:
                break
            has_lineno, _ = _detect_lineno('\n'.join(ele_before.itertext()))
            if has_lineno:
                node.getparent().remove(ele_before)
                found = True
            break
        ele_before = child

    if not found:
        _detect_and_remove_subling_lineno(node.getparent(), depth - 1)


def replace_node_by_cccode(node: HtmlElement, by: str, in_pre_tag: bool = True, inline: bool = False) -> None:
    """将 node 替换为 cccode 标签.

    Args:
        node: 要替换的节点
        by: 替换后的标签
    """
    origin_html = element_to_html(node)

    _detect_and_remove_subling_lineno(node)

    language = __detect_language(node)

    # 如果不是由 pre 保护格式，那么把空白字符和换行都去掉
    if not in_pre_tag:
        if node.text:
            node.text = remove_html_newline_and_spaces(node.text)
        for sub_node in node.iter(None):
            if sub_node == node:
                continue
            if sub_node.text:
                sub_node.text = remove_html_newline_and_spaces(sub_node.text)
            if sub_node.tail:
                sub_node.tail = remove_html_newline_and_spaces(sub_node.tail)

    for block_ele in _BLOCK_ELES:
        x = f'.//{block_ele}'
        for ele in node.xpath(x):
            assert isinstance(ele, HtmlElement)

            # 如果树最右链的一个子元素是分块元素,那分块就没有必要换行
            if hit_last_leaf(ele):
                continue

            ele.tail = ('\n' + ele.tail) if ele.tail else ('\n')  # type: ignore

    full_text = ''.join(node.itertext(None)).replace('\r\n', '\n').replace('\r', '\n')
    chunks = [sub_text.replace(' ', ' ').rstrip() for sub_text in full_text.split('\n')]

    while len(chunks) > 0 and not chunks[0]:
        chunks = chunks[1:]
    while len(chunks) > 0 and not chunks[len(chunks) - 1]:
        chunks = chunks[:-1]

    full_text = '\n'.join(chunks)
    has_lineno, line_indents = _detect_lineno(full_text)
    if has_lineno:
        full_text = _remove_linenos(full_text, line_indents)

    node.clear(keep_tail=True)
    if language:
        node.set('language', language)
    node.set('by', by)
    node.set('html', origin_html)
    node.set('inline', 'true' if inline else 'false')
    node.tag = CCTag.CC_CODE_INLINE if inline else CCTag.CC_CODE  # type: ignore
    node.text = full_text  # type: ignore
