import copy
import re
import uuid
from typing import Dict, List, Tuple

from bs4 import BeautifulSoup
from lxml import etree, html

# 行内标签
inline_tags = {
    'map', 'optgroup', 'span', 'br', 'input', 'time', 'u', 'strong', 'textarea', 'small', 'sub',
    'samp', 'blink', 'b', 'code', 'nobr', 'strike', 'bdo', 'basefont', 'abbr', 'var', 'i', 'cccode-inline',
    'select', 's', 'pic', 'label', 'mark', 'object', 'dd', 'dt', 'ccmath-inline', 'svg', 'li',
    'button', 'a', 'font', 'dfn', 'sup', 'kbd', 'q', 'script', 'acronym', 'option', 'img', 'big', 'cite',
    'em',
    # 'td', 'th'
}

# 需要删除的标签
tags_to_remove = {
    'head', 'header', 'footer', 'nav', 'aside', 'style', 'script', 'select', 'noscript', 'link', 'meta', 'iframe', 'frame'
}

# 需要保留的特殊标签（即使它们是行内标签）
EXCLUDED_TAGS = {'img', 'br', 'li', 'dt', 'dd', 'td', 'th'}

# 需要删除的属性名模式（独立单词）
ATTR_PATTERNS_TO_REMOVE = {
    'nav', 'footer', 'header',  # 独立单词
}

# 需要删除的属性名模式（特定前缀/后缀）
ATTR_SUFFIX_TO_REMOVE = {
    '-nav', '_nav',
    # '-footer', '_footer',  # 有特例，可能dl列表一组最后一项添加了自定义footer属性，先注释
    # '-header', '_header',  # 有特例，可能自定义的header中有标题，先注释
}


def add_data_uids(dom: html.HtmlElement) -> None:
    """为DOM所有节点添加data-uid属性（递归所有子节点）"""
    for node in dom.iter():
        try:
            node.set('data-uid', str(uuid.uuid4()))
        except TypeError:
            pass


def remove_all_uids(dom: html.HtmlElement) -> None:
    """移除DOM中所有data-uid属性."""
    for node in dom.iter():
        if 'data-uid' in node.attrib:
            del node.attrib['data-uid']


def build_uid_map(dom: html.HtmlElement) -> Dict[str, html.HtmlElement]:
    """构建data-uid到节点的映射字典."""
    return {node.get('data-uid'): node for node in dom.iter() if node.get('data-uid')}


def is_unique_attribute(tree, attr_name, attr_value):
    """检查给定的属性名和值组合是否在文档中唯一。"""
    elements = tree.xpath(f"//*[@{attr_name}='{attr_value}']")
    return len(elements) == 1


def get_relative_xpath(element):
    root_tree = element.getroottree()
    current_element = element
    path_from_element = []
    found_unique_ancestor = False

    # 从当前元素开始向上查找
    while current_element is not None and current_element.getparent() is not None:
        siblings = [sib for sib in current_element.getparent() if sib.tag == current_element.tag]

        # 检查当前元素是否有唯一属性
        unique_attr = None
        candidate_attrs = [
            attr for attr in current_element.attrib
            if not (attr.startswith('data-') or attr == 'style' or
                    attr == '_item_id' or
                    (current_element.attrib[attr].startswith('{') and current_element.attrib[attr].endswith('}')))
        ]

        for attr in candidate_attrs:
            if is_unique_attribute(root_tree, attr, current_element.attrib[attr]):
                unique_attr = attr
                break

        # 如果有唯一属性，构建相对路径并停止向上查找
        if unique_attr is not None:
            path_from_element.insert(0, f'*[@{unique_attr}="{current_element.attrib[unique_attr]}"]')
            found_unique_ancestor = True
            break
        else:
            # 没有唯一属性，使用常规方式
            if len(siblings) > 1:
                index = siblings.index(current_element) + 1
                path_from_element.insert(0, f'{current_element.tag}[{index}]')
            else:
                path_from_element.insert(0, current_element.tag)

        current_element = current_element.getparent()

    # 构建最终的XPath
    if found_unique_ancestor:
        return f'//{"/".join(path_from_element)}'
    else:
        # 如果没有找到唯一属性祖先，返回完整路径
        return f'//{"/".join(path_from_element)}'


def is_data_table(table_element: html.HtmlElement) -> bool:
    """判断表格是否是数据表格而非布局表格."""
    # 检查表格是否有 caption 标签
    if table_element.xpath('.//caption'):
        return True

    # 检查是否有 th 标签
    if table_element.xpath('.//th'):
        return True

    # 检查是否有 thead 或 tfoot 标签
    if table_element.xpath('.//thead') or table_element.xpath('.//tfoot'):
        return True

    # 检查是否有 colgroup 或 col 标签
    if table_element.xpath('.//colgroup') or table_element.xpath('.//col'):
        return True

    # 检查是否有 summary 属性
    if table_element.get('summary'):
        return True

    # 检查是否有 role="table" 或 data-table 属性
    if table_element.get('role') == 'table' or table_element.get('data-table'):
        return True

    # 检查单元格是否有 headers 属性
    if table_element.xpath('.//*[@headers]'):
        return True

    return False


def extract_paragraphs(processing_dom: html.HtmlElement, uid_map: Dict[str, html.HtmlElement],
                       include_parents: bool = True) -> List[Dict[str, str]]:
    """获取段落.

    content_type 字段：用于标识段落内容的类型，可能的值包括：

        'block_element'：独立的块级元素

        'inline_elements'：纯内联元素组合

        'unwrapped_text'：未包裹的纯文本内容

        'mixed'：混合内容（包含文本和内联元素）

    :param processing_dom:
    :param uid_map:
    :param include_parents:
    :return: 段落列表，每个段落包含html、content_type和_original_element字段
    """

    # 创建表格类型映射，记录每个表格是数据表格还是布局表格
    table_types = {}

    # 先分析所有表格的类型
    for table in processing_dom.xpath('.//table'):
        table_types[table.get('data-uid')] = is_data_table(table)

    def is_block_element(node) -> bool:
        """判断是否为块级元素."""
        # 处理表格单元格特殊情况
        if node.tag in ('td', 'th'):
            # 找到最近的祖先table元素
            table_ancestor = node
            while table_ancestor is not None and table_ancestor.tag != 'table':
                table_ancestor = table_ancestor.getparent()

            # 如果是表格单元格，根据表格类型决定是否为块级元素
            if table_ancestor is not None:
                table_uid = table_ancestor.get('data-uid')
                if table_types.get(table_uid, False):
                    # 数据表格的td/th不作为块级元素
                    return False
                else:
                    # 布局表格的td/th作为块级元素
                    return True

        # 默认处理其他元素
        if node.tag in inline_tags:
            return False
        return isinstance(node, html.HtmlElement)

    def has_block_children(node) -> bool:
        """判断是否有块级子元素."""
        return any(is_block_element(child) for child in node.iterchildren())

    def clone_structure(path: List[html.HtmlElement]) -> Tuple[html.HtmlElement, html.HtmlElement]:
        """克隆节点结构."""
        if not path:
            raise ValueError('Path cannot be empty')
        if not include_parents:
            last_node = html.Element(path[-1].tag, **path[-1].attrib)
            return last_node, last_node
        root = html.Element(path[0].tag, **path[0].attrib)
        current = root
        for node in path[1:-1]:
            new_node = html.Element(node.tag, **node.attrib)
            current.append(new_node)
            current = new_node
        last_node = html.Element(path[-1].tag, **path[-1].attrib)
        current.append(last_node)
        return root, last_node

    paragraphs = []

    def process_node(node: html.HtmlElement, path: List[html.HtmlElement]):
        """递归处理节点."""
        current_path = path + [node]
        inline_content = []
        content_sources = []

        # 处理节点文本
        if node.text and node.text.strip():
            inline_content.append(('direct_text', node.text.strip()))
            content_sources.append('direct_text')

        # 处理子节点
        for child in node:
            if is_block_element(child):
                # 处理累积的内联内容
                if inline_content:
                    try:
                        root, last_node = clone_structure(current_path)
                        merge_inline_content(last_node, inline_content)

                        content_type = 'mixed'
                        if all(t == 'direct_text' for t in content_sources):
                            content_type = 'unwrapped_text'
                        elif all(t == 'element' for t in content_sources):
                            content_type = 'inline_elements'

                        # 获取原始元素
                        original_element = uid_map.get(node.get('data-uid'))
                        paragraphs.append({
                            'html': etree.tostring(root, encoding='unicode').strip(),
                            'content_type': content_type,
                            '_original_element': original_element  # 添加原始元素引用
                        })
                    except ValueError:
                        pass
                    inline_content = []
                    content_sources = []

                # 处理块级元素
                if not has_block_children(child):
                    try:
                        root, last_node = clone_structure(current_path + [child])
                        last_node.text = child.text if child.text else None
                        for grandchild in child:
                            last_node.append(copy.deepcopy(grandchild))

                        # 获取原始元素
                        original_element = uid_map.get(child.get('data-uid'))
                        paragraphs.append({
                            'html': etree.tostring(root, encoding='unicode').strip(),
                            'content_type': 'block_element',
                            '_original_element': original_element  # 添加原始元素引用
                        })
                    except ValueError:
                        pass
                else:
                    process_node(child, current_path)

                # 处理tail文本
                if child.tail and child.tail.strip():
                    inline_content.append(('tail_text', child.tail.strip()))
                    content_sources.append('tail_text')
            else:
                inline_content.append(('element', child))
                content_sources.append('element')
                if child.tail and child.tail.strip():
                    inline_content.append(('tail_text', child.tail.strip()))
                    content_sources.append('tail_text')

        # 处理剩余的内联内容
        if inline_content:
            try:
                root, last_node = clone_structure(current_path)
                merge_inline_content(last_node, inline_content)

                content_type = 'mixed'
                if all(t == 'direct_text' for t in content_sources):
                    content_type = 'unwrapped_text'
                elif all(t == 'element' for t in content_sources):
                    content_type = 'inline_elements'
                elif all(t in ('direct_text', 'tail_text') for t in content_sources):
                    content_type = 'unwrapped_text'

                # 获取原始元素
                original_element = uid_map.get(node.get('data-uid'))
                paragraphs.append({
                    'html': etree.tostring(root, encoding='unicode').strip(),
                    'content_type': content_type,
                    '_original_element': original_element  # 添加原始元素引用
                })
            except ValueError:
                pass

    def merge_inline_content(parent: html.HtmlElement, content_list: List[Tuple[str, str]]):
        """合并内联内容."""
        last_inserted = None
        for item_type, item in content_list:
            if item_type in ('direct_text', 'tail_text'):
                if last_inserted is None:
                    if not parent.text:
                        parent.text = item
                    else:
                        parent.text += ' ' + item
                else:
                    if last_inserted.tail is None:
                        last_inserted.tail = item
                    else:
                        last_inserted.tail += ' ' + item
            else:
                parent.append(copy.deepcopy(item))
                last_inserted = item

    # 开始处理
    process_node(processing_dom, [])

    # 去重
    seen = set()
    unique_paragraphs = []
    for p in paragraphs:
        if p['html'] not in seen:
            seen.add(p['html'])
            unique_paragraphs.append(p)

    return unique_paragraphs


def remove_xml_declaration(html_string):
    # 正则表达式匹配 <?xml ...?> 或 <?xml ...>（没有问号结尾的情况）
    pattern = r'<\?xml\s+.*?\??>'
    html_content = re.sub(pattern, '', html_string, flags=re.DOTALL)
    # 1. 删除HTML注释
    html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
    return html_content


def post_process_html(html_content: str) -> str:
    """对简化后的HTML进行后处理."""
    if not html_content:
        return html_content

    # 1. 删除HTML注释
    html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)

    # 2. 处理标签外的空白（保留标签内文本的换行）
    def replace_outside_tag_space(match):
        """只替换标签外的连续空白."""
        if match.group(1):  # 如果是标签内容
            return match.group(1)
        elif match.group(2):  # 如果是非标签内容
            # 将非标签内容中的连续空白替换为单个空格
            return re.sub(r'\s+', ' ', match.group(2))
        return match.group(0)  # 默认返回整个匹配

    # 使用正则匹配所有标签内容和非标签内容
    html_content = re.sub(r'(<[^>]+>)|([^<]+)', replace_outside_tag_space, html_content)

    return html_content.strip()


def remove_tags(dom):
    """删除特定的标签.

    :param dom:
    :return:
    """
    for tag in tags_to_remove:
        for node in dom.xpath(f'.//{tag}'):
            parent = node.getparent()
            if parent is not None:
                parent.remove(node)


def is_meaningful_content(element) -> bool:
    """严格判断元素是否包含有效内容."""
    if element.text and element.text.strip():
        return True
    if element.tag == 'img':
        src = element.get('src', '')
        return bool(src and src.strip())
    for child in element:
        if is_meaningful_content(child):
            return True
    if element.tail and element.tail.strip():
        return True
    return False


def clean_attributes(element):
    """清理元素属性，只保留图片的有效src."""
    if element.tag == 'img':
        src = element.get('src', '').strip()
        element.attrib.clear()
        if src:
            element.set('src', src)
    else:
        element.attrib.clear()
    for child in element:
        clean_attributes(child)


def remove_inline_tags(element):
    """递归移除所有指定的行内标签（包括嵌套情况），保留img和br等EXCLUDED_TAGS标签."""
    # 先处理子元素（深度优先）
    for child in list(element.iterchildren()):
        remove_inline_tags(child)

    # 如果当前元素是需要移除的行内标签
    if element.tag in inline_tags and element.tag not in EXCLUDED_TAGS:
        parent = element.getparent()
        if parent is None:
            return

        # 检查是否包含需要保留的标签（如img、br等）
        has_excluded_tags = any(
            child.tag in EXCLUDED_TAGS
            for child in element.iterdescendants()
        )

        # 如果包含需要保留的标签，则不移除当前元素
        if has_excluded_tags:
            return

        # 保存当前元素的各部分内容
        leading_text = element.text or ''  # 元素开始前的文本
        trailing_text = element.tail or ''  # 元素结束后的文本
        children = list(element)  # 子元素列表

        # 获取当前元素在父元素中的位置
        element_index = parent.index(element)

        # 1. 处理leading_text（元素开始前的文本）
        if leading_text:
            if element_index == 0:  # 如果是第一个子元素
                parent.text = (parent.text or '') + leading_text
            else:
                prev_sibling = parent[element_index - 1]
                prev_sibling.tail = (prev_sibling.tail or '') + leading_text

        # 2. 转移子元素到父元素中
        for child in reversed(children):
            parent.insert(element_index, child)

        # 3. 处理trailing_text（元素结束后的文本）
        if trailing_text:
            if len(children) > 0:  # 如果有子元素，追加到最后一个子元素的tail
                last_child = children[-1]
                last_child.tail = (last_child.tail or '') + trailing_text
            elif element_index == 0:  # 如果没有子元素且是第一个子元素
                parent.text = (parent.text or '') + trailing_text
            else:  # 如果没有子元素且不是第一个子元素
                prev_sibling = parent[element_index - 1] if element_index > 0 else None
                if prev_sibling is not None:
                    prev_sibling.tail = (prev_sibling.tail or '') + trailing_text
                else:
                    parent.text = (parent.text or '') + trailing_text

        # 4. 移除当前元素
        parent.remove(element)


def simplify_list(element):
    """简化列表元素，只保留第一组和最后一组（对于dl列表保留完整的dt+所有dd）"""
    if element.tag in ('ul', 'ol'):
        # 处理普通列表(ul/ol)
        items = list(element.iterchildren())
        if len(items) > 2:
            # 保留第一个和最后一个子元素
            for item in items[1:-1]:
                element.remove(item)

            # 在第一个和最后一个之间添加省略号
            ellipsis = etree.Element('span')
            ellipsis.text = '...'
            items[-1].addprevious(ellipsis)

    elif element.tag == 'dl':
        # 处理定义列表(dl)
        items = list(element.iterchildren())
        if len(items) > 2:
            # 找出所有dt元素
            dts = [item for item in items if item.tag == 'dt']

            if len(dts) > 1:
                # 获取第一组dt和所有后续dd
                first_dt_index = items.index(dts[0])
                next_dt_index = items.index(dts[1])
                first_group = items[first_dt_index:next_dt_index]

                # 获取最后一组dt和所有后续dd
                last_dt_index = items.index(dts[-1])
                last_group = items[last_dt_index:]

                # 清空dl元素
                for child in list(element.iterchildren()):
                    element.remove(child)

                # 添加第一组完整内容
                for item in first_group:
                    element.append(item)

                # 添加省略号
                ellipsis = etree.Element('span')
                ellipsis.text = '...'
                element.append(ellipsis)

                # 添加最后一组完整内容
                for item in last_group:
                    element.append(item)

    # 递归处理子元素
    for child in element:
        simplify_list(child)


def should_remove_element(element) -> bool:
    """判断元素的class或id属性是否匹配需要删除的模式."""
    # 检查class属性
    class_name = element.get('class', '')
    if class_name:
        class_parts = class_name.strip().split()
        for part in class_parts:
            # 检查是否完全匹配独立单词
            if part in ATTR_PATTERNS_TO_REMOVE:
                return True
            # 检查是否包含特定前缀/后缀
            for pattern in ATTR_SUFFIX_TO_REMOVE:
                if pattern in part:
                    return True

    # 检查id属性
    id_name = element.get('id', '')
    if id_name:
        id_parts = id_name.strip().split('-')  # id通常用连字符分隔
        for part in id_parts:
            # 检查是否完全匹配独立单词
            if part in ATTR_PATTERNS_TO_REMOVE:
                return True
            # 检查是否包含特定前缀/后缀
            for pattern in ATTR_SUFFIX_TO_REMOVE:
                if pattern in part:
                    return True

    # 检查style属性
    style_attr = element.get('style', '')
    if style_attr:
        if 'display: none' in style_attr or 'display:none' in style_attr:
            return True

    return False


def remove_specific_elements(element):
    """删除class或id名匹配特定模式的标签及其内容."""
    for child in list(element.iterchildren()):
        remove_specific_elements(child)

    if should_remove_element(element):
        parent = element.getparent()
        if parent is not None:
            parent.remove(element)


def truncate_text_content(element, max_length=500):
    """递归处理元素及其子元素的文本内容，总长度超过max_length时截断 但保持标签结构完整."""
    # 首先收集所有文本节点（包括text和tail）
    text_nodes = []

    # 收集元素的text
    if element.text and element.text.strip():
        text_nodes.append(('text', element, element.text))

    # 递归处理子元素
    for child in element:
        truncate_text_content(child, max_length)
        # 收集子元素的tail
        if child.tail and child.tail.strip():
            text_nodes.append(('tail', child, child.tail))

    # 计算当前元素下的总文本长度
    total_length = sum(len(text) for (typ, node, text) in text_nodes)

    # 如果总长度不超过限制，直接返回
    if total_length <= max_length:
        return

    # 否则进行截断处理
    remaining = max_length
    for typ, node, text in text_nodes:
        if remaining <= 0:
            # 已经达到限制，清空剩余的文本内容
            if typ == 'text':
                node.text = None
            else:
                node.tail = None
            continue

        if len(text) > remaining:
            # 需要截断这个文本节点
            if typ == 'text':
                node.text = text[:remaining] + '...'
            else:
                node.tail = text[:remaining] + '...'
            remaining = 0
        else:
            remaining -= len(text)


def process_paragraphs(paragraphs: List[Dict[str, str]], uid_map: Dict[str, html.HtmlElement], is_xpath: bool = True) -> Tuple[str, html.HtmlElement]:
    """处理段落并添加 _item_id，同时在原始DOM的对应元素上添加相同ID.

    Args:
        paragraphs: 段落列表，每个段落包含html、content_type和_original_element
        original_dom: 原始DOM树

    Returns:
        Tuple[简化后的HTML, 标记后的原始DOM]
    """
    result = []
    item_id = 1

    for para in paragraphs:
        try:
            html_content = re.sub(r'<!--.*?-->', '', para['html'], flags=re.DOTALL)
            # 解析段落HTML
            root = html.fromstring(html_content)
            root_for_xpath = copy.deepcopy(root)
            content_type = para.get('content_type', 'block_element')

            # 公共处理步骤
            clean_attributes(root)
            simplify_list(root)
            remove_inline_tags(root)

            # 跳过无意义内容
            if not is_meaningful_content(root):
                continue

            # 截断过长的文本内容
            truncate_text_content(root, max_length=1000)

            para_xpath = []
            if is_xpath:
                if content_type in ('inline_elements', 'mixed'):
                    for child in root_for_xpath.iterchildren():
                        original_element = uid_map.get(child.get('data-uid'))
                        try:
                            _xpath = get_relative_xpath(original_element)
                        except Exception:
                            _xpath = None
                        para_xpath.append(_xpath)
                elif content_type == 'block_element':
                    try:
                        _xpath = get_relative_xpath(para['_original_element'])
                    except Exception:
                        _xpath = None
                    para_xpath.append(_xpath)
                else:
                    try:
                        _xpath = get_relative_xpath(para['_original_element'])
                    except Exception:
                        _xpath = None
                    para_xpath.append(_xpath)

            # 为当前段落和原始元素添加相同的 _item_id
            current_id = str(item_id)
            root.set('_item_id', current_id)

            # 对于非块级元素（inline_elements, unwrapped_text, mixed）
            original_parent = para['_original_element']  # 原网页中直接子元素的父节点
            if content_type != 'block_element':
                if original_parent is not None:
                    # root_for_xpath有子元素
                    if len(root_for_xpath) > 0:
                        if root_for_xpath.tag in inline_tags and uid_map.get(root_for_xpath.get('data-uid')).tag != 'body':
                            original_element = uid_map.get(root_for_xpath.get('data-uid'))
                            original_element.set('_item_id', current_id)
                        else:
                            # 收集需要包裹的子元素
                            children_to_wrap = []
                            for child in root_for_xpath.iterchildren():
                                child_uid = child.get('data-uid')
                                if child_uid and child_uid in uid_map:
                                    original_child = uid_map[child_uid]
                                    children_to_wrap.append(original_child)

                            if children_to_wrap:
                                # 确定包裹范围
                                first_child = children_to_wrap[0]
                                last_child = children_to_wrap[-1]

                                # 获取在父节点中的位置
                                start_idx = original_parent.index(first_child)
                                end_idx = original_parent.index(last_child)

                                # 收集所有需要移动的节点
                                nodes_to_wrap = []
                                for i in range(start_idx, end_idx + 1):
                                    nodes_to_wrap.append(original_parent[i])

                                # 处理前面的文本
                                leading_text = original_parent.text if start_idx == 0 else original_parent[
                                    start_idx - 1].tail

                                # 处理后面的文本
                                # trailing_text = last_child.tail

                                # 创建wrapper元素
                                wrapper = etree.Element('cc-alg-uc-tex')
                                wrapper.set('_item_id', current_id)

                                # 设置前面的文本
                                if leading_text:
                                    wrapper.text = leading_text
                                    if start_idx == 0:
                                        original_parent.text = None
                                    else:
                                        original_parent[start_idx - 1].tail = None

                                # 移动节点到wrapper中
                                for node in nodes_to_wrap:
                                    original_parent.remove(node)
                                    wrapper.append(node)

                                # 插入wrapper
                                original_parent.insert(start_idx, wrapper)

                                # 设置后面的文本
                                # if trailing_text:
                                #     wrapper.tail = trailing_text
                                #     last_child.tail = None
                    else:
                        if content_type == 'inline_elements':
                            original_element = uid_map.get(root_for_xpath.get('data-uid'))
                            original_element.set('_item_id', current_id)
                        else:
                            # root_for_xpath只有文本内容
                            if root_for_xpath.text and root_for_xpath.text.strip():
                                # 1. 在原始DOM中查找匹配的文本节点
                                found = False

                                # 检查父节点的text
                                if original_parent.text and original_parent.text.strip() == root_for_xpath.text.strip():
                                    # 创建wrapper
                                    wrapper = etree.Element('cc-alg-uc-tex')
                                    wrapper.set('_item_id', current_id)
                                    wrapper.text = original_parent.text

                                    # 替换父节点的text
                                    original_parent.text = None

                                    # 插入wrapper作为第一个子节点
                                    if len(original_parent) > 0:
                                        original_parent.insert(0, wrapper)
                                    else:
                                        original_parent.append(wrapper)

                                    found = True

                                # 检查子节点的tail
                                if not found:
                                    for child in original_parent.iterchildren():
                                        if child.tail and child.tail.strip() == root_for_xpath.text.strip():
                                            # 创建wrapper
                                            wrapper = etree.Element('cc-alg-uc-tex')
                                            wrapper.set('_item_id', current_id)
                                            wrapper.text = child.tail

                                            # 替换tail
                                            child.tail = None

                                            # 插入wrapper到子节点之后
                                            parent = child.getparent()
                                            index = parent.index(child)
                                            parent.insert(index + 1, wrapper)

                                            found = True
                                            break

                                # 如果没有找到匹配的文本节点，使用父节点作为包裹对象
                                if not found:
                                    wrapper = etree.Element('cc-alg-uc-tex')
                                    wrapper.set('_item_id', current_id)
                                    wrapper.text = root_for_xpath.text
                                    # 将父节点的内容移动到wrapper中
                                    for child in list(original_parent.iterchildren()):
                                        wrapper.append(child)
                                        original_parent.remove(child)

                                    # 添加wrapper到父节点
                                    original_parent.append(wrapper)
            else:
                # 块级元素直接设置属性
                original_parent.set('_item_id', current_id)

            item_id += 1

            # 保存处理结果
            cleaned_html = etree.tostring(root, method='html', encoding='unicode').strip()
            result.append({
                'html': cleaned_html,
                '_item_id': current_id,
                '_xpath': para_xpath,
                'content_type': content_type
            })

        except Exception:
            # import traceback
            # print(f'处理段落出错: {traceback.format_exc()}')
            continue

    # 组装最终HTML
    simplified_html = '<html><head><meta charset="utf-8"></head><body>' + ''.join(
        p['html'] for p in result) + '</body></html>'

    return post_process_html(simplified_html), result


def simplify_html(html_str, is_xpath: bool = True) -> etree.Element:
    """
   :return:
       simplified_html: 精简HTML
       original_html: 添加_item_id的原始HTML
       _xpath_mapping: xpath映射
   """
    # 预处理
    preprocessed_html = remove_xml_declaration(html_str)

    # 用 BeautifulSoup 修复未闭合标签，lxml 无法完全修复
    soup = BeautifulSoup(preprocessed_html, 'html.parser')
    fixed_html = str(soup)

    # 解析原始DOM
    original_dom = html.fromstring(fixed_html)
    add_data_uids(original_dom)
    original_uid_map = build_uid_map(original_dom)

    # 创建处理用的DOM（深拷贝）
    processing_dom = copy.deepcopy(original_dom)
    # 清理DOM
    remove_tags(processing_dom)
    remove_specific_elements(processing_dom)

    # 提取段落（会记录原始元素引用）
    paragraphs = extract_paragraphs(processing_dom, original_uid_map, include_parents=False)

    # 处理段落（同步添加ID）
    simplified_html, result = process_paragraphs(paragraphs, original_uid_map, is_xpath)

    remove_all_uids(original_dom)
    original_html = etree.tostring(original_dom, pretty_print=True, method='html', encoding='unicode')

    _xpath_mapping = {item['_item_id']: {
        '_xpath': item['_xpath'],
        'content_type': item['content_type']
    } for item in result}

    return simplified_html, original_html, _xpath_mapping
