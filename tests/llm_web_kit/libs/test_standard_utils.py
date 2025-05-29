# Copyright (c) Opendatalab. All rights reserved.
"""Common basic operation unit test."""
import unittest
from typing import Union

import pytest

from llm_web_kit.libs.standard_utils import (compress_and_decompress_str,
                                             json_dumps, json_loads)


@pytest.mark.parametrize('input, target_dict', [
    ('{}', {}),
    (b'{"0": "aaa", "1": "bbb", "2": "ccc"}', {
        '0': 'aaa',
        '1': 'bbb',
        '2': 'ccc'
    }),
    ('''{"track_id": "7c5b99d3-711d-45df-bda9-e1c809684b94",
                               "url_host_name": "%D0%9E%D0%B1%D1%8A%D1%8F%D1%81%D0%BD%D1%8F%D0%B5%D0%BC.%D1%80%D1%84",
                               "warc_record_offset": 65390694,
                               "warc_record_length": "16190",
                               "html_type": "html_structure",
                               "layout_id": 0}''', {
        'track_id': '7c5b99d3-711d-45df-bda9-e1c809684b94',
        'url_host_name': '%D0%9E%D0%B1%D1%8A%D1%8F%D1%81%D0%BD%D1%8F%D0%B5%D0%BC.%D1%80%D1%84',
        'warc_record_offset': 65390694,
        'warc_record_length': '16190',
        'html_type': 'html_structure',
        'layout_id': 0
    }),
])
def test_json_loads(input: Union[str, bytes], target_dict) -> None:
    """
    test json_loads function.
    Args:
        input: The JSON-formatted string or bytes.
        target_dict: target result.

    Returns: None

    """
    assert target_dict == json_loads(input)


@pytest.mark.parametrize('input_dict, target_str', [
    ({}, '{}'),
    ({'0': 'aaa', '1': 'bbb', '2': 'ccc'}, '''{"0":"aaa","1":"bbb","2":"ccc"}'''),
    ({'track_id': '7c5b99d3', 'warc_record_offset': 65390694, 'warc_record_length': '16190', 'layout_id': 0},
     '{"track_id":"7c5b99d3","warc_record_offset":65390694,"warc_record_length":"16190","layout_id":0}'),
])
def test_json_dumps(input_dict: dict, target_str) -> None:
    """
    test json_dumps function.
    Args:
        input_dict: The Python dict.
        target_str: target result.

    Returns: None

    """
    expected_obj = json_loads(target_str)
    # 比较两个对象是否相等
    for key, value in input_dict.items():
        assert expected_obj[key] == value

    # 比较json_dumps的输出是否与target_str相等
    json_str = json_dumps(input_dict)  # 由于不同的python版本，json_dumps的输出可能不同，所以需要比较json_loads的输出
    obj = json_loads(json_str)
    for key, value in input_dict.items():
        assert obj[key] == value


TEST_COMPRESS_CASES = [
    {'input': '测试数据', 'com_expected': b'x\x9c{\xb6\xb5\xfb\xc5\xfa\xa9\xcf\xa6nx\xd6\xbb\x0e\x009C\x08\x9f',
     'base_expected': 'eJx7trX7xfqpz6ZueNa7DgA5Qwif'},
    {'input': 'Оренбург, штакетник П-образный узкий, цена',
     'com_expected': b'x\x9c\x1d\x8c\xdb\t\x800\x10\x04[\xb9\x02\xb4\xc7`@\x04{\xd0\x16"\x12b\x02g\rs\x1d\xb9\xf8\xb5\xc3\xbe8"Qq\xae\xc8\xa2{\xb2\xd8b\xa10\xa8R\xe7a\x18\xe7\xcc\xabF\x92\xdf\xf0\xd8\xe9\x16Y8\x14wM\xd6\xff\xa2|\xfer4T',
     'base_expected': 'eJwdjNsJgDAQBFu5ArTHYEAEe9AWIhJiAmcNcx25+LXDvjgiUXGuyKJ7sthioTCoUudhGOfMq0aS3/DY6RZZOBR3Tdb/onz+cjRU'},
    {'input': b'x\x9c{\xb6\xb5\xfb\xc5\xfa\xa9\xcf\xa6nx\xd6\xbb\x0e\x009C\x08\x9f', 'com_expected': b'x\x9c\xab\x98S\xbdm\xeb\xef\xa3\xbfV\x9e_\x96Wqm7\x1f\x83\xa53\xc7|\x00\x91b\x0b{', 'base_expected': 'eJyrmFO9bevvo79Wnl+WV3FtNx+DpTPHfACRYgt7'},
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
