from lxml import etree

from llm_web_kit.pipeline.extractor.html.recognizer.code.common import \
    replace_node_by_cccode


def detect(body: etree._Element) -> bool:
    for _ in body.iter('code'):
        return True
    return False


def get_dist(node_paths: list[list[str]]) -> list[list[int]]:
    dist: list[list[int]] = []
    for i in range(len(node_paths)):
        dist.append([])
        for j in range(len(node_paths)):
            if i == j:
                dist[i].append(0)
            elif i > j:
                dist[i].append(dist[j][i])
            else:
                common_node_idx = min(len(node_paths[i]), len(node_paths[j]))
                for idx, (x, y) in enumerate(zip(node_paths[i], node_paths[j])):
                    if idx == 0:
                        # node_paths[x][0] is always 'body'
                        continue
                    if x != y:
                        common_node_idx = idx
                        break
                d = len(node_paths[i]) + len(node_paths[j]) - common_node_idx * 2
                dist[i].append(d)

    dist_counter = {}
    for i in range(len(node_paths)):
        for j in range(len(node_paths)):
            if dist[i][j] not in dist_counter:
                dist_counter[dist[i][j]] = 0
            dist_counter[dist[i][j]] += 1
    dist_counter = dict(sorted(list(dist_counter.items())))
    # print(dist_counter)

    return dist


def get_tree_roots(
    root: etree._Element,
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
        # print(l)
        # print()
        # print()
        for i in range(len(node_paths)):
            if i == get_father(i):
                path = '/'.join(root_paths[i])
                path = path.removeprefix('/html/')
                # print('------------------------------------')
                text = ''.join(root.find(path, {'og': 'http://ogp.me/ns'}).itertext())
                # print(text)
                # print('------------------------------------')
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

    # print(used_edge)

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


def get_candidates(
    root: etree._ElementTree,
    node: etree._Element,
    tree_roots: list[str],
) -> list[etree._Element]:
    node_path: str = root.getpath(node)
    hit = False
    prefix_hit = False
    for tree_root in tree_roots:
        if tree_root.startswith(node_path):
            prefix_hit = True
        if tree_root == node_path:
            hit = True

    if not prefix_hit:
        return []

    if hit:
        return [node]

    rtn = []
    for cnode in node.getchildren():
        assert isinstance(cnode, etree._Element)
        rtn.extend(get_candidates(root, cnode, tree_roots))
    return rtn


def get_node_paths(tree: etree._ElementTree, body: etree._Element) -> list[list[str]]:
    node_set: set[str] = set()
    node_paths: list[list[str]] = []

    for code_node in body.iter('code'):
        assert isinstance(code_node, etree._Element)
        node_path: str = tree.getpath(code_node)
        node_set.add(node_path)

    remove_node_set: set[str] = set()
    # 如果出现 code 嵌套 code，取最外层
    for maybe_parent in node_set:
        for maybe_child in node_set:
            if len(maybe_parent) < len(maybe_child):
                if maybe_child.startswith(maybe_parent):
                    remove_node_set.add(maybe_child)
    node_set = {node_path for node_path in node_set if node_path not in remove_node_set}

    for node_path in node_set:
        node_paths.append(node_path.split('/'))

    return node_paths


def modify_tree(root: etree._Element) -> None:
    tree: etree._ElementTree = etree.ElementTree(root)
    node_paths = get_node_paths(tree, root)

    dist = get_dist(node_paths)

    tree_roots = get_tree_roots(root, node_paths, dist)

    # for tree_root in tree_roots:
    #     print(tree_root)

    nodes = get_candidates(tree, root, tree_roots)
    for node in nodes:
        replace_node_by_cccode(node, 'tag_code')
