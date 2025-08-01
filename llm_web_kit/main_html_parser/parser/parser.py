from abc import ABC, abstractmethod

from llm_web_kit.input.pre_data_json import PreDataJson


class BaseMainHtmlParser(ABC):
    """主HTML解析器的抽象基类."""

    def __init__(self, config: dict, *args, **kwargs):
        """从参数指定的配置中初始化这个解析器.

        Args:
            config (dict): 配置字典
        """
        self.__config = config

    @abstractmethod
    def parse(self, pre_data: PreDataJson) -> PreDataJson:
        """解析HTML字符串并返回解析后的结果.

        Args:
            html (str): HTML字符串

        Returns:
            str: 解析后的结果
        """

        raise NotImplementedError
