import re
from typing import Optional

from lxml.html import HtmlElement

from llm_web_kit.extractor.html.recognizer.recognizer import CCTag
from llm_web_kit.libs.html_utils import element_to_html

_RE_NUMBER = re.compile(r'^(\s*)([0-9]+)(\s*)')
_RE_NUMBER_NO_CODE = re.compile(r'^(\s*)([0-9]+)(\s*)$')
_RE_COMBINE_WHITESPACE = re.compile(r' +')
_BLOCK_ELES = [
    'br',
    'tr',
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
    return _RE_COMBINE_WHITESPACE.sub(' ', s.replace('\n', '').replace('\r', ''))


def hit_last_leaf(ele: HtmlElement) -> bool:
    children = ele.getchildren()
    if len(children) == 0:
        return False
    if children[-1].tag in _BLOCK_ELES:
        return True
    return hit_last_leaf(children[-1])


def _detect_lineno(s: str, is_code_after_lineno: bool = True) -> tuple[bool, list[int]]:
    """
    is_code_after_lineno: 行号后是否有代码正文
    """
    lines = s.split('\n')
    maybe_linenos: list[tuple[int, int, int, int | None]] = []
    empty_lines = 0
    for line in lines:
        if not line:
            empty_lines += 1
        if is_code_after_lineno:
            match = _RE_NUMBER.match(line)
        else:
            match = _RE_NUMBER_NO_CODE.match(line)
        if match:
            groups = match.groups()
            maybe_linenos.append(
                (
                    len(groups[0]),  # 行号前的空白符号
                    len(groups[1]),  # 行号
                    len(groups[2]),  # 行号后的空白符号
                    int(groups[1]),
                )
            )
        else:
            maybe_linenos.append((0, 0, 0, None))

    # 允许行号断裂，计算连续数字最大出现的次数
    linenos = [maybe_lineno for _, _, _, maybe_lineno in maybe_linenos if maybe_lineno]
    # 至少七成有行号
    if len(linenos) < (len(maybe_linenos) - empty_lines) * 0.7:
        return False, []

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

    # 行号到代码的空白符长度
    post_lineno_indent = min([pos_lineno for _, _, pos_lineno, _ in maybe_linenos])
    # 认为存在有三个连续数字就是行号
    # （发现了只有一行行号的 bad case，但是没办法）
    indents = []
    for pre_lineno, lineno_len, _, lineno in maybe_linenos:
        if lineno is not None:
            indents.append(pre_lineno + lineno_len + post_lineno_indent)
        else:
            indents.append(0)
    return max_count > 2, indents


def _remove_linenos(s: str, line_indents: list[int]) -> str:
    lines = s.split('\n')
    new_lines = []
    for line, pos in zip(lines, line_indents):
        new_lines.append(line[pos:])
    return '\n'.join(new_lines)


def _detect_and_remove_subling_lineno(node: HtmlElement, depth: int = 4):
    if depth == 0 or node is None or node.getparent() is None:
        return

    parent = node.getparent()
    ele_before = node.getprevious()

    if ele_before is not None:
        text = '\n'.join(ele_before.itertext())
        has_lineno, _ = _detect_lineno(text, False)
        if has_lineno:
            parent.remove(ele_before)
            return  # 删除后立即返回，不再递归

    # 继续递归父节点
    _detect_and_remove_subling_lineno(parent, depth - 1)


def get_full_text(sub_tree: HtmlElement) -> tuple[bool, str, str]:
    t = ''
    last_tail = sub_tree.text or ''
    is_block = False
    for child in sub_tree.iterchildren(None):
        is_block, text, tail = get_full_text(child)
        if not last_tail.isspace() or not is_block:
            t += last_tail
        t += text
        last_tail = tail

    if not last_tail.isspace() or sub_tree.tag not in _BLOCK_ELES:
        t += last_tail

    if not is_block and sub_tree.tag in _BLOCK_ELES:
        return True, (t or '') + '\n', sub_tree.tail or ''

    return sub_tree.tag in _BLOCK_ELES or is_block, t, sub_tree.tail or ''


def replace_node_by_cccode(
    node: HtmlElement, by: str, in_pre_tag: bool = True, inline: bool = False
) -> None:
    """将 node 替换为 cccode 标签.

    Args:
        node: 要替换的节点
        by: 替换后的标签
    """
    origin_html = element_to_html(node)

    if not inline:
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

    if in_pre_tag:
        for block_ele in _BLOCK_ELES:
            x = f'.//{block_ele}'
            for ele in node.xpath(x):
                assert isinstance(ele, HtmlElement)

                # 如果树最右链的一个子元素是分块元素,那分块就没有必要换行
                if hit_last_leaf(ele):
                    continue

                ele.tail = ('\n' + ele.tail) if ele.tail else ('\n')  # type: ignore
        full_text = ''.join(node.itertext(None))
    else:
        _, full_text, _ = get_full_text(node)

    full_text = full_text.replace('\r\n', '\n').replace('\r', '\n').replace(' ', ' ')
    chunks = [sub_text.rstrip() for sub_text in full_text.split('\n')]

    while len(chunks) > 0 and not chunks[0]:
        chunks = chunks[1:]
    while len(chunks) > 0 and not chunks[len(chunks) - 1]:
        chunks = chunks[:-1]

    full_text = '\n'.join(chunks)
    has_lineno, line_indents = _detect_lineno(full_text)
    if has_lineno:
        full_text = _remove_linenos(full_text, line_indents)

    chunks = full_text.split('\n')
    common_space = 0
    add_space = True
    while add_space:
        add_space = False
        first_space = None
        for chunk in chunks:
            if len(chunk) <= common_space:
                continue
            if chunk[common_space].isspace():
                if first_space is None:
                    add_space = True
                    first_space = chunk[common_space]
                elif first_space != chunk[common_space]:
                    add_space = False
                    break
            else:
                add_space = False
                break
        if add_space:
            common_space += 1

    chunks = [chunk[common_space:] for chunk in chunks]
    full_text = '\n'.join(chunks)

    node.clear(keep_tail=True)
    if language:
        node.set('language', language)
    node.set('by', by)
    node.set('html', origin_html)
    node.set('inline', 'true' if inline else 'false')
    node.tag = CCTag.CC_CODE_INLINE if inline else CCTag.CC_CODE  # type: ignore
    node.text = full_text  # type: ignore
