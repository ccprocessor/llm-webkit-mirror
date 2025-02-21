from overrides import override

from llm_web_kit.input.datajson import DataJson
from llm_web_kit.pipeline.formatter.base import AbstractFormatter


class HTMLFormatter(AbstractFormatter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @override
    def format(self, data_json: DataJson) -> DataJson:
        return data_json
