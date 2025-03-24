"""Test cases for model_interface.py."""

import pytest

from llm_web_kit.model.model_interface import (BatchProcessConfig,
                                               ModelPredictor, ModelRequest,
                                               ModelResource, ModelResponse,
                                               PoliticalPredictor,
                                               PoliticalRequest,
                                               PoliticalResponse,
                                               PornPredictor, PornRequest,
                                               PornResponse,
                                               ResourceRequirement,
                                               ResourceType)


def test_model_request() -> None:
    """Test ModelRequest initialization and attributes."""
    request = ModelRequest(content='Hello, world!', language='en')
    assert request.content == 'Hello, world!'
    assert request.language == 'en'


def test_model_response() -> None:
    """Test ModelResponse initialization and attributes."""
    response = ModelResponse(is_remained=True, details={'score': 0.95})
    assert response.is_remained
    assert response.details['score'] == 0.95


def test_political_request() -> None:
    """Test PoliticalRequest initialization and attributes."""
    request = PoliticalRequest(content='Hello, world!', language='en')
    assert request.content == 'Hello, world!'
    assert request.language == 'en'


def test_political_response() -> None:
    """Test PoliticalResponse initialization and attributes."""
    response = PoliticalResponse(is_remained=True, details={'score': 0.95})
    assert response.is_remained
    assert response.details['score'] == 0.95


def test_porn_request() -> None:
    """Test PornRequest initialization and attributes."""
    request = PornRequest(content='Hello, world!', language='en')
    assert request.content == 'Hello, world!'
    assert request.language == 'en'


def test_porn_response() -> None:
    """Test PornResponse initialization and attributes."""
    response = PornResponse(is_remained=True, details={'score': 0.95})
    assert response.is_remained
    assert response.details['score'] == 0.95


def test_batch_process_config() -> None:
    """Test BatchProcessConfig initialization and attributes."""
    config = BatchProcessConfig(
        max_batch_size=100,
        optimal_batch_size=50,
        min_batch_size=10
    )
    assert config.max_batch_size == 100
    assert config.optimal_batch_size == 50
    assert config.min_batch_size == 10


def test_resource_type() -> None:
    """Test ResourceType enum values."""
    assert ResourceType.CPU
    assert ResourceType.GPU
    assert ResourceType.DEFAULT


def test_resource_requirement() -> None:
    """Test ResourceRequirement initialization and conversion to ray
    resources."""
    requirement = ResourceRequirement(num_cpus=1, memory_GB=4, num_gpus=0.25)
    assert requirement.num_cpus == 1
    assert requirement.memory_GB == 4
    assert requirement.num_gpus == 0.25
    assert requirement.to_ray_resources() == {
        'num_cpus': 1,
        'memory': 4 * 2**30,
        'num_gpus': 0.25
    }

    cpu_only_requirement = ResourceRequirement(num_cpus=1, memory_GB=4)
    assert cpu_only_requirement.to_ray_resources() == {
        'num_cpus': 1,
        'memory': 4 * 2**30,
        'resources': {'cpu_only': 1}
    }


def test_model_resource() -> None:
    """Test that ModelResource cannot be instantiated directly."""
    with pytest.raises(TypeError):
        ModelResource()


def test_model_predictor() -> None:
    """Test that ModelPredictor cannot be instantiated directly."""
    with pytest.raises(TypeError):
        ModelPredictor()


def test_political_predictor() -> None:
    """Test PoliticalPredictor implementation."""
    with pytest.raises(TypeError):
        predictor = PoliticalPredictor()
        assert isinstance(predictor, ModelPredictor)


def test_porn_predictor() -> None:
    """Test PornPredictor implementation."""
    with pytest.raises(TypeError):
        predictor = PornPredictor()
        assert isinstance(predictor, ModelPredictor)
