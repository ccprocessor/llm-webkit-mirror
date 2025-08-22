import re
from typing import Dict, List, Optional

from lxml import etree

from llm_web_kit.html_layout.html_layout_cosin import (RE_MD5, RE_NUM, RE_SHA1,
                                                       RE_TIMESTAMP, RE_UUID)
from llm_web_kit.libs.html_utils import element_to_html, html_to_element


def restore_html_trim_ends_only(processed_html: str, llm_response: Dict[str, int]) -> Dict[str, object]:
    """只删除HTML开头和结尾连续状态为0的元素，保留其他所有元素， 并删除所有的_item_id属性。同时将删除的节点信息记录在
    post_delete_node 字段中，删除规则。

    Args:
        processed_html: 带有_item_id属性的HTML字符串
        llm_response: LLM的响应，格式为 {'item_id 1': 0, 'item_id 2': 1, ...}
                     0表示删除，1表示保留

    Returns:
        { 'html': 处理后的HTML字符串, 'post_delete_node': List[dict] }
    """
    if not processed_html:
        return {'html': '', 'post_delete_node': []}
    if not llm_response:
        # 如果没有LLM响应，则返回原始HTML
        return {'html': processed_html, 'post_delete_node': []}

    try:
        tree = html_to_element(processed_html)
    except Exception as e:
        raise ValueError(f'Invalid HTML input: {e}')

    # 预处理LLM响应：转换为{item_id: 状态}的字典
    item_status = {}
    for key, status in llm_response.items():
        # 提取'item_id X'中的数字X作为item_id
        item_id = int(key.split()[1])
        item_status[item_id] = status

    # 只处理开头和结尾的删除元素，并记录删除信息
    deletion_logger = _DeletionLogger()
    __trim_ends_only(tree, item_status, deletion_logger)

    # 移除所有_item_id属性
    __remove_all_item_id_attributes(tree)

    return {'html': element_to_html(tree), 'post_delete_node': deletion_logger.records}


def __trim_ends_only(
    tree: etree.Element,
    item_status: Dict[int, int],
    deletion_logger: '_DeletionLogger',
) -> None:
    """只删除开头和结尾连续状态为0的元素.

    Args:
        tree: HTML DOM树根节点
        item_status: 元素状态字典
    """
    # 获取所有带_item_id的元素
    elements = tree.xpath('//*[@_item_id]')
    if not elements:
        return

    # 从开头删除连续状态为0的元素
    start_index = 0
    while start_index < len(elements):
        element = elements[start_index]
        try:
            item_id = int(element.get('_item_id', ''))
        except ValueError:
            start_index += 1
            continue

        status = item_status.get(item_id, 1)
        if status == 0:
            # 记录并删除元素及内容，并检查父节点是否需要删除
            __remove_element_and_check_parent(
                root=tree,
                element=element,
                del_location='start',
                deletion_logger=deletion_logger
            )
            start_index += 1
        else:
            break  # 遇到保留状态的元素，停止删除

    # 重新获取元素列表（因为可能有变化）
    elements = tree.xpath('//*[@_item_id]')
    if not elements:
        return

    # 从结尾删除连续状态为0的元素
    end_index = len(elements) - 1
    while end_index >= 0:
        element = elements[end_index]
        try:
            item_id = int(element.get('_item_id', ''))
        except ValueError:
            end_index -= 1
            continue

        status = item_status.get(item_id, 1)
        if status == 0:
            # 记录并删除元素及内容，并检查父节点是否需要删除
            __remove_element_and_check_parent(
                root=tree,
                element=element,
                del_location='end',
                deletion_logger=deletion_logger
            )
            end_index -= 1
        else:
            break  # 遇到保留状态的元素，停止删除


def __remove_element_and_check_parent(
    *,
    root: etree.Element,
    element: etree.Element,
    del_location: str,
    deletion_logger: '_DeletionLogger',
) -> None:
    """删除元素并检查其父节点是否需要删除.

    Args:
        element: 要删除的元素
    """
    # 在移除前记录要删除的元素
    deletion_logger.record_element(root, element, del_location)

    parent = element.getparent()
    if parent is None:
        return

    # 记录父节点原始状态
    parent_has_item_id = '_item_id' in parent.attrib

    # 直接从父节点中移除元素
    parent.remove(element)

    # 如果父节点有_item_id，不需要进一步处理
    if parent_has_item_id:
        return

    # 检查父节点是否还有子元素或者文本内容
    __check_and_remove_empty_parent(root, parent, del_location, deletion_logger)


def __check_and_remove_empty_parent(
    root: etree.Element, parent: etree.Element, del_location: str, deletion_logger: '_DeletionLogger'
) -> None:
    """检查父节点是否为空，如果为空则删除它（递归检查）

    Args:
        parent: 要检查的父节点
    """
    # 检查父节点是否为空（没有子元素且没有文本内容）
    last_snapshot: Optional[dict] = None
    while parent is not None and __is_element_empty(parent):
        grandparent = parent.getparent()

        # 如果父节点有_item_id，停止递归
        if '_item_id' in parent.attrib:
            break

        # 如果没有父节点（已经是根节点），停止递归
        if grandparent is None:
            break

        # 在移除前拍摄快照，用于最终仅记录最顶层被级联删除的父节点
        last_snapshot = deletion_logger.snapshot_element(root, parent, del_location)
        # 移除空的父节点
        grandparent.remove(parent)
        parent = grandparent

    # 仅在存在级联删除时，记录一次父节点删除，并清理其所有子节点的记录
    if last_snapshot is not None:
        deletion_logger.prune_descendants_and_record_parent(last_snapshot)


class _DeletionLogger:
    """记录被删除节点的信息，并在父节点被级联删除时，仅保留父节点记录。

    记录字段示例：
    {
        'xpath': '/html/body/div[1]/p[2]',
        'tag': 'p',
        'attributes': {'class': 'note', 'id': 'note'},
        'index_in_parent': 1,
        'parent_xpath': '/html/body/div[1]',
        'parent_tag': 'div',
        'parent_attributes': {'class': 'container', 'id': 'container'}
    }
    """

    def __init__(self) -> None:
        self.records: List[dict] = []
        self._xpaths: set[str] = set()

    def _compute_xpath(self, root: etree.Element, element: etree.Element) -> str:
        # 使用 root 构建 ElementTree，并计算 element 的 XPath
        try:
            return etree.ElementTree(root).getpath(element)
        except Exception:
            # 尝试使用 element 自己的 roottree
            try:
                return element.getroottree().getpath(element)
            except Exception:
                return ''

    def snapshot_element(self, root: etree.Element, element: etree.Element, del_location: str) -> dict:
        xpath = self._compute_xpath(root, element)
        parent = element.getparent()
        parent_xpath = self._compute_xpath(root, parent) if parent is not None else ''
        parent_tag = parent.tag if parent is not None else ''
        parent_attributes = self.parse_attrs(parent) if parent is not None else {}

        index_in_parent = -1
        if parent is not None:
            try:
                index_in_parent = list(parent).index(element)
            except ValueError:
                index_in_parent = -1

        attrs = self.parse_attrs(element)

        snapshot = {
            'del_location': del_location,
            'xpath': xpath,
            'tag': element.tag,
            'attributes': attrs,
            'index_in_parent': index_in_parent,
            'parent_xpath': parent_xpath,
            'parent_tag': parent_tag,
            'parent_attributes': parent_attributes,
        }
        return snapshot

    def parse_attrs(self, element: etree.Element) -> Dict:
        attrs = {k: self.dynamic_attributes_preprocess(v) for k, v in element.attrib.items() if
                 k in ['class', 'id']} if element.attrib else {}
        return attrs

    def dynamic_attributes_preprocess(self, attr_str: str) -> str:
        """动态属性值标准化处理."""
        res_attr_str = ''
        if attr_str:
            attr_lst = attr_str.split()
            if len(attr_lst) > 1:
                res_attr_str = ' '.join([i for i in attr_lst if not RE_NUM.search(i)])
            elif len(attr_lst) == 1:
                res_attr_str = self.standardizing_dynamic_attributes(attr_lst[0])
        return res_attr_str

    def standardizing_dynamic_attributes(self, attr_value: str) -> str:
        """将动态属性值标准化为统一表示."""
        if RE_MD5.fullmatch(attr_value):
            return '[MD5]'
        if RE_SHA1.fullmatch(attr_value):
            return '[SHA1]'
        if RE_UUID.fullmatch(attr_value):
            return '[UUID]'
        if RE_TIMESTAMP.fullmatch(attr_value):
            return '[TIMESTAMP]'
        if RE_NUM.search(attr_value):
            return re.sub(r'\d+', '', attr_value)

        return attr_value

    def record_element(self, root: etree.Element, element: etree.Element, del_location: str) -> None:
        snap = self.snapshot_element(root, element, del_location)
        # 去重：相同 xpath 的记录只保留一次（优先保留先记录的）
        if snap['xpath'] and snap['xpath'] not in self._xpaths:
            self.records.append(snap)
            self._xpaths.add(snap['xpath'])

    def prune_descendants_and_record_parent(self, parent_snapshot: dict) -> None:
        """删除所有位于 parent_snapshot['xpath'] 之下的子节点记录，仅保留父节点记录。"""
        parent_xpath = parent_snapshot.get('xpath', '')
        if not parent_xpath:
            return

        # 过滤掉所有子孙节点记录
        kept: List[dict] = []
        new_xpaths: set[str] = set()
        prefix = parent_xpath + '/'
        for rec in self.records:
            xp = rec.get('xpath', '')
            if xp == parent_xpath or xp.startswith(prefix):
                # 丢弃，稍后添加父节点快照
                continue
            kept.append(rec)
            if xp:
                new_xpaths.add(xp)

        # 添加父节点快照（若未存在）
        if parent_xpath not in new_xpaths:
            kept.append(parent_snapshot)
            new_xpaths.add(parent_xpath)

        self.records = kept
        self._xpaths = new_xpaths


def __is_element_empty(element: etree.Element) -> bool:
    """检查元素是否为空（没有子元素且没有有意义的文本内容）

    Args:
        element: 要检查的元素

    Returns:
        如果元素为空返回True，否则返回False
    """
    # 检查是否有子元素
    if len(element) > 0:
        return False

    # 检查是否有文本内容
    if element.text and element.text.strip():
        return False

    # 检查是否有tail内容
    if element.tail and element.tail.strip():
        return False

    return True


def __remove_all_item_id_attributes(tree: etree.Element) -> None:
    """移除DOM树中所有元素的_item_id属性.

    Args:
        tree: HTML DOM树根节点
    """
    for element in tree.iter():
        if '_item_id' in element.attrib:
            del element.attrib['_item_id']
