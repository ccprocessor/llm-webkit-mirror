from typing import Any, Type

from llm_web_kit.model.domain_safety_detector import DomainFilter
from llm_web_kit.model.source_safety_detector import SourceFilter
from llm_web_kit.model.unsafe_words_detector import UnsafeWordsFilter


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


class RuleBasedSafetyModuleDataPack:
    """The data pack for the rule-based-safety module."""

    def __init__(
        self,
        content_str: str,
        language: str,
        language_details: str,
        content_style: str,
        url: str,
        dataset_name: str,
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
        check_type('content_style', content_style, str)
        self.content_style = content_style

        # the url of the content
        check_type('url', url, str)
        self.url = url

        # the data source of the content
        check_type('dataset_name', dataset_name, str)
        self.dataset_name = dataset_name

        # the flag of the processed data should be remained or not
        self.safety_remained = True
        # the details of the clean process
        self.safety_infos = {}

    def set_process_result(self, safety_remained: bool, safety_infos: dict) -> None:
        """set the process result of the rule_based_safety module."""
        check_type('safety_remained', safety_remained, bool)
        check_type('safety_infos', safety_infos, dict)
        if safety_remained is False:
            self.safety_remained = False
        self.safety_infos.update(safety_infos)

    def get_output(self) -> dict:
        """get the output of the data pack."""
        return {
            'safety_remained': self.safety_remained,
            'safety_infos': self.safety_infos,
        }


class RuleBasedSafetyModule:
    def __init__(self, prod: bool):
        # when in production mode
        # the process will return immediately when the data is not safe
        self.prod = prod
        self.domain_filter = DomainFilter()
        self.source_filter = SourceFilter()
        self.unsafe_words_filter = UnsafeWordsFilter()

    def process(
        self,
        content_str: str,
        language: str,
        language_details: str,
        content_style: str,
        url: str,
        dataset_name: str,
    ) -> dict:
        """The process of the rule based safety."""
        data_pack = RuleBasedSafetyModuleDataPack(
            content_str=content_str,
            language=language,
            language_details=language_details,
            content_style=content_style,
            url=url,
            dataset_name=dataset_name,
        )
        data_pack = self.process_core(data_pack)
        return data_pack.get_output()

    def process_core(
        self, data_pack: RuleBasedSafetyModuleDataPack
    ) -> RuleBasedSafetyModuleDataPack:
        """The core process of the rule based safety."""
        content_str = data_pack.content_str
        language = data_pack.language
        language_details = data_pack.language_details
        content_style = data_pack.content_style
        url = data_pack.url
        data_source = data_pack.dataset_name

        domain_safe_remained, domain_safe_info = self.domain_filter.filter(
            content_str, language, url, language_details, content_style
        )
        data_pack.set_process_result(domain_safe_remained, domain_safe_info)
        if not domain_safe_remained and self.prod:
            return data_pack

        source_type_dict = self.source_filter.filter(
            content_str, language, data_source, language_details,content_style
        )

        from_safe_source = source_type_dict['from_safe_source']
        from_domestic_source = source_type_dict['from_domestic_source']
        unsafe_words_remained, process_info = self.unsafe_words_filter.filter(
            content_str,
            language,
            language_details,
            content_style,
            from_safe_source,
            from_domestic_source,
        )
        data_pack.set_process_result(unsafe_words_remained, process_info)
        return data_pack

    def get_version(self):
        version_str = '1.0.0'
        return version_str
