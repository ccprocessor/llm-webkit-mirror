import copy
import re
import uuid
from typing import Dict, List, Tuple

from lxml import etree, html

# 行内标签
inline_tags = {
    'map', 'optgroup', 'span', 'br', 'input', 'time', 'u', 'td', 'strong', 'textarea', 'small', 'sub',
    'samp', 'blink', 'b', 'code', 'nobr', 'strike', 'bdo', 'basefont', 'abbr', 'var', 'i', 'cccode-inline',
    'th', 'select', 's', 'pic', 'label', 'mark', 'object', 'dd', 'dt', 'ccmath-inline', 'svg', 'li',
    'button', 'a', 'font', 'dfn', 'sup', 'kbd', 'q', 'script', 'acronym', 'option', 'img', 'big', 'cite',
    'em'
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
    path = []
    root_element = element.getroottree().getroot()

    while element is not None and element.getparent() is not None:
        siblings = [sib for sib in element.getparent() if sib.tag == element.tag]

        found_unique_attr = False  # 初始化变量

        if len(siblings) > 1:
            # 如果有多个同名兄弟节点，则尝试使用属性路径来区分
            candidate_attrs = [
                attr for attr in element.attrib
                if not (attr.startswith('data-') or attr == 'style' or
                        attr == '_item_id' or
                        (element.attrib[attr].startswith('{') and element.attrib[attr].endswith('}')))
            ]

            for attr in candidate_attrs:
                if is_unique_attribute(root_element.getroottree(), attr, element.attrib[attr]):
                    # 插入唯一属性的XPath片段
                    path.insert(0, f'*[@{attr}="{element.attrib[attr]}"]')
                    found_unique_attr = True
                    break

            if not found_unique_attr:
                index = siblings.index(element) + 1
                path.insert(0, f'{element.tag}[{index}]')
        else:
            # 如果没有同名兄弟节点，则直接使用标签名
            path.insert(0, element.tag)

        # 提前返回简化版本的XPath，如果当前元素有一个唯一属性
        if found_unique_attr:
            simplified_path = f'//{"/".join(path)}'
            return simplified_path

        element = element.getparent()

    # 返回完整路径
    return f'//{"/".join(path)}'


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

    def is_block_element(node) -> bool:
        """判断是否为块级元素."""
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
    return re.sub(pattern, '', html_string, flags=re.DOTALL)


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
    """递归移除所有指定的行内标签（包括嵌套情况），保留img和br标签 优化点：确保文本顺序正确，正确处理嵌套标签的文本转移."""
    # 先处理子元素（深度优先）
    for child in list(element.iterchildren()):
        remove_inline_tags(child)

    # 如果当前元素是需要移除的行内标签
    if element.tag in inline_tags and element.tag not in EXCLUDED_TAGS:
        parent = element.getparent()
        if parent is None:
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
            # print(f"para: {para['html']}")
            # 解析段落HTML
            root = html.fromstring(post_process_html(para['html']))
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

            # 为当前段落和原始元素添加相同的 _item_id
            current_id = str(item_id)
            root.set('_item_id', current_id)
            para['_original_element'].set('_item_id', current_id)

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

            item_id += 1

            # 保存处理结果
            cleaned_html = etree.tostring(root, encoding='unicode').strip()
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

    return simplified_html, result


def simplify_html(html_str, is_xpath: bool = True) -> etree.Element:
    """
   :return:
       simplified_html: 精简HTML
       original_html: 添加_item_id的原始HTML
       _xpath_mapping: xpath映射
   """
    # 预处理
    preprocessed_html = remove_xml_declaration(html_str)

    # 解析原始DOM
    original_dom = html.fromstring(preprocessed_html)
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
    original_html = etree.tostring(original_dom, pretty_print=True, encoding='unicode')

    _xpath_mapping = {item['_item_id']: {
        '_xpath': item['_xpath'],
        'content_type': item['content_type']
    } for item in result}

    return simplified_html, original_html, _xpath_mapping
