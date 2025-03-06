# Copyright (c) Opendatalab. All rights reserved.
"""Actual data extraction main program."""
from overrides import override

from llm_web_kit.extractor.extractor import BaseFileFormatExtractor
from llm_web_kit.input.datajson import DataJson


class PDFFileFormatExtractor(BaseFileFormatExtractor):
    """An extractor for extracting data from pdf files.

    Args:
        BaseFileFormatExtractor (_type_): _description_
    """

    def __init__(self, config: dict):
        super().__init__(config)

    @override
    def _filter_by_rule(self, data_json: DataJson) -> bool:
        """Filter data_json according to rules.

        Args:
            data_json (ContentList): Determine whether content_list is the data you want to intercept and process.
        Returns:
            bool: If it is the data you want to process, return True, otherwise return False.
        """
        return self.is_pdf_format(data_json)

    @override
    def _do_extract(self, data_json: DataJson) -> DataJson:
        """The actual data extraction process.

        Args:
            data_json (ContentList): Datasets to be processed.
        """
        # TODO
        return data_json
