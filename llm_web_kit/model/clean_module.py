from enum import Enum
from typing import Any, Type

from llm_web_kit.model.quality_model import QualityFilter


# 定义枚举类型 ContentStyle
class ContentStyle(Enum):
    ARTICLE = 'article'
    BOOK = 'book'
    PAPER = 'paper'


def check_type(arg_name: str, arg_value: Any, arg_type: Type):
    """check the type of the argument and raise TypeError if the type is not
    matched."""
    if not isinstance(arg_value, arg_type):
        # TODO change TypeError to custom exception
        raise TypeError(
            'The type of {} should be {}, but got {}'.format(
                arg_name, arg_type, type(arg_value)
            )
        )


class CleanModuleDataPack:
    """The data pack for the clean module."""

    def __init__(
        self,
        content_str: str,
        language: str,
        language_details: str,
        content_style: ContentStyle,
    ):

        # the content of the dataset
        check_type('content_str', content_str, str)
        self.content_str = content_str

        # the language of the content
        check_type('language', language, str)
        self.language = language

        # the details of the language
        check_type('language_details', language_details, str)
        self.language_details = language_details

        # the content style of the content
        check_type('content_style', content_style, ContentStyle)

        self.content_style = content_style.value

        # the flag of the processed data should be remained or not
        self.clean_remained = True
        # the details of the clean process
        self.clean_infos = {}

    def set_process_result(self, clean_remained: bool, clean_infos: dict) -> None:
        """set the process result of the clean module."""
        check_type('clean_remained', clean_remained, bool)
        check_type('clean_infos', clean_infos, dict)
        if clean_remained is False:
            self.clean_remained = False
        self.clean_infos.update(clean_infos)

    def get_output(self) -> dict:
        """get the output of the data pack."""
        return {
            'clean_remained': self.clean_remained,
            'clean_infos': self.clean_infos,
        }


class CleanModule:
    def __init__(self, prod: bool):
        # when in production mode
        # the process will return immediately when the data is not clean
        self.prod = prod
        self.quality_filter = QualityFilter()

    def process(
        self,
        content_str: str,
        language: str,
        language_details: str,
        content_style: str,
    ) -> dict:
        """The process of the rule based safety."""
        data_pack = CleanModuleDataPack(
            content_str=content_str,
            language=language,
            language_details=language_details,
            content_style=content_style,
        )
        data_pack = self.process_core(data_pack)
        return data_pack.get_output()

    def process_core(self, data_pack: CleanModuleDataPack) -> CleanModuleDataPack:
        """The core process of the rule based safety."""
        content_str = data_pack.content_str
        language = data_pack.language
        language_details = data_pack.language_details
        content_style = data_pack.content_style
        remained, process_info = self.quality_filter.filter(
            content_str, language, language_details, content_style
        )
        data_pack.set_process_result(remained, process_info)
        return data_pack

    def get_version(self):
        version_str = '1.0.0'
        return version_str
