"""Test cases for math_detector.py."""

import unittest
from unittest import TestCase
from unittest.mock import MagicMock, patch

import torch


class TestE5ScoreModel(TestCase):
    """Test cases for E5ScoreModel."""

    @patch('llm_web_kit.model.math_detector.import_transformer')
    @patch('llm_web_kit.model.math_detector.torch.cuda.is_available')
    @patch('llm_web_kit.model.math_detector.E5ScoreModel.auto_download')
    def test_init_default_config(self, mock_auto_download, mock_cuda_available, mock_import_transformer):
        """Test initialization with default configuration."""
        from llm_web_kit.model.math_detector import E5ScoreModel

        # Setup mocks
        mock_auto_download.return_value = None
        mock_cuda_available.return_value = False

        mock_transformers = MagicMock()
        mock_model = MagicMock()
        mock_tokenizer = MagicMock()

        mock_transformers.AutoModelForSequenceClassification.from_pretrained.return_value = mock_model
        mock_transformers.AutoTokenizer.from_pretrained.return_value = mock_tokenizer
        mock_import_transformer.return_value = mock_transformers

        # Test initialization
        model = E5ScoreModel()

        # Verify default configuration
        assert model.model_name == 'HuggingFaceTB/finemath-classifier'
        assert model.max_tokens == 512
        assert model.batch_size == 32
        assert model.device == 'cpu'
        assert not model.use_flash_attn

        # Verify model and tokenizer loading
        mock_transformers.AutoModelForSequenceClassification.from_pretrained.assert_called_once()
        mock_transformers.AutoTokenizer.from_pretrained.assert_called_once()

    @patch('llm_web_kit.model.math_detector.import_transformer')
    @patch('llm_web_kit.model.math_detector.torch.cuda.is_available')
    @patch('llm_web_kit.model.math_detector.E5ScoreModel.auto_download')
    def test_init_custom_config(self, mock_auto_download, mock_cuda_available, mock_import_transformer):
        """Test initialization with custom configuration."""
        from llm_web_kit.model.math_detector import E5ScoreModel

        # Setup mocks
        mock_auto_download.return_value = None
        mock_cuda_available.return_value = False

        mock_transformers = MagicMock()
        mock_model = MagicMock()
        mock_tokenizer = MagicMock()

        mock_transformers.AutoModelForSequenceClassification.from_pretrained.return_value = mock_model
        mock_transformers.AutoTokenizer.from_pretrained.return_value = mock_tokenizer
        mock_import_transformer.return_value = mock_transformers

        # Custom configuration
        custom_config = {
            'model_name': 'custom/model',
            'max_tokens': 256,
            'batch_size': 16,
            'device': 'cpu'
        }

        # Test initialization
        model = E5ScoreModel(config=custom_config)

        # Verify custom configuration
        assert model.model_name == 'custom/model'
        assert model.max_tokens == 256
        assert model.batch_size == 16
        assert model.device == 'cpu'

    @patch('llm_web_kit.model.math_detector.import_transformer')
    @patch('llm_web_kit.model.math_detector.torch.cuda.is_available')
    @patch('llm_web_kit.model.math_detector.E5ScoreModel.auto_download')
    def test_init_gpu_with_accelerate(self, mock_auto_download, mock_cuda_available, mock_import_transformer):
        """Test initialization with GPU and accelerate available."""
        from llm_web_kit.model.math_detector import E5ScoreModel

        # Setup mocks
        mock_auto_download.return_value = None
        mock_cuda_available.return_value = True

        mock_transformers = MagicMock()
        mock_model = MagicMock()
        mock_tokenizer = MagicMock()

        mock_transformers.AutoModelForSequenceClassification.from_pretrained.return_value = mock_model
        mock_transformers.AutoTokenizer.from_pretrained.return_value = mock_tokenizer
        mock_import_transformer.return_value = mock_transformers

        # Test initialization with GPU config
        config = {'device': 'cuda'}
        model = E5ScoreModel(config=config)

        # Verify GPU configuration
        assert model.device == 'cuda'

        # Verify model loading with GPU parameters
        call_args = mock_transformers.AutoModelForSequenceClassification.from_pretrained.call_args
        assert call_args[1]['trust_remote_code'] is True
        assert 'torch_dtype' in call_args[1]
        assert 'device_map' in call_args[1]

    @patch('llm_web_kit.model.math_detector.import_transformer')
    @patch('llm_web_kit.model.math_detector.torch.cuda.is_available')
    @patch('llm_web_kit.model.math_detector.E5ScoreModel.auto_download')
    def test_init_gpu_fallback_to_cpu(self, mock_auto_download, mock_cuda_available, mock_import_transformer):
        """Test GPU initialization falling back to CPU when accelerate
        unavailable."""
        from llm_web_kit.model.math_detector import E5ScoreModel

        # Setup mocks
        mock_auto_download.return_value = None
        mock_cuda_available.return_value = True

        mock_transformers = MagicMock()
        mock_model = MagicMock()
        mock_tokenizer = MagicMock()

        # First call (with GPU params) raises ImportError, second call (CPU) succeeds
        mock_transformers.AutoModelForSequenceClassification.from_pretrained.side_effect = [
            ImportError('accelerate not available'),
            mock_model
        ]
        mock_transformers.AutoTokenizer.from_pretrained.return_value = mock_tokenizer
        mock_import_transformer.return_value = mock_transformers

        # Test initialization with GPU config
        config = {'device': 'cuda'}
        model = E5ScoreModel(config=config)

        # Verify fallback to CPU
        assert model.device == 'cpu'

        # Verify model loading was attempted twice (GPU then CPU)
        assert mock_transformers.AutoModelForSequenceClassification.from_pretrained.call_count == 2

    def test_get_output_key(self):
        """Test output key generation with prefix and postfix."""
        from llm_web_kit.model.math_detector import E5ScoreModel

        with patch.object(E5ScoreModel, '__init__', return_value=None):
            model = E5ScoreModel()
            model.output_prefix = ''
            model.output_postfix = ''

            # Test without prefix/postfix
            assert model.get_output_key('score') == 'score'

            # Test with prefix
            model.output_prefix = 'math'
            assert model.get_output_key('score') == 'math_score'

            # Test with postfix
            model.output_prefix = ''
            model.output_postfix = 'v2'
            assert model.get_output_key('score') == 'score_v2'

            # Test with both prefix and postfix
            model.output_prefix = 'math'
            model.output_postfix = 'v2'
            assert model.get_output_key('score') == 'math_score_v2'

    @patch('llm_web_kit.model.math_detector.load_config')
    def test_auto_download_success(self, mock_load_config):
        """Test successful auto-download of model resources."""
        from llm_web_kit.model.math_detector import E5ScoreModel

        # Setup mock config
        mock_config = {
            'resources': {
                'math_detector_25m7': {
                    'download_path': 's3://test/path.zip',
                    'md5': 'test_md5'
                }
            }
        }
        mock_load_config.return_value = mock_config

        with patch.object(E5ScoreModel, '__init__', return_value=None):
            model = E5ScoreModel()

            with patch('llm_web_kit.model.math_detector.os.path.exists') as mock_exists, \
                 patch('llm_web_kit.model.math_detector.download_auto_file') as mock_download, \
                 patch('llm_web_kit.model.math_detector.unzip_local_file') as mock_unzip:

                # Mock that unzip path doesn't exist, zip path doesn't exist
                mock_exists.side_effect = [False, False]  # unzip_path, zip_path
                mock_download.return_value = '/cache/math_detector_25m7.zip'
                mock_unzip.return_value = '/cache/math_detector_25m7'

                result = model.auto_download()

                assert result == '/cache/math_detector_25m7'
                mock_download.assert_called_once()
                mock_unzip.assert_called_once()

    @patch('llm_web_kit.model.math_detector.load_config')
    def test_auto_download_failure(self, mock_load_config):
        """Test auto-download failure handling."""
        from llm_web_kit.model.math_detector import E5ScoreModel

        # Setup mock to raise exception
        mock_load_config.side_effect = KeyError('math_detector_25m7')

        with patch.object(E5ScoreModel, '__init__', return_value=None):
            model = E5ScoreModel()

            result = model.auto_download()

            assert result is None

    @patch('llm_web_kit.model.math_detector.import_transformer')
    @patch('llm_web_kit.model.math_detector.torch.cuda.is_available')
    @patch('llm_web_kit.model.math_detector.E5ScoreModel.auto_download')
    def test_predict_single_text(self, mock_auto_download, mock_cuda_available, mock_import_transformer):
        """Test prediction with single text input."""
        from llm_web_kit.model.math_detector import E5ScoreModel

        # Setup mocks
        mock_auto_download.return_value = None
        mock_cuda_available.return_value = False

        mock_transformers = MagicMock()
        mock_model = MagicMock()
        mock_tokenizer = MagicMock()

        # Mock tokenizer output
        mock_inputs = {
            'input_ids': torch.tensor([[1, 2, 3]]),
            'attention_mask': torch.tensor([[1, 1, 1]])
        }
        mock_tokenizer.return_value = mock_inputs

        # Mock model output
        mock_outputs = MagicMock()
        mock_logits = torch.tensor([[2.5]])
        mock_outputs.logits = mock_logits
        mock_model.return_value = mock_outputs

        mock_transformers.AutoModelForSequenceClassification.from_pretrained.return_value = mock_model
        mock_transformers.AutoTokenizer.from_pretrained.return_value = mock_tokenizer
        mock_import_transformer.return_value = mock_transformers

        # Test prediction
        model = E5ScoreModel()
        result = model.predict('Test mathematical equation: E = mc²')

        # Verify result format
        assert len(result) == 1
        assert 'text' in result[0]
        assert 'score' in result[0]
        assert 'int_score' in result[0]
        assert result[0]['text'] == 'Test mathematical equation: E = mc²'
        assert isinstance(result[0]['score'], float)
        assert isinstance(result[0]['int_score'], int)
        assert 0 <= result[0]['int_score'] <= 5

    @patch('llm_web_kit.model.math_detector.import_transformer')
    @patch('llm_web_kit.model.math_detector.torch.cuda.is_available')
    @patch('llm_web_kit.model.math_detector.E5ScoreModel.auto_download')
    def test_predict_batch_texts(self, mock_auto_download, mock_cuda_available, mock_import_transformer):
        """Test prediction with batch text inputs."""
        from llm_web_kit.model.math_detector import E5ScoreModel

        # Setup mocks
        mock_auto_download.return_value = None
        mock_cuda_available.return_value = False

        mock_transformers = MagicMock()
        mock_model = MagicMock()
        mock_tokenizer = MagicMock()

        # Mock tokenizer output for batch
        mock_inputs = {
            'input_ids': torch.tensor([[1, 2, 3], [4, 5, 6]]),
            'attention_mask': torch.tensor([[1, 1, 1], [1, 1, 1]])
        }
        mock_tokenizer.return_value = mock_inputs

        # Mock model output for batch
        mock_outputs = MagicMock()
        mock_logits = torch.tensor([[1.5], [4.2]])
        mock_outputs.logits = mock_logits
        mock_model.return_value = mock_outputs

        mock_transformers.AutoModelForSequenceClassification.from_pretrained.return_value = mock_model
        mock_transformers.AutoTokenizer.from_pretrained.return_value = mock_tokenizer
        mock_import_transformer.return_value = mock_transformers

        # Test batch prediction
        model = E5ScoreModel()
        texts = ['Simple text', 'Calculate the derivative of f(x) = x²']
        results = model.predict(texts)

        # Verify results
        assert len(results) == 2

        # Check first result
        assert results[0]['text'] == 'Simple text'
        assert isinstance(results[0]['score'], float)
        assert isinstance(results[0]['int_score'], int)

        # Check second result
        assert results[1]['text'] == 'Calculate the derivative of f(x) = x²'
        assert isinstance(results[1]['score'], float)
        assert isinstance(results[1]['int_score'], int)

        # Verify tokenizer was called with correct parameters
        mock_tokenizer.assert_called_once_with(texts, return_tensors='pt', padding='longest', truncation=True)

    @patch('llm_web_kit.model.math_detector.import_transformer')
    @patch('llm_web_kit.model.math_detector.torch.cuda.is_available')
    @patch('llm_web_kit.model.math_detector.E5ScoreModel.auto_download')
    def test_predict_score_clamping(self, mock_auto_download, mock_cuda_available, mock_import_transformer):
        """Test that scores are properly clamped to 0-5 range."""
        from llm_web_kit.model.math_detector import E5ScoreModel

        # Setup mocks
        mock_auto_download.return_value = None
        mock_cuda_available.return_value = False

        mock_transformers = MagicMock()
        mock_model = MagicMock()
        mock_tokenizer = MagicMock()

        # Mock tokenizer output
        mock_inputs = {
            'input_ids': torch.tensor([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
            'attention_mask': torch.tensor([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
        }
        mock_tokenizer.return_value = mock_inputs

        # Mock model output with extreme values
        mock_outputs = MagicMock()
        mock_logits = torch.tensor([[-2.0], [3.7], [8.5]])  # Below 0, normal, above 5
        mock_outputs.logits = mock_logits
        mock_model.return_value = mock_outputs

        mock_transformers.AutoModelForSequenceClassification.from_pretrained.return_value = mock_model
        mock_transformers.AutoTokenizer.from_pretrained.return_value = mock_tokenizer
        mock_import_transformer.return_value = mock_transformers

        # Test prediction
        model = E5ScoreModel()
        texts = ['text1', 'text2', 'text3']
        results = model.predict(texts)

        # Verify score clamping
        assert len(results) == 3

        # Negative score should be clamped to 0
        assert results[0]['int_score'] == 0

        # Normal score should be rounded normally
        assert results[1]['int_score'] == 4  # round(3.7) = 4

        # High score should be clamped to 5
        assert results[2]['int_score'] == 5

    @patch('llm_web_kit.model.math_detector.import_transformer')
    @patch('llm_web_kit.model.math_detector.torch.cuda.is_available')
    @patch('llm_web_kit.model.math_detector.E5ScoreModel.auto_download')
    def test_predict_cuda_device_handling(self, mock_auto_download, mock_cuda_available, mock_import_transformer):
        """Test CUDA device handling in prediction."""
        from llm_web_kit.model.math_detector import E5ScoreModel

        # Setup mocks for CUDA
        mock_auto_download.return_value = None
        mock_cuda_available.return_value = True

        mock_transformers = MagicMock()
        mock_model = MagicMock()
        mock_tokenizer = MagicMock()

        # Mock tokenizer output
        mock_inputs = {
            'input_ids': torch.tensor([[1, 2, 3]]),
            'attention_mask': torch.tensor([[1, 1, 1]])
        }
        mock_tokenizer.return_value = mock_inputs

        # Mock model output
        mock_outputs = MagicMock()
        mock_logits = torch.tensor([[2.5]])
        mock_outputs.logits = mock_logits
        mock_model.return_value = mock_outputs

        mock_transformers.AutoModelForSequenceClassification.from_pretrained.return_value = mock_model
        mock_transformers.AutoTokenizer.from_pretrained.return_value = mock_tokenizer
        mock_import_transformer.return_value = mock_transformers

        # Test with CUDA device
        config = {'device': 'cuda'}
        model = E5ScoreModel(config=config)

        # Mock the to() method for tensor movement
        for key in mock_inputs:
            mock_inputs[key].to = MagicMock(return_value=mock_inputs[key])

        model.predict('Test text')

        # Verify that tensors were moved to CUDA device
        for key in mock_inputs:
            mock_inputs[key].to.assert_called_with('cuda')

    @patch('llm_web_kit.model.math_detector.import_transformer')
    @patch('llm_web_kit.model.math_detector.torch.cuda.is_available')
    @patch('llm_web_kit.model.math_detector.E5ScoreModel.auto_download')
    def test_predict_empty_input(self, mock_auto_download, mock_cuda_available, mock_import_transformer):
        """Test prediction with empty input."""
        from llm_web_kit.model.math_detector import E5ScoreModel

        # Setup mocks
        mock_auto_download.return_value = None
        mock_cuda_available.return_value = False

        mock_transformers = MagicMock()
        mock_model = MagicMock()
        mock_tokenizer = MagicMock()

        # Mock tokenizer output for empty list
        mock_inputs = {
            'input_ids': torch.tensor([]),
            'attention_mask': torch.tensor([])
        }
        mock_tokenizer.return_value = mock_inputs

        # Mock model output for empty batch
        mock_outputs = MagicMock()
        mock_logits = torch.tensor([])
        mock_outputs.logits = mock_logits
        mock_model.return_value = mock_outputs

        mock_transformers.AutoModelForSequenceClassification.from_pretrained.return_value = mock_model
        mock_transformers.AutoTokenizer.from_pretrained.return_value = mock_tokenizer
        mock_import_transformer.return_value = mock_transformers

        # Test with empty list
        model = E5ScoreModel()
        results = model.predict([])

        # Should return empty list
        assert results == []

    @patch('llm_web_kit.model.math_detector.import_transformer')
    @patch('llm_web_kit.model.math_detector.torch.cuda.is_available')
    @patch('llm_web_kit.model.math_detector.E5ScoreModel.auto_download')
    def test_predict_output_key_compatibility(self, mock_auto_download, mock_cuda_available, mock_import_transformer):
        """Test that prediction output includes both new format and legacy
        output keys."""
        from llm_web_kit.model.math_detector import E5ScoreModel

        # Setup mocks
        mock_auto_download.return_value = None
        mock_cuda_available.return_value = False

        mock_transformers = MagicMock()
        mock_model = MagicMock()
        mock_tokenizer = MagicMock()

        # Mock tokenizer output
        mock_inputs = {
            'input_ids': torch.tensor([[1, 2, 3]]),
            'attention_mask': torch.tensor([[1, 1, 1]])
        }
        mock_tokenizer.return_value = mock_inputs

        # Mock model output
        mock_outputs = MagicMock()
        mock_logits = torch.tensor([[3.2]])
        mock_outputs.logits = mock_logits
        mock_model.return_value = mock_outputs

        mock_transformers.AutoModelForSequenceClassification.from_pretrained.return_value = mock_model
        mock_transformers.AutoTokenizer.from_pretrained.return_value = mock_tokenizer
        mock_import_transformer.return_value = mock_transformers

        # Test prediction
        model = E5ScoreModel()
        result = model.predict('Test text')[0]

        # Verify both new format and legacy output keys are present
        assert 'text' in result
        assert 'score' in result
        assert 'int_score' in result

        # Legacy output keys (for compatibility with existing interface)
        assert model.get_output_key('score') in result
        assert model.get_output_key('int_score') in result

        # Verify values are consistent
        assert result['score'] == result[model.get_output_key('score')]
        assert result['int_score'] == result[model.get_output_key('int_score')]

    def test_model_path_parameter(self):
        """Test initialization with explicit model path."""
        from llm_web_kit.model.math_detector import E5ScoreModel

        with patch('llm_web_kit.model.math_detector.import_transformer') as mock_import_transformer, \
             patch('llm_web_kit.model.math_detector.torch.cuda.is_available') as mock_cuda_available:

            mock_cuda_available.return_value = False
            mock_transformers = MagicMock()
            mock_model = MagicMock()
            mock_tokenizer = MagicMock()

            mock_transformers.AutoModelForSequenceClassification.from_pretrained.return_value = mock_model
            mock_transformers.AutoTokenizer.from_pretrained.return_value = mock_tokenizer
            mock_import_transformer.return_value = mock_transformers

            # Test with explicit model path (should not call auto_download)
            with patch.object(E5ScoreModel, 'auto_download') as mock_auto_download:
                E5ScoreModel(model_path='/custom/path')

                # auto_download should not be called when model_path is provided
                mock_auto_download.assert_not_called()


if __name__ == '__main__':
    unittest.main()
