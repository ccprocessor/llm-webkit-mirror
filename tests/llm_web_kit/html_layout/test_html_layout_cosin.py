import unittest
from pathlib import Path

from llm_web_kit.html_layout.html_layout_cosin import (cluster_html_struct,
                                                       get_feature, similarity,
                                                       sum_tags)

base_dir = Path(__file__).parent

TEST_FEATURE_HTML = [
    {'input': 'assets/feature.html', 'expected': 2},
    {'input': 'assets/feature3.html', 'expected': None},
    {'input': 'assets/feature4.html', 'expected': 2},
]
TEST_SIMIL_HTMLS = [
    {'input1': 'assets/feature.html', 'input2': 'assets/cosin.html', 'expected': 0.22013982},
    {'input1': 'assets/feature1.html', 'input2': 'assets/feature2.html', 'layer_n': 12, 'expected': 0.9463744},
    {'input1': 'assets/feature1.html', 'input2': 'assets/data_structure.html', 'layer_n': 12, 'expected': 0},
]
TEST_SIMIL_FEATURES = [
    ({}, {}, 0),
    (None, None, 62102000),
    ({'tags': {}}, {}, 0),
    (
        {'tags': {1: ['<body>/div'], 2: ['<div>[2]/div', '<div>[1]/div', '<div>[3]/ul']}},
        {'tags': {'1': ['<body>/div'], '2': ['<div>[2]/div', '<div>[1]/div', '<div>[3]/ul']},
         'attrs': {'1': ['nav', 'content', 'footer'], '2': ['foot', 'container']}},
        1.0,
    )
]
TEST_CLUSTER_HTMLS = [
    {'input': ['assets/feature1.html', 'assets/cosin.html'], 'expected': [-1]},
    {'input': ['assets/feature1.html', 'assets/feature2.html'], 'expected': [-1]},
    {'input': ['assets/100.html', 'assets/101.html', 'assets/102.html', 'assets/103.html', 'assets/104.html',
               'assets/105.html', 'assets/106.html'], 'expected': [0, 1, -1]}

]

TEST_SUM_TAGS = [
    {
        'input': {'tags': {1: ['div', 'div', 'div'], 2: ['div', 'div', 'ul'], 3: ['div', 'ul', 'p', 'li'],
                           4: ['dl', 'a', 'ul', 'p', 'div', 'table', 'div', 'table', 'ul', 'div']}},
        'expected': {'layer_n': {1: 3, 2: 3, 3: 4, 4: 10}, 'total_n': 20}},
    {
        'input': {'tags': {1: ['div'], 2: ['div', 'div', 'footer', 'div', 'header'],
                           3: ['div', 'div', 'div', 'div', 'div', 'div', 'div'],
                           4: ['div', 'div', 'header', 'article', 'aside', 'div', 'a', 'div', 'div']}},
        'expected': {'layer_n': {1: 1, 2: 5, 3: 7, 4: 9}, 'total_n': 22}}
]


class TestHtmllayoutcosin(unittest.TestCase):

    def test_get_feature(self):
        for test_case in TEST_FEATURE_HTML:
            raw_html_path = base_dir.joinpath(test_case['input'])
            raw_html = raw_html_path.read_text(encoding='utf-8')
            features = get_feature(raw_html)
            if features is not None:
                self.assertEqual(len(features), test_case['expected'])

                layer_n, total_n = sum_tags(get_feature(raw_html, is_ignore_tag=False)['tags'])
                ignore_layer_n, ignore_total_n = sum_tags(get_feature(raw_html)['tags'])
                self.assertEqual(len(layer_n) == len(ignore_layer_n), True)
                self.assertEqual(total_n > ignore_total_n, True)
            else:
                self.assertEqual(features, test_case['expected'])

    def test_cluster_html_struct(self):
        for TEST_CLUSTER_HTML in TEST_CLUSTER_HTMLS:
            features = [{'feature': get_feature(base_dir.joinpath(line).read_text(encoding='utf-8'))} for line in
                        TEST_CLUSTER_HTML['input']]
            res, layout_list = cluster_html_struct(features)
            self.assertEqual(TEST_CLUSTER_HTML['expected'], layout_list)

    def test_similarity(self):
        for TEST_SIMIL_HTML in TEST_SIMIL_HTMLS:
            feature1 = get_feature(base_dir.joinpath(TEST_SIMIL_HTML['input1']).read_text(encoding='utf-8'))
            feature2 = get_feature(base_dir.joinpath(TEST_SIMIL_HTML['input2']).read_text(encoding='utf-8'))
            cosin = similarity(feature1, feature2, layer_n=TEST_SIMIL_HTML.get('layer_n', 5))
            self.assertEqual('{:.2f}'.format(TEST_SIMIL_HTML['expected']), '{:.2f}'.format(cosin))
        for TEST_SIMIL_FEATURE in TEST_SIMIL_FEATURES:
            try:
                cosin = similarity(TEST_SIMIL_FEATURE[0], TEST_SIMIL_FEATURE[1])
                self.assertEqual(TEST_SIMIL_FEATURE[2], cosin)
            except Exception as e:
                self.assertEqual(e.error_code, TEST_SIMIL_FEATURE[2])

    def test_sum_tags(self):
        for TEST_SUM_TAG in TEST_SUM_TAGS:
            layer_n, total_n = sum_tags(TEST_SUM_TAG['input']['tags'])
            self.assertEqual(TEST_SUM_TAG['expected']['layer_n'], layer_n)
            self.assertEqual(TEST_SUM_TAG['expected']['total_n'], total_n)
