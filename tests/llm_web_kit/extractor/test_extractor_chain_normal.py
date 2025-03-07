import json
import os
import unittest

from llm_web_kit.exception.exception import (ExtractorChainInputException,
                                             ExtractorNotFoundException)
from llm_web_kit.extractor.extractor_chain import ExtractSimpleFactory
from llm_web_kit.input.datajson import DataJson


class TestExtractorChainNormal(unittest.TestCase):
    """Test basic ExtractorChain functionality."""

    def setUp(self):
        self.base_path = os.path.dirname(os.path.abspath(__file__))

        # Basic HTML config
        self.html_config = {
            'extractor_pipe': {
                'pre_extractor': [
                    {
                        'enable': True,
                        'python_class': 'llm_web_kit.extractor.html.pre_extractor.HTMLFileFormatFilterPreExtractor',
                        'class_init_kwargs': {},
                    },
                    {
                        'enable': True,
                        'python_class': 'llm_web_kit.extractor.html.pre_extractor.HTMLFileFormatCleanTagsPreExtractor',
                        'class_init_kwargs': {},
                    }
                ],
                'extractor': [
                    {
                        'enable': True,
                        'python_class': 'llm_web_kit.extractor.html.extractor.HTMLFileFormatExtractor',
                        'class_init_kwargs': {},
                    }
                ],
                'post_extractor': [
                    {
                        'enable': False,
                        'python_class': 'llm_web_kit.extractor.html.post_extractor.HTMLFileFormatPostExtractor',
                        'class_init_kwargs': {},
                    }
                ],
            }
        }

        # Basic PDF config
        self.pdf_config = {
            'extractor_pipe': {
                'pre_extractor': [
                    {
                        'enable': True,
                        'python_class': 'llm_web_kit.extractor.pdf.pre_extractor.PDFFileFormatFilterPreExtractor',
                        'class_init_kwargs': {},
                    }
                ],
                'extractor': [
                    {
                        'enable': True,
                        'python_class': 'llm_web_kit.extractor.pdf.extractor.PDFFileFormatExtractor',
                        'class_init_kwargs': {},
                    }
                ],
                'post_extractor': [
                    {
                        'enable': False,
                        'python_class': 'llm_web_kit.extractor.pdf.post_extractor.PDFFileFormatPostExtractor',
                        'class_init_kwargs': {},
                    }
                ],
            }
        }

        # Basic EBOOK config
        self.ebook_config = {
            'extractor_pipe': {
                'pre_extractor': [
                    {
                        'enable': True,
                        'python_class': 'llm_web_kit.extractor.ebook.pre_extractor.EBOOKFileFormatFilterPreExtractor',
                        'class_init_kwargs': {},
                    }
                ],
                'extractor': [
                    {
                        'enable': True,
                        'python_class': 'llm_web_kit.extractor.ebook.extractor.EBOOKFileFormatExtractor',
                        'class_init_kwargs': {},
                    }
                ],
                'post_extractor': [
                    {
                        'enable': False,
                        'python_class': 'llm_web_kit.extractor.ebook.post_extractor.EBOOKFileFormatPostExtractor',
                        'class_init_kwargs': {},
                    }
                ],
            }
        }

    def test_factory_create(self):
        """Test factory creation with different inputs."""
        # Test with dict config
        chain = ExtractSimpleFactory.create(self.html_config)
        self.assertIsNotNone(chain)

        # Test with config file
        config_path = os.path.join(self.base_path, 'assets/test_config.jsonc')
        with open(config_path, 'w') as f:
            json.dump(self.html_config, f)
        chain = ExtractSimpleFactory.create(config_path)
        self.assertIsNotNone(chain)
        os.remove(config_path)

    def test_basic_html_extraction(self):
        """Test basic HTML extraction."""
        chain = ExtractSimpleFactory.create(self.html_config)
        self.assertIsNotNone(chain)

        input_data = DataJson(
            {
                'dataset_name': 'news',
                'data_source_category': 'html',
                'html': '<html><body><h1>hello</h1></body></html>',
                'url': 'http://www.baidu.com',
            }
        )
        data_e: DataJson = chain.extract(input_data)
        self.assertEqual(data_e.get_content_list().length(), 1)
        self.assertEqual(data_e.get_dataset_name(), 'news')
        self.assertEqual(data_e.get_file_format(), 'html')

    def test_basic_pdf_extraction(self):
        """Test basic PDF extraction."""
        chain = ExtractSimpleFactory.create(self.pdf_config)
        self.assertIsNotNone(chain)

        input_data = DataJson({'dataset_name': 'news', 'data_source_category': 'pdf'})
        data_e: DataJson = chain.extract(input_data)
        self.assertEqual(data_e.get_content_list().length(), 0)
        self.assertEqual(data_e.get_dataset_name(), 'news')
        self.assertEqual(data_e.get_file_format(), 'pdf')

    def test_basic_ebook_extraction(self):
        """Test basic EBOOK extraction."""
        chain = ExtractSimpleFactory.create(self.ebook_config)
        self.assertIsNotNone(chain)

        input_data = DataJson({'dataset_name': 'news', 'data_source_category': 'ebook', 'content_list': [[], []]})
        data_e: DataJson = chain.extract(input_data)
        self.assertEqual(data_e.get_content_list().length(), 2)
        self.assertEqual(data_e.get_dataset_name(), 'news')
        self.assertEqual(data_e.get_file_format(), 'ebook')

    def test_error_handling(self):
        """Test error handling cases."""
        chain = ExtractSimpleFactory.create(self.html_config)

        # Test invalid input type
        with self.assertRaises(ExtractorChainInputException):
            chain.extract(DataJson({'data_source_category': 'html', 'html': '<h1>Test</h1>'}))

        # Test invalid config
        invalid_config = {'extractor_pipe': {'extractor': [{'enable': True, 'python_class': 'non.existent.Extractor'}]}}
        with self.assertRaises(ExtractorNotFoundException):
            chain = ExtractSimpleFactory.create(invalid_config)
            chain.extract(
                DataJson(
                    {
                        'track_id': '214c1bec-0bc2-4627-a229-24dbfb4adb9b',
                        'dataset_name': 'test_cli_sdk',
                        'url': 'https://www.test.com',
                        'data_source_category': 'HTML',
                        'html': '<html><body><h1>Test</h1><p>This is a test content.</p></body></html>',
                        'file_bytes': 1000,
                        'meta_info': {'input_datetime': '2020-01-01 00:00:00'},
                    }
                )
            )

        # Test missing required fields
        with self.assertRaises(ExtractorChainInputException):
            chain.extract(DataJson({'data_source_category': 'html'}))
