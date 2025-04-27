import unittest
from pathlib import Path

from llm_web_kit.input.pre_data_json import PreDataJson, PreDataJsonKey
from llm_web_kit.main_html_parser.parser.typical_html_selector import \
    TypicalHtmlSelectorParser

base_dir = Path(__file__).resolve().parent


class MyTestCase(unittest.TestCase):
    def test_typical_html_selector(self):
        file_dir = base_dir / 'assets/test_html_data/test_typical_html_data'
        html_files = [f'{file_dir}/{i}.html' for i in range(10)]
        html_content = []
        for file_path in html_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content.append({
                    'track_id': Path(file_path).name,
                    'html': f.read()
                })
        data_dict = {PreDataJsonKey.LAYOUT_FILE_LIST: html_content}
        pre_data = PreDataJson(data_dict)
        pre_data_result = TypicalHtmlSelectorParser({}).parse(pre_data)
        typical_html = pre_data_result.get(PreDataJsonKey.TYPICAL_RAW_HTML, '')
        self.assertEqual(typical_html['track_id'], '9.html')


if __name__ == '__main__':
    unittest.main()
