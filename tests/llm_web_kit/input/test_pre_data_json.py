import copy
import unittest

from llm_web_kit.input.pre_data_json import PreDataJson, PreDataJsonKey


class TestPreDataJsonInit(unittest.TestCase):
    def test_pre_data_json_init(self):
        # Test empty initialization
        pre_data_json = PreDataJson()
        assert isinstance(pre_data_json.get_layout_file_list(), list)
        assert len(pre_data_json.get_layout_file_list()) == 0

        # Test with initial data
        data = {
            PreDataJsonKey.DOMAIN_NAME: 'example.com',
            PreDataJsonKey.DOMAIN_ID: 'domain_123',
            PreDataJsonKey.LAYOUT_NAME: 'test_layout',
            PreDataJsonKey.LAYOUT_ID: 'layout_123',
            PreDataJsonKey.LAYOUT_FILE_LIST: ['file1.html', 'file2.html'],
            PreDataJsonKey.RECORD_COUNT: 100
        }
        pre_data_json = PreDataJson(data)
        assert pre_data_json[PreDataJsonKey.DOMAIN_NAME] == 'example.com'
        assert pre_data_json[PreDataJsonKey.DOMAIN_ID] == 'domain_123'
        assert pre_data_json[PreDataJsonKey.LAYOUT_NAME] == 'test_layout'
        assert pre_data_json[PreDataJsonKey.LAYOUT_ID] == 'layout_123'
        assert len(pre_data_json.get_layout_file_list()) == 2
        assert pre_data_json[PreDataJsonKey.RECORD_COUNT] == 100

    def test_pre_data_json_dict_operations(self):
        data = {
            'key1': 'value1',
            PreDataJsonKey.LAYOUT_FILE_LIST: ['file1.html']
        }
        pre_data_json = PreDataJson(data)

        # Test __getitem__
        assert pre_data_json['key1'] == 'value1'

        # Test __setitem__
        pre_data_json['key2'] = 'value2'
        assert pre_data_json['key2'] == 'value2'

        # Test get() method
        assert pre_data_json.get('key1') == 'value1'
        assert pre_data_json.get('non_existent', 'default') == 'default'

        # Test __contains__
        assert 'key1' in pre_data_json
        assert 'non_existent' not in pre_data_json

    def test_pre_data_json_layout_file_list_operations(self):
        data = {
            PreDataJsonKey.LAYOUT_FILE_LIST: ['file1.html', 'file2.html']
        }
        pre_data_json = PreDataJson(data)
        layout_file_list = pre_data_json.get_layout_file_list()

        # Test layout_file_list access
        assert layout_file_list[0] == 'file1.html'
        assert layout_file_list[1] == 'file2.html'

        # Test layout_file_list modification
        layout_file_list[0] = 'modified_file.html'
        assert layout_file_list[0] == 'modified_file.html'

        # Test layout_file_list append
        layout_file_list.append('file3.html')
        assert len(layout_file_list) == 3
        assert layout_file_list[2] == 'file3.html'

    def test_pre_data_json_keys_values_items(self):
        data = {
            'key1': 'value1',
            'key2': 'value2',
            PreDataJsonKey.LAYOUT_FILE_LIST: ['file1.html']
        }
        pre_data_json = PreDataJson(data)

        # Test keys()
        keys = list(pre_data_json.keys())
        assert 'key1' in keys
        assert 'key2' in keys
        assert PreDataJsonKey.LAYOUT_FILE_LIST in keys

        # Test values()
        values = list(pre_data_json.values())
        assert 'value1' in values
        assert 'value2' in values
        assert ['file1.html'] in values

        # Test items()
        items = list(pre_data_json.items())
        assert ('key1', 'value1') in items
        assert ('key2', 'value2') in items
        assert (PreDataJsonKey.LAYOUT_FILE_LIST, ['file1.html']) in items

    def test_pre_data_json_serialization(self):
        data = {
            PreDataJsonKey.DOMAIN_NAME: 'example.com',
            PreDataJsonKey.LAYOUT_NAME: 'test_layout',
            PreDataJsonKey.LAYOUT_FILE_LIST: ['file1.html', 'file2.html']
        }
        pre_data_json = PreDataJson(data)

        # Test to_dict()
        dict_data = pre_data_json.to_dict()
        assert isinstance(dict_data, dict)
        assert dict_data[PreDataJsonKey.DOMAIN_NAME] == 'example.com'
        assert dict_data[PreDataJsonKey.LAYOUT_NAME] == 'test_layout'
        assert len(dict_data[PreDataJsonKey.LAYOUT_FILE_LIST]) == 2

        # Test to_json()
        json_str = pre_data_json.to_json()
        assert isinstance(json_str, str)
        assert 'example.com' in json_str
        assert 'test_layout' in json_str
        assert 'file1.html' in json_str
        assert 'file2.html' in json_str

        # Test to_json() with pretty=True
        pretty_json_str = pre_data_json.to_json(pretty=True)
        assert isinstance(pretty_json_str, str)
        assert 'example.com' in pretty_json_str
        assert 'test_layout' in pretty_json_str
        assert 'file1.html' in pretty_json_str
        assert 'file2.html' in pretty_json_str
        # Pretty JSON should have newlines and indentation
        assert '\n' in pretty_json_str
        assert '  ' in pretty_json_str

    def test_pre_data_json_deep_copy(self):
        """Test that PreDataJson deep-copies the input data."""
        original_data = {
            PreDataJsonKey.DOMAIN_NAME: 'example.com',
            PreDataJsonKey.LAYOUT_FILE_LIST: ['file1.html', 'file2.html']
        }
        original_copy = copy.deepcopy(original_data)

        # Create PreDataJson with original data
        pre_data_json = PreDataJson(original_data)

        # Modify the PreDataJson object
        pre_data_json[PreDataJsonKey.DOMAIN_NAME] = 'modified.com'
        pre_data_json.get_layout_file_list().append('file3.html')

        # Original data should not be affected
        assert original_data == original_copy
        assert original_data[PreDataJsonKey.DOMAIN_NAME] == 'example.com'
        assert len(original_data[PreDataJsonKey.LAYOUT_FILE_LIST]) == 2

    def test_pre_data_json_to_dict_immutability(self):
        """Test that to_dict() returns a copy that doesn't affect the
        original."""
        pre_data_json = PreDataJson({
            PreDataJsonKey.DOMAIN_NAME: 'example.com',
            PreDataJsonKey.LAYOUT_FILE_LIST: ['file1.html', 'file2.html']
        })

        # Get dict representation
        dict_data = pre_data_json.to_dict()

        # Modify the returned dict
        dict_data[PreDataJsonKey.DOMAIN_NAME] = 'modified.com'
        dict_data[PreDataJsonKey.LAYOUT_FILE_LIST].append('file3.html')

        # Original PreDataJson should not be affected
        assert pre_data_json[PreDataJsonKey.DOMAIN_NAME] == 'example.com'
        assert len(pre_data_json.get_layout_file_list()) == 2
        assert 'file3.html' not in pre_data_json.get_layout_file_list()


class TestPreDataJsonKey(unittest.TestCase):
    def test_pre_data_json_key_constants(self):
        """Test that PreDataJsonKey constants are defined correctly."""
        # Check that all required keys are defined
        assert hasattr(PreDataJsonKey, 'DOMAIN_NAME')
        assert hasattr(PreDataJsonKey, 'DOMAIN_ID')
        assert hasattr(PreDataJsonKey, 'DOMAIN_FILE_LIST')
        assert hasattr(PreDataJsonKey, 'LAYOUT_NAME')
        assert hasattr(PreDataJsonKey, 'LAYOUT_ID')
        assert hasattr(PreDataJsonKey, 'LAYOUT_FILE_LIST')
        assert hasattr(PreDataJsonKey, 'RECORD_COUNT')
        assert hasattr(PreDataJsonKey, 'TYPICAL_RAW_HTML')
        assert hasattr(PreDataJsonKey, 'TYPICAL_RAW_TAG_HTML')
        assert hasattr(PreDataJsonKey, 'TYPICAL_SIMPLIFIED_HTML')
        assert hasattr(PreDataJsonKey, 'LLM_RESPONSE')
        assert hasattr(PreDataJsonKey, 'HTML_ELEMENT_LIST')
        assert hasattr(PreDataJsonKey, 'HTML_TARGET_LIST')
        assert hasattr(PreDataJsonKey, 'MAIN_HTML')
        assert hasattr(PreDataJsonKey, 'FILTERED_MAIN_HTML')

        # Check actual values
        assert PreDataJsonKey.DOMAIN_NAME == 'domain_name'
        assert PreDataJsonKey.LAYOUT_FILE_LIST == 'layout_file_list'
        assert PreDataJsonKey.MAIN_HTML == 'main_html'
