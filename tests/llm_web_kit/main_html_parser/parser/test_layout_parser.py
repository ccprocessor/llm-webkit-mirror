import json
import re
import unittest
from pathlib import Path

from llm_web_kit.input.pre_data_json import PreDataJson, PreDataJsonKey
from llm_web_kit.main_html_parser.parser.layout_batch_parser import \
    LayoutBatchParser

TEST_CASES = [
    {
        'input': (
            ['assets/input_layout_batch_parser/www.wdi.it.html',
             'assets/input_layout_batch_parser/template_www.wdi.it.json', 'https://www.wdi.it/'],
            ['assets/input_layout_batch_parser/answers.acrobatusers.html',
             'assets/input_layout_batch_parser/template_answers.acrobatusers.json',
             'https://answers.acrobatusers.com/change-default-open-size-Acrobat-Pro-XI-q302177.aspx'],
        ),
        'expected': [
            'assets/output_layout_batch_parser/wdi_main_html.html',
            'assets/output_layout_batch_parser/answers_acrobatusers_main_html.html'
        ],
    }
]

base_dir = Path(__file__).parent


def parse_tuple_key(key_str):
    if key_str.startswith('(') and key_str.endswith(')'):
        try:
            # Convert "(1, 2)" → (1, 2) using ast.literal_eval (safer than eval)
            return eval(key_str)  # WARNING: eval is unsafe for untrusted data!
        except (SyntaxError, ValueError):
            return key_str  # Fallback if parsing fails
    return key_str


class TestLayoutParser(unittest.TestCase):
    def test_layout_batch_parser(self):
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][0][0])
            element_path = base_dir.joinpath(test_case['input'][0][1])
            raw_html = raw_html_path.read_text(encoding='utf-8')
            # element_json = json.loads(element_path.read_text())
            element_dict_str = json.loads(element_path.read_text(encoding='utf-8'))
            element_dict = {}
            for layer, layer_dict in element_dict_str.items():
                layer_dict_json = {parse_tuple_key(k): v for k, v in layer_dict.items()}
                element_dict[int(layer)] = layer_dict_json
            data_dict = {'html_source': raw_html, 'html_element_dict': element_dict, 'ori_html': raw_html,
                         'typical_main_html': raw_html, 'similarity_layer': 5}
            expected_html = base_dir.joinpath(test_case['expected'][0]).read_text(encoding='utf-8')
            pre_data = PreDataJson(data_dict)
            parser = LayoutBatchParser(element_dict)
            parts = parser.parse(pre_data)
            assert parts.get(PreDataJsonKey.MAIN_HTML_BODY) == expected_html

    def test_layout_batch_parser_answers(self):
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][1][0])
            element_path = base_dir.joinpath(test_case['input'][1][1])
            raw_html = raw_html_path.read_text(encoding='utf-8')
            # element_json = json.loads(element_path.read_text())
            element_dict_str = json.loads(element_path.read_text(encoding='utf-8'))
            element_dict = {}
            for layer, layer_dict in element_dict_str.items():
                layer_dict_json = {parse_tuple_key(k): v for k, v in layer_dict.items()}
                element_dict[int(layer)] = layer_dict_json
            data_dict = {'html_source': raw_html, 'html_element_dict': element_dict, 'ori_html': raw_html,
                         'typical_main_html': raw_html, 'similarity_layer': 5}
            expected_html = base_dir.joinpath(test_case['expected'][1]).read_text(encoding='utf-8')
            pre_data = PreDataJson(data_dict)
            parser = LayoutBatchParser(element_dict)
            parts = parser.parse(pre_data)
            cleaned_expected = re.sub(r'\s+', ' ', expected_html)
            cleaned_actual = re.sub(r'\s+', ' ', parts.get(PreDataJsonKey.MAIN_HTML_BODY))
            assert cleaned_actual == cleaned_expected

    def test_layout_batch_parser_24ssports(self):
        raw_html_path = base_dir.joinpath('assets/input_layout_batch_parser/24ssports.com.html')
        element_path = base_dir.joinpath('assets/input_layout_batch_parser/template_24ssports.com.json')
        expected_html = base_dir.joinpath('assets/output_layout_batch_parser/24ssports.com_main_html.html').read_text()
        raw_html = raw_html_path.read_text()
        # element_json = json.loads(element_path.read_text())
        element_dict_str = json.loads(element_path.read_text(encoding='utf-8'))
        element_dict = {}
        for layer, layer_dict in element_dict_str.items():
            layer_dict_json = {parse_tuple_key(k): v for k, v in layer_dict.items()}
            element_dict[int(layer)] = layer_dict_json
        data_dict = {'html_source': raw_html, 'html_element_dict': element_dict, 'ori_html': raw_html,
                     'typical_main_html': raw_html, 'similarity_layer': 5}
        pre_data = PreDataJson(data_dict)
        parser = LayoutBatchParser(element_dict)
        parts = parser.parse(pre_data)
        assert parts.get(PreDataJsonKey.MAIN_HTML_BODY) == expected_html

    def test_layout_batch_parser_sv_m_wiktionary_org(self):
        raw_html_path = base_dir.joinpath('assets/input_layout_batch_parser/sv.m.wiktionary.org.html')
        element_path = base_dir.joinpath('assets/input_layout_batch_parser/template_sv.m.wiktionary.org_0.json')
        expected_html = base_dir.joinpath(
            'assets/output_layout_batch_parser/parser_sv_m_wiktionary_org.html').read_text(encoding='utf-8')
        raw_html = raw_html_path.read_text(encoding='utf-8')
        element_dict = element_path.read_text(encoding='utf-8')
        data_dict = {'html_source': raw_html, 'html_element_dict': element_dict, 'ori_html': raw_html,
                     'typical_main_html': raw_html, 'similarity_layer': 5}
        pre_data = PreDataJson(data_dict)
        parser = LayoutBatchParser(element_dict)
        parts = parser.parse(pre_data)
        print(parts.get(PreDataJsonKey.MAIN_HTML_BODY))
        assert parts.get(PreDataJsonKey.MAIN_HTML_BODY) == expected_html

    def test_layout_barch_parser_similarity(self):
        """测试相似度计算逻辑，提供两个html案例，一个与模版相似度差异较小，一个与模版相似度差异较大，分别通过与不通过阈值检验."""
        success_html = base_dir.joinpath('assets/input_layout_batch_parser/test_similarity_success.html').read_text(
            encoding='utf-8')
        fail_html = base_dir.joinpath('assets/input_layout_batch_parser/test_similarity_fail.html').read_text(
            encoding='utf-8')
        template_html = base_dir.joinpath('assets/input_layout_batch_parser/test_similarity_template.html').read_text(
            encoding='utf-8')
        element_dict = base_dir.joinpath(
            'assets/input_layout_batch_parser/test_similarity_element_dict.json').read_text(encoding='utf-8')

        data_dict = {'html_source': success_html, 'html_element_dict': element_dict,
                     'typical_main_html': template_html}
        pre_data = PreDataJson(data_dict)
        parser = LayoutBatchParser(element_dict)
        parts = parser.parse(pre_data)
        assert parts.get(PreDataJsonKey.MAIN_HTML_SUCCESS) is True

        data_dict = {'html_source': fail_html, 'html_element_dict': element_dict,
                     'typical_main_html': template_html}
        pre_data = PreDataJson(data_dict)
        parts = parser.parse(pre_data)
        assert parts.get(PreDataJsonKey.MAIN_HTML_SUCCESS) is False
