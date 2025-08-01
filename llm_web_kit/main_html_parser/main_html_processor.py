import traceback
from typing import Any, Dict

from llm_web_kit.input.pre_data_json import PreDataJson
from llm_web_kit.main_html_parser.parser.domain_clustering import \
    DomainClusteringParser
from llm_web_kit.main_html_parser.parser.layout_batch_parser import \
    LayoutBatchParser
from llm_web_kit.main_html_parser.parser.layout_clustering import \
    LayoutClusteringParser
from llm_web_kit.main_html_parser.parser.layout_subtree_parser import \
    LayoutSubtreeParser
from llm_web_kit.main_html_parser.parser.llm_main_identifier import \
    LlmMainIdentifierParser
from llm_web_kit.main_html_parser.parser.tag_mapping import \
    MapItemToHtmlTagsParser
from llm_web_kit.main_html_parser.parser.tag_simplifier import \
    HtmlTagSimplifierParser
from llm_web_kit.main_html_parser.parser.typical_html_selector import \
    TypicalHtmlSelectorParser
from llm_web_kit.main_html_parser.processor import AbstractProcessor


class MainHtmlProcessor(AbstractProcessor):
    """MAIN HTML处理器基类，实现通用的处理流程和错误处理."""

    def __init__(self, config: Dict[str, Any] = None, *args, **kwargs):
        """初始化处理器.

        Args:
            config (Dict[str, Any], optional): 配置信息
        """
        super().__init__(config, *args, **kwargs)
        self.__domain_clustering_parser = DomainClusteringParser()
        self.__layout_batch_parser = LayoutBatchParser()
        self.__layout_clustering_parser = LayoutClusteringParser()
        self.__layout_subtree_parser = LayoutSubtreeParser()
        self.__llm_main_identifier = LlmMainIdentifierParser()
        self.__tag_mapping = MapItemToHtmlTagsParser()
        self.__tag_simplifier = HtmlTagSimplifierParser()
        self.__typical_html_selector = TypicalHtmlSelectorParser()

    def _do_process(self, pre_data: PreDataJson) -> PreDataJson:
        """执行处理逻辑，包含通用的前后处理和日志记录.

        Args:
            pre_data (PreDataJson): 包含处理数据的PreDataJson对象

        Returns:
            PreDataJson: 处理后的PreDataJson对象
        """
        try:
            # 核心处理逻辑
            for parser_func in [self.__domain_clustering_parser, self.__layout_batch_parser, self.__layout_clustering_parser,
                                self.__layout_subtree_parser, self.__llm_main_identifier, self.__tag_mapping,
                                self.__tag_simplifier, self.__typical_html_selector]:
                pre_data = parser_func.parse(pre_data)

            return pre_data
        except Exception as e:
            e.trace_info = traceback.format_exc()
            raise e
