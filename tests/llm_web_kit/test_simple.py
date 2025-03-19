import unittest
from unittest.mock import MagicMock, patch

from llm_web_kit.input.datajson import DataJson
from llm_web_kit.simple import (ExtractorFactory, ExtractorType,
                                extract_html_to_md, extract_html_to_mm_md)


class TestSimple(unittest.TestCase):
    def setUp(self):
        self.url = 'https://example.com'
        self.html_content = '<html><body><h1>Test Content</h1><p>This is a test paragraph.</p></body></html>'

    @patch('llm_web_kit.simple.ExtractSimpleFactory.create')
    @patch('llm_web_kit.simple.load_pipe_tpl')
    def test_extractor_factory(self, mock_load_pipe_tpl, mock_create):
        # Setup mocks
        mock_chain = MagicMock()
        mock_create.return_value = mock_chain
        mock_load_pipe_tpl.return_value = {'config': 'test'}

        # Test HTML extractor creation
        extractor = ExtractorFactory.get_extractor(ExtractorType.HTML)
        self.assertEqual(extractor, mock_chain)
        mock_load_pipe_tpl.assert_called_once_with('html')
        mock_create.assert_called_once_with({'config': 'test'})

        # Test caching - should reuse the same extractor
        ExtractorFactory.get_extractor(ExtractorType.HTML)
        # Verify the mocks were not called again
        mock_load_pipe_tpl.assert_called_once()
        mock_create.assert_called_once()

        # Test invalid extractor type
        with self.assertRaises(ValueError):
            ExtractorFactory.get_extractor('invalid_type')

    @patch('llm_web_kit.simple.ExtractorFactory.get_extractor')
    def test_extract_html_to_md(self, mock_get_extractor):
        # Setup mock
        mock_extractor = MagicMock()
        mock_result = MagicMock()
        mock_content_list = MagicMock()
        mock_content_list.to_mm_md.return_value = '# Test Content\n\nThis is a test paragraph.'
        mock_result.get_content_list.return_value = mock_content_list
        mock_extractor.extract.return_value = mock_result
        mock_get_extractor.return_value = mock_extractor

        # Test extract_html_to_md
        result = extract_html_to_md(self.url, self.html_content)
        self.assertEqual(result, '# Test Content\n\nThis is a test paragraph.')

        # Verify the mock was called with correct parameters
        mock_get_extractor.assert_called_once_with(ExtractorType.HTML)
        mock_extractor.extract.assert_called_once()
        # Verify DataJson was created with correct data
        call_args = mock_extractor.extract.call_args[0][0]
        self.assertIsInstance(call_args, DataJson)
        self.assertEqual(call_args.get('url'), self.url)
        self.assertEqual(call_args.get('html_content'), self.html_content)
        self.assertEqual(call_args.get('dataset_name'), 'llm-web-kit-quickstart')
        self.assertEqual(call_args.get('data_source_category'), 'HTML')

    @patch('llm_web_kit.simple.ExtractorFactory.get_extractor')
    def test_extract_html_to_mm_md(self, mock_get_extractor):
        # Setup mock
        mock_extractor = MagicMock()
        mock_result = MagicMock()
        mock_content_list = MagicMock()
        mock_content_list.to_mm_md.return_value = '# Test Content\n\nThis is a test paragraph.'
        mock_result.get_content_list.return_value = mock_content_list
        mock_extractor.extract.return_value = mock_result
        mock_get_extractor.return_value = mock_extractor

        # Test extract_html_to_mm_md
        result = extract_html_to_mm_md(self.url, self.html_content)
        self.assertEqual(result, '# Test Content\n\nThis is a test paragraph.')

        # Verify the mock was called with correct parameters
        mock_get_extractor.assert_called_once_with(ExtractorType.HTML)
        mock_extractor.extract.assert_called_once()
        # Verify DataJson was created with correct data
        call_args = mock_extractor.extract.call_args[0][0]
        self.assertIsInstance(call_args, DataJson)
        self.assertEqual(call_args.get('url'), self.url)
        self.assertEqual(call_args.get('html_content'), self.html_content)
