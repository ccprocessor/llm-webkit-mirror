import traceback
from abc import ABC, abstractmethod
from typing import Any, Dict

from llm_web_kit.input.pre_data_json import PreDataJson
from llm_web_kit.libs.logger import mylogger as logger


class AbstractMainHtmlProcessor(ABC):
    """MAIN HTML提取处理器的抽象基类，定义了处理MAIN HTML内容的标准接口."""

    def __init__(self, config: Dict[str, Any] = None, *args, **kwargs):
        """初始化处理器.

        Args:
            config (Dict[str, Any], optional): 配置信息
        """
        self.config = config or {}

    @abstractmethod
    def process(self, pre_data: PreDataJson) -> PreDataJson:
        """处理HTML数据的核心方法，每个子类必须实现.

        Args:
            pre_data (PreDataJson): 包含处理数据的PreDataJson对象

        Returns:
            PreDataJson: 处理后的PreDataJson对象
        """
        pass

    def get_name(self) -> str:
        """获取处理器名称.

        Returns:
            str: 处理器名称
        """
        return self.name


class AbstractPreProcessor(ABC):
    """前置处理器抽象类，定义前置处理的标准接口."""

    def __init__(self, config: Dict[str, Any] = None, *args, **kwargs):
        """初始化前置处理器.

        Args:
            config (Dict[str, Any], optional): 配置信息
        """
        self.config = config or {}
        self.name = self.__class__.__name__

    @abstractmethod
    def pre_process(self, pre_data: PreDataJson) -> PreDataJson:
        """执行前置处理逻辑.

        Args:
            pre_data (PreDataJson): 包含处理数据的PreDataJson对象

        Returns:
            PreDataJson: 前置处理后的PreDataJson对象
        """
        pass

    def get_name(self) -> str:
        """获取处理器名称.

        Returns:
            str: 处理器名称
        """
        return self.name


class AbstractPostProcessor(ABC):
    """后置处理器抽象类，定义后置处理的标准接口."""

    def __init__(self, config: Dict[str, Any] = None, *args, **kwargs):
        """初始化后置处理器.

        Args:
            config (Dict[str, Any], optional): 配置信息
        """
        self.config = config or {}
        self.name = self.__class__.__name__

    @abstractmethod
    def post_process(self, pre_data: PreDataJson) -> PreDataJson:
        """执行后置处理逻辑.

        Args:
            pre_data (PreDataJson): 包含处理数据的PreDataJson对象

        Returns:
            PreDataJson: 后置处理后的PreDataJson对象
        """
        pass

    def get_name(self) -> str:
        """获取处理器名称.

        Returns:
            str: 处理器名称
        """
        return self.name


# 具体实现类
class MainHtmlProcessor(AbstractMainHtmlProcessor):
    """MAIN HTML处理器基类，实现通用的处理流程和错误处理."""

    def __init__(self, config: Dict[str, Any] = None, *args, **kwargs):
        """初始化处理器.

        Args:
            config (Dict[str, Any], optional): 配置信息
        """
        super().__init__(config, *args, **kwargs)
        self.pre_processors = []
        self.post_processors = []

    def add_pre_processor(self, pre_processor: AbstractPreProcessor):
        """添加前置处理器.

        Args:
            pre_processor (AbstractPreProcessor): 前置处理器实例
        """
        self.pre_processors.append(pre_processor)

    def add_post_processor(self, post_processor: AbstractPostProcessor):
        """添加后置处理器.

        Args:
            post_processor (AbstractPostProcessor): 后置处理器实例
        """
        self.post_processors.append(post_processor)

    def execute(self, pre_data: PreDataJson) -> PreDataJson:
        """执行处理逻辑，包含通用的前后处理和日志记录.

        Args:
            pre_data (PreDataJson): 包含处理数据的PreDataJson对象

        Returns:
            PreDataJson: 处理后的PreDataJson对象
        """
        try:
            logger.debug(f'开始执行 {self.name} 处理')

            # 执行所有前置处理器
            for pre_processor in self.pre_processors:
                logger.debug(f'执行前置处理器 {pre_processor.get_name()}')
                pre_data = pre_processor.pre_process(pre_data)

            # 核心处理逻辑
            pre_data = self.process(pre_data)

            # 执行所有后置处理器
            for post_processor in self.post_processors:
                logger.debug(f'执行后置处理器 {post_processor.get_name()}')
                pre_data = post_processor.post_process(pre_data)

            logger.debug(f'{self.name} 处理完成')

            return pre_data
        except Exception as e:
            e.trace_info = traceback.format_exc()
            logger.error(f'{self.name} 处理失败: {str(e)}')
            raise e


class MainHtmlProcessorChain:
    """HTML处理器链，串联多个处理器执行HTML处理流程."""

    def __init__(self, processors=None, config: dict = None):
        """初始化处理器链.

        Args:
            processors (list, optional): 处理器列表
            config (Dict[str, Any], optional): 配置信息
        """
        self.processors = processors or []
        self.config = config or {}

    def add_processor(self, processor: AbstractMainHtmlProcessor):
        """添加处理器到链中.

        Args:
            processor (AbstractMainHtmlProcessor): 处理器实例
        """
        self.processors.append(processor)

    def process(self, pre_data: PreDataJson) -> PreDataJson:
        """执行整个处理链.

        Args:
            pre_data (PreDataJson): 包含初始数据的PreDataJson对象

        Returns:
            PreDataJson: 处理后的PreDataJson对象
        """
        try:
            for processor in self.processors:
                pre_data = processor.execute(pre_data)
        except Exception as e:
            logger.error(f'main html处理链执行失败: {str(e)}')
            raise e

        return pre_data
