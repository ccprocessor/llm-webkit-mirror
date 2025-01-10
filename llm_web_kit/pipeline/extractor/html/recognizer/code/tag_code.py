from lxml.html import HtmlElement

from llm_web_kit.pipeline.extractor.html.recognizer.code.common import \
    replace_node_by_cccode

"""
处理仅由<code>标签组成的代码块
"""


def __group_code_by_distance(
    root: HtmlElement,
    node_paths: list[list[str]],
    dist: list[list[int]],
) -> list[str]:
    father = list(range(len(node_paths)))

    def get_father(x: int) -> int:
        if father[x] == x:
            return x
        father[x] = get_father(father[x])
        return father[x]

    edges: list[tuple[int, int, int]] = []
    root_paths: list[list[str]] = []
    for i in range(len(node_paths)):
        root_paths.append(node_paths[i])
        for j in range(i + 1, len(node_paths)):
            edges.append((dist[i][j], i, j))
    edges = sorted(edges)

    def check_trees_done(length: int) -> bool:
        for i in range(len(node_paths)):
            if i == get_father(i):
                path = '/'.join(root_paths[i])
                path = path.removeprefix('/html/')
                text = ''.join(root.find(path, {'og': 'http://ogp.me/ns'}).itertext())
                # 替换之前的 magic number
                # 如果出现一棵子树，其组成的内容不存在任何单词
                # 那么认为它是用于代码格式化的空白换行结构，或是 { } 等格式符号
                # 即：代码的树依旧不完整
                if not any(c.isalpha() for c in text):
                    return False
        return True

    used_edge = 0
    edge_len = edges[0][0]
    for edge in edges:
        l, i, j = edge
        i = get_father(i)
        j = get_father(j)
        if i != j:
            if l > edge_len:
                if check_trees_done(l):
                    break
                edge_len = l
            used_edge += 1
            father[j] = i
            for idx, (x, y) in enumerate(zip(root_paths[i], root_paths[j])):
                if idx == 0:
                    continue
                if x != y:
                    common_node_idx = idx
                    break
            root_paths[i] = root_paths[i][:common_node_idx]

    root_paths = [
        root_path for i, root_path in enumerate(root_paths) if i == get_father(i)
    ]

    removed = set()
    root_paths_joined = sorted(
        list(set(['/'.join(root_path) for root_path in root_paths]))
    )
    for x in root_paths_joined:
        for y in root_paths_joined:
            if len(x) < len(y) and y.startswith(x):
                removed.add(y)
    return [x for x in root_paths_joined if x not in removed]


def __compute_distance_matrix(node_paths: list[list[str]]) -> list[list[int]]:
    """
    计算节点路径的距离矩阵，具体步骤：
    1. 创建距离矩阵，计算每两个节点之间的距离
    2. 距离计算方法：从共同祖先节点到两个节点的路径长度之和
    例如：
    节点1路径：/html/body/div/code
    节点2路径：/html/body/pre/code
    共同祖先到 body，距离为 2（div->code) + 2(pre->code) = 4
    节点1和节点2的距离为 4

    距离矩阵（对称矩阵）：
    [0, 1, 2, 3],
    [1, 0, 1, 2],
    [2, 1, 0, 1],
    [3, 2, 1, 0]

    Args:
        node_paths: 节点路径

    Returns:
        list[list[int]]: 距离矩阵
    """
    def get_lca_depth(path1: list[str], path2: list[str]) -> int:
        for i, (x, y) in enumerate(zip(path1, path2)):
            if x != y:
                return i
        return min(len(path1), len(path2))

    n = len(node_paths)
    dist = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            lca_depth = get_lca_depth(node_paths[i], node_paths[j])
            d = len(node_paths[i]) + len(node_paths[j]) - 2 * lca_depth
            dist[i][j] = dist[j][i] = d

    return dist


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
    for _ in body.iter('code'):
        return True
    return False


def modify_tree(root: HtmlElement) -> None:
    """将 html 树中所有 code 标签转换为代码块.

    Args:
        root: html 树的根节点
    """
    node_paths = __get_code_node_paths(root)  # 获取所有 code 标签的路径，不包含嵌套的子code 标签
    dist_matrix = __compute_distance_matrix(node_paths)  # 计算距离矩阵
    tree_roots = __group_code_by_distance(root, node_paths, dist_matrix)  # 根据距离矩阵，对code标签进行分组

    nodes = __get_code_blocks_nodes(root, tree_roots)  # 获取所有需要被转换为代码块的节点，并进行标签替换
    for node in nodes:
        replace_node_by_cccode(node, 'tag_code')
