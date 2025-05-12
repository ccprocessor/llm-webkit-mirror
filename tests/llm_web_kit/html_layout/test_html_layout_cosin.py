import unittest
from pathlib import Path

from llm_web_kit.html_layout.html_layout_cosin import (cluster_html_struct,
                                                       get_feature, similarity)

base_dir = Path(__file__).parent

TEST_FEATURE_HTML = [{'input': 'assets/feature.html', 'expected': 2}]
TEST_SIMIL_HTMLS = [
    {'input1': 'assets/feature.html', 'input2': 'assets/cosin.html', 'expected': 0.22013982},
    {'input1': 'assets/feature1.html', 'input2': 'assets/feature2.html', 'layer_n': 12, 'expected': 0.9357468},

]
TEST_CLUSTER_HTMLS = [
    {'input': ['assets/feature1.html', 'assets/cosin.html'], 'expected': [-1]},
    {'input': ['assets/feature1.html', 'assets/feature2.html'], 'expected': [-1]},
    {'input': ['assets/100.html', 'assets/101.html', 'assets/102.html', 'assets/103.html', 'assets/104.html',
               'assets/105.html', 'assets/106.html'], 'expected': [0, 1, -1]}

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
