from typing import List

from lxml import html

from llm_web_kit.libs.html_utils import element_to_html, html_to_element


def mapping_html_by_rules(html_content: str, xpaths_to_remove: List[dict]) -> tuple[str, bool]:
    """从HTML中删除指定XPath匹配的所有节点.

    Args:
        html_content (str): 原始HTML内容
        xpaths_to_remove (list): 需要删除的元素列表

    Returns:
        str: 处理后的HTML
        bool: 推广是否成功
    """
    if not html_content:
        return html_content, False

    is_success = False
    tree = html_to_element(html_content)

    # 获取所有元素节点
    all_elements = [element for element in tree.iter() if isinstance(element, html.HtmlElement)]

    for remove_node in xpaths_to_remove:
        xpath_content = remove_node.get('xpath')
        for node in tree.xpath(xpath_content):
            # 获取节点内容占比
            content_rate = __calculate_node_content_ratio(tree, node)
            if content_rate > 0.4:
                continue
            # 获取节点的位置
            node_position = __analyze_node_position(all_elements, node)
            if node_position == 'middle':
                continue
            # 删除节点及其所有子节点
            node.getparent().remove(node)
            is_success = True

    return element_to_html(tree), is_success


def __calculate_node_content_ratio(tree: html.HtmlElement, node: html.HtmlElement) -> float:
    """计算节点内容占比.

    Args:
        tree(html.HtmlElement): 根节点对象
        node(html.HtmlElement): 节点对象

    Returns:
        float: 节点内容占比
    """
    # 获取节点的文本内容
    text_content = node.text_content()

    total_contents = tree.text_content()
    content_rate = len(text_content) / len(total_contents) if total_contents else 0
    return content_rate


def __analyze_node_position(all_elements: List[html.HtmlElement], target_node: html.HtmlElement):
    # 计算总节点数
    total_nodes = len(all_elements)

    # 新增逻辑：检查元素是否在<header>或<footer>标签内
    parent = target_node.getparent()
    while parent is not None:
        if parent.tag == 'header':
            return 'start'
        elif parent.tag == 'footer':
            return 'end'
        parent = parent.getparent()

    # 查找当前节点在全部节点中的索引
    node_index = -1
    for idx, element in enumerate(all_elements):
        if element == target_node:
            node_index = idx
            break

    if node_index == -1:
        # 无法定位节点在文档中的位置
        return None

    # 计算位置比例
    position_ratio = (node_index + 1) / total_nodes

    # 判断位置
    if position_ratio < 0.4:
        position = 'start'
    elif position_ratio > 0.7:
        position = 'end'
    else:
        position = 'middle'

    return position
