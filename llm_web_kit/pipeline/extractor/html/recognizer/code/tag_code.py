import html

from lxml import etree

from llm_web_kit.pipeline.extractor.html.recognizer.code.common import detect_language


def detect(body: etree._Element) -> bool:
    for _ in body.iter("code"):
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

    return ["/".join(root_path) for root_path in root_paths]


def split_tree_by_roots(
    root: etree._ElementTree,
    node: etree._Element,
    tree_roots: list[str],
) -> list[tuple[str, str]]:
    node_path: str = root.getpath(node)
    node_path = node_path.removeprefix("/html")
    hit = False
    prefix_hit = False
    for tree_root in tree_roots:
        if tree_root.startswith(node_path):
            prefix_hit = True
        if tree_root == node_path:
            hit = True

    if not prefix_hit:
        html_str: str = etree.tostring(node).decode()
        return [(html_str, html_str)]

    if hit:
        language = detect_language(node)
        html_str: str = etree.tostring(node).decode()
        full_text = "".join(node.itertext(None))
        full_text: str = html.escape(full_text)
        code_str = (
            f'<cccode language="{language}" by="tag_code">\n{full_text}\n</cccode>'
        )
        return [(html_str, code_str)]

    rtn: list[tuple[str, str]] = []
    if node.text:
        rtn.append((node.text, node.text))
    for cnode in node.getchildren():
        assert isinstance(cnode, etree._Element)
        rtn.extend(split_tree_by_roots(root, cnode, tree_roots))
        if cnode.tail:
            rtn.append((cnode.tail, cnode.tail))
    return rtn


def split_code(body: etree._Element) -> list[tuple[str, str]]:
    node_paths: list[list[str]] = []
    tree: etree._ElementTree = etree.ElementTree(body)
    for code_node in body.iter("code"):
        assert isinstance(code_node, etree._Element)
        node_path: str = tree.getpath(code_node)
        node_paths.append(node_path.split("/"))

    dist = get_dist(node_paths)

    # TODO: cut dist

    cut = 4

    tree_roots = get_tree_roots(node_paths, cut, dist)
    return split_tree_by_roots(tree, body, tree_roots)
