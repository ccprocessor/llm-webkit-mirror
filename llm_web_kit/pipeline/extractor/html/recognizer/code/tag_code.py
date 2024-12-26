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
    print(dist_counter)

    return dist


def get_tree_roots(
    node_paths: list[list[str]],
    cut: int,
    dist: list[list[int]],
) -> list[str]:
    father = list(range(len(node_paths)))

    def get_father(x: int) -> int:
        if father[x] == x:
            return x
        father[x] = get_father(father[x])
        return father[x]

    for nlen in range(1, cut + 1):
        for i in range(len(node_paths)):
            for j in range(len(node_paths)):
                if dist[i][j] == nlen and get_father(i) != get_father(j):
                    father[i] = father[j]

    tree_size = [0] * len(node_paths)
    for i in range(len(node_paths)):
        tree_size[get_father(i)] += 1

    root_paths: list[list[str]] = []

    tree_index = -1
    for i in range(len(node_paths)):
        if tree_size[i]:
            root_paths.append(node_paths[i])
            tree_index += 1

            for j in range(len(node_paths)):
                if i != j and get_father(j) == i:
                    for idx, (x, y) in enumerate(
                        zip(root_paths[tree_index], node_paths[j])
                    ):
                        if idx == 0:
                            continue
                        if x != y:
                            common_node_idx = idx
                            break
                    root_paths[tree_index] = root_paths[tree_index][:common_node_idx]

    removed = set()
    root_paths_joined = ['/'.join(root_path) for root_path in root_paths]
    for x in root_paths_joined:
        for y in root_paths_joined:
            if len(x) < len(y) and y.startswith(x):
                removed.add(y)
    return [x for x in root_paths_joined if x not in removed]


def modify_tree_by_roots(
    root: etree._ElementTree,
    node: etree._Element,
    tree_roots: list[str],
) -> None:
    node_path: str = root.getpath(node)
    hit = False
    prefix_hit = False
    for tree_root in tree_roots:
        if tree_root.startswith(node_path):
            prefix_hit = True
        if tree_root == node_path:
            hit = True

    if not prefix_hit:
        return

    if hit:
        replace_node_by_cccode(node, 'tag_code')
        return

    for cnode in node.getchildren():
        assert isinstance(cnode, etree._Element)
        modify_tree_by_roots(root, cnode, tree_roots)


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

    cut = 6  # magic number

    tree_roots = get_tree_roots(node_paths, cut, dist)

    for tree_root in tree_roots:
        print(tree_root)

    modify_tree_by_roots(tree, root, tree_roots)
