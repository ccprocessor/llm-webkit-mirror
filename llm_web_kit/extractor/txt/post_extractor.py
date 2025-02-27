# Copyright (c) Opendatalab. All rights reserved.
"""Data extraction post-processing program."""
from overrides import override

from llm_web_kit.extractor.post_extractor import BaseFileFormatPostExtractor
from llm_web_kit.input.datajson import DataJson


class TXTFileFormatPostExtractor(BaseFileFormatPostExtractor):
    """Process the extracted data after extraction according to the rules.

    Args:
        BaseFileFormatPostExtractor (_type_): _description_
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
    def _do_post_extract(self, data_json: DataJson) -> DataJson:
        """
        Post-extraction data processing procedures.
        Args:
            data_json:

        Returns:

        """
        # TODO
        raise NotImplementedError('Subclass must implement abstract method')
