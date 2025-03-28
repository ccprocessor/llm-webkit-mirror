"""Test cases for source_safety_detector.py."""

import unittest
from unittest.mock import patch

from llm_web_kit.model.source_safety_detector import (
    SourceFilter, auto_download, build_data_source_map,
    decide_domestic_source_by_data_source, decide_safe_source_by_data_source,
    get_data_source_map, lookup_safe_type_by_data_source)


class TestSourceSafetyDetector(unittest.TestCase):
    """Test cases for source safety detector functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_data = [
            'data_source,content_style,safe_type',
            'example.com,问答,safe_source',
            'test.cn,文章,domestic_source',
            'unknown.com,forum,other',
        ]

    @patch('llm_web_kit.model.source_safety_detector.download_auto_file')
    @patch('llm_web_kit.model.source_safety_detector.load_config')
    def test_auto_download(self, mock_load_config, mock_download):
        """Test auto_download function."""
        mock_load_config.return_value = {
            'resources': {
                'data_source_safe_type': {
                    'download_path': 'http://example.com/test.csv',
                    'md5': 'test_md5',
                },
            },
        }
        mock_download.return_value = 'test_path.csv'

        result = auto_download()
        self.assertEqual(result, 'test_path.csv')
        mock_download.assert_called_once()

    @patch('llm_web_kit.model.source_safety_detector.auto_download')
    def test_build_data_source_map(self, mock_auto_download):
        """Test build_data_source_map function."""
        mock_auto_download.return_value = 'test.csv'

        with patch('builtins.open', unittest.mock.mock_open(read_data='\n'.join(self.test_data))):
            result = build_data_source_map()

            self.assertIn('example.com', result)
            self.assertIn('test.cn', result)
            self.assertIn('unknown.com', result)

            # Test content style mapping
            self.assertEqual(result['example.com']['content_style'], 'qna')
            self.assertEqual(result['test.cn']['content_style'], 'article')
            self.assertEqual(result['unknown.com']['content_style'], None)

            # Test safe type mapping
            self.assertEqual(result['example.com']['safe_type'], 'safe_source')
            self.assertEqual(result['test.cn']['safe_type'], 'domestic_source')
            self.assertEqual(result['unknown.com']['safe_type'], 'other')

    @patch('llm_web_kit.model.source_safety_detector.build_data_source_map')
    @patch('llm_web_kit.model.source_safety_detector.singleton_resource_manager')
    def test_get_data_source_map(self, mock_manager, mock_build_map):
        """Test get_data_source_map function."""
        mock_map = {'test.com': {'content_style': 'qna', 'safe_type': 'safe_source'}}
        mock_build_map.return_value = mock_map
        mock_manager.has_name.return_value = False
        mock_manager.get_resource.return_value = mock_map

        result = get_data_source_map()

        self.assertEqual(result, mock_map)
        mock_manager.get_resource.assert_called_once_with('data_source_safety_map')

    def test_lookup_safe_type_by_data_source(self):
        """Test lookup_safe_type_by_data_source function."""
        with patch('llm_web_kit.model.source_safety_detector.get_data_source_map') as mock_get_map:
            mock_get_map.return_value = {
                'example.com': {'safe_type': 'safe_source'},
                'test.cn': {'safe_type': 'domestic_source'},
            }

            # Test existing sources
            self.assertEqual(lookup_safe_type_by_data_source('example.com'), 'safe_source')
            self.assertEqual(lookup_safe_type_by_data_source('test.cn'), 'domestic_source')

            # Test non-existing source
            self.assertIsNone(lookup_safe_type_by_data_source('unknown.com'))

    def test_decide_domestic_source_by_data_source(self):
        """Test decide_domestic_source_by_data_source function."""
        with patch('llm_web_kit.model.source_safety_detector.lookup_safe_type_by_data_source') as mock_lookup:
            # Test domestic source
            mock_lookup.return_value = 'domestic_source'
            self.assertTrue(decide_domestic_source_by_data_source('test.cn'))

            # Test non-domestic source
            mock_lookup.return_value = 'safe_source'
            self.assertFalse(decide_domestic_source_by_data_source('example.com'))

            # Test unknown source
            mock_lookup.return_value = None
            self.assertFalse(decide_domestic_source_by_data_source('unknown.com'))

    def test_decide_safe_source_by_data_source(self):
        """Test decide_safe_source_by_data_source function."""
        with patch('llm_web_kit.model.source_safety_detector.lookup_safe_type_by_data_source') as mock_lookup:
            # Test safe source
            mock_lookup.return_value = 'safe_source'
            self.assertTrue(decide_safe_source_by_data_source('example.com'))

            # Test non-safe source
            mock_lookup.return_value = 'domestic_source'
            self.assertFalse(decide_safe_source_by_data_source('test.cn'))

            # Test unknown source
            mock_lookup.return_value = None
            self.assertFalse(decide_safe_source_by_data_source('unknown.com'))


class TestSourceFilter(unittest.TestCase):
    """Test cases for SourceFilter class."""

    def setUp(self):
        """Set up test fixtures."""
        self.filter = SourceFilter()

    @patch('llm_web_kit.model.source_safety_detector.decide_safe_source_by_data_source')
    @patch('llm_web_kit.model.source_safety_detector.decide_domestic_source_by_data_source')
    def test_filter(self, mock_decide_domestic, mock_decide_safe):
        """Test filter method."""
        # Test safe source
        mock_decide_safe.return_value = True
        mock_decide_domestic.return_value = False
        result = self.filter.filter(
            content_str='Safe content',
            language='en',
            data_source='example.com',
            language_details='formal',
            content_style='article',
        )
        self.assertTrue(result['from_safe_source'])
        self.assertFalse(result['from_domestic_source'])

        # Test domestic source
        mock_decide_safe.return_value = False
        mock_decide_domestic.return_value = True
        result = self.filter.filter(
            content_str='Domestic content',
            language='zh',
            data_source='test.cn',
            language_details='formal',
            content_style='article',
        )
        self.assertFalse(result['from_safe_source'])
        self.assertTrue(result['from_domestic_source'])

        # Test unsafe source
        mock_decide_safe.return_value = False
        mock_decide_domestic.return_value = False
        result = self.filter.filter(
            content_str='Unsafe content',
            language='en',
            data_source='unknown.com',
            language_details='informal',
            content_style='forum',
        )
        self.assertFalse(result['from_safe_source'])
        self.assertFalse(result['from_domestic_source'])


if __name__ == '__main__':
    unittest.main()
