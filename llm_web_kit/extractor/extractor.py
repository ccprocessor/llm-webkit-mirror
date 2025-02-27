from abc import ABC, abstractmethod

from overrides import override

from llm_web_kit.extractor.base import FileTypeMatcher
from llm_web_kit.input.datajson import DataJson


class AbstractExtractor(ABC):
    """一个抽象的数据提取器.

    Args:
        ABC (_type_): _description_
    """

    def __init__(self, config: dict, *args, **kwargs):
        """从参数指定的配置中初始化这个流水线链.

        Args:
            config (dict): 配置字典
        """
        self.__config = config

    def extract(self, data_json: DataJson) -> DataJson:
        """实现针对一条输入数据的提取.

        Args:
            data_json (DataJson): _description_

        Returns:
            dict: _description_
        """
        if self._filter_by_rule(data_json):
            return self._do_extract(data_json)
        else:
            return data_json

    @abstractmethod
    def _filter_by_rule(self, data_json: DataJson) -> bool:
        """data_json.

        Args:
            data_json (DataJson): data_json

        Returns:
            bool: 如果是希望处理的数据，返回True，否则返回False
        """
        raise NotImplementedError('Subclass must implement abstract method')

    @abstractmethod
    def _do_extract(self, data_json: DataJson) -> DataJson:
        """实现真正的数据提取.

        Args:
            data_json (DataJson): 需要处理的数据集
        """
        raise NotImplementedError('Subclass must implement abstract method')


class BaseRuleFilterExtractor(AbstractExtractor):
    """一个从markdown文件中提取数据的提取器.

    Args:
        AbstractExtractor (_type_): _description_
    """

    def __init__(self, config: dict, *args, **kwargs):
        """从参数指定的配置中初始化这个流水线链.

        Args:
            config (dict): 配置字典
        """
        super().__init__(config, *args, **kwargs)


class BaseFileFormatExtractor(BaseRuleFilterExtractor, FileTypeMatcher):
    """一个从html文件中提取数据的提取器.

    Args:
        AbstractExtractor (_type_): _description_
    """

    def __init__(self, config: dict, *args, **kwargs):
        """从参数指定的配置中初始化这个流水线链.

        Args:
            config (dict): 配置字典
        """
        super().__init__(config, *args, **kwargs)


class NoOpExtractor(AbstractExtractor):
    """一个什么都不做的提取器, 让架构更加一致。 通常在disable某个步骤的时候使用，充当透传功能。

    Args:
        AbstractExtractor (_type_): _description_
    """

    def __init__(self, config: dict, *args, **kwargs):
        """从参数指定的配置中初始化这个流水线链.

        Args:
            config (dict): 配置字典
        """
        super().__init__(config, *args, **kwargs)

    @override
    def _filter_by_rule(self, data_json: DataJson) -> bool:
        """data_json.

        Args:
            data_json (DataJson): 判断data_json是否是自己想要拦截处理的数据

        Returns:
            bool: 如果是希望处理的数据，返回True，否则返回False
        """
        return True

    @override
    def _do_extract(self, data_json: DataJson) -> DataJson:
        """实现真正的数据提取.

        Args:
            data_json (DataJson): 需要处理的数据集
        """
        return data_json
