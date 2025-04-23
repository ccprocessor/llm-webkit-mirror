import json
import os
import unittest
from llm_web_kit.main_html_parser.parser.tag_mapping import MapItemToHtmlTagsParser
from llm_web_kit.input.pre_data_json import PreDataJson
from llm_web_kit.input.pre_data_json import PreDataJson, PreDataJsonKey
from llm_web_kit.input.pre_data_json import PreDataJson, PreDataJsonKey


class TestTagMapping(unittest.TestCase):
    def test_construct_main_tree(self):
        data = []
        with open('../assets/test_tag_mapping_web.jsonl', 'r', encoding='utf-8') as f:
            for line in f:
                data.append(json.loads(line.strip()))  # 解析每行 JSON
        mock_dict = data[0]
        pre_data = PreDataJson(mock_dict["pre_data"])
        parser = MapItemToHtmlTagsParser({})
        pre_data = parser.parse(pre_data)
        content_list = pre_data.get(PreDataJsonKey.HTML_TARGET_LIST, [])
        element_dict = pre_data.get(PreDataJsonKey.HTML_ELEMENT_LIST, [])
        self.assertEqual(content_list, mock_dict['expected_content_list'])
        expected_element_dict = mock_dict['expected_element_dict']
        self.assertEqual(str(element_dict), expected_element_dict)
