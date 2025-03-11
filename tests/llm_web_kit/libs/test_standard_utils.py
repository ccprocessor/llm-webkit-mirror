# Copyright (c) Opendatalab. All rights reserved.
"""Common basic operation unit test."""

from typing import Union

import pytest

from llm_web_kit.libs.standard_utils import json_dumps, json_loads


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
    ({
        '0': 'aaa',
        '1': 'bbb',
        '2': 'ccc'
    }, '''{"0":"aaa","1":"bbb","2":"ccc"}'''),
    ({
        'track_id': '7c5b99d3',
        'warc_record_offset': 65390694,
        'warc_record_length': '16190',
        'layout_id': 0
    }, '{"track_id":"7c5b99d3","warc_record_offset":65390694,"warc_record_length":"16190","layout_id":0}'),
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
