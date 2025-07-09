from abc import abstractmethod
from enum import Enum
from typing import Dict, List, Type, Union

from llm_web_kit.exception.exception import (ModelInitException,
                                             ModelInputException,
                                             ModelRuntimeException)
from llm_web_kit.model.model_interface import (BatchProcessConfig, MathRequest,
                                               MathResponse, ModelPredictor,
                                               ModelResource, ModelResponse,
                                               PoliticalRequest,
                                               PoliticalResponse, PornRequest,
                                               PornResponse,
                                               ResourceRequirement)
from llm_web_kit.model.politics_detector import (
    GTEModel, get_singleton_political_detect, update_political_by_str)


class ModelType(Enum):
    """模型类型枚举."""

    POLITICAL = 'political'  # 涉政模型
    PORN = 'porn'  # 色情模型
    MATH = 'math'  # 数学内容模型


class DeviceType(Enum):
    """设备类型枚举."""

    CPU = 'cpu'
    GPU = 'gpu'


class BaseModelResource(ModelResource):
    """基础模型资源类."""

    def __init__(self):
        self.model = None

    def initialize(self) -> None:
        self.model = self._load_model()

    @abstractmethod
    def _load_model(self):
        pass

    @abstractmethod
    def convert_result_to_response(self, result: dict) -> ModelResponse:
        pass

    def cleanup(self) -> None:
        if self.model:
            self._cleanup_model()
            self.model = None

    def _cleanup_model(self):
        pass


class BasePredictor(ModelPredictor):
    """基础预测器类."""

    def __init__(self, language: Union[str, List[str]], device_type: DeviceType):
        self.language = language
        self.model = self._create_model(language, device_type)

        # 初始化模型
        self.model.initialize()

    @abstractmethod
    def _create_model(self, language: Union[str, List[str]]) -> ModelResource:
        pass

    def get_resource_requirement(self):
        return self.model.get_resource_requirement()


# 涉政模型实现
class PoliticalCPUModel(BaseModelResource):
    """涉政检测CPU模型."""

    def _load_model(self):
        try:
            model = get_singleton_political_detect()
            if model is None:
                raise RuntimeError('Failed to load political model')
            return model
        except Exception as e:
            raise RuntimeError(f'Failed to load political CPU model: {e}')

    def get_resource_requirement(self):
        return ResourceRequirement(num_cpus=1, memory_GB=4, num_gpus=0)

    def get_batch_config(self) -> BatchProcessConfig:
        return BatchProcessConfig(
            max_batch_size=1000, optimal_batch_size=512, min_batch_size=8
        )

    def predict_batch(self, contents: List[str]) -> List[dict]:
        if not self.model:
            raise RuntimeError('Model not initialized')
        try:
            # 批量处理
            results = []
            for content in contents:
                result = update_political_by_str(content)
                results.append(result)

            return results
        except Exception as e:
            raise RuntimeError(f'Prediction failed: {e}')

    def convert_result_to_response(self, result: dict) -> ModelResponse:
        # raise NotImplementedError
        # TODO convert result to response ensure the threshold
        return PoliticalResponse(
            is_remained=result['political_prob'] > 0.89, details=result
        )


class PoliticalGPUModel(BaseModelResource):
    """涉政检测GPU模型."""

    def _load_model(self):
        try:
            model = GTEModel()
            if model is None:
                raise RuntimeError('Failed to load political model')
            return model
        except Exception as e:
            raise RuntimeError(f'Failed to load political GPU model: {e}')

    def get_resource_requirement(self):
        return ResourceRequirement(num_cpus=12, memory_GB=64, num_gpus=1)

    def get_batch_config(self) -> BatchProcessConfig:
        return BatchProcessConfig(
            max_batch_size=256, optimal_batch_size=32, min_batch_size=8
        )

    def predict_batch(self, contents: List[str]) -> List[dict]:
        if not self.model:
            raise RuntimeError('Model not initialized')
        try:
            # 批量处理
            results = self.model.predict(contents)
            return [
                {'political_prob': result[self.model.get_output_key('prob')]}
                for result in results
            ]

        except Exception as e:
            raise RuntimeError(f'Prediction failed: {e}')

    def convert_result_to_response(self, result: dict) -> ModelResponse:
        return PoliticalResponse(
            is_remained=result['political_prob'] > 0.63, details=result
        )


class PoliticalPredictorImpl(BasePredictor):
    """涉政检测预测器实现."""

    def _create_model(self, language: Union[str, List[str]], device_type: DeviceType) -> ModelResource:
        lang_list = language if isinstance(language, list) else [language]
        for lang in lang_list:
            if lang not in ['zh', 'en']:
                raise ModelInitException(
                    f'Poltical model does not support language: {lang}'
                )
        if device_type == DeviceType.CPU:
            return PoliticalCPUModel()
        elif device_type == DeviceType.GPU:
            return PoliticalGPUModel()
        else:
            raise ModelInitException(
                f'Poltical model does not support device type: {device_type}'
            )

    def predict_batch(
        self, requests: List[PoliticalRequest]
    ) -> List[PoliticalResponse]:
        """批量预测接口."""

        try:
            # 收集所有请求内容
            batch_contents = []

            for req in requests:
                # 验证语言支持
                if req.language not in self.language:
                    raise ModelInputException(
                        f'Language mismatch: {req.language} not in {self.language}'
                    )
                batch_contents.append(req.content)

            if batch_contents:
                # 批量处理
                probs = self.model.predict_batch(batch_contents)
                responses = [self.model.convert_result_to_response(prob) for prob in probs]
        except Exception as e:
            raise ModelRuntimeException(f'Political prediction failed: {e}')

        return responses


# 色情模型实现
class PornEnGPUModel(BaseModelResource):
    """英文色情检测GPU模型."""

    def _load_model(self):
        try:
            from llm_web_kit.model.porn_detector import \
                BertModel as PornEnModel

            return PornEnModel()
        except Exception as e:
            raise ModelInitException(f'Failed to init the en porn model: {e}')

    def get_resource_requirement(self):
        # S2 cluster has 96 CPUs, 1TB memory, 8 GPUs
        # so we can use 12 CPUs, 64GB memory, 1 GPU for this model
        return ResourceRequirement(num_cpus=12, memory_GB=64, num_gpus=1)

    def get_batch_config(self) -> BatchProcessConfig:
        return BatchProcessConfig(
            max_batch_size=1000, optimal_batch_size=512, min_batch_size=8
        )

    def predict_batch(self, contents: List[str]) -> List[dict]:
        if not self.model:
            raise RuntimeError('Model not initialized')
        try:
            # 色情模型本身支持批处理
            results = self.model.predict(contents)
            return [
                {'porn_prob': result[self.model.get_output_key('prob')]}
                for result in results
            ]
        except Exception as e:
            raise RuntimeError(f'Prediction failed: {e}')

    def convert_result_to_response(self, result: dict) -> ModelResponse:
        # raise NotImplementedError
        # TODO convert result to response ensure the threshold
        return PornResponse(is_remained=result['porn_prob'] < 0.2, details=result)


class PornZhGPUModel(BaseModelResource):
    """中文色情检测GPU模型."""

    def _load_model(self):
        try:
            from llm_web_kit.model.porn_detector import \
                XlmrModel as PornZhModel

            return PornZhModel()
        except Exception as e:
            raise ModelInitException(f'Failed to init the zh porn model: {e}')

    def get_resource_requirement(self):
        # S2 cluster has at least 96 CPUs, 1TB memory, 8 GPUs
        # so we can use 12 CPUs, 64GB memory, 1 GPU for this model
        return ResourceRequirement(num_cpus=12, memory_GB=64, num_gpus=1)

    def get_batch_config(self) -> BatchProcessConfig:
        return BatchProcessConfig(
            max_batch_size=300, optimal_batch_size=256, min_batch_size=8
        )

    def predict_batch(self, contents: List[str]) -> List[dict]:
        if not self.model:
            raise RuntimeError('Model not initialized')
        try:
            # 色情模型本身支持批处理
            results = self.model.predict(contents)
            return [
                {'porn_prob': result[self.model.get_output_key('prob')]}
                for result in results
            ]
        except Exception as e:
            raise RuntimeError(f'Prediction failed: {e}')

    def convert_result_to_response(self, result: dict) -> ModelResponse:
        # raise NotImplementedError
        # TODO convert result to response ensure the threshold
        return PornResponse(is_remained=result['porn_prob'] > 0.95, details=result)


# 数学内容模型实现
class MathGPUModel(BaseModelResource):
    """数学内容检测GPU模型."""

    def _load_model(self):
        try:
            from llm_web_kit.model.math_detector import \
                E5ScoreModel as MathModel

            return MathModel()
        except Exception as e:
            raise ModelInitException(f'Failed to init the math model: {e}')

    def get_resource_requirement(self):
        # Math model requires similar resources to other GPU models
        return ResourceRequirement(num_cpus=12, memory_GB=64, num_gpus=1)

    def get_batch_config(self) -> BatchProcessConfig:
        return BatchProcessConfig(
            max_batch_size=512, optimal_batch_size=256, min_batch_size=8
        )

    def predict_batch(self, contents: List[str]) -> List[dict]:
        if not self.model:
            raise RuntimeError('Model not initialized')
        try:
            # Math model supports batch processing
            results = self.model.predict(contents)
            return [
                {
                    'math_score': result[self.model.get_output_key('score')],
                    'math_int_score': result[self.model.get_output_key('int_score')]
                }
                for result in results
            ]
        except Exception as e:
            raise RuntimeError(f'Prediction failed: {e}')

    def convert_result_to_response(self, result: dict) -> ModelResponse:
        # Math content is considered "remained" if score is above threshold (e.g., 3.0)
        # This means mathematical content should be kept/processed
        return MathResponse(
            is_remained=result['math_score'] >= 3.0,
            details=result
        )


class MathPredictorImpl(BasePredictor):
    """数学内容检测预测器实现."""

    def _create_model(self, language: Union[str, List[str]], device_type: DeviceType) -> ModelResource:
        if device_type == DeviceType.CPU:
            raise ModelInitException(f'Math model does not support device type: {device_type}')
        # Math model supports multiple languages without restrictions
        return MathGPUModel()

    def predict_batch(self, requests: List[MathRequest]) -> List[MathResponse]:
        """批量预测接口."""
        try:
            # 收集所有请求内容
            batch_contents = []

            for req in requests:
                batch_contents.append(req.content)

            if batch_contents:
                # 批量处理
                results = self.model.predict_batch(batch_contents)
                responses = [self.model.convert_result_to_response(result) for result in results]
            else:
                responses = []
        except Exception as e:
            raise ModelRuntimeException(f'Math prediction failed: {e}')
        return responses


class PornPredictorImpl(BasePredictor):
    """色情检测预测器实现."""

    def _create_model(self, language: str, device_type: DeviceType) -> ModelResource:
        if device_type == DeviceType.CPU:
            raise ModelInitException(f'Porn model does not support device type: {device_type}')
        if language == 'en':
            return PornEnGPUModel()
        elif language == 'zh':
            return PornZhGPUModel()
        raise ModelInitException(f'Porn model does not support language: {language}')

    def predict_batch(self, requests: List[PornRequest]) -> List[PornResponse]:
        """批量预测接口."""
        try:
            # 收集所有请求内容
            batch_contents = []

            for req in requests:
                # 验证语言支持
                if req.language != self.language:
                    raise ModelInputException(
                        f'Language mismatch: {req.language} vs {self.language}'
                    )
                batch_contents.append(req.content)

            if batch_contents:
                # 批量处理
                probs = self.model.predict_batch(batch_contents)
                responses = [self.model.convert_result_to_response(prob) for prob in probs]
        except Exception as e:
            raise ModelRuntimeException(f'Porn prediction failed: {e}')
        return responses


# 模型工厂
class ModelFactory:
    """模型工厂类."""

    _predictor_registry: Dict[ModelType, Type[BasePredictor]] = {
        ModelType.POLITICAL: PoliticalPredictorImpl,
        ModelType.PORN: PornPredictorImpl,
        ModelType.MATH: MathPredictorImpl,
    }

    @classmethod
    def create_predictor(cls, model_type: ModelType, language: Union[str, List[str]], device_type: DeviceType) -> BasePredictor:
        """创建预测器实例."""
        predictor_class = cls._predictor_registry.get(model_type)
        print(predictor_class)
        if not predictor_class:
            raise ValueError(f'No predictor registered for type: {model_type}')
        return predictor_class(language=language, device_type=device_type)
