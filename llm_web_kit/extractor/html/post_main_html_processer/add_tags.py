from typing import Generator

from lxml import etree

from llm_web_kit.libs.html_utils import element_to_html, html_to_element


def process_html(input_html: str) -> str:
    """处理HTML，为元素添加连续的_item_id属性.

    Args:
        input_html: 输入的HTML字符串

    Returns:
        处理后的HTML字符串，其中每个文本节点都有唯一的_item_id
    """
    if not input_html:
        return ''

    try:
        tree = html_to_element(input_html)
        root = tree.xpath('//body')[0] if tree.xpath('//body') else tree
    except Exception as e:
        raise ValueError(f'Invalid HTML input: {e}')

    # 使用ID生成器确保ID连续
    id_generator = __item_id_generator()

    # 遍历所有元素并处理
    __process_elements(root, id_generator)

    return element_to_html(root)


def __item_id_generator() -> Generator[int, None, None]:
    """生成连续的ID序列.

    Yields:
        连续递增的整数ID
    """
    counter = 1
    while True:
        yield counter
        counter += 1


def __process_elements(tree: etree.Element, id_generator: Generator[int, None, None]) -> None:
    """处理DOM树中的所有元素，为文本节点添加_item_id.

    Args:
        tree: HTML DOM树根节点
        id_generator: ID生成器
    """
    # 创建静态列表避免在迭代时修改DOM结构
    elements_to_process = list(tree.iter())

    for element in elements_to_process:
        # 处理叶子节点（无子元素）
        if len(element) == 0:
            __process_leaf_element(element, id_generator)
        else:
            # 处理非叶子节点
            __process_non_leaf_element(element, id_generator)


def __process_leaf_element(element: etree.Element,
                           id_generator: Generator[int, None, None]) -> None:
    """处理叶子节点元素.

    Args:
        element: 叶子节点元素
        id_generator: ID生成器
    """
    # 为叶子节点分配_item_id
    element.set('_item_id', str(next(id_generator)))

    # 处理tail文本
    if element.tail and element.tail.strip():
        parent = element.getparent()
        if parent is not None:
            # 创建custom_tail元素并插入到当前元素之后
            custom_tail = __create_custom_element(
                'custom_tail', element.tail, id_generator
            )
            element.tail = None

            # 插入到正确位置
            parent_index = parent.index(element)
            parent.insert(parent_index + 1, custom_tail)


def __process_non_leaf_element(element: etree.Element,
                               id_generator: Generator[int, None, None]) -> None:
    """处理非叶子节点元素.

    Args:
        element: 非叶子节点元素
        id_generator: ID生成器
    """
    parent = element.getparent()
    parent_index = parent.index(element) if parent is not None else -1

    # 处理元素的text内容
    if element.text and element.text.strip():
        custom_text = __create_custom_element(
            'custom_text', element.text, id_generator
        )
        element.text = None
        element.insert(0, custom_text)

    # 处理元素的tail内容
    if element.tail and element.tail.strip():
        if parent is not None:
            custom_tail = __create_custom_element(
                'custom_tail', element.tail, id_generator
            )
            element.tail = None
            parent.insert(parent_index + 1, custom_tail)


def __create_custom_element(tag: str, text_content: str,
                            id_generator: Generator[int, None, None]) -> etree.Element:
    """创建带_item_id的自定义元素.

    Args:
        tag: 元素标签名
        text_content: 元素文本内容
        id_generator: ID生成器

    Returns:
        带_item_id属性的自定义元素
    """
    custom_elem = etree.Element(tag)
    custom_elem.text = text_content
    custom_elem.set('_item_id', str(next(id_generator)))
    return custom_elem
