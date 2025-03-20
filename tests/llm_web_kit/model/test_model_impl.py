"""Test cases for model_impl.py."""

import unittest
from unittest import TestCase
from unittest.mock import MagicMock, patch

from llm_web_kit.exception.exception import (ModelInitException,
                                             ModelRuntimeException)
from llm_web_kit.model.model_impl import (ModelFactory, ModelType,
                                          PoliticalCPUModel,
                                          PoliticalPredictorImpl,
                                          PornEnGPUModel, PornPredictorImpl,
                                          PornZhGPUModel)
from llm_web_kit.model.model_interface import (PoliticalRequest,
                                               PoliticalResponse, PornRequest,
                                               PornResponse)


class TestPoliticalCPUModel(TestCase):
    """Test cases for PoliticalCPUModel."""

    @patch('llm_web_kit.model.model_impl.get_singleton_political_detect')
    def test_load_model_success(self, mock_get_singleton_political_detect):
        """Test successful model loading."""
        # Setup mock
        mock_model = MagicMock()
        mock_get_singleton_political_detect.return_value = mock_model

        # Create model and load
        model = PoliticalCPUModel()

        # Verify
        assert model._load_model() == mock_model
        mock_get_singleton_political_detect.assert_called_once()

        mock_get_singleton_political_detect.return_value = None
        with self.assertRaises(RuntimeError):
            model._load_model()


    @patch.object(PoliticalCPUModel, '_load_model')
    def test_get_resource_requirement(self, mock_load_model):
        """Test resource requirements."""
        mock_load_model.return_value = MagicMock()
        model = PoliticalCPUModel()
        resource_requirement = model.get_resource_requirement()
        assert resource_requirement.num_cpus == 1
        assert resource_requirement.memory_GB == 4
        assert resource_requirement.num_gpus == 0

    @patch.object(PoliticalCPUModel, '_load_model')
    def test_get_batch_config(self, mock_load_model):
        """Test batch configuration."""
        mock_load_model.return_value = MagicMock()
        model = PoliticalCPUModel()
        batch_config = model.get_batch_config()
        assert batch_config.max_batch_size == 1000
        assert batch_config.optimal_batch_size == 512
        assert batch_config.min_batch_size == 8

    @patch.object(PoliticalCPUModel, '_load_model')
    @patch('llm_web_kit.model.model_impl.update_political_by_str')
    def test_predict_batch(self, mock_update_political_by_str, mock_load_model):
        """Test batch prediction."""
        mock_model = MagicMock()
        mock_load_model.return_value = mock_model
        mock_update_political_by_str.return_value = {'political_prob': 0.96}

        model = PoliticalCPUModel()
        model.model = mock_model

        results = model.predict_batch(['test1', 'test2'])
        assert len(results) == 2
        assert results[0]['political_prob'] == 0.96
        assert results[1]['political_prob'] == 0.96
        assert mock_update_political_by_str.call_count == 2

        # Test model not initialized
        model.model = None
        with self.assertRaises(RuntimeError):
            model.predict_batch(['test'])

        # Test prediction failure
        model.model = mock_model
        mock_update_political_by_str.side_effect = Exception('Test prediction failure')
        with self.assertRaises(RuntimeError) as context:
            model.predict_batch(['test'])
        self.assertIn('Prediction failed: Test prediction failure', str(context.exception))

    @patch.object(PoliticalCPUModel, '_load_model')
    def test_convert_result_to_response(self, mock_load_model):
        """Test result conversion to response."""
        mock_load_model.return_value = MagicMock()
        model = PoliticalCPUModel()

        # Test case where political_prob > 0.99 (should be flagged)
        result = {'political_prob': 0.995}
        response = model.convert_result_to_response(result)
        assert response.is_remained
        assert response.details == result

        # Test case where political_prob <= 0.99 (should not be flagged)
        result = {'political_prob': 0.985}
        response = model.convert_result_to_response(result)
        assert not response.is_remained
        assert response.details == result


class TestPoliticalPredictorImpl(TestCase):
    """Test cases for PoliticalPredictorImpl."""

    @patch.object(PoliticalCPUModel, '_load_model')
    def test_init(self, mock_load_model):
        """Test PoliticalPredictorImpl initialization."""
        mock_load_model.return_value = MagicMock()
        predictor = PoliticalPredictorImpl('en')
        assert predictor.language == 'en'
        assert predictor.model is not None
        assert mock_load_model.call_count == 1

    @patch.object(PoliticalCPUModel, '_load_model')
    def test_create_model(self, mock_load_model):
        """Test model creation for different languages."""
        mock_load_model.return_value = MagicMock()
        predictor = PoliticalPredictorImpl('en')

        # Test supported languages
        model_en = predictor._create_model('en')
        assert isinstance(model_en, PoliticalCPUModel)
        model_zh = predictor._create_model('zh')
        assert isinstance(model_zh, PoliticalCPUModel)

        # Test unsupported language
        with self.assertRaises(ModelInitException) as context:
            predictor._create_model('fr')
        self.assertIn('Poltical model does not support language: fr', str(context.exception))

    @patch.object(PoliticalCPUModel, '_load_model')
    def test_predict_batch(self, mock_load_model):
        """Test batch prediction functionality."""
        # Create a mock model with predict_batch method
        mock_model = MagicMock()
        mock_model.predict_batch.return_value = [
            {'political_prob': 0.995},
        ]
        mock_model.convert_result_to_response.return_value = PoliticalResponse(is_remained=True, details={'political_prob': 0.995}),
        mock_load_model.return_value = mock_model

        predictor = PoliticalPredictorImpl('en')
        predictor.model = mock_model

        # Test with mixed language requests
        with self.assertRaises(ModelRuntimeException):
            predictor.predict_batch([
                PoliticalRequest(content='Hello, world!', language='en'),
                PoliticalRequest(content='你好', language='zh')
            ])

        # Test with correct language requests
        results = predictor.predict_batch([
            PoliticalRequest(content='Hello, world!', language='en'),
        ])
        assert len(results) == 1
        assert results[0][0].is_remained  # political_prob > 0.99

    @patch.object(PoliticalCPUModel, '_load_model')
    def test_model_not_initialized(self, mock_load_model):
        """Test behavior when model is not initialized."""
        mock_load_model.return_value = MagicMock()
        predictor = PoliticalPredictorImpl('en')
        predictor.model = None

        with self.assertRaises(ModelRuntimeException):
            predictor.predict_batch([
                PoliticalRequest(content='Hello, world!', language='en')
            ])


class TestPornEnGPUModel(TestCase):
    """Test cases for PornEnGPUModel."""

    from llm_web_kit.model.porn_detector import BertModel as PornEnModel

    @patch.object(PornEnModel, '__init__')
    def test_load_model(self, mock_init):
        """Test model loading."""
        mock_init.return_value = None
        model = PornEnGPUModel()
        model._load_model()
        assert mock_init.call_count == 1

    @patch.object(PornEnGPUModel, '_load_model')
    def test_get_resource_requirement(self, mock_load_model):
        """Test resource requirements."""
        mock_load_model.return_value = MagicMock()
        model = PornEnGPUModel()
        resource_requirement = model.get_resource_requirement()
        assert resource_requirement.num_cpus == 12
        assert resource_requirement.memory_GB == 64
        assert resource_requirement.num_gpus == 1

    @patch.object(PornEnGPUModel, '_load_model')
    def test_get_batch_config(self, mock_load_model):
        """Test batch configuration."""
        mock_load_model.return_value = MagicMock()
        model = PornEnGPUModel()
        batch_config = model.get_batch_config()
        assert batch_config.max_batch_size == 1000
        assert batch_config.optimal_batch_size == 512
        assert batch_config.min_batch_size == 8

    @patch.object(PornEnGPUModel, '_load_model')
    def test_predict_batch(self, mock_load_model):
        """Test batch prediction."""
        mock_model = MagicMock()
        mock_model.get_output_key.return_value = 'prob'
        mock_model.predict.return_value = [{'prob': 0.96}, {'prob': 0.94}]
        mock_load_model.return_value = mock_model

        model = PornEnGPUModel()
        model.model = mock_model

        results = model.predict_batch(['test1', 'test2'])
        assert len(results) == 2
        assert results[0]['porn_prob'] == 0.96
        assert results[1]['porn_prob'] == 0.94

        # Test model not initialized
        model.model = None
        with self.assertRaises(RuntimeError):
            model.predict_batch(['test'])

    @patch.object(PornEnGPUModel, '_load_model')
    def test_convert_result_to_response(self, mock_load_model):
        """Test result conversion to response."""
        mock_load_model.return_value = MagicMock()
        model = PornEnGPUModel()

        # Test with high probability (should be remained)
        response = model.convert_result_to_response({'porn_prob': 0.21})
        assert isinstance(response, PornResponse)
        assert not response.is_remained
        assert response.details == {'porn_prob': 0.21}

        # Test with low probability (should not be remained)
        response = model.convert_result_to_response({'porn_prob': 0.19})
        assert isinstance(response, PornResponse)
        assert response.is_remained
        assert response.details == {'porn_prob': 0.19}


class TestPornZhGPUModel(TestCase):
    """Test cases for PornZhGPUModel."""

    from llm_web_kit.model.porn_detector import XlmrModel as PornZhModel

    @patch.object(PornZhModel, '__init__')
    def test_load_model(self, mock_init):
        """Test model loading."""
        mock_init.return_value = None
        model = PornZhGPUModel()
        model._load_model()
        assert mock_init.call_count == 1

    @patch.object(PornZhGPUModel, '_load_model')
    def test_get_resource_requirement(self, mock_load_model):
        """Test resource requirements."""
        mock_load_model.return_value = MagicMock()
        model = PornZhGPUModel()
        resource_requirement = model.get_resource_requirement()
        assert resource_requirement.num_cpus == 12
        assert resource_requirement.memory_GB == 64
        assert resource_requirement.num_gpus == 1

    @patch.object(PornZhGPUModel, '_load_model')
    def test_get_batch_config(self, mock_load_model):
        """Test batch configuration."""
        mock_load_model.return_value = MagicMock()
        model = PornZhGPUModel()
        batch_config = model.get_batch_config()
        assert batch_config.max_batch_size == 300
        assert batch_config.optimal_batch_size == 256
        assert batch_config.min_batch_size == 8

    @patch.object(PornZhGPUModel, '_load_model')
    def test_predict_batch(self, mock_load_model):
        """Test batch prediction."""
        mock_model = MagicMock()
        mock_model.get_output_key.return_value = 'prob'
        mock_model.predict.return_value = [{'prob': 0.96}, {'prob': 0.94}]
        mock_load_model.return_value = mock_model

        model = PornZhGPUModel()
        model.model = mock_model

        results = model.predict_batch(['test1', 'test2'])
        assert len(results) == 2
        assert results[0]['porn_prob'] == 0.96
        assert results[1]['porn_prob'] == 0.94

        # Test model not initialized
        model.model = None
        with self.assertRaises(RuntimeError):
            model.predict_batch(['test'])

    @patch.object(PornZhGPUModel, '_load_model')
    def test_convert_result_to_response(self, mock_load_model):
        """Test result conversion to response."""
        mock_load_model.return_value = MagicMock()
        model = PornZhGPUModel()

        # Test with high probability (should be remained)
        response = model.convert_result_to_response({'porn_prob': 0.96})
        assert isinstance(response, PornResponse)
        assert response.is_remained
        assert response.details == {'porn_prob': 0.96}

        # Test with low probability (should not be remained)
        response = model.convert_result_to_response({'porn_prob': 0.94})
        assert isinstance(response, PornResponse)
        assert not response.is_remained
        assert response.details == {'porn_prob': 0.94}


class TestPornPredictorImpl(TestCase):
    """Test cases for PornPredictorImpl."""

    @patch.object(PornEnGPUModel, '_load_model')
    @patch.object(PornZhGPUModel, '_load_model')
    @patch.object(PornZhGPUModel, 'predict_batch')
    @patch.object(PornEnGPUModel, 'predict_batch')
    def test_predict_batch(self, mock_predict_batch_en, mock_predict_batch_zh,
                         mock_load_model_en, mock_load_model_zh):
        """Test batch prediction."""
        mock_load_model_en.return_value = MagicMock()
        mock_load_model_zh.return_value = MagicMock()
        mock_predict_batch_en.return_value = [{'porn_prob': 0.19}, {'porn_prob': 0.3}]
        mock_predict_batch_zh.return_value = [{'porn_prob': 0.19}, {'porn_prob': 0.3}]

        predictor = PornPredictorImpl('en')
        assert predictor.language == 'en'
        with self.assertRaises(ModelRuntimeException):
            predictor.predict_batch([
                PornRequest(content='Hello, world!', language='en'),
                PornRequest(content='你好', language='zh')
            ])
            assert mock_predict_batch_en.call_count == 1

        results = predictor.predict_batch([
            PornRequest(content='Hello, world!', language='en'),
            PornRequest(content='nihao', language='en')
        ])
        assert results[0].is_remained
        assert not results[1].is_remained

    @patch.object(PornEnGPUModel, '_load_model')
    @patch.object(PornZhGPUModel, '_load_model')
    def test_create_model(self, mock_load_model_en, mock_load_model_zh):
        """Test model creation."""
        mock_load_model_en.return_value = MagicMock()
        mock_load_model_zh.return_value = MagicMock()
        predictor = PornPredictorImpl('en')
        assert predictor.language == 'en'
        assert predictor.model is not None


def test_model_factory():
    """Test ModelFactory creation."""
    factory = ModelFactory()
    assert factory is not None


class TestModelFactory(TestCase):
    """Test cases for ModelFactory."""

    @patch.object(PoliticalPredictorImpl, '_create_model')
    @patch.object(PoliticalCPUModel, '_load_model')
    def test_create_predictor(self, mock_load_model, mock_create_model):
        """Test ModelFactory.create_predictor method."""
        mock_load_model.return_value = MagicMock()
        mock_create_model.return_value = MagicMock()
        predictor = ModelFactory.create_predictor(ModelType.POLITICAL, 'en')
        assert isinstance(predictor, PoliticalPredictorImpl)
        assert mock_create_model.call_count == 1

    @patch.object(PornPredictorImpl, '_create_model')
    @patch.object(PornEnGPUModel, '_load_model')
    def test_create_predictor_porn(self, mock_load_model, mock_create_model):
        """Test ModelFactory.create_predictor method for porn model."""
        mock_load_model.return_value = MagicMock()
        mock_create_model.return_value = MagicMock()
        predictor = ModelFactory.create_predictor(ModelType.PORN, 'en')
        assert isinstance(predictor, PornPredictorImpl)
        assert mock_create_model.call_count == 1

    @patch.object(PornPredictorImpl, '_create_model')
    @patch.object(PornZhGPUModel, '_load_model')
    def test_create_predictor_porn_zh(self, mock_load_model, mock_create_model):
        """Test ModelFactory.create_predictor method for porn model."""
        mock_load_model.return_value = MagicMock()
        mock_create_model.return_value = MagicMock()
        predictor = ModelFactory.create_predictor(ModelType.PORN, 'zh')
        assert isinstance(predictor, PornPredictorImpl)
        assert mock_create_model.call_count == 1


class TestBaseModelResource(TestCase):
    """Test cases for BaseModelResource."""

    @patch.object(PoliticalCPUModel, '_load_model')
    def test_cleanup_model(self, mock_load_model):
        """Test model cleanup functionality."""
        # Create a mock model
        mock_model = MagicMock()
        mock_load_model.return_value = mock_model

        # Create a model instance
        model = PoliticalCPUModel()
        model.model = mock_model

        # Test cleanup
        model._cleanup_model()
        assert isinstance(model.model, MagicMock)

        # Test cleanup with no model
        model.model = None
        model._cleanup_model()  # Should not raise any error
        assert model.model is None


    @patch.object(PoliticalCPUModel, '_load_model')
    def test_cleanup(self, mock_load_model):
        """Test cleanup functionality."""
        # Create a mock model
        mock_model = MagicMock()
        mock_load_model.return_value = mock_model

        # Create a model instance
        model = PoliticalCPUModel()
        model.model = mock_model

        # Test cleanup
        model.cleanup()
        assert model.model is None

        # Test cleanup with no model
        model.model = None
        model.cleanup()  # Should not raise any error
        assert model.model is None


class TestBasePredictor(TestCase):
    """Test cases for BasePredictor."""

    @patch.object(PoliticalCPUModel, '_load_model')
    def test_get_resource_requirement_political(self, mock_load_model):
        """Test resource requirements for political model."""
        mock_load_model.return_value = MagicMock()
        predictor = PoliticalPredictorImpl('en')
        requirement = predictor.get_resource_requirement()
        assert requirement.num_cpus == 1
        assert requirement.memory_GB == 4
        assert requirement.num_gpus == 0

    @patch.object(PornEnGPUModel, '_load_model')
    def test_get_resource_requirement_porn_en(self, mock_load_model):
        """Test resource requirements for English porn model."""
        mock_load_model.return_value = MagicMock()
        predictor = PornPredictorImpl('en')
        requirement = predictor.get_resource_requirement()
        assert requirement.num_cpus == 12
        assert requirement.memory_GB == 64
        assert requirement.num_gpus == 1

    @patch.object(PornZhGPUModel, '_load_model')
    def test_get_resource_requirement_porn_zh(self, mock_load_model):
        """Test resource requirements for Chinese porn model."""
        mock_load_model.return_value = MagicMock()
        predictor = PornPredictorImpl('zh')
        requirement = predictor.get_resource_requirement()
        assert requirement.num_cpus == 12
        assert requirement.memory_GB == 64
        assert requirement.num_gpus == 1



if __name__ == '__main__':
    unittest.main()
