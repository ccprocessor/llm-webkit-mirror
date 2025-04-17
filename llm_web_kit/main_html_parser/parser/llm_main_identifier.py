from llm_web_kit.input.pre_data_json import PreDataJson, PreDataJsonKey
from llm_web_kit.main_html_parser.parser.parser import BaseMainHtmlParser


class LlmMainIdentifierParser(BaseMainHtmlParser):
    def parse(self, pre_data: PreDataJson) -> PreDataJson:
        """结合prompt提示词，对精简后的html网页进行正文内容（即main_html）框定，输出item_id结构的页面判定结果.

        Args:
            pre_data (PreDataJson): 包含精简HTML的PreDataJson对象

        Returns:
            PreDataJson: 包含LLM抽取结果的PreDataJson对象
        """
        # 大模型抽取逻辑
        # ...

        # 设置输出数据
        pre_data[PreDataJsonKey.LLM_RESPONSE] = {}

        return pre_data
