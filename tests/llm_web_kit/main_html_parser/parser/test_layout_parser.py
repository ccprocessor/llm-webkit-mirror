import json
import re
import unittest
from pathlib import Path

from llm_web_kit.input.pre_data_json import PreDataJson, PreDataJsonKey
from llm_web_kit.main_html_parser.parser.layout_batch_parser import \
    LayoutBatchParser
from llm_web_kit.main_html_parser.parser.tag_mapping import \
    MapItemToHtmlTagsParser
from llm_web_kit.main_html_parser.simplify_html.simplify_html import \
    simplify_html

TEST_CASES = [
    {
        'input': (
            ['assets/input_layout_batch_parser/www.wdi.it.html',
             'assets/input_layout_batch_parser/template_www.wdi.it.json', 'https://www.wdi.it/'],
            ['assets/input_layout_batch_parser/answers.acrobatusers.html',
             'assets/input_layout_batch_parser/template_answers.acrobatusers.json',
             'https://answers.acrobatusers.com/change-default-open-size-Acrobat-Pro-XI-q302177.aspx'],
            ['assets/input_layout_batch_parser/template_www.wdi.it_llm.json']
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
                         'typical_main_html': raw_html, 'similarity_layer': 5, 'typical_dict_html': raw_html}
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
                         'typical_main_html': raw_html, 'similarity_layer': 5, 'typical_dict_html': raw_html}
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
                     'typical_main_html': raw_html, 'similarity_layer': 5, 'typical_dict_html': raw_html}
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
                     'typical_main_html': raw_html, 'similarity_layer': 5, 'typical_dict_html': raw_html}
        pre_data = PreDataJson(data_dict)
        parser = LayoutBatchParser(element_dict)
        parts = parser.parse(pre_data)
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
                     'typical_main_html': template_html, 'typical_dict_html': template_html}
        pre_data = PreDataJson(data_dict)
        parser = LayoutBatchParser(element_dict)
        parts = parser.parse(pre_data)
        assert parts.get(PreDataJsonKey.MAIN_HTML_SUCCESS) is True

        data_dict = {'html_source': fail_html, 'html_element_dict': element_dict,
                     'typical_main_html': template_html, 'typical_dict_html': template_html}
        pre_data = PreDataJson(data_dict)
        parts = parser.parse(pre_data)
        assert parts.get(PreDataJsonKey.MAIN_HTML_SUCCESS) is False

    def test_dynamic_id(self):
        """测试推广方法的动态id识别功能."""
        # 构造测试html
        html_source = base_dir.joinpath('assets/input_layout_batch_parser/www.wdi.it.html').read_text(
            encoding='utf-8')
        template_source = re.sub(
            'clearfix post post-37041 type-post status-publish format-standard hentry category-economia ' +
            'category-societa tag-camera tag-commercio tag-cosenza tag-diritto tag-economia-2 tag-imprese tag-libro ' +
            'tag-usi item-wrap',
            'post-id', html_source)
        template_source = re.sub('post-37041', 'test-37041', template_source)
        expand_source = re.sub('test-37041', 'test-25031', template_source)
        # 简化网页
        simplified_html, typical_raw_tag_html, _ = simplify_html(template_source)
        # 模型结果格式改写
        llm_path = base_dir.joinpath(TEST_CASES[0]['input'][2][0])
        llm_response = json.loads(llm_path.read_text(encoding='utf-8'))
        for key in llm_response.keys():
            llm_response[key] = 1 if llm_response[key] == 'Yes' else 0
        pre_data = {'typical_raw_tag_html': typical_raw_tag_html, 'typical_raw_html': template_source,
                    'llm_response': llm_response}
        pre_data = PreDataJson(pre_data)
        # 映射
        parser = MapItemToHtmlTagsParser({})
        pre_data = parser.parse(pre_data)
        element_dict = pre_data.get(PreDataJsonKey.HTML_ELEMENT_DICT, {})
        # 推广
        pre_data[PreDataJsonKey.HTML_SOURCE] = expand_source
        pre_data[PreDataJsonKey.DYNAMIC_ID_ENABLE] = True
        parser = LayoutBatchParser(element_dict)
        parts = parser.parse(pre_data)
        main_html_body = parts[PreDataJsonKey.MAIN_HTML_BODY]
        assert 'Permalink link a questo articolo' not in main_html_body and 'Con la stesura di un' in main_html_body
