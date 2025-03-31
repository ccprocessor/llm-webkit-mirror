from typing import Optional

from lxml.html import HtmlElement

from llm_web_kit.extractor.html.recognizer.code.common import (
    _BLOCK_ELES, replace_node_by_cccode)
from llm_web_kit.extractor.html.recognizer.recognizer import CCTag

"""
处理仅由<code>标签组成的代码块
"""


def __get_html_element(root: HtmlElement, node_path: list[str]) -> HtmlElement:
    path = '/'.join(node_path)
    path = '/'.join(path.removeprefix('/').split('/')[1:])
    if not path:
        return root
    node = root.find(path, {'og': 'http://ogp.me/ns'})
    assert node is not None
    return node


def __is_all_chars_in_code_element(node: HtmlElement) -> bool:
    full_text = ''.join([x for x in ''.join(node.itertext(None)) if not x.isspace() and not x.isdigit()])
    code_text = ''
    for s in node.xpath('.//code//text()'):
        for c in s:
            if not c.isspace() and not c.isdigit():
                code_text += c
    return full_text == code_text


def __get_code_node_paths(html_el: HtmlElement) -> list[list[str]]:
    """获取 html_el 中所有 code 标签的路径 只获取最外层的code标签， 如果code标签内还有code标签，则不获取。

    Args:
        html_el: 根节点

    Returns:
        list[list[str]]: 所有 code 标签的路径: 如[['body', 'div', 'code'], ['body', 'div', 'span', 'code']]
    """
    node_paths: list[list[str]] = []
    for code_node in html_el.iterchildren():
        if code_node.tag == 'code':
            hit = False
            for _ in code_node.iter('cccode'):
                hit = True
                break
            if hit:
                continue
            node_path = code_node.getroottree().getpath(code_node)
            node_paths.append(node_path.split('/'))
        else:
            node_paths.extend(__get_code_node_paths(code_node))
    return node_paths


def __get_code_blocks_nodes(node: HtmlElement, tree_roots: list[str]) -> list[HtmlElement]:
    """找出所有需要被转换为代码块的候选节点.

    Args:
        node: 当前正在检查的节点
        tree_roots: 代码块组的根节点路径列表

    Returns:
        list[HtmlElement]: 需要被转换的候选节点列表
    """
    current_path = node.getroottree().getpath(node)

    # 检查当前节点是否是某个代码块组的根节点
    if current_path in tree_roots:
        return [node]

    # 检查当前节点是否是某个代码块组的祖先节点
    is_ancestor = any(root_path.startswith(current_path) for root_path in tree_roots)
    if not is_ancestor:
        return []

    # 递归检查子节点
    candidates = []
    for child in node.getchildren():
        if isinstance(child, HtmlElement):
            candidates.extend(__get_code_blocks_nodes(child, tree_roots))

    return candidates


def detect(body: HtmlElement) -> bool:
    for code_node in body.iter('code'):
        hit = False
        for _ in code_node.iter('cccode'):
            hit = True
            break
        if not hit:
            return True
    return False


def __detect_inline_code(root: HtmlElement, node_paths: list[list[str]]) -> tuple[list[list[str]], list[HtmlElement]]:
    new_node_paths = []
    inline_code = []

    for node_path in node_paths:
        ele = __get_html_element(root, node_path)

        parent = ele
        while parent.tag not in _BLOCK_ELES and parent.getparent() is not None:
            parent = parent.getparent()

        """
        并非所有 inline code 都可以识别出来
        """
        if not __is_all_chars_in_code_element(parent):
            inline_code.append(ele)
            continue

        new_node_paths.append(node_path)

    return new_node_paths, inline_code


def __group_code(root: HtmlElement, node_paths: list[list[str]]) -> list[str]:
    root_paths = []

    def next_parent(code_node: HtmlElement, code_tags: int) -> tuple[Optional[HtmlElement], int]:
        parent: Optional[HtmlElement] = code_node.getparent()
        while parent is not None:
            new_code_tags = len(parent.xpath('.//code'))
            if new_code_tags == code_tags:
                parent = parent.getparent()
            else:
                return parent, new_code_tags
        return None, 0

    while len(node_paths):
        code_node = __get_html_element(root, node_paths[0])
        code_tags = len(code_node.xpath('.//code'))

        parent, new_code_tags = next_parent(code_node, code_tags)
        while parent is not None:
            if not __is_all_chars_in_code_element(parent):
                break

            if len(parent.xpath(f'.//{CCTag.CC_CODE}|.//{CCTag.CC_CODE_INLINE}')) > 0:
                break

            code_node = parent
            code_tags = new_code_tags

            parent, new_code_tags = next_parent(code_node, code_tags)

        root_path = code_node.getroottree().getpath(code_node)
        root_paths.append(root_path)

        new_node_path = []
        for node_path in node_paths:
            if '/'.join(node_path).startswith(root_path):
                continue
            new_node_path.append(node_path)
        node_paths = new_node_path

    return root_paths


def modify_tree(root: HtmlElement) -> None:
    """将 html 树中所有 code 标签转换为代码块.

    Args:
        root: html 树的根节点
    """
    node_paths = __get_code_node_paths(root)  # 获取所有 code 标签的路径，不包含嵌套的子 code 标签
    node_paths, inline_code = __detect_inline_code(root, node_paths)
    for node in inline_code:
        replace_node_by_cccode(node, 'tag_code', False, True)

    if len(node_paths) == 0:
        tree_roots = []
    elif len(node_paths) == 1:
        tree_roots = ['/'.join(node_paths[0])]
    else:
        tree_roots = __group_code(root, node_paths)  # 根据距离矩阵，对code标签进行分组
        tree_roots = sorted(tree_roots)

    nodes = __get_code_blocks_nodes(root, tree_roots)  # 获取所有需要被转换为代码块的节点，并进行标签替换
    for node in nodes:
        replace_node_by_cccode(node, 'tag_code', False)
