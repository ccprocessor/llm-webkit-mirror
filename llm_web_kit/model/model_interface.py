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

    is_remained: bool
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
class MathRequest(ModelRequest):
    """数学内容检测请求."""

    pass


@dataclass
class MathResponse(ModelResponse):
    """数学内容检测响应."""

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
    def __init__(self, num_cpus: float, memory_GB: float, num_gpus: float = 0.0):
        self.num_cpus = num_cpus
        self.memory_GB = memory_GB
        self.num_gpus = num_gpus

    def to_ray_resources(self) -> Dict:
        if self.num_gpus > 0:
            resources = {
                'num_cpus': self.num_cpus,
                'memory': self.memory_GB * 2**30,
                'num_gpus': self.num_gpus,
            }
        else:
            # prefer to use CPU on CPU only node
            # we set dummy resource "cpu_only" on CPU only node
            # so set resources.cpu_only = 1 to ensure the task can be scheduled on CPU only node
            resources = {
                'num_cpus': self.num_cpus,
                'memory': self.memory_GB * 2**30,
                'resources': {'cpu_only': 1},
            }

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
    def predict_batch(self, contents: List[str]) -> List[dict]:
        """批量预测."""
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """清理资源."""
        pass

    @abstractmethod
    def get_resource_requirement(self) -> ResourceRequirement:
        """获取资源需求."""
        pass


class ModelPredictor(ABC):
    """通用预测器接口."""

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

    def predict_batch(
        self, requests: List[PoliticalRequest]
    ) -> List[PoliticalResponse]:
        pass


class PornPredictor(ModelPredictor):
    """色情预测器接口."""

    def predict_batch(self, requests: List[PornRequest]) -> List[PornResponse]:
        pass


class MathPredictor(ModelPredictor):
    """数学内容预测器接口."""

    def predict_batch(self, requests: List[MathRequest]) -> List[MathResponse]:
        pass
