import copy

import pytest

from llm_web_kit.exception.exception import ExtractorChainInputException
from llm_web_kit.input.datajson import ContentList, DataJson, DataJsonKey
from llm_web_kit.libs.doc_element_type import DocElementType


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
    with pytest.raises(ExtractorChainInputException):
        DataJson([])  # List instead of dict

    # Test invalid content_list type
    with pytest.raises(ExtractorChainInputException):
        DataJson({DataJsonKey.CONTENT_LIST: 'invalid'})  # String instead of list


def test_datajson_exclude_nodes_to_nlp_md():
    data = {
        DataJsonKey.DATASET_NAME: 'test_dataset',
        DataJsonKey.FILE_FORMAT: 'html',
        DataJsonKey.CONTENT_LIST: [[{
            'type': 'simple_table',
            'raw_content': "<table class=\"table itemDisplayTable\"><tr><td class=\"metadataFieldLabel dc_title\">Title: </td><td class=\"metadataFieldValue dc_title\">T.J. Byrne, Slide of floor plan, Poor Law Commission cottage, 1872.</td></tr><tr><td class=\"metadataFieldLabel dc_contributor\">Authors: </td><td class=\"metadataFieldValue dc_contributor\"><a class=\"author\" href=\"/browse?type=author&amp;value=T.J.%2C+Byrne\">T.J., Byrne</a><br><a class=\"author\" href=\"/browse?type=author&amp;value=Fewer%2C+Michael\">Fewer, Michael</a></td></tr><tr><td class=\"metadataFieldLabel dc_subject\">Keywords: </td><td class=\"metadataFieldValue dc_subject\">T.J. Byrne<br>Cottages<br>Poor Law Commission</td></tr><tr><td class=\"metadataFieldLabel dc_date_issued\">Issue Date: </td><td class=\"metadataFieldValue dc_date_issued\">2011<br>2011</td></tr><tr><td class=\"metadataFieldLabel dc_description\">Description: </td><td class=\"metadataFieldValue dc_description\">T.J. Byrne's slide of a one storey cottage, labelled 'Mr Barney's Plan', recommended by the Poor Law Commission, 1872.</td></tr><tr><td class=\"metadataFieldLabel dc_identifier_uri\">URI: </td><td class=\"metadataFieldValue dc_identifier_uri\"><a href=\"https://hdl.handle.net/10599/5719\">https://hdl.handle.net/10599/5719</a></td></tr><tr><td class=\"metadataFieldLabel\">Appears in Collections:</td><td class=\"metadataFieldValue\"><a href=\"/handle/10599/3\">Published Items</a><br><a href=\"/handle/10599/5553\">T.J. Byrne Collection</a><br></td></tr></table>",
            'content': {
                'html': "<table><tr><td>Title:</td><td>T.J. Byrne, Slide of floor plan, Poor Law Commission cottage, 1872.</td></tr><tr><td>Authors:</td><td>T.J., Byrne Fewer, Michael</td></tr><tr><td>Keywords:</td><td>T.J. Byrne Cottages Poor Law Commission</td></tr><tr><td>Issue Date:</td><td>2011 2011</td></tr><tr><td>Description:</td><td>T.J. Byrne's slide of a one storey cottage, labelled 'Mr Barney's Plan', recommended by the Poor Law Commission, 1872.</td></tr><tr><td>URI:</td><td>https://hdl.handle.net/10599/5719</td></tr><tr><td>Appears in Collections:</td><td>Published Items T.J. Byrne Collection</td></tr></table>",
                'is_complex': False,
                'table_nest_level': '1'
            }
        }]]
    }
    datajson = DataJson(data)
    md = datajson.get_content_list().to_nlp_md(exclude_nodes=DocElementType.COMPLEX_TABLE)
    assert '<table>' not in md


def test_datajson_exclude_nodes_to_mmd():
    data = {
        DataJsonKey.DATASET_NAME: 'test_dataset',
        DataJsonKey.FILE_FORMAT: 'html',
        DataJsonKey.CONTENT_LIST: [[{
            'type': 'simple_table',
            'raw_content': "<table class=\"table itemDisplayTable\"><tr><td class=\"metadataFieldLabel dc_title\">Title: </td><td class=\"metadataFieldValue dc_title\">T.J. Byrne, Slide of floor plan, Poor Law Commission cottage, 1872.</td></tr><tr><td class=\"metadataFieldLabel dc_contributor\">Authors: </td><td class=\"metadataFieldValue dc_contributor\"><a class=\"author\" href=\"/browse?type=author&amp;value=T.J.%2C+Byrne\">T.J., Byrne</a><br><a class=\"author\" href=\"/browse?type=author&amp;value=Fewer%2C+Michael\">Fewer, Michael</a></td></tr><tr><td class=\"metadataFieldLabel dc_subject\">Keywords: </td><td class=\"metadataFieldValue dc_subject\">T.J. Byrne<br>Cottages<br>Poor Law Commission</td></tr><tr><td class=\"metadataFieldLabel dc_date_issued\">Issue Date: </td><td class=\"metadataFieldValue dc_date_issued\">2011<br>2011</td></tr><tr><td class=\"metadataFieldLabel dc_description\">Description: </td><td class=\"metadataFieldValue dc_description\">T.J. Byrne's slide of a one storey cottage, labelled 'Mr Barney's Plan', recommended by the Poor Law Commission, 1872.</td></tr><tr><td class=\"metadataFieldLabel dc_identifier_uri\">URI: </td><td class=\"metadataFieldValue dc_identifier_uri\"><a href=\"https://hdl.handle.net/10599/5719\">https://hdl.handle.net/10599/5719</a></td></tr><tr><td class=\"metadataFieldLabel\">Appears in Collections:</td><td class=\"metadataFieldValue\"><a href=\"/handle/10599/3\">Published Items</a><br><a href=\"/handle/10599/5553\">T.J. Byrne Collection</a><br></td></tr></table>",
            'content': {
                'html': "<table><tr><td>Title:</td><td>T.J. Byrne, Slide of floor plan, Poor Law Commission cottage, 1872.</td></tr><tr><td>Authors:</td><td>T.J., Byrne Fewer, Michael</td></tr><tr><td>Keywords:</td><td>T.J. Byrne Cottages Poor Law Commission</td></tr><tr><td>Issue Date:</td><td>2011 2011</td></tr><tr><td>Description:</td><td>T.J. Byrne's slide of a one storey cottage, labelled 'Mr Barney's Plan', recommended by the Poor Law Commission, 1872.</td></tr><tr><td>URI:</td><td>https://hdl.handle.net/10599/5719</td></tr><tr><td>Appears in Collections:</td><td>Published Items T.J. Byrne Collection</td></tr></table>",
                'is_complex': False,
                'table_nest_level': '1'
            }
        }, {
            'type': 'complex_table',
            'raw_content': "<table class=\"table itemDisplayTable\"><tr><td class=\"metadataFieldLabel dc_title\">Title: </td><td class=\"metadataFieldValue dc_title\">T.J. Byrne, Slide of floor plan, Poor Law Commission cottage, 1872.</td></tr><tr><td class=\"metadataFieldLabel dc_contributor\">Authors: </td><td class=\"metadataFieldValue dc_contributor\"><a class=\"author\" href=\"/browse?type=author&amp;value=T.J.%2C+Byrne\">T.J., Byrne</a><br><a class=\"author\" href=\"/browse?type=author&amp;value=Fewer%2C+Michael\">Fewer, Michael</a></td></tr><tr><td class=\"metadataFieldLabel dc_subject\">Keywords: </td><td class=\"metadataFieldValue dc_subject\">T.J. Byrne<br>Cottages<br>Poor Law Commission</td></tr><tr><td class=\"metadataFieldLabel dc_date_issued\">Issue Date: </td><td class=\"metadataFieldValue dc_date_issued\">2011<br>2011</td></tr><tr><td class=\"metadataFieldLabel dc_description\">Description: </td><td class=\"metadataFieldValue dc_description\">T.J. Byrne's slide of a one storey cottage, labelled 'Mr Barney's Plan', recommended by the Poor Law Commission, 1872.</td></tr><tr><td class=\"metadataFieldLabel dc_identifier_uri\">URI: </td><td class=\"metadataFieldValue dc_identifier_uri\"><a href=\"https://hdl.handle.net/10599/5719\">https://hdl.handle.net/10599/5719</a></td></tr><tr><td class=\"metadataFieldLabel\">Appears in Collections:</td><td class=\"metadataFieldValue\"><a href=\"/handle/10599/3\">Published Items</a><br><a href=\"/handle/10599/5553\">T.J. Byrne Collection</a><br></td></tr></table>",
            'content': {
                'html': "<table><tr><td>Title:</td><td>T.J. Byrne, Slide of floor plan, Poor Law Commission cottage, 1872.</td></tr><tr><td>Authors:</td><td>T.J., Byrne Fewer, Michael</td></tr><tr><td>Keywords:</td><td>T.J. Byrne Cottages Poor Law Commission</td></tr><tr><td>Issue Date:</td><td>2011 2011</td></tr><tr><td>Description:</td><td>T.J. Byrne's slide of a one storey cottage, labelled 'Mr Barney's Plan', recommended by the Poor Law Commission, 1872.</td></tr><tr><td>URI:</td><td>https://hdl.handle.net/10599/5719</td></tr><tr><td>Appears in Collections:</td><td>Published Items T.J. Byrne Collection</td></tr></table>",
                'is_complex': True,
                'table_nest_level': '1'
            }
        }, {
            'type': 'image',
            'raw_content': "<img decoding=\"async\" loading=\"lazy\" aria-describedby=\"caption-attachment-17269\" class=\"wp-image-17269 size-full\" title=\"Curtindo o apartamento com piscina no centro de SP. \" src=\"https://naproadavida.com/wp-content/uploads/2020/11/20201024-Airbnb-SP-Consolacao_getaway_manha_Sony-1.jpg\" alt=\"Curtindo o apartamento com piscina no centro de SP. \" width=\"765\" height=\"510\" srcset=\"https://naproadavida.com/wp-content/uploads/2020/11/20201024-Airbnb-SP-Consolacao_getaway_manha_Sony-1.jpg 765w, https://naproadavida.com/wp-content/uploads/2020/11/20201024-Airbnb-SP-Consolacao_getaway_manha_Sony-1-480x320.jpg 480w\" sizes=\"(min-width: 0px) and (max-width: 480px) 480px, (min-width: 481px) 765px, 100vw\">",
            'content': {
                'url': 'https://naproadavida.com/wp-content/uploads/2020/11/20201024-Airbnb-SP-Consolacao_getaway_manha_Sony-1.jpg',
                'data': None,
                'alt': 'Curtindo o apartamento com piscina no centro de SP. ',
                'title': 'Curtindo o apartamento com piscina no centro de SP. ',
                'caption': None
            }
        }]]
    }
    datajson = DataJson(data)
    md = datajson.get_content_list().to_mm_md(exclude_nodes=DocElementType.COMPLEX_TABLE)
    assert '<table>' not in md
    assert 'Curtindo o apartamento com piscina no centro de SP.' in md


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
                    'type': 'simple_table',
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
        md = datajson.get_content_list().to_nlp_md(exclude_nodes=[DocElementType.COMPLEX_TABLE, DocElementType.SIMPLE_TABLE])
        assert 'Ziet u iets wat niet hoort of niet klopt?' in md
        assert 'Openingstijden' in md
        assert 'Maandag' not in md
        assert 'frame.open();\nframe.write(html);\nframe.close();' in md

    test_default_exclude()
    test_custom_exclude()
