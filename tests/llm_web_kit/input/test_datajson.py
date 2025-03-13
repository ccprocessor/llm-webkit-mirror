import copy

import pytest

from llm_web_kit.input.datajson import ContentList, DataJson, DataJsonKey


def test_datajson_init():
    # Test empty initialization
    data = {}
    datajson = DataJson(data)
    assert isinstance(datajson.get_content_list(), ContentList)
    assert datajson.get_content_list().length() == 0

    # Test with content list
    data = {
        DataJsonKey.DATASET_NAME: 'test_dataset',
        DataJsonKey.FILE_FORMAT: 'html',
        DataJsonKey.CONTENT_LIST: [
            {'type': 'text', 'content': 'test content'}
        ]
    }
    datajson = DataJson(data)
    assert datajson.get_dataset_name() == 'test_dataset'
    assert datajson.get_file_format() == 'html'
    assert datajson.get_content_list().length() == 1


def test_datajson_dict_operations():
    data = {
        'key1': 'value1',
        DataJsonKey.CONTENT_LIST: []
    }
    datajson = DataJson(data)

    # Test __getitem__
    assert datajson['key1'] == 'value1'

    # Test __setitem__
    datajson['key2'] = 'value2'
    assert datajson['key2'] == 'value2'

    # Test get() method
    assert datajson.get('key1') == 'value1'
    assert datajson.get('non_existent', 'default') == 'default'

    # Test __delitem__
    del datajson['key1']
    with pytest.raises(KeyError):
        _ = datajson['key1']


def test_datajson_content_list_operations():
    data = {
        DataJsonKey.CONTENT_LIST: [
            {'type': 'text', 'content': 'content1'},
            {'type': 'code', 'content': 'code1'}
        ]
    }
    datajson = DataJson(data)
    content_list = datajson.get_content_list()

    # Test content list access
    assert content_list[0]['type'] == 'text'
    assert content_list[1]['content'] == 'code1'

    # Test content list modification
    content_list[0] = {'type': 'text', 'content': 'modified'}
    assert content_list[0]['content'] == 'modified'

    # Test content list append
    content_list.append({'type': 'image', 'content': 'image1'})
    assert content_list.length() == 3


def test_datajson_serialization():
    data = {
        DataJsonKey.DATASET_NAME: 'test_dataset',
        DataJsonKey.FILE_FORMAT: 'html',
        DataJsonKey.CONTENT_LIST: [
            {'type': 'text', 'content': 'test content'}
        ]
    }
    datajson = DataJson(data)

    # Test to_dict()
    dict_data = datajson.to_dict()
    assert isinstance(dict_data, dict)
    assert dict_data[DataJsonKey.DATASET_NAME] == 'test_dataset'
    assert len(dict_data[DataJsonKey.CONTENT_LIST]) == 1

    # Test to_json()
    json_str = datajson.to_json()
    assert isinstance(json_str, str)
    assert 'test_dataset' in json_str
    assert 'test content' in json_str


def test_datajson_validation():
    # Test invalid input type
    with pytest.raises(ValueError):
        DataJson([])  # List instead of dict

    # Test invalid content_list type
    with pytest.raises(ValueError):
        DataJson({DataJsonKey.CONTENT_LIST: 'invalid'})  # String instead of list


def test_data_json_deepcopy():
    """从一个外部dict构建datajson, 改变datajson，不改变外部dict."""
    d = {'track_id': '32266dfa-c335-45c5-896e-56f057889d28',
        'url': 'http://mathematica.stackexchange.com/users/1931/ywdr1987?tab=activity&sort=all',
        'html':'',
        'page_layout_type': 'forum',
        'domain': 'mathematica.stackexchange.com',
        'dataset_name': 'math',
        'data_source_category': 'HTML',
        'meta_info': {'warc_headers': {'WARC-IP-Address': '104.16.12.13'}}}
    copied = copy.deepcopy(d)
    _ = DataJson(copied)
    cl = copied.get('content_list')  # 不该变外部变量d
    assert cl is None

    def test_datajson_to_dict_immutable():
        """测试to_dict()返回的dict修改不会影响原DataJson对象."""
        data = {
            DataJsonKey.DATASET_NAME: 'test_dataset',
            DataJsonKey.FILE_FORMAT: 'html',
            DataJsonKey.CONTENT_LIST: [
                {'type': 'text', 'content': 'test content'}
            ]
        }
        datajson = DataJson(data)

        # Get dict representation
        dict_data = datajson.to_dict()

        # Modify the returned dict
        dict_data[DataJsonKey.DATASET_NAME] = 'modified_dataset'
        dict_data[DataJsonKey.CONTENT_LIST][0]['content'] = 'modified content'

        # Original DataJson should remain unchanged
        assert datajson.get_dataset_name() == 'test_dataset'
        assert datajson.get_content_list()._get_data()[0]['content'] == 'test content'

        # Verify the modifications only affected the dict copy
        assert dict_data[DataJsonKey.DATASET_NAME] == 'modified_dataset'
        assert dict_data[DataJsonKey.CONTENT_LIST][0]['content'] == 'modified content'
