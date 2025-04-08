import unittest
from pathlib import Path

from llm_web_kit.html_layout.html_layout_cosin import (cluster_html_struct,
                                                       cosin_similarity,
                                                       get_feature)

base_dir = Path(__file__).parent

TEST_FEATURE_HTML = [{'input': 'assets/feature.html', 'expected': 2}]
TEST_SIMIL_HTML = {'input1': 'assets/feature.html', 'input2': 'assets/cosin.html', 'expected': 1.0}
TEST_CLUSTER_HTML = {'input1': 'assets/feature.html', 'input2': 'assets/cosin.html',
                     'current_host_name': 'M211bmlvbi5uZXQ=', 'expected': [0]}


class TestHtmllayoutcosin(unittest.TestCase):

    def test_get_feature(self):
        for test_case in TEST_FEATURE_HTML:
            raw_html_path = base_dir.joinpath(test_case['input'])
            raw_html = raw_html_path.read_text(encoding='utf-8')
            features = get_feature(raw_html)
            self.assertEqual(len(features), test_case['expected'])

    def test_cosin_similarity(self):
        feature1 = get_feature(base_dir.joinpath(TEST_SIMIL_HTML['input1']).read_text(encoding='utf-8'))
        feature2 = get_feature(base_dir.joinpath(TEST_SIMIL_HTML['input1']).read_text(encoding='utf-8'))
        cosin = round(cosin_similarity(feature1, feature2), 4)
        self.assertEqual(TEST_SIMIL_HTML['expected'], cosin)

    def test_cluster_html_struct(self):
        feature1 = get_feature(base_dir.joinpath(TEST_CLUSTER_HTML['input1']).read_text(encoding='utf-8'))
        feature2 = get_feature(base_dir.joinpath(TEST_CLUSTER_HTML['input1']).read_text(encoding='utf-8'))
        res, layout_list = cluster_html_struct([{'feature': feature1}, {'feature': feature2}],
                                               TEST_CLUSTER_HTML['current_host_name'])
        self.assertEqual(TEST_CLUSTER_HTML['expected'], layout_list)
