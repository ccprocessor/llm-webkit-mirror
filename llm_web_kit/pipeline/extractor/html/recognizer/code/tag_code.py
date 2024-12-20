from lxml import etree

from functools import reduce


def detect(body: etree._Element) -> bool:
    for _ in body.iter("code"):
        return True
    return False


def split_code(body: etree._Element) -> list[tuple[str, str]]:
    node_paths: list[str] = []
    node_paths_chunks: list[list[str]] = []
    tree: etree._ElementTree = etree.ElementTree(body)
    for code_node in body.iter("code"):
        assert isinstance(code_node, etree._Element)
        node_path: str = tree.getpath(code_node)
        node_paths.append(node_path)
        node_paths_chunks.append(node_path.split("/"))

    dist: list[list[int]] = [[0] * len(node_paths)] * len(node_paths)
    for i in range(len(node_paths)):
        for j in range(len(node_paths)):
            if i == j:
                dist[i][j] = 0
            else:
                for idx, (x, y) in enumerate(
                    zip(node_paths_chunks[i], node_paths_chunks[j])
                ):
                    if x != y:
                        common_node_idx = idx
                        break

                dist[i][j] = (
                    len(node_paths_chunks[i])
                    + len(node_paths_chunks[j])
                    - common_node_idx * 2
                )

    dist_flat = sorted(reduce(lambda x, y: x + y, dist, []))
    dist_map = {}
    for x in dist_flat:
        if x not in dist_map:
            dist_map[x] = 0
        dist_map[x] += 1
    print(dist_map)
    return []
