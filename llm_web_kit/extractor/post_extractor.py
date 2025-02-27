from abc import ABC, abstractmethod

from overrides import override

from llm_web_kit.extractor.base import FileTypeMatcher
from llm_web_kit.input.datajson import DataJson


class AbstractPostExtractor(ABC):
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

    def post_extract(self, data_json: DataJson) -> DataJson:
        """实现针对一条输入数据的提取.

        Args:
            data_json (DataJson): _description_

        Returns:
            dict: _description_
        """
        if self._filter_by_rule(data_json):
            return self._do_post_extract(data_json)
        else:
            return data_json

    @abstractmethod
    def _filter_by_rule(self, data_json: DataJson) -> bool:
        """根据规则过滤content_list.

        Args:
            data_json (DataJson): 判断content_list是否是自己想要拦截处理的数据

        Returns:
            bool: 如果是希望处理的数据，返回True，否则返回False
        """
        raise NotImplementedError('Subclass must implement abstract method')

    @abstractmethod
    def _do_post_extract(self, data_json: DataJson) -> DataJson:
        """实现真正的数据提取.

        Args:
            data_json (DataJson): 需要处理的数据集
        """
        raise NotImplementedError('Subclass must implement abstract method')


class BaseRuleFilterPostExtractor(AbstractPostExtractor):
    """一个基础的规则过滤提取器.

    Args:
        AbstractPostExtractor (_type_): 一个抽象的数据提取器
    """
    pass


class BaseFileFormatPostExtractor(BaseRuleFilterPostExtractor, FileTypeMatcher):
    """一个基础的规则过滤提取器.

    Args:
        AbstractPostExtractor (_type_): 一个抽象的数据提取器
    """
    pass


class NoOpPostExtractor(BaseRuleFilterPostExtractor):
    """一个什么都不做的提取器.

    Args:
        BaseRuleFilterPostExtractor (_type_): 一个基础的规则过滤提取器
    """

    @override
    def _filter_by_rule(self, data_json: DataJson) -> bool:
        """根据规则过滤content_list.

        Args:
            data_json (DataJson): 判断content_list是否是自己想要拦截处理的数据

        Returns:
            bool: 如果是希望处理的数据，返回True，否则返回False
        """
        return True

    @override
    def _do_post_extract(self, data_json: DataJson) -> DataJson:
        """实现真正的数据提取.

        Args:
            data_json (DataJson): 需要处理的数据集
        """
        return data_json
