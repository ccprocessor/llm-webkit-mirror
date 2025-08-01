# Copyright (c) Opendatalab. All rights reserved.
"""Common basic operation unit test."""
import json
import unittest
from unittest.mock import MagicMock, patch

from llm_web_kit.libs.standard_utils import (compress_and_decompress_str,
                                             json_dumps, json_loads)

TEST_COMPRESS_CASES = [
    {'input': '测试数据', 'com_expected': b'x\x9c{\xb6\xb5\xfb\xc5\xfa\xa9\xcf\xa6nx\xd6\xbb\x0e\x009C\x08\x9f',
     'base_expected': 'eJx7trX7xfqpz6ZueNa7DgA5Qwif'},
    {'input': 'Оренбург, штакетник П-образный узкий, цена',
     'com_expected': b'x\x9c\x1d\x8c\xdb\t\x800\x10\x04[\xb9\x02\xb4\xc7`@\x04{\xd0\x16"\x12b\x02g\rs\x1d\xb9\xf8\xb5\xc3\xbe8"Qq\xae\xc8\xa2{\xb2\xd8b\xa10\xa8R\xe7a\x18\xe7\xcc\xabF\x92\xdf\xf0\xd8\xe9\x16Y8\x14wM\xd6\xff\xa2|\xfer4T',
     'base_expected': 'eJwdjNsJgDAQBFu5ArTHYEAEe9AWIhJiAmcNcx25+LXDvjgiUXGuyKJ7sthioTCoUudhGOfMq0aS3/DY6RZZOBR3Tdb/onz+cjRU'},
    {'input': b'x\x9c{\xb6\xb5\xfb\xc5\xfa\xa9\xcf\xa6nx\xd6\xbb\x0e\x009C\x08\x9f',
     'com_expected': b'x\x9c\xab\x98S\xbdm\xeb\xef\xa3\xbfV\x9e_\x96Wqm7\x1f\x83\xa53\xc7|\x00\x91b\x0b{',
     'base_expected': 'eJyrmFO9bevvo79Wnl+WV3FtNx+DpTPHfACRYgt7'},
    {'input': 12345, 'expected': 10000000},
]
TEST_DISCOMPRESS_CASES = [
    {'input': b'x\x9c{\xb6\xb5\xfb\xc5\xfa\xa9\xcf\xa6nx\xd6\xbb\x0e\x009C\x08\x9f', 'expected': '测试数据'},
    {'input': 'eJx7trX7xfqpz6ZueNa7DgA5Qwif', 'expected': '测试数据'},
    {'input': bytearray(b'x\x9c{\xb6\xb5\xfb\xc5\xfa\xa9\xcf\xa6nx\xd6\xbb\x0e\x009C\x08\x9f'), 'expected': '测试数据'},
    {'input': b'x\x9c{\xb6\xb5\xfb\xc5\xfa\xa9\xcf\xa6nx\xd6\xbb\x0e', 'expected': 10000000},
    {'input': 98877, 'expected': 10000000},
]


class TestStandardUtils(unittest.TestCase):

    def test_compress_and_decompress_str(self):
        for compress_case in TEST_COMPRESS_CASES:
            try:
                com_res = compress_and_decompress_str(compress_case['input'])
                base_res = compress_and_decompress_str(compress_case['input'], base=True)
                self.assertEqual(com_res, compress_case['com_expected'])
                self.assertEqual(base_res, compress_case['base_expected'])
            except Exception as e:
                self.assertEqual(e.error_code, compress_case['expected'])
        for discompress_case in TEST_DISCOMPRESS_CASES:
            try:
                res = compress_and_decompress_str(discompress_case['input'], compress=False)
                self.assertEqual(res, discompress_case['expected'])
            except Exception as e:
                self.assertEqual(e.error_code, discompress_case['expected'])

    @patch('llm_web_kit.libs.standard_utils.orjson.loads', return_value={'key': 'value'})
    def test_orjson_success(self, mock_orjson):
        result = json_loads('{"key": "value"}')
        self.assertEqual(result, {'key': 'value'})
        mock_orjson.assert_called_once_with('{"key": "value"}')

    @patch('llm_web_kit.libs.standard_utils.json.loads', return_value={'key': 'value'})
    def test_json_loads_with_kwargs(self, mock_json):
        result = json_loads('{"key": "value"}', encoding='utf-8')
        self.assertEqual(result, {'key': 'value'})
        mock_json.assert_called_once_with('{"key": "value"}', encoding='utf-8')

    @patch('llm_web_kit.libs.standard_utils.orjson.loads', side_effect=AttributeError('AttributeError'))
    @patch('llm_web_kit.libs.standard_utils.json.loads', return_value={'key': 'value'})
    def test_orjson_attribute_error_fallback_to_json(self, mock_json, mock_orjson):
        result = json_loads('{"key": "value"}')
        self.assertEqual(result, {'key': 'value'})
        mock_json.assert_called_once_with('{"key": "value"}')

    @patch('llm_web_kit.libs.standard_utils.json.loads', side_effect=Exception('Unknown error'))
    def test_json_loads_unknown_error(self, mock_json):
        with self.assertRaises(Exception) as context:
            json_loads('invalid json')
        self.assertIn('Unknown error', str(context.exception))
        mock_json.assert_called_once_with('invalid json')

    @patch('llm_web_kit.libs.standard_utils.json.loads',
           side_effect=ValueError('Expecting value: line 1 column 1 (char 0): enclosed in double quotes'))
    @patch('llm_web_kit.libs.standard_utils.ast.literal_eval', return_value={'key': 'value'})
    def test_json_loads_literal_eval_success(self, mock_literal_eval, mock_json):
        result = json_loads("{'key': 'value'}")
        self.assertEqual(result, {'key': 'value'})
        mock_literal_eval.assert_called_once_with("{'key': 'value'}")

    @patch('llm_web_kit.libs.standard_utils.orjson.loads', return_value={'key': 'value'})
    def test_bytes_input_orjson_success(self, mock_orjson):
        result = json_loads(b'{"key": "value"}')
        self.assertEqual(result, {'key': 'value'})
        mock_orjson.assert_called_once_with(b'{"key": "value"}')

    @patch('llm_web_kit.libs.standard_utils.json.loads',
           side_effect=ValueError('Expecting value: line 1 column 1 (char 0): enclosed in double quotes'))
    @patch('llm_web_kit.libs.standard_utils.ast.literal_eval', return_value={'key': 'value'})
    def test_bytes_input_literal_eval_success(self, mock_literal_eval, mock_orjson):
        result = json_loads(b"{'key': 'value'}")
        self.assertEqual(result, {'key': 'value'})
        mock_literal_eval.assert_called_once_with("{'key': 'value'}")

    def test_dumps_with_orjson_success(self):
        data = {'name': '张三', 'age': 30}
        expected = '{"name":"张三","age":30}'

        with patch('llm_web_kit.libs.standard_utils.orjson') as mock_orjson:
            mock_orjson.dumps.return_value = expected.encode('utf-8')
            result = json_dumps(data)
            self.assertEqual(result, expected)

    def test_dumps_orjson_attribute_error_fallback_to_json(self):
        data = {'name': '李四', 'city': '北京'}
        expected = json.dumps(data, ensure_ascii=False)

        with patch('llm_web_kit.libs.standard_utils.orjson') as mock_orjson:
            type(mock_orjson).dumps = MagicMock(side_effect=AttributeError)
            result = json_dumps(data)
            self.assertEqual(result, expected)

    def test_dumps_with_kwargs_bypass_orjson(self):
        data = {'key': 'value'}
        expected = json.dumps(data, indent=2, ensure_ascii=False)

        with patch('llm_web_kit.libs.standard_utils.orjson'):
            result = json_dumps(data, indent=2)
            self.assertEqual(result, expected)

    def test_dumps_non_ascii_characters(self):
        data = {'message': '你好，世界！'}
        expected = '{"message":"你好，世界！"}'

        with patch('llm_web_kit.libs.standard_utils.orjson') as mock_orjson:
            mock_orjson.dumps.return_value = expected.encode('utf-8')
            result = json_dumps(data)
            self.assertEqual(result, expected)

    def test_dumps_empty_dict(self):
        data = {}
        expected = '{}'

        with patch('llm_web_kit.libs.standard_utils.orjson') as mock_orjson:
            mock_orjson.dumps.return_value = expected.encode('utf-8')
            result = json_dumps(data)
            self.assertEqual(result, expected)

    def test_dumps_complex_nested_structure(self):
        data = {
            'users': [
                {'id': 1, 'name': 'Alice'},
                {'id': 2, 'name': 'Bob'}
            ],
            'total': 2
        }
        expected = '{"users":[{"id":1,"name":"Alice"},{"id":2,"name":"Bob"}],"total":2}'

        with patch('llm_web_kit.libs.standard_utils.orjson') as mock_orjson:
            mock_orjson.dumps.return_value = expected.encode('utf-8')
            result = json_dumps(data)
            self.assertEqual(result, expected)
