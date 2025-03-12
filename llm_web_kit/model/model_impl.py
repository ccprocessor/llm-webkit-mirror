from abc import abstractmethod
from enum import Enum
from typing import Dict, List, Type

from llm_web_kit.model.model_interface import (BatchProcessConfig,
                                               ModelPredictor, ModelResource,
                                               PoliticalRequest,
                                               PoliticalResponse, PornRequest,
                                               PornResponse,
                                               ResourceRequirement,
                                               ResourceType)
from llm_web_kit.model.policical import (get_singleton_political_detect,
                                         update_political_by_str)
from llm_web_kit.model.porn_detector import BertModel as PornBertModel


class ModelType(Enum):
    """模型类型枚举."""

    POLITICAL = 'political'  # 涉政模型
    PORN = 'porn'  # 色情模型


class DeviceType(Enum):
    """设备类型枚举."""

    CPU = 'cpu'
    GPU = 'gpu'


class BaseModelResource(ModelResource):
    """基础模型资源类."""

    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None

    def initialize(self) -> None:
        self.model = self._load_model()

    @abstractmethod
    def _load_model(self):
        pass

    def cleanup(self) -> None:
        if self.model:
            self._cleanup_model()
            self.model = None

    def _cleanup_model(self):
        pass


class BasePredictor(ModelPredictor):
    """基础预测器类."""

    def __init__(self, cpu_model_path: str, gpu_model_path: str):
        self.cpu_model = self._create_cpu_model(cpu_model_path)
        self.gpu_model = self._create_gpu_model(gpu_model_path)

        # 初始化模型
        if self.cpu_model:
            self.cpu_model.initialize()
        if self.gpu_model:
            self.gpu_model.initialize()

        self.language_map = {
            'zh': DeviceType.CPU,
            'en': DeviceType.CPU,
            # 其他语言映射到GPU
        }

    @abstractmethod
    def _create_cpu_model(self, model_path: str) -> ModelResource:
        pass

    @abstractmethod
    def _create_gpu_model(self, model_path: str) -> ModelResource:
        pass

    def get_model_info(self) -> Dict[str, BatchProcessConfig]:
        info = {}
        if self.cpu_model:
            info[DeviceType.CPU.value] = self.cpu_model.get_batch_config()
        if self.gpu_model:
            info[DeviceType.GPU.value] = self.gpu_model.get_batch_config()
        return info


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

    def get_batch_config(self) -> BatchProcessConfig:
        return BatchProcessConfig(max_batch_size=128, optimal_batch_size=64, min_batch_size=8)

    def predict_batch(self, contents: List[str]) -> List[float]:
        if not self.model:
            raise RuntimeError('Model not initialized')
        try:
            # 批量处理
            results = []
            for content in contents:
                result = update_political_by_str(content)
                results.append(result['political_prob'])
            return results
        except Exception as e:
            raise RuntimeError(f'Prediction failed: {e}')


class PoliticalPredictorImpl(BasePredictor):
    """涉政检测预测器实现."""

    def _create_cpu_model(self, model_path: str) -> ModelResource:
        return PoliticalCPUModel(model_path)

    def _create_gpu_model(self, model_path: str) -> ModelResource:
        return None

    def get_resource_requirement(self, language: str) -> ResourceRequirement:
        """获取资源需求."""
        # 涉政模型对中英文使用CPU，其他语言使用默认资源
        if language in ['zh', 'en']:
            return ResourceRequirement(resource_type=ResourceType.CPU)
        return ResourceRequirement()

    def predict_batch(self, requests: List[PoliticalRequest]) -> List[PoliticalResponse]:
        """批量预测接口."""
        responses = [None] * len(requests)

        try:
            # 收集所有请求内容
            batch_contents = []
            valid_indices = []

            for idx, req in enumerate(requests):
                try:
                    # 验证语言支持
                    if req.language not in ['zh', 'en']:
                        continue
                    batch_contents.append(req.content)
                    valid_indices.append(idx)
                except Exception as e:
                    print(f'Skip invalid request at index {idx}: {e}')

            if batch_contents:
                # 批量处理
                probs = self.cpu_model.predict_batch(batch_contents)
                # 填充结果
                for idx, prob in zip(valid_indices, probs):
                    responses[idx] = PoliticalResponse(probability=prob)

        except Exception as e:
            raise RuntimeError(f'Political prediction failed: {e}')

        return responses


# 色情模型实现
class PornGPUModel(BaseModelResource):
    """色情检测GPU模型."""

    def _load_model(self):
        try:
            return PornBertModel('')
        except Exception as e:
            raise RuntimeError(f'Failed to load porn GPU model: {e}')

    def get_batch_config(self) -> BatchProcessConfig:
        return BatchProcessConfig(max_batch_size=128, optimal_batch_size=64, min_batch_size=8)

    def predict_batch(self, contents: List[str]) -> List[float]:
        if not self.model:
            raise RuntimeError('Model not initialized')
        try:
            # 色情模型本身支持批处理
            results = self.model.predict(contents)
            return [result[self.model.get_output_key('prob')] for result in results]
        except Exception as e:
            raise RuntimeError(f'Prediction failed: {e}')


class PornPredictorImpl(BasePredictor):
    """色情检测预测器实现."""

    def _create_cpu_model(self, model_path: str) -> ModelResource:
        return None

    def _create_gpu_model(self, model_path: str) -> ModelResource:
        return PornGPUModel(model_path='')

    def get_resource_requirement(self, language: str) -> ResourceRequirement:
        """获取资源需求."""
        # 色情模型统一使用GPU
        return ResourceRequirement(resource_type=ResourceType.GPU)

    def predict_batch(self, requests: List[PornRequest]) -> List[PornResponse]:
        """批量预测接口."""
        responses = [None] * len(requests)

        try:
            # 收集所有中英文请求
            batch_contents = []
            valid_indices = []

            for idx, req in enumerate(requests):
                if req.language in ['zh', 'en']:
                    batch_contents.append(req.content)
                    valid_indices.append(idx)

            if batch_contents:
                # 批量处理
                probs = self.gpu_model.predict_batch(batch_contents)
                # 填充结果
                for idx, prob in zip(valid_indices, probs):
                    responses[idx] = PornResponse(probability=prob)

        except Exception as e:
            raise RuntimeError(f'Porn prediction failed: {e}')

        return responses


# 模型工厂
class ModelFactory:
    """模型工厂类."""

    _predictor_registry: Dict[ModelType, Type[BasePredictor]] = {
        ModelType.POLITICAL: PoliticalPredictorImpl,
        ModelType.PORN: PornPredictorImpl,
    }

    @classmethod
    def create_predictor(cls, model_type: ModelType, cpu_model_path: str, gpu_model_path: str) -> BasePredictor:
        """创建预测器实例."""
        predictor_class = cls._predictor_registry.get(model_type)
        if not predictor_class:
            raise ValueError(f'No predictor registered for type: {model_type}')
        return predictor_class(cpu_model_path, gpu_model_path)