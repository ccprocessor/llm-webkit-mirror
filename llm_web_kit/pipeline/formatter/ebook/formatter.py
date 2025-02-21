# Copyright (c) Opendatalab. All rights reserved.
"""ebook formatter rule."""
from overrides import override

from llm_web_kit.input.datajson import DataJson
from llm_web_kit.pipeline.formatter.base import AbstractFormatter


class EBOOKFormatter(AbstractFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @override
    def format(self, data_json: DataJson) -> DataJson:
        # TODO
        return data_json
