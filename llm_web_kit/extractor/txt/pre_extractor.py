# Copyright (c) Opendatalab. All rights reserved.
"""Data extraction pre-processing program."""
from overrides import override

from llm_web_kit.extractor.pre_extractor import \
    BaseFileFormatFilterPreExtractor
from llm_web_kit.input.datajson import DataJson


class TXTFileFormatFilterPreExtractor(BaseFileFormatFilterPreExtractor):
    """Process the data before extraction according to the rules.

    Args:
        BaseFileFormatFilterPreExtractor (_type_): _description_
    """

    def __init__(self, config: dict):
        super().__init__(config)

    @override
    def _filter_by_rule(self, data_json: DataJson) -> bool:
        """Filter data_json according to rules.

        Args:
            data_json:
        Returns:
        """
        return self.is_txt_format(data_json)

    @override
    def _do_pre_extract(self, data_json: DataJson) -> DataJson:
        """Pre-extraction data processing program.

        Args:
            data_json:
        Returns:
        """
        # TODO
        raise NotImplementedError('Subclass must implement abstract method')
