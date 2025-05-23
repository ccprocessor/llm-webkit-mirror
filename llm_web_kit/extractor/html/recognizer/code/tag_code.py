from collections import deque
from typing import Optional

from lxml.html import HtmlElement

from llm_web_kit.extractor.html.recognizer.code.common import (
    _BLOCK_ELES, replace_node_by_cccode)
from llm_web_kit.extractor.html.recognizer.recognizer import CCTag

"""
处理仅由<code>标签组成的代码块
"""


def __is_all_chars_in_code_element(node: HtmlElement) -> bool:

    if node.tag == 'code':
        return True

    full_chars = (
        c for text in node.itertext()
        for c in text
        if not c.isspace() and not c.isdigit()
    )

    node_texts = node.xpath('.//code//text()')
    code_chars = (
        c for code in node_texts
        for text in code
        for c in text
        if not c.isspace() and not c.isdigit()
    )

    for f, c in zip(full_chars, code_chars):
        if f != c:
            return False

    return next(full_chars, None) is None and next(code_chars, None) is None


def __get_code_nodes(html_el: HtmlElement) -> list[HtmlElement]:
    """获取 html_el 中所有 code 标签的路径 只获取最外层的code标签， 如果code标签内还有code标签，则不获取。

    Args:
        html_el: 根节点

    Returns:
        list[list[str]]: 所有 code 标签的路径: 如[['body', 'div', 'code'], ['body', 'div', 'span', 'code']]
    """
    nodes: list[HtmlElement] = []
    for code_node in html_el.iterchildren(None):
        if code_node.tag == 'code':
            hit = False
            for _ in code_node.iter('cccode'):
                hit = True
                break
            if hit:
                continue
            nodes.append(code_node)
        else:
            nodes.extend(__get_code_nodes(code_node))

    return nodes


def detect(body: HtmlElement) -> bool:
    for code_node in body.iter('code'):
        hit = False
        for _ in code_node.iter('cccode'):
            hit = True
            break
        if not hit:
            return True
    return False


def __detect_inline_code(nodes: list[HtmlElement]) -> tuple[list[HtmlElement], list[HtmlElement]]:
    new_nodes = []
    inline_code = []

    for ele in nodes:
        ele_text = ''.join(ele.itertext(None))
        # 行内代码不能有换行
        if '\r' in ele_text or '\n' in ele_text:
            new_nodes.append(ele)
            continue

        parent = ele
        while parent.tag not in _BLOCK_ELES and parent.getparent() is not None:
            parent = parent.getparent()

        """
        并非所有 inline code 都可以识别出来
        这里认为在父 block ele 中如果参杂了非 code 的可见文字，那这段 code 应该是行内的
        """
        if not __is_all_chars_in_code_element(parent):
            inline_code.append(ele)
            continue

        new_nodes.append(ele)

    return new_nodes, inline_code


def __group_code(nodes: list[HtmlElement]) -> list[HtmlElement]:
    """从 HtmlElement 列表中提取包含 <code> 标签的根节点。

    Args:
        nodes: 输入的 HtmlElement 列表
    Returns:
        包含 <code> 标签的根节点列表
    """
    root_nodes: list[HtmlElement] = []
    processed = set()
    nodes_deque = deque(nodes)

    def next_parent(code_node: HtmlElement, code_tags: int) -> tuple[Optional[HtmlElement], int]:
        """查找父节点中第一个 <code> 标签数量不同的节点。

        Args:
            code_node: 当前节点
            code_tags: 当前节点的 <code> 标签数量
        Returns:
            (父节点, 父节点的 <code> 标签数量)，若无符合条件的父节点则返回 (None, 0)
        """
        parent: Optional[HtmlElement] = code_node.getparent()
        while parent is not None:
            new_code_tags = len(parent.xpath('.//code'))
            if new_code_tags == code_tags:
                parent = parent.getparent()
            else:
                return parent, new_code_tags
        return None, 0

    def get_descendants(node: HtmlElement) -> set:
        """获取节点的所有后代节点的 id 集合。

        Args:
            node: 当前节点
        Returns:
            后代节点的 id 集合
        """
        descendants = set()
        for child in node.iterdescendants():
            descendants.add(id(child))
        return descendants

    while nodes_deque:
        code_node = nodes_deque.popleft()
        if id(code_node) in processed:
            continue

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

        root_nodes.append(code_node)
        processed.add(id(code_node))
        descendants = get_descendants(code_node)
        processed.update(descendants)

    return root_nodes


def modify_tree(root: HtmlElement) -> None:
    """将 html 树中所有 code 标签转换为代码块.

    Args:
        root: html 树的根节点
    """
    nodes = __get_code_nodes(root)  # 获取所有 code 标签的路径，不包含嵌套的子 code 标签
    nodes, inline_code = __detect_inline_code(nodes)
    for node in inline_code:
        replace_node_by_cccode(node, 'tag_code', False, True)

    if len(nodes) == 0:
        tree_roots = []
    elif len(nodes) == 1:
        tree_roots = [nodes[0]]
    else:
        tree_roots = __group_code(nodes)  # 根据距离矩阵，对code标签进行分组

    for node in tree_roots:
        replace_node_by_cccode(node, 'tag_code', False)
