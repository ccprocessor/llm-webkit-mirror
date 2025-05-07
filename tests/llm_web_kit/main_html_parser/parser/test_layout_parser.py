import json
import unittest
from pathlib import Path

from llm_web_kit.input.pre_data_json import PreDataJson, PreDataJsonKey
from llm_web_kit.main_html_parser.parser.layout_batch_parser import \
    LayoutBatchParser

TEST_CASES = [
    {
        'input': (
            ['assets/input_layout_batch_parser/www.wdi.it.html', 'assets/input_layout_batch_parser/template_www.wdi.it.json', 'https://www.wdi.it/'],
            ['assets/input_layout_batch_parser/answers.acrobatusers.html', 'assets/input_layout_batch_parser/template_answers.acrobatusers.json', 'https://answers.acrobatusers.com/change-default-open-size-Acrobat-Pro-XI-q302177.aspx'],
        ),
         'expected': [
            'assets/output_layout_batch_parser/wdi_main_html.html',
            'assets/output_layout_batch_parser/answers_acrobatusers_main_html.html'
        ],
    }
]

base_dir = Path(__file__).parent


class TestLayoutParser(unittest.TestCase):
    def test_layout_batch_parser(self):
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][0][0])
            element_path = base_dir.joinpath(test_case['input'][0][1])
            raw_html = raw_html_path.read_text()
            element_json = json.loads(element_path.read_text())
            data_dict = {'HTML': raw_html, 'TEMPLATE_DATA': element_json, 'ORI_HTML': raw_html}
            expected_html = base_dir.joinpath(test_case['expected'][0]).read_text()
            pre_data = PreDataJson(data_dict)
            parser = LayoutBatchParser(element_json)
            parts = parser.parse(pre_data)
            assert parts.get(PreDataJsonKey.MAIN_HTML_BODY) == expected_html

    def test_layout_batch_parser_answers(self):
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][1][0])
            element_path = base_dir.joinpath(test_case['input'][1][1])
            raw_html = raw_html_path.read_text()
            element_json = json.loads(element_path.read_text())
            data_dict = {'HTML': raw_html, 'TEMPLATE_DATA': element_json, 'ORI_HTML': raw_html}
            expected_html = base_dir.joinpath(test_case['expected'][1]).read_text()
            pre_data = PreDataJson(data_dict)
            parser = LayoutBatchParser(element_json)
            parts = parser.parse(pre_data)
            assert parts.get(PreDataJsonKey.MAIN_HTML_BODY) == expected_html
