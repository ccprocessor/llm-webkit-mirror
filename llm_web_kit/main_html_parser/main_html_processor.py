from abc import ABC, abstractmethod

from llm_web_kit.input.pre_data_json import PreDataJson
from llm_web_kit.libs.logger import mylogger as logger


class AbstractMainHtmlProcessor(ABC):
    """MAIN HTML提取处理器的抽象基类，定义了处理MAIN HTML内容的标准接口."""

    def __init__(self, config: dict = None):
        """初始化处理器.

        Args:
            config (dict): 配置信息
        """

        self.config = config or {}
        self.name = self.__class__.__name__

    @abstractmethod
    def process(self, pre_data: PreDataJson) -> PreDataJson:
        """处理HTML数据的核心方法，每个子类必须实现.

        Args:
            pre_data (PreDataJson): 包含处理数据的PreDataJson对象

        Returns:
            PreDataJson: 处理后的PreDataJson对象
        """
        pass

    def execute(self, pre_data: PreDataJson) -> PreDataJson:
        """执行处理逻辑，包含通用的前后处理和日志记录.

        Args:
            pre_data (PreDataJson): 包含处理数据的PreDataJson对象

        Returns:
            PreDataJson: 处理后的PreDataJson对象
        """
        try:
            logger.debug(f'开始执行 {self.name} 处理')

            # 前置处理
            pre_data = self.pre_process(pre_data)

            # 核心处理逻辑
            pre_data = self.process(pre_data)

            # 后置处理
            pre_data = self.post_process(pre_data)

            logger.debug(f'{self.name} 处理完成')

            return pre_data
        except Exception as e:
            logger.error(f'{self.name} 处理失败: {str(e)}')

    def pre_process(self, pre_data: PreDataJson) -> PreDataJson:
        """处理前的准备工作，子类可以覆盖此方法.

        Args:
            pre_data (PreDataJson): 包含处理数据的PreDataJson对象

        Returns:
            PreDataJson: 准备后的PreDataJson对象
        """
        return pre_data

    def post_process(self, pre_data: PreDataJson) -> PreDataJson:
        """处理后的收尾工作，子类可以覆盖此方法.

        Args:
            pre_data (PreDataJson): 包含处理数据的PreDataJson对象

        Returns:
            PreDataJson: 收尾后的PreDataJson对象
        """
        return pre_data


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
