import json
import unittest
from pathlib import Path

from llm_web_kit.input.pre_data_json import PreDataJson, PreDataJsonKey
from llm_web_kit.main_html_parser.parser.tag_mapping import \
    MapItemToHtmlTagsParser

base_dir = Path(__file__).parent.parent


def parse_tuple_key(key_str):
    if key_str.startswith('(') and key_str.endswith(')'):
        try:
            # Convert "(1, 2)" → (1, 2) using ast.literal_eval (safer than eval)
            return eval(key_str)
        except Exception:
            return key_str
    return key_str


class TestTagMapping(unittest.TestCase):
    def test_construct_main_tree(self):
        data = []
        raw_html_path = base_dir.joinpath('assets/test_tag_mapping_web.jsonl')
        with open(raw_html_path, 'r', encoding='utf-8') as f:
            for line in f:
                data.append(json.loads(line.strip()))  # 解析每行 JSON
        mock_dict = data[0]
        pre_data = PreDataJson(mock_dict['pre_data'])
        parser = MapItemToHtmlTagsParser({})
        pre_data = parser.parse(pre_data)
        content_list = pre_data.get(PreDataJsonKey.HTML_TARGET_LIST, [])
        element_dict = pre_data.get(PreDataJsonKey.HTML_ELEMENT_LIST, [])
        self.assertEqual(content_list, mock_dict['expected_content_list'])
        verify_key = mock_dict['verify_key']
        new_res = element_dict[8][tuple(verify_key)][0]
        self.assertEqual('red', new_res)
