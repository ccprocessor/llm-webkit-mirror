from abc import ABC, abstractmethod

from overrides import override

from llm_web_kit.input.datajson import DataJson


class AbstractFormatter(ABC):

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def format(self, data_json: DataJson) -> DataJson:
        raise NotImplementedError


class NoOpFormatter(AbstractFormatter):
    """一个什么也不做的formatter，架构占位符.

    Args:
        AbstractFormatter (_type_): _description_
    """

    @override
    def format(self, data_json: DataJson) -> DataJson:
        return data_json
