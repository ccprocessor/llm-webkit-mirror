import json
import os
import unittest
from unittest.mock import MagicMock, patch

from llm_web_kit.exception.exception import (ExtractorChainBaseException,
                                             ExtractorChainConfigException,
                                             ExtractorChainInputException,
                                             ExtractorInitException,
                                             ExtractorNotFoundException,
                                             LlmWebKitBaseException)
from llm_web_kit.extractor.extractor_chain import (ExtractorChain,
                                                   ExtractSimpleFactory)
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
            chain.extract(DataJson({
                'dataset_name': 'test_dataset',  # 添加 dataset_name
                'data_source_category': 'html',
                'html': '<h1>Test</h1>'
            }))

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
            chain.extract(DataJson({'data_source_category': 'html', 'dataset_name': 'test_dataset'}))

    def test_empty_config(self):
        """测试空配置和禁用提取器."""
        # 测试完全空的配置
        chain = ExtractorChain({})
        self.assertEqual(len(chain._ExtractorChain__pre_extractors), 0)
        self.assertEqual(len(chain._ExtractorChain__extractors), 0)
        self.assertEqual(len(chain._ExtractorChain__post_extractors), 0)

        # 测试只有 extractor_pipe 但没有具体配置的情况
        chain = ExtractorChain({'extractor_pipe': {}})
        self.assertEqual(len(chain._ExtractorChain__pre_extractors), 0)
        self.assertEqual(len(chain._ExtractorChain__extractors), 0)
        self.assertEqual(len(chain._ExtractorChain__post_extractors), 0)

        # 测试禁用的提取器
        config = {
            'extractor_pipe': {
                'pre_extractor': [
                    {
                        'enable': False,
                        'python_class': 'llm_web_kit.extractor.html.pre_extractor.HTMLFileFormatFilterPreExtractor',
                        'class_init_kwargs': {},
                    }
                ],
                'extractor': [
                    {
                        'enable': False,
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
                ]
            }
        }
        chain = ExtractorChain(config)
        self.assertEqual(len(chain._ExtractorChain__pre_extractors), 0)
        self.assertEqual(len(chain._ExtractorChain__extractors), 0)
        self.assertEqual(len(chain._ExtractorChain__post_extractors), 0)

    def test_config_errors(self):
        """测试配置错误."""
        # 测试缺少 python_class 的情况
        config = {
            'extractor_pipe': {
                'extractor': [
                    {
                        'enable': True,
                        # 缺少 python_class
                        'class_init_kwargs': {},
                    }
                ]
            }
        }
        with self.assertRaises(ExtractorChainConfigException) as context:
            ExtractorChain(config)
        self.assertIn('python_class not specified', str(context.exception))

    @patch('llm_web_kit.libs.class_loader.load_python_class_by_name')
    def test_extractor_initialization_errors(self, mock_load):
        """测试提取器初始化错误."""
        # 测试导入错误
        mock_load.side_effect = ImportError('Module not found')

        config = {
            'extractor_pipe': {
                'extractor': [
                    {
                        'enable': True,
                        'python_class': 'llm_web_kit.extractor.html.extractor.NonExistentExtractor',
                        'class_init_kwargs': {},
                    }
                ]
            }
        }

        with self.assertRaises(ExtractorChainBaseException) as context:
            ExtractorChain(config)
        self.assertIn('Failed to initialize extractor', str(context.exception))

        # 重置 mock 并设置新的 side_effect
        mock_load.reset_mock()
        mock_load.side_effect = ValueError('Invalid configuration')

        with self.assertRaises(ExtractorInitException) as context:
            ExtractorChain(config)
        self.assertIn('Failed to initialize extractor', str(context.exception))

    @patch('llm_web_kit.libs.class_loader.load_python_class_by_name')
    def test_exception_handling_with_dataset_name(self, mock_load):
        """测试异常处理中的 dataset_name 设置."""
        # 创建一个会抛出 KeyError 的 Mock 提取器
        mock_extractor = MagicMock()
        mock_extractor.extract.side_effect = KeyError('required_field')

        # 直接设置 mock 返回值
        mock_load.return_value = mock_extractor

        config = {
            'extractor_pipe': {
                'extractor': [
                    {
                        'enable': True,
                        'python_class': 'llm_web_kit.extractor.html.extractor.HTMLFileFormatExtractor',
                        'class_init_kwargs': {},
                    }
                ]
            }
        }

        chain = ExtractorChain(config)

        # 测试有 dataset_name 的情况
        data = DataJson({'dataset_name': 'test_dataset'})
        with self.assertRaises(ExtractorChainInputException) as context:
            chain.extract(data)
        self.assertEqual(context.exception.dataset_name, 'test_dataset')
        self.assertIn('Required field missing', str(context.exception))

    def test_exception_propagation(self):
        """测试不同类型异常的传播."""
        # 创建一个会抛出 LlmWebKitBaseException 的 Mock 提取器
        mock_base_error = MagicMock()
        base_exception = LlmWebKitBaseException('Base error')
        mock_base_error.extract.side_effect = base_exception

        # 创建一个会抛出 ExtractorChainBaseException 的 Mock 提取器
        mock_chain_error = MagicMock()
        chain_exception = ExtractorChainBaseException('Chain error')
        mock_chain_error.extract.side_effect = chain_exception

        # 创建一个会抛出一般异常的 Mock 提取器
        mock_general_error = MagicMock()
        mock_general_error.extract.side_effect = ValueError('General error')

        # 创建一个测试用的 ExtractorChain 子类
        class TestExtractorChain(ExtractorChain):
            """用于测试的 ExtractorChain 子类，使用类变量存储 mock 对象."""
            current_mock = None

            def __init__(self, config, mock_extractor):
                # 先设置类变量
                TestExtractorChain.current_mock = mock_extractor
                super().__init__(config)

            def _ExtractorChain__create_extractor(self, config):
                return self.current_mock

        config = {
            'extractor_pipe': {
                'extractor': [
                    {
                        'enable': True,
                        'python_class': 'llm_web_kit.extractor.html.extractor.HTMLFileFormatExtractor',
                        'class_init_kwargs': {},
                    }
                ]
            }
        }

        # 创建包含所有必要字段的 DataJson 对象
        data = DataJson({
            'dataset_name': 'test_dataset',
            'data_source_category': 'html',
            'html': '<h1>Test</h1>',
            'url': 'https://example.com'
        })

        # 测试 LlmWebKitBaseException 传播
        chain = TestExtractorChain(config, mock_base_error)
        with self.assertRaises(LlmWebKitBaseException) as context:
            chain.extract(data)
        self.assertEqual(context.exception.dataset_name, 'test_dataset')
        self.assertIsInstance(context.exception, LlmWebKitBaseException)
        self.assertIn('Base error', str(context.exception))

        # 测试 ExtractorChainBaseException 传播
        chain = TestExtractorChain(config, mock_chain_error)
        with self.assertRaises(ExtractorChainBaseException) as context:
            chain.extract(data)
        self.assertEqual(context.exception.dataset_name, 'test_dataset')
        self.assertIsInstance(context.exception, ExtractorChainBaseException)
        self.assertIn('Chain error', str(context.exception))

        # 测试一般异常包装为 ExtractorChainBaseException
        chain = TestExtractorChain(config, mock_general_error)
        with self.assertRaises(ExtractorChainBaseException) as context:
            chain.extract(data)
        self.assertEqual(context.exception.dataset_name, 'test_dataset')
        self.assertIn('Error during extraction', str(context.exception))
        self.assertIsInstance(context.exception.__cause__, ValueError)

    def test_factory_method(self):
        """测试工厂方法."""
        # 测试 ExtractSimpleFactory.create 方法
        config = self.html_config
        chain = ExtractSimpleFactory.create(config)
        self.assertIsInstance(chain, ExtractorChain)

        # 测试空配置
        chain = ExtractSimpleFactory.create({})
        self.assertIsInstance(chain, ExtractorChain)
        self.assertEqual(len(chain._ExtractorChain__pre_extractors), 0)
        self.assertEqual(len(chain._ExtractorChain__extractors), 0)
        self.assertEqual(len(chain._ExtractorChain__post_extractors), 0)

    @patch('llm_web_kit.libs.class_loader.load_python_class_by_name')
    def test_post_extractor_exceptions(self, mock_load):
        """测试后处理阶段的异常处理."""
        # 创建一个正常的提取器
        mock_extractor = MagicMock()
        mock_extractor.extract = lambda data: data

        # 创建会抛出 KeyError 的后处理器
        mock_key_error_post = MagicMock()
        mock_key_error_post.post_extract.side_effect = KeyError('post_required_field')

        # 创建会抛出 ExtractorChainBaseException 的后处理器
        mock_chain_error_post = MagicMock()
        chain_exception = ExtractorChainBaseException('Post chain error')
        mock_chain_error_post.post_extract.side_effect = chain_exception

        # 创建会抛出 LlmWebKitBaseException 的后处理器
        mock_base_error_post = MagicMock()
        base_exception = LlmWebKitBaseException('Post base error')
        mock_base_error_post.post_extract.side_effect = base_exception

        # 创建会抛出一般异常的后处理器
        mock_general_error_post = MagicMock()
        mock_general_error_post.post_extract.side_effect = ValueError('Post general error')
