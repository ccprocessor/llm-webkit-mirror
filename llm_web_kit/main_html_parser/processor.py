from abc import ABC, abstractmethod

from overrides import override

from llm_web_kit.input.pre_data_json import PreDataJson


class AbstractProcessor(ABC):
    """MAIN HTML提取处理器的抽象基类，定义了处理MAIN HTML内容的标准接口."""

    def __init__(self, config: dict = None, *args, **kwargs):
        """初始化处理器.

        Args:
            config (dict, optional): 配置信息. Defaults to None.
        """
        self.__config = config or {}

    def process(self, pre_data: PreDataJson) -> PreDataJson:
        """处理HTML数据的方法，包含通用流程控制.

        Args:
            pre_data (PreDataJson): 包含处理数据的PreDataJson对象

        Returns:
            PreDataJson: 处理后的PreDataJson对象
        """
        if self._filter_by_rule(pre_data):
            return self._do_process(pre_data)
        else:
            return pre_data

    @abstractmethod
    def _filter_by_rule(self, pre_data: PreDataJson) -> bool:
        """判断是否需要处理当前数据.

        Args:
            pre_data (PreDataJson): 包含处理数据的PreDataJson对象

        Returns:
            bool: 如果需要处理返回True，否则返回False
        """
        raise NotImplementedError('Subclass must implement abstract method')

    @abstractmethod
    def _do_process(self, pre_data: PreDataJson) -> PreDataJson:
        """实现真正的处理逻辑.

        Args:
            pre_data (PreDataJson): 包含处理数据的PreDataJson对象

        Returns:
            PreDataJson: 处理后的PreDataJson对象
        """
        raise NotImplementedError('Subclass must implement abstract method')


class BaseRuleFilterProcessor(AbstractProcessor):
    """从html网页中筛选数据的处理器.

    Args:
        AbstractProcessor (_type_): _description_
    """

    def __init__(self, config: dict, *args, **kwargs):
        """从参数指定的配置中初始化这个流水线链.

        Args:
            config (dict): 配置字典
        """
        super().__init__(config, *args, **kwargs)


class NoOpProcessor(AbstractProcessor):
    """一个什么都不做的处理器，让架构更加一致。通常在disable某个步骤时使用，充当透传功能."""

    def __init__(self, config: dict = None, *args, **kwargs):
        """初始化处理器.

        Args:
            config (dict, optional): 配置信息. Defaults to None.
        """
        super().__init__(config, *args, **kwargs)

    @override
    def _filter_by_rule(self, pre_data: PreDataJson) -> bool:
        """判断是否需要处理当前数据.

        Args:
            pre_data (PreDataJson): 包含处理数据的PreDataJson对象

        Returns:
            bool: 始终返回True
        """
        return True

    @override
    def _do_process(self, pre_data: PreDataJson) -> PreDataJson:
        """实现透传处理逻辑.

        Args:
            pre_data (PreDataJson): 包含处理数据的PreDataJson对象

        Returns:
            PreDataJson: 不作任何修改的PreDataJson对象
        """
        return pre_data
