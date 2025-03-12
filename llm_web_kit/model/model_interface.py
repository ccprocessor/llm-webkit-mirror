from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List


@dataclass
class ModelRequest:
    """通用模型请求基类."""

    content: str
    language: str
    extra_params: Dict[str, Any] = None


@dataclass
class ModelResponse:
    """通用模型响应基类."""

    probability: float
    details: Dict[str, Any] = None


@dataclass
class PoliticalRequest(ModelRequest):
    """涉政检测请求."""

    pass


@dataclass
class PoliticalResponse(ModelResponse):
    """涉政检测响应."""

    pass


@dataclass
class PornRequest(ModelRequest):
    """色情检测请求."""

    pass


@dataclass
class PornResponse(ModelResponse):
    """色情检测响应."""

    pass


@dataclass
class BatchProcessConfig:
    """批处理配置."""

    max_batch_size: int
    optimal_batch_size: int
    min_batch_size: int


class ResourceType(Enum):
    """资源类型枚举."""

    CPU = 'cpu_only'
    GPU = 'num_gpus'
    DEFAULT = 'default'


class ResourceRequirement:
    """资源需求配置."""

    def __init__(self, resource_type: ResourceType = ResourceType.DEFAULT, num_cpus: int = 1, memory: int = 4 << 30):
        self.resource_type = resource_type
        self.num_cpus = num_cpus
        self.memory = memory

    def to_ray_resources(self) -> Dict:
        """转换为Ray资源配置."""
        resources = {
            'num_cpus': self.num_cpus,
            'memory': self.memory,
        }

        # 根据资源类型设置正确的资源配置
        if self.resource_type == ResourceType.CPU:
            resources['resources'] = {'cpu_only': 1}
        elif self.resource_type == ResourceType.GPU:
            # 使用 num_gpus 而不是在 resources 字典中设置
            resources['num_gpus'] = 0.25

        return resources


class ModelResource(ABC):
    """模型资源接口."""

    @abstractmethod
    def initialize(self) -> None:
        """初始化模型资源."""
        pass

    @abstractmethod
    def get_batch_config(self) -> BatchProcessConfig:
        """获取模型的批处理配置."""
        pass

    @abstractmethod
    def predict_batch(self, contents: List[str]) -> List[float]:
        """批量预测."""
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """清理资源."""
        pass


class ModelPredictor(ABC):
    """通用预测器接口."""

    @abstractmethod
    def get_model_info(self) -> Dict[str, BatchProcessConfig]:
        """获取模型信息."""
        pass

    @abstractmethod
    def get_resource_requirement(self, language: str) -> ResourceRequirement:
        """获取资源需求."""
        pass

    @abstractmethod
    def predict_batch(self, requests: List[ModelRequest]) -> List[ModelResponse]:
        """批量预测接口 - 同步版本."""
        pass


class PoliticalPredictor(ModelPredictor):
    """涉政预测器接口."""

    def predict_batch(self, requests: List[PoliticalRequest]) -> List[PoliticalResponse]:
        pass


class PornPredictor(ModelPredictor):
    """色情预测器接口."""

    def predict_batch(self, requests: List[PornRequest]) -> List[PornResponse]:
        pass