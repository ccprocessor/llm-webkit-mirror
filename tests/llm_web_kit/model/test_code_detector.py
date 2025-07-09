import logging
import warnings
from unittest import TestCase
from unittest.mock import MagicMock, patch

from llm_web_kit.exception.exception import ModelResourceException
from llm_web_kit.model.code_detector import (CodeClassification,
                                             get_singleton_code_detect,
                                             update_code_prob_by_str)

# Suppress external dependency warnings for clean pytest runs
warnings.filterwarnings('ignore', category=DeprecationWarning, module='jieba')
warnings.filterwarnings('ignore', category=DeprecationWarning, module='pkg_resources')
warnings.filterwarnings('ignore', category=DeprecationWarning, module='jupyter_client')


class TestEnvironment:
    """Manages test environment and determines if real model downloads are
    available."""

    _real_model_available = None

    @classmethod
    def can_download_real_model(cls) -> bool:
        """Check if real model download is possible."""
        if cls._real_model_available is not None:
            return cls._real_model_available

        try:
            CodeClassification()
            cls._real_model_available = True
            return True
        except (ModelResourceException, ConnectionError, TimeoutError, OSError, Exception) as e:
            logging.info(f'Real model download failed, using mocked tests: {e}')
            cls._real_model_available = False
            return False

    @classmethod
    def reset(cls):
        """Reset environment detection for testing."""
        cls._real_model_available = None


class BaseTestCase(TestCase):
    """Base test case with common functionality."""

    def assert_prediction_format(self, result):
        """Assert that prediction result has correct format."""
        self.assertIsInstance(result, dict)
        self.assertIn('has_code_prob_0409', result)
        self.assertIsInstance(result['has_code_prob_0409'], (int, float))
        self.assertGreaterEqual(result['has_code_prob_0409'], 0.0)
        self.assertLessEqual(result['has_code_prob_0409'], 1.0)

    def get_test_samples(self):
        """Get test samples for code detection."""
        return {
            'code': ['import pandas as pd', 'def hello():\n    pass', 'SELECT * FROM users'],
            'non_code': ['这是普通文本', 'Regular English text', 'Lorem ipsum'],
            'edge': ['', '   \t\n\r   ', '!@#$%', 'a' * 1000]
        }

    def setup_mock_classifier(self, mock_auto_download, mock_load_model):
        """Setup a mocked classifier with standard configuration."""
        mock_auto_download.return_value = '/fake/model/path'
        classifier = CodeClassification()
        return classifier


class TestCodeClassificationIntegration(BaseTestCase):
    """Integration tests using real model downloads when available."""

    @classmethod
    def setUpClass(cls):
        """Set up class-level resources."""
        cls.use_real_model = TestEnvironment.can_download_real_model()
        if not cls.use_real_model:
            logging.info('Real model unavailable, skipping integration tests')

    def setUp(self):
        """Set up test fixtures."""
        if not self.use_real_model:
            self.skipTest('Real model not available')

    def test_real_model_functionality(self):
        """Test real model initialization and basic functionality."""
        classifier = CodeClassification()
        self.assertIsNotNone(classifier.model)
        self.assertEqual(classifier.version, 'v4_0409')

        # Test with code and non-code samples
        samples = self.get_test_samples()

        # Test code detection
        for code_sample in samples['code']:
            result = classifier.predict(code_sample)
            self.assert_prediction_format(result)

        # Test non-code detection
        for non_code_sample in samples['non_code']:
            result = classifier.predict(non_code_sample)
            self.assert_prediction_format(result)

        # Test edge cases
        for edge_case in samples['edge']:
            result = classifier.predict(edge_case)
            self.assert_prediction_format(result)

    def test_real_model_singleton(self):
        """Test singleton behavior with real model."""
        instance1 = get_singleton_code_detect()
        instance2 = get_singleton_code_detect()
        self.assertIs(instance1, instance2)

        result1 = instance1.predict('import pandas as pd')
        result2 = instance2.predict('import pandas as pd')
        self.assertEqual(result1, result2)


class TestCodeClassificationMocked(BaseTestCase):
    """Mocked tests that always run regardless of model availability."""

    @patch('llm_web_kit.model.code_detector.fasttext.load_model')
    @patch('llm_web_kit.model.code_detector.CodeClassification.auto_download')
    def test_initialization(self, mock_auto_download, mock_load_model):
        """Test initialization with both default and custom paths."""
        # Test default path
        mock_auto_download.return_value = '/fake/model/path'
        CodeClassification()
        mock_auto_download.assert_called_once_with(None)
        mock_load_model.assert_called_with('/fake/model/path')

        # Test custom path
        mock_load_model.reset_mock()
        CodeClassification('custom_model_path')
        mock_load_model.assert_called_with('custom_model_path')

    @patch('llm_web_kit.model.code_detector.fasttext.load_model')
    @patch('llm_web_kit.model.code_detector.CodeClassification.auto_download')
    @patch('llm_web_kit.model.code_detector.jieba.lcut')
    def test_jieba_cut_functionality(self, mock_jieba_lcut, mock_auto_download, mock_load_model):
        """Test jieba_cut text preprocessing functionality."""
        classifier = self.setup_mock_classifier(mock_auto_download, mock_load_model)

        # Test basic functionality
        mock_jieba_lcut.return_value = ['这是', '一个', '测试', '文本']
        result = classifier.jieba_cut('这是一个测试文本')
        self.assertIsInstance(result, str)
        self.assertIn('这是', result)
        self.assertIn('测试', result)

        # Test stop words removal
        mock_jieba_lcut.return_value = ['这是', '\r', '一个', '\n', '测试', ' ', '文本', '']
        result = classifier.jieba_cut('这是\r一个\n测试 文本')
        self.assertNotIn('\r', result)
        self.assertNotIn('\n', result)
        self.assertIn('这是', result)

        # Test truncation
        long_word_list = ['word'] * (CodeClassification.MAX_WORD_NUM + 100)
        mock_jieba_lcut.return_value = long_word_list
        result = classifier.jieba_cut('very long text')
        word_count = len(result.split())
        self.assertLessEqual(word_count, CodeClassification.MAX_WORD_NUM)

        # Test special character removal
        mock_jieba_lcut.return_value = ['测试', '文本', '!', '?', ',']
        result = classifier.jieba_cut('测试文本!?,')
        self.assertNotIn('!', result)
        self.assertNotIn('?', result)

        # Test edge cases
        mock_jieba_lcut.return_value = []
        result = classifier.jieba_cut('')
        self.assertEqual(result, '')

    @patch('llm_web_kit.model.code_detector.fasttext.load_model')
    @patch('llm_web_kit.model.code_detector.CodeClassification.auto_download')
    def test_predict_functionality(self, mock_auto_download, mock_load_model):
        """Test predict method with various scenarios."""
        classifier = self.setup_mock_classifier(mock_auto_download, mock_load_model)

        # Test code label (1)
        classifier.model.predict.return_value = (['__label__1'], [0.8])
        result = classifier.predict('import pandas as pd')
        self.assert_prediction_format(result)
        self.assertEqual(result['has_code_prob_0409'], 0.8)

        # Test non-code label (0)
        classifier.model.predict.return_value = (['__label__0'], [0.7])
        result = classifier.predict('这是普通文本')
        self.assert_prediction_format(result)
        self.assertAlmostEqual(result['has_code_prob_0409'], 0.3, places=5)  # 1 - 0.7

        # Test confidence capping
        classifier.model.predict.return_value = (['__label__1'], [1.5])
        result = classifier.predict('test')
        self.assertEqual(result['has_code_prob_0409'], 1.0)

        # Test empty predictions
        classifier.model.predict.return_value = ([], [])
        result = classifier.predict('test')
        self.assertEqual(result['has_code_prob_0409'], 0.0)

        # Test version property
        self.assertEqual(classifier.version, 'v4_0409')


class TestErrorHandlingAndUtilities(BaseTestCase):
    """Test cases for error handling and utility functions."""

    @patch('llm_web_kit.model.code_detector.CodeClassification.auto_download')
    @patch('llm_web_kit.model.code_detector.fasttext.load_model')
    def test_download_failure_scenarios(self, mock_load_model, mock_auto_download):
        """Test various download failure scenarios."""
        # Test network failure
        mock_auto_download.side_effect = ConnectionError('Network unreachable')
        with self.assertRaises(ConnectionError):
            CodeClassification()

        # Test model resource exception
        mock_auto_download.side_effect = ModelResourceException('Model download failed')
        with self.assertRaises(ModelResourceException):
            CodeClassification()

        # Test timeout
        mock_auto_download.side_effect = TimeoutError('Download timeout')
        with self.assertRaises(TimeoutError):
            CodeClassification()

        # Test file not found
        mock_auto_download.side_effect = None
        mock_auto_download.return_value = '/nonexistent/path'
        mock_load_model.side_effect = OSError('File not found')
        with self.assertRaises(OSError):
            CodeClassification()

    def test_environment_detection_caching(self):
        """Test that environment detection results are cached properly."""
        TestEnvironment.reset()
        result1 = TestEnvironment.can_download_real_model()
        result2 = TestEnvironment.can_download_real_model()
        self.assertEqual(result1, result2)

        TestEnvironment.reset()
        result3 = TestEnvironment.can_download_real_model()
        self.assertEqual(result1, result3)

    @patch('llm_web_kit.model.code_detector.singleton_resource_manager')
    @patch('llm_web_kit.model.code_detector.CodeClassification')
    def test_singleton_functionality(self, mock_code_classification, mock_singleton_manager):
        """Test singleton pattern functionality."""
        # Test new instance creation
        mock_singleton_manager.has_name.return_value = False
        mock_instance = MagicMock()
        mock_code_classification.return_value = mock_instance
        mock_singleton_manager.get_resource.return_value = mock_instance

        result = get_singleton_code_detect()
        mock_singleton_manager.set_resource.assert_called_once_with('code_detect_v4_0409', mock_instance)
        self.assertIsNotNone(result)

        # Test existing instance
        mock_singleton_manager.reset_mock()
        mock_singleton_manager.has_name.return_value = True
        mock_singleton_manager.get_resource.return_value = mock_instance

        result = get_singleton_code_detect()
        mock_singleton_manager.set_resource.assert_not_called()
        self.assertEqual(result, mock_instance)

    @patch('llm_web_kit.model.code_detector.get_singleton_code_detect')
    def test_update_code_prob_by_str(self, mock_get_singleton):
        """Test update_code_prob_by_str function."""
        mock_classifier = MagicMock()
        mock_classifier.predict.return_value = {'has_code_prob_0409': 0.75}
        mock_get_singleton.return_value = mock_classifier

        result = update_code_prob_by_str('import pandas as pd')
        self.assertEqual(result, {'has_code_prob_0409': 0.75})
        mock_classifier.predict.assert_called_once_with('import pandas as pd')
