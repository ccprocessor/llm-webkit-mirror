import unittest
from pathlib import Path

from llm_web_kit.html_layout.html_layout_cosin import (cluster_html_struct,
                                                       get_feature, similarity)

base_dir = Path(__file__).parent

TEST_FEATURE_HTML = [{'input': 'assets/feature.html', 'expected': 2}]
TEST_SIMIL_HTMLS = [
    {'input1': 'assets/feature.html', 'input2': 'assets/cosin.html', 'expected': 0.1748186},
    {'input1': 'assets/feature1.html', 'input2': 'assets/feature2.html', 'layer_n': 12, 'expected': 0.925361},
]
TEST_CLUSTER_HTMLS = [
    {'input1': 'assets/feature1.html', 'input2': 'assets/cosin.html', 'expected': [0]},
    {'input1': 'assets/feature1.html', 'input2': 'assets/feature2.html', 'expected': [-1]}
]


class TestHtmllayoutcosin(unittest.TestCase):

    def test_get_feature(self):
        for test_case in TEST_FEATURE_HTML:
            raw_html_path = base_dir.joinpath(test_case['input'])
            raw_html = raw_html_path.read_text(encoding='utf-8')
            features = get_feature(raw_html)
            self.assertEqual(len(features), test_case['expected'])

    def test_cluster_html_struct(self):
        for TEST_CLUSTER_HTML in TEST_CLUSTER_HTMLS:
            feature1 = get_feature(base_dir.joinpath(TEST_CLUSTER_HTML['input1']).read_text(encoding='utf-8'))
            feature2 = get_feature(base_dir.joinpath(TEST_CLUSTER_HTML['input2']).read_text(encoding='utf-8'))
            res, layout_list = cluster_html_struct([{'feature': feature1}, {'feature': feature2}])
            self.assertEqual(TEST_CLUSTER_HTML['expected'], layout_list)

    def test_similarity(self):
        for TEST_SIMIL_HTML in TEST_SIMIL_HTMLS:
            feature1 = get_feature(base_dir.joinpath(TEST_SIMIL_HTML['input1']).read_text(encoding='utf-8'))
            feature2 = get_feature(base_dir.joinpath(TEST_SIMIL_HTML['input2']).read_text(encoding='utf-8'))
            cosin = similarity(feature1, feature2, layer_n=TEST_SIMIL_HTML.get('layer_n', 5))
            self.assertEqual(TEST_SIMIL_HTML['expected'], cosin)
