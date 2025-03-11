import unittest
from pathlib import Path
from unittest.mock import patch

from llm_web_kit.exception.exception import (CleanModelException,
                                             EbookFileExtractorException,
                                             ErrorMsg, ExtractorBaseException,
                                             ExtractorChainBaseException,
                                             ExtractorChainConfigException,
                                             ExtractorChainInputException,
                                             ExtractorInitException,
                                             ExtractorNotFoundException,
                                             HtmlAudioRecognizerException,
                                             HtmlCodeRecognizerException,
                                             HtmlExtractorException,
                                             HtmlFileExtractorException,
                                             HtmlImageRecognizerException,
                                             HtmlListRecognizerException,
                                             HtmlMathRecognizerException,
                                             HtmlPostExtractorException,
                                             HtmlPreExtractorException,
                                             HtmlRecognizerException,
                                             HtmlTableRecognizerException,
                                             HtmlTextRecognizerException,
                                             HtmlTitleRecognizerException,
                                             HtmlVideoRecognizerException,
                                             LlmWebKitBaseException,
                                             MagicHtmlExtractorException,
                                             ModelBaseException,
                                             ModelInitException,
                                             ModelInputException,
                                             ModelOutputException,
                                             ModelResourceException,
                                             OtherFileExtractorException,
                                             PdfFileExtractorException,
                                             SafeModelException)


class TestException(unittest.TestCase):
    """Test exception system."""

    def test_error_message_retrieval(self):
        """Test getting error messages from error codes."""
        test_cases = {
            10000000: 'LlmWebKit base exception',
            20000000: 'ExtractorChain base exception',
            21000000: 'ExtractorChain initialization exception',
            22000000: 'ExtractorChain configuration exception',
            23000000: 'ExtractorChain input exception',
            24000000: 'Extractor not found exception',
            31000000: 'HTML file extractor exception',
            31020000: 'HTML pre-extractor exception',
            31030000: 'HTML extractor exception',
            31031100: 'HTML math recognizer exception',
            31031200: 'HTML code recognizer exception',
            99999999: 'unknown error code 99999999',
        }

        for code, expected_message in test_cases.items():
            with self.subTest(code=code):
                self.assertEqual(ErrorMsg.get_error_message(code), expected_message)

    def test_error_code_retrieval(self):
        """Test getting error codes from module and error names."""
        test_cases = [
            ('ExtractorChain', 'ExtractorChainInitException', 21000000),
            ('Extractor', 'PdfFileExtractorException', 32000000),
            ('HtmlRecognizer', 'HtmlMathRecognizerException', 31031100),
        ]

        for module, error_name, expected_code in test_cases:
            with self.subTest(module=module, error_name=error_name):
                self.assertEqual(ErrorMsg.get_error_code(module, error_name), expected_code)

    def test_invalid_error_code_retrieval(self):
        """Test getting error code with invalid module/error name."""
        with self.assertRaises(ValueError):
            ErrorMsg.get_error_code('InvalidModule', 'InvalidException')

    def test_base_exceptions(self):
        """Test base exception classes."""
        # Test LlmWebKitBaseException
        base_exc = LlmWebKitBaseException()
        self.assertIsNotNone(base_exc.error_code)
        self.assertIsNotNone(base_exc.message)

        # Test with custom error code
        custom_exc = LlmWebKitBaseException(error_code=99999999)
        self.assertEqual(custom_exc.error_code, 99999999)
        self.assertEqual(custom_exc.message, 'unknown error code 99999999')

        # Test ExtractorChainBaseException
        chain_exc = ExtractorChainBaseException()
        self.assertEqual(chain_exc.error_code, 20000000)

        # Test with custom error code
        custom_chain_exc = ExtractorChainBaseException(error_code=99999999)
        self.assertEqual(custom_chain_exc.error_code, 99999999)

        # Test default error code
        extractor_base = ExtractorBaseException()
        self.assertEqual(extractor_base.error_code, 30000000)

        # Test with custom error code
        custom_extractor_base = ExtractorBaseException(error_code=99999999)
        self.assertEqual(custom_extractor_base.error_code, 99999999)

        # Test with custom message
        extractor_base_with_msg = ExtractorBaseException(custom_message='Base error')
        self.assertEqual(extractor_base_with_msg.error_code, 30000000)
        self.assertEqual(extractor_base_with_msg.custom_message, 'Base error')

    def test_concrete_exceptions(self):
        """Test concrete exception instances."""
        test_cases = [
            (ExtractorInitException('Test message'), 21000000),
            (ExtractorChainInputException('Invalid input'), 23000000),
            (ExtractorChainConfigException('Config error'), 22000000),
            (ExtractorNotFoundException('Not found'), 24000000),
            (HtmlPreExtractorException('Pre-process error'), 31020000),
            (HtmlMathRecognizerException('Math parse error'), 31031100),
        ]

        for exc, expected_code in test_cases:
            with self.subTest(exception_type=type(exc).__name__):
                self.assertEqual(exc.error_code, expected_code)
                self.assertIsNotNone(exc.message)
                self.assertIsNotNone(exc.custom_message)

    def test_exception_str_format(self):
        """Test string representation of exceptions."""
        exc = ExtractorInitException('Custom message')
        str_repr = str(exc)

        # Check string format
        self.assertRegex(str_repr, r'.+\.py: \d+#\d+#.+#.+')
        self.assertIn(str(exc.error_code), str_repr)
        self.assertIn(exc.message, str_repr)
        self.assertIn(exc.custom_message, str_repr)

    def test_html_recognizer_exceptions(self):
        """Test all HTML recognizer exceptions."""
        test_cases = [
            (HtmlRecognizerException(), 31031000),
            (HtmlMathRecognizerException('Math error'), 31031100),
            (HtmlCodeRecognizerException('Code error'), 31031200),
            (HtmlTableRecognizerException('Table error'), 31031300),
            (HtmlImageRecognizerException('Image error'), 31031400),
            (HtmlListRecognizerException('List error'), 31031500),
            (HtmlAudioRecognizerException('Audio error'), 31031600),
            (HtmlVideoRecognizerException('Video error'), 31031700),
            (HtmlTitleRecognizerException('Title error'), 31031800),
            (HtmlTextRecognizerException('Text error'), 31031900),
        ]

        for exc, expected_code in test_cases:
            with self.subTest(exception_type=type(exc).__name__):
                self.assertEqual(exc.error_code, expected_code)
                self.assertIsNotNone(exc.message)

    def test_file_extractor_exceptions(self):
        """Test file extractor exceptions."""
        test_cases = [
            (HtmlFileExtractorException(), 31000000),
            (PdfFileExtractorException(), 32000000),
            (EbookFileExtractorException(), 33000000),
            (OtherFileExtractorException(), 34000000),
            (MagicHtmlExtractorException(), 31010000),
            (HtmlPreExtractorException(), 31020000),
            (HtmlExtractorException(), 31030000),
            (HtmlPostExtractorException(), 31040000),
        ]

        for exc, expected_code in test_cases:
            with self.subTest(exception_type=type(exc).__name__):
                self.assertEqual(exc.error_code, expected_code)
                self.assertIsNotNone(exc.message)

    def test_clean_module_exceptions(self):
        """Test clean module exceptions."""
        test_cases = [
            (ModelBaseException(), 40000000),
            (ModelResourceException(), 41000000),
            (ModelInitException(), 42000000),
            (ModelInputException(), 43000000),
            (ModelOutputException(), 44000000),
            (SafeModelException(), 45000000),
            (CleanModelException(), 46000000),
        ]

        for exc, expected_code in test_cases:
            with self.subTest(exception_type=type(exc).__name__):
                self.assertEqual(exc.error_code, expected_code)
                self.assertIsNotNone(exc.message)

    def test_error_code_uniqueness(self):
        """Test that all error codes in the JSON file are unique."""
        error_codes = set()
        json_path = Path(__file__).parent.parent.parent.parent / 'llm_web_kit/exception/exception.jsonc'

        with open(json_path, 'r', encoding='utf-8') as f:
            import commentjson as json

            data = json.load(f)

            for module in data.values():
                for error_info in module.values():
                    code = error_info['code']
                    self.assertNotIn(code, error_codes, f'Duplicate error code found: {code}')
                    error_codes.add(code)

    def test_exception_dataset_name(self):
        """Test dataset_name handling in exceptions."""
        # Test base exception initialization with empty dataset_name
        base_exc = LlmWebKitBaseException('test message')
        self.assertEqual(base_exc.dataset_name, '')

        # Test custom dataset_name assignment
        base_exc.dataset_name = 'test_dataset'
        self.assertEqual(base_exc.dataset_name, 'test_dataset')

        # Test dataset_name in child exceptions
        chain_exc = ExtractorChainBaseException('chain error')
        self.assertEqual(chain_exc.dataset_name, '')
        chain_exc.dataset_name = 'chain_dataset'
        self.assertEqual(chain_exc.dataset_name, 'chain_dataset')

        # Test dataset_name in concrete exceptions
        test_cases = [
            (ExtractorInitException('init error'), 'init_dataset'),
            (ExtractorChainInputException('input error'), 'input_dataset'),
            (ExtractorChainConfigException('config error'), 'config_dataset'),
            (ExtractorNotFoundException('not found error'), 'notfound_dataset'),
        ]

        for exc, dataset_name in test_cases:
            with self.subTest(exception_type=type(exc).__name__):
                self.assertEqual(exc.dataset_name, '')
                exc.dataset_name = dataset_name
                self.assertEqual(exc.dataset_name, dataset_name)

        # Test exception handling when DataJson has no dataset_name
        from llm_web_kit.extractor.extractor_chain import ExtractSimpleFactory
        from llm_web_kit.input.datajson import DataJson

        config = {
            'extractor_pipe': {
                'pre_extractor': [
                    {
                        'enable': True,
                        'python_class': 'llm_web_kit.extractor.html.pre_extractor.HTMLFileFormatFilterPreExtractor',
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
            }
        }
        chain = ExtractSimpleFactory.create(config)

        input_data = DataJson(
            {
                'dataset_name': 'test_dataset',
            }
        )

        with self.assertRaises(ExtractorChainBaseException) as context:
            chain.extract(input_data)
        self.assertEqual(context.exception.dataset_name, 'test_dataset')

    @patch('llm_web_kit.libs.class_loader.load_python_class_by_name')
    def test_extractor_chain_exceptions(self, mock_load_class):
        """测试 ExtractorChain 中的异常处理机制."""
        from llm_web_kit.extractor.extractor_chain import ExtractSimpleFactory
        from llm_web_kit.input.datajson import DataJson

        # 定义简单的 Mock 类，每个类负责抛出一种异常
        class KeyErrorExtractor:
            def __init__(self, config, **kwargs):
                pass

            def extract(self, data):
                raise KeyError('test_key')

        class BaseExceptionExtractor:
            def __init__(self, config, **kwargs):
                pass

            def extract(self, data):
                raise LlmWebKitBaseException('Base exception')

        class ChainExceptionExtractor:
            def __init__(self, config, **kwargs):
                pass

            def extract(self, data):
                raise ExtractorChainBaseException('Chain exception')

        class GeneralExceptionExtractor:
            def __init__(self, config, **kwargs):
                pass

            def extract(self, data):
                raise ValueError('General exception')

        mock_load_class.return_value = KeyErrorExtractor(None)

        # 基础配置
        config = {
            'extractor_pipe': {
                'pre_extractor': [
                    {
                        'enable': True,
                        'python_class': 'llm_web_kit.extractor.html.pre_extractor.HTMLFileFormatFilterPreExtractor',
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
            }
        }

        # 测试数据
        data = DataJson({'dataset_name': 'test_dataset'})

        # 测试场景 1: KeyError -> ExtractorChainInputException
        chain = ExtractSimpleFactory.create(config)
        with self.assertRaises(ExtractorChainInputException) as context:
            chain.extract(data)
        self.assertEqual(context.exception.dataset_name, 'test_dataset')
        self.assertIn('Required field missing', str(context.exception))

        # 测试场景 2: LlmWebKitBaseException 传递
        mock_load_class.return_value = BaseExceptionExtractor(None)
        chain = ExtractSimpleFactory.create(config)
        with self.assertRaises(LlmWebKitBaseException) as context:
            chain.extract(data)
        self.assertEqual(context.exception.dataset_name, 'test_dataset')

        # 测试场景 3: ExtractorChainBaseException 传递
        mock_load_class.return_value = ChainExceptionExtractor(None)
        chain = ExtractSimpleFactory.create(config)
        with self.assertRaises(ExtractorChainBaseException) as context:
            chain.extract(data)
        self.assertEqual(context.exception.dataset_name, 'test_dataset')
