import unittest
from pathlib import Path

from llm_web_kit.input.pre_data_json import PreDataJson, PreDataJsonKey
from llm_web_kit.main_html_parser.parser.tag_simplifier import \
    HtmlTagSimplifierParser

base_dir = Path(__file__).resolve().parent


class MyTestCase(unittest.TestCase):
    def test_tag_simplifier(self):
        file_path = base_dir / 'assets/test_html_data/test_tah_simplifier.html'
        with open(file_path, 'r', encoding='utf-8') as file:
            raw_html = file.read()
        data_dict = {PreDataJsonKey.TYPICAL_RAW_HTML: raw_html}
        pre_data = PreDataJson(data_dict)
        pre_data_result = HtmlTagSimplifierParser({}).parse(pre_data)
        simplifier_raw_html = pre_data_result.get(PreDataJsonKey.TYPICAL_SIMPLIFIED_HTML, '')
        _item_id_count = simplifier_raw_html.count('_item_id')
        self.assertEqual(_item_id_count, 32)

    def test_tag_simplifier1(self):
        file_path = base_dir / 'assets/test_html_data/normal_dl.html'
        with open(file_path, 'r', encoding='utf-8') as file:
            raw_html = file.read()
        data_dict = {PreDataJsonKey.TYPICAL_RAW_HTML: raw_html}
        pre_data = PreDataJson(data_dict)
        pre_data_result = HtmlTagSimplifierParser({}).parse(pre_data)
        simplifier_raw_html = pre_data_result.get(PreDataJsonKey.TYPICAL_SIMPLIFIED_HTML, '')
        _item_id_count = simplifier_raw_html.count('_item_id')
        self.assertEqual(_item_id_count, 18)

    def test_tag_simplifier2(self):
        file_path = base_dir / 'assets/test_html_data/normal_table.html'
        with open(file_path, 'r', encoding='utf-8') as file:
            raw_html = file.read()
        data_dict = {PreDataJsonKey.TYPICAL_RAW_HTML: raw_html}
        pre_data = PreDataJson(data_dict)
        pre_data_result = HtmlTagSimplifierParser({}).parse(pre_data)
        simplifier_raw_html = pre_data_result.get(PreDataJsonKey.TYPICAL_SIMPLIFIED_HTML, '')
        _item_id_count = simplifier_raw_html.count('_item_id')
        self.assertEqual(_item_id_count, 30)

    def test_tag_simplifier3(self):
        file_path = base_dir / 'assets/test_html_data/special_table_1.html'
        with open(file_path, 'r', encoding='utf-8') as file:
            raw_html = file.read()
        data_dict = {PreDataJsonKey.TYPICAL_RAW_HTML: raw_html}
        pre_data = PreDataJson(data_dict)
        pre_data_result = HtmlTagSimplifierParser({}).parse(pre_data)
        simplifier_raw_html = pre_data_result.get(PreDataJsonKey.TYPICAL_SIMPLIFIED_HTML, '')
        _item_id_count = simplifier_raw_html.count('_item_id')
        self.assertEqual(_item_id_count, 66)

    def test_tag_simplifier4(self):
        file_path = base_dir / 'assets/test_html_data/1.html'
        with open(file_path, 'r', encoding='utf-8') as file:
            raw_html = file.read()
        data_dict = {PreDataJsonKey.TYPICAL_RAW_HTML: raw_html}
        pre_data = PreDataJson(data_dict)
        pre_data_result = HtmlTagSimplifierParser({}).parse(pre_data)
        simplifier_raw_html = pre_data_result.get(PreDataJsonKey.TYPICAL_SIMPLIFIED_HTML, '')
        _item_id_count = simplifier_raw_html.count('_item_id')
        self.assertEqual(_item_id_count, 51)


if __name__ == '__main__':
    unittest.main()
