from collections import Counter, defaultdict
from typing import Dict, List

import numpy as np
from lxml import html
from lxml.html import HtmlComment, HtmlElement
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import cosine_similarity

TAGS_TO_IGNORE = ['script', 'style', 'meta', 'link', 'br', 'noscript']  # , 'b', 'i', 'strong'
TAGS_IGNORE_ATTR = ['a', 'i', 'b', 'li', 'tr', 'td', 'img', 'p', 'body']


def __parse_html_to_tree(html_source: str) -> HtmlElement:
    # html转element并获取有效DOM结构数据
    tree = html.fromstring(html_source)
    root = tree.find('body') if tree.find('body') is not None else tree
    return root


def __combine_dicts_with_defaultdict(dict_list):
    # 按照layer构建树结构
    tag_dict = defaultdict(set)
    attr_dict = defaultdict(set)

    for item in dict_list:
        for key, value in item.items():
            if key == '0':
                continue
            tag_dict[key].add(value['tags'])
            if value.get('attrs'):
                [attr_dict[key].add(i) for i in value['attrs']]
    return {'tags': {k: list(v) for k, v in tag_dict.items()}, 'attrs': {k: list(v) for k, v in attr_dict.items()}}


def get_feature(html_source: str) -> dict:
    # 获取DOM有效数据
    doc = __parse_html_to_tree(html_source)
    return __combine_dicts_with_defaultdict(__recursive_extract_tags(doc))


def __recursive_extract_tags(el, current_path=None):
    # 递归获取标签及属性
    if current_path is None:
        current_path = []
    if isinstance(el, HtmlComment) or el.tag.lower() in TAGS_TO_IGNORE:
        return []
    tag = el.tag.lower()
    index = 0
    full_path = current_path[-1] + '/' + tag if current_path else tag
    if tag in TAGS_IGNORE_ATTR:
        tags = [{len(current_path): {'tags': full_path}}]
        pass
    else:
        attrs_str = [v for k, v in el.attrib.items() if k in ['class', 'id'] and v]
        # 计算当前节点在其父节点中的位置（索引从1开始）
        try:
            index = len(el.xpath(f'preceding-sibling::{tag}')) + 1
        except Exception:
            return []
        tags = [{len(current_path): {'tags': full_path, 'attrs': attrs_str}}]

    if index:
        current_path.append(f'<{tag}>[{index}]')
    else:
        current_path.append(f'<{tag}>')

    for child in el.getchildren():
        if child.tag is not None:
            tags.extend(__recursive_extract_tags(child, current_path))

    current_path.pop()
    return tags


def __list_to_dict(lst):
    res = {}
    for d in lst:
        res.update(d)
    return res


def __feature_vec(feature1, feature2):
    if not feature1 and not feature2:
        return 1
    vectorizer = DictVectorizer(sparse=False)
    X = vectorizer.fit_transform([feature1, feature2])
    return cosine_similarity(X)[0][1]


def cosin_similarity(feature1: dict, feature2: dict, k=0.5):
    # 相似度计算
    tag_sim = __feature_vec(feature1.get('tags', {}), feature2.get('tags', {}))
    attr_sim = __feature_vec(feature1.get('attrs', {}), feature2.get('attrs', {}))

    cos_sim = tag_sim * k + attr_sim * (1 - k)
    return cos_sim


def __simp_tags(d: dict, layer_n: int):
    # 根据layer_n获取有效内容
    return __list_to_dict([{tag: 1 for tag in v} for k, v in d.items() if k < layer_n])


def __simp_features(features_list: list, layer_n: int):
    res_feature = []
    for feature in features_list:
        res_feature.append({'tags': __simp_tags(feature.get('tags', {}), layer_n),
                            'attrs': __simp_tags(feature.get('attrs', {}), layer_n)})
    return res_feature


def cluster_html_struct(sampled_list: List[Dict], current_host_name: str, threshold=0.95) -> List[Dict]:
    # 批量domain数据计算layout
    success = []
    layout_list = []
    features = [tt['feature'] for tt in sampled_list]

    layer_max_l = []
    for data in features:
        max_key = max(data['tags'], key=lambda k: len(data['tags'][k]))
        layer_max_l.append(max_key)
    counter = Counter(layer_max_l)
    layer_n = counter.most_common(1)[0][0]
    print(f'max layer_n: {layer_n}')

    features = __simp_features(features, layer_n)

    features_num = len(features)
    similarity_matrix = np.zeros((features_num, features_num))
    for i in range(features_num):
        for j in range(i, features_num):
            if i == j:
                simil_rate = 1.0
            else:
                simil_rate = cosin_similarity(features[i], features[j])
            similarity_matrix[i, j] = simil_rate
            similarity_matrix[j, i] = simil_rate
    similarity_matrix = np.clip(similarity_matrix, 0, 1)
    clustering = DBSCAN(eps=1 - threshold, min_samples=2, metric='precomputed')
    layout_ids = clustering.fit_predict(1 - similarity_matrix)
    print(f'layout_ids:{layout_ids}')
    for idd, data in zip(layout_ids, sampled_list):
        layout_list.append(int(idd))
        data['layout_id'] = int(idd)
        data['sub_path'] = f'{current_host_name}_{idd}'
        success.append(data)
    return success, list(set(layout_list))

# import time
# import json
#
# start_time = time.time()
# path = r"D:\ls\layout.json"
# # path = r"D:\ls\test_layout.json"
# # path = r"D:\ls\test_layout1.json"
# sample_list = []
# current_host_name = "M211bmlvbi5uZXQ="
# with open(path, "r", encoding="utf-8") as f:
#     datas = f.readlines()
#     idx = 0
#     unfeature = []
#     for detail_datas in datas:
#         if idx > 1:
#             break
#         idx += 1
#         detail_datas = json.loads(detail_datas)
#         print(detail_datas["html"])
#         html_structure = get_feature(detail_datas["html"])
#         print('--------\n' * 5)
#         print(html_structure)
#         detail_datas["feature"] = html_structure
#         sample_list.append(detail_datas)
#
# res, layout_list = cluster_html_struct(sample_list, current_host_name)
# print(layout_list)
# end_time = time.time()
# print("total spend time", end_time - start_time)
