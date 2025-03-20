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
         'html': '',
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


def test_data_json_to_nlp_md():
    d = {
        'track_id': '9fc6d25e-03ef-42a5-9675-7817c2b01936',
        'url': 'http://boards.fool.com/quoti-think-flegs-watching-what-he-eats-30294220.aspx?sort=username',
        'html': '',
        'content_list': [
            [
                {
                    'type': 'paragraph',
                    'raw_content': '<div class=\"content\"><div class=\"description-wrapper\"><div class=\"container description\"><div class=\"report text-center\"><span class=\"text-muted\">\n\t\t\t\tZiet u iets wat niet hoort of niet klopt?\n\t\t\t</span></div></div></div></div>',
                    'content': [
                        {
                            'c': 'Ziet u iets wat niet hoort of niet klopt?',
                            't': 'text'
                        }
                    ]
                },
                {
                    'type': 'title',
                    'raw_content': '<h2 class=\"text-center \" data-step=\"4\">Openingstijden</h2>',
                    'content': {
                        'title_content': 'Openingstijden',
                        'level': '2'
                    }
                },
                {
                    'type': 'table',
                    'raw_content': '<table class=\"table table-hover\" id=\"table-visitinghours\"><tr class=\"\"><td>\n\t\t\t\tMaandag\n\t\t\t</td><td class=\"text-right\">\n\n\t\t\t\t\t\t\t\t\t\t\t\t-\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td></tr><tr class=\"\"><td>\n\t\t\t\tDinsdag\n\t\t\t</td><td class=\"text-right\">\n\n\t\t\t\t\t\t\t\t\t\t\t\t-\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td></tr><tr class=\"\"><td>\n\t\t\t\tWoensdag\n\t\t\t</td><td class=\"text-right\">\n\n\t\t\t\t\t\t\t\t\t\t\t\t-\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td></tr><tr class=\"\"><td>\n\t\t\t\tDonderdag\n\t\t\t</td><td class=\"text-right\">\n\n\t\t\t\t\t\t\t\t\t\t\t\t-\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td></tr><tr class=\"\"><td>\n\t\t\t\tVrijdag\n\t\t\t</td><td class=\"text-right\">\n\n\t\t\t\t\t\t\t\t\t\t\t\t-\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td></tr><tr class=\"\"><td>\n\t\t\t\tZaterdag\n\t\t\t</td><td class=\"text-right\">\n\n\t\t\t\t\t\t\t\t\t\t\t\t-\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td></tr><tr class=\"\"><td>\n\t\t\t\tZondag\n\t\t\t</td><td class=\"text-right\">\n\n\t\t\t\t\t\t\t\t\t\t\t\t-\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td></tr></table>',
                    'content': {
                        'html': '<table><tr><td>Maandag</td><td>-</td></tr><tr><td>Dinsdag</td><td>-</td></tr><tr><td>Woensdag</td><td>-</td></tr><tr><td>Donderdag</td><td>-</td></tr><tr><td>Vrijdag</td><td>-</td></tr><tr><td>Zaterdag</td><td>-</td></tr><tr><td>Zondag</td><td>-</td></tr></table>',
                        'is_complex': False,
                        'table_nest_level': '1'
                    }
                },
                {
                    'type': 'code',
                    'raw_content': '<code>frame.open();\nframe.write(html);\nframe.close();\n</code>',
                    'inline': False,
                    'content': {
                        'code_content': 'frame.open();\nframe.write(html);\nframe.close();',
                        'by': 'tag_pre_code'
                    }
                }
            ]
        ]
    }

    def test_default_exclude():
        datajson = DataJson(d)
        md = datajson.get_content_list().to_nlp_md()
        assert 'Ziet u iets wat niet hoort of niet klopt?' in md
        assert 'Openingstijden' in md
        assert 'Maandag' in md
        assert 'frame.open();\nframe.write(html);\nframe.close();' in md

    def test_custom_exclude():
        datajson = DataJson(d)
        md = datajson.get_content_list().to_nlp_md(MM_NODE_LIST=['table'])
        assert 'Ziet u iets wat niet hoort of niet klopt?' in md
        assert 'Openingstijden' in md
        assert 'Maandag' not in md
        assert 'frame.open();\nframe.write(html);\nframe.close();' in md

    test_default_exclude()
    test_custom_exclude()
