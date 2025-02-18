import json
import os
import sys
import unittest
from unittest.mock import mock_open, patch

current_file_path = os.path.abspath(__file__)
parent_dir_path = os.path.join(current_file_path, *[os.pardir] * 5)
normalized_path = os.path.normpath(parent_dir_path)
sys.path.append(normalized_path)

from llm_web_kit.model.basic_functions.character import (  # noqa: E402
    RES_MAP, get_all_punc_list, get_common_punc_end_list, get_common_punc_list,
    get_punc_set, has_chinese_char)


class TestCharacter(unittest.TestCase):
    def setUp(self):
        RES_MAP.clear()
        self.sample_data = [
            '{"punc": ".", "en_cc_top_30": true, "zh_cc_top_30": false, "en_cc_end_top_30": true, "zh_cc_end_top_30": false}',
            '{"punc": "，", "en_cc_top_30": false, "zh_cc_top_30": true, "en_cc_end_top_30": false, "zh_cc_end_top_30": true}'
        ]
        self.sample_file_content = '\n'.join(self.sample_data)

    @patch('builtins.open', new_callable=mock_open, read_data='')
    def test_get_all_punc_list_empty(self, mock_file):
        result = get_all_punc_list()
        self.assertEqual(result, [])

    @patch('builtins.open', new_callable=mock_open, read_data='invalid_json')
    def test_get_all_punc_list_invalid_json(self, mock_file):
        with self.assertRaises(json.JSONDecodeError):
            get_all_punc_list()

    def test_get_all_punc_list(self):
        with patch('builtins.open', mock_open(read_data=self.sample_file_content)) as mock_file:  # noqa: F841
            result = get_all_punc_list()
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]['punc'], '.')
            self.assertEqual(result[1]['punc'], '，')

    def test_get_punc_set(self):
        with patch('llm_web_kit.model.basic_functions.character.get_all_punc_list', return_value=[json.loads(line.strip()) for line in self.sample_data]):
            result = get_punc_set(include_keys=['en_cc_top_30'])
            self.assertTrue('.' in result)
            self.assertFalse('，' in result)

            result = get_punc_set(exclude_keys=['zh_cc_top_30'])
            self.assertTrue('.' in result)
            self.assertFalse('，' in result)

    def test_get_common_punc_list(self):
        with patch('llm_web_kit.model.basic_functions.character.get_punc_set') as mocked_get_punc_set:
            mocked_get_punc_set.side_effect = [
                {'.', '!'},  # English common punctuation
                {'，', '！'}  # Chinese common punctuation
            ]
            result = get_common_punc_list()
            self.assertEqual(set(result), {'.', '!', '，', '！'})

    def test_get_common_punc_end_list(self):
        with patch('llm_web_kit.model.basic_functions.character.get_punc_set') as mocked_get_punc_set:
            mocked_get_punc_set.side_effect = [
                {'.', '!'},  # English common end punctuation
                {'。', '！'}  # Chinese common end punctuation
            ]
            result = get_common_punc_end_list()
            self.assertEqual(set(result), {'.', '!', '。', '！'})

    def test_has_chinese_char(self):
        self.assertTrue(has_chinese_char('测试'))
        self.assertFalse(has_chinese_char('test'))


if __name__ == '__main__':
    unittest.main()
