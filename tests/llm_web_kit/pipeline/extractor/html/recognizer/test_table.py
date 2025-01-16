import json
import unittest
from pathlib import Path

from llm_web_kit.libs.html_utils import html_to_element
from llm_web_kit.pipeline.extractor.html.recognizer.recognizer import CCTag
from llm_web_kit.pipeline.extractor.html.recognizer.table import \
    TableRecognizer

TEST_CASES = [
    {
        'input': (
            'assets/recognizer/table.html',
            'assets/recognizer/table_exclude.html',
            'assets/recognizer/only_table.html',
            'assets/recognizer/table_simple_compex.html',
            'assets/recognizer/table_to_content_list_simple.html',
            'assets/recognizer/table_to_content_list_complex.html',
        ),
        'expected': [
            ('assets/recognizer/table_to_content_list_simple_res.json'),
            ('assets/recognizer/table_to_content_list_complex_res.json')
        ],
    }
]

base_dir = Path(__file__).parent


class TestTableRecognizer(unittest.TestCase):
    def setUp(self):
        self.rec = TableRecognizer()

    def test_involve_cctale(self):
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][0])
            base_url = test_case['input'][1]
            raw_html = raw_html_path.read_text()
            parts = self.rec.recognize(base_url, [(raw_html, raw_html)], raw_html)
            self.assertEqual(len(parts), 4)

    def test_not_involve_table(self):
        """不包含表格."""
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][1])
            base_url = test_case['input'][1]
            raw_html = raw_html_path.read_text()
            parts = self.rec.recognize(base_url, [(raw_html, raw_html)], raw_html)
            self.assertEqual(len(parts), 1)

    def test_only_involve_table(self):
        """只包含表格的Html解析."""
        for test_case in TEST_CASES:

            raw_html_path = base_dir.joinpath(test_case['input'][2])
            base_url = test_case['input'][1]
            raw_html = raw_html_path.read_text()
            parts = self.rec.recognize(base_url, [(raw_html, raw_html)], raw_html)
            self.assertEqual(len(parts), 2)

    def test_simple_complex_table(self):
        """包含简单和复杂table."""
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][3])
            base_url = test_case['input'][1]
            raw_html = raw_html_path.read_text(encoding='utf-8')
            parts = self.rec.recognize(base_url, [(raw_html, raw_html)], raw_html)
            assert len(parts) == 4
            simple_table_tag = html_to_element(parts[1][0]).xpath(f'.//{CCTag.CC_TABLE}')[0]
            simple_table_type = simple_table_tag.attrib
            assert simple_table_type['table_type'] == 'simple'
            complex_table_tag = html_to_element(parts[2][0]).xpath(f'.//{CCTag.CC_TABLE}')[0]
            complex_table_type = complex_table_tag.attrib
            assert complex_table_type['table_type'] == 'complex'

    def test_table_to_content_list_node_simple(self):
        """测试table的 to content list node方法."""
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][4])
            base_url = test_case['input'][1]
            raw_html = raw_html_path.read_text(encoding='utf-8')
            parsed_content = raw_html
            result = self.rec.to_content_list_node(base_url, parsed_content, raw_html)
            expect = base_dir.joinpath(test_case['expected'][0])
            expect_json = expect.read_text(encoding='utf-8')
            assert result == json.loads(expect_json)

    def test_table_to_content_list_node_complex(self):
        """测试table的 complex table to content list node方法."""
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][5])
            base_url = test_case['input'][1]
            raw_html = raw_html_path.read_text(encoding='utf-8')
            parsed_content = raw_html
            result = self.rec.to_content_list_node(base_url, parsed_content, raw_html)
            expect = base_dir.joinpath(test_case['expected'][1])
            expect_json = expect.read_text(encoding='utf-8')
            assert result['type'] == json.loads(expect_json)['type']
            assert result['content']['is_complex'] == json.loads(expect_json)['content']['is_complex']
            assert result['raw_content'] == json.loads(expect_json)['raw_content']
            assert result['content']['html'] == json.loads(expect_json)['content']['html']


if __name__ == '__main__':
    r = TestTableRecognizer()
    r.setUp()
    r.test_table_to_content_list_node_complex()
