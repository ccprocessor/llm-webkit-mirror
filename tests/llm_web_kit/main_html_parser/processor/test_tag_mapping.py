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
    """测试模版正文结构树抽取."""
    def test_construct_main_tree(self):
        data = []
        raw_html_path = base_dir.joinpath('assets/test_tag_mapping_web.jsonl')
        with open(raw_html_path, 'r', encoding='utf-8') as f:
            for line in f:
                data.append(json.loads(line.strip()))  # 解析每行 JSON
        mock_dict = data[0]
        pre_data = PreDataJson(mock_dict['pre_data'])
        # 实际使用原网页html字段作为typical_raw_html
        pre_data[PreDataJsonKey.TYPICAL_RAW_HTML] = pre_data[PreDataJsonKey.TYPICAL_RAW_TAG_HTML]
        parser = MapItemToHtmlTagsParser({})
        pre_data = parser.parse(pre_data)
        content_list = pre_data.get(PreDataJsonKey.HTML_TARGET_LIST, [])
        element_dict = pre_data.get(PreDataJsonKey.HTML_ELEMENT_DICT, [])
        self.assertEqual(content_list, mock_dict['expected_content_list'])
        verify_key = mock_dict['verify_key1']
        verify_key = (verify_key[0], verify_key[1], verify_key[2], verify_key[4], verify_key[5])
        new_res = element_dict[8][verify_key][0]
        self.assertEqual('red', new_res)

        verify_key = mock_dict['verify_key2']
        verify_key = (verify_key[0], verify_key[1], verify_key[2], verify_key[4], verify_key[5])
        new_res = element_dict[7][verify_key][0]
        self.assertEqual('red', new_res)

    def test_construct_main_tree_fail_by_similarity(self):
        """测试由于抽取正文和原网页相似度过高导致构建失败，模拟模型给出的结果中没有正文标签，根据推广算法会保留全网页."""
        data = []
        raw_html_path = base_dir.joinpath('assets/test_tag_mapping_web.jsonl')
        with open(raw_html_path, 'r', encoding='utf-8') as f:
            for line in f:
                data.append(json.loads(line.strip()))  # 解析每行 JSON
        mock_dict = data[0]
        pre_data = PreDataJson(mock_dict['pre_data'])
        pre_data[PreDataJsonKey.TYPICAL_RAW_HTML] = pre_data[PreDataJsonKey.TYPICAL_RAW_TAG_HTML]
        # 用bad模型结果替换
        pre_data[PreDataJsonKey.LLM_RESPONSE] = pre_data['llm_response_bad']
        parser = MapItemToHtmlTagsParser({})
        pre_data = parser.parse(pre_data)
        construct_success = pre_data.get(PreDataJsonKey.TYPICAL_MAIN_HTML_SUCCESS)
        self.assertEqual(False, construct_success)

    def test_parse_single(self):
        data = []
        raw_html_path = base_dir.joinpath('assets/test_tag_mapping_web.jsonl')
        with open(raw_html_path, 'r', encoding='utf-8') as f:
            for line in f:
                data.append(json.loads(line.strip()))  # 解析每行 JSON
        mock_dict = data[0]
        pre_data = PreDataJson(mock_dict['pre_data'])
        pre_data[PreDataJsonKey.TYPICAL_RAW_HTML] = pre_data[PreDataJsonKey.TYPICAL_RAW_TAG_HTML]
        parser = MapItemToHtmlTagsParser({})
        pre_data = parser.parse_single(pre_data)
        content_list = pre_data[PreDataJsonKey.HTML_TARGET_LIST]
        self.assertEqual(content_list, mock_dict['expected_content_list'])
        self.assertEqual(len(pre_data['typical_main_html']), 2269)
