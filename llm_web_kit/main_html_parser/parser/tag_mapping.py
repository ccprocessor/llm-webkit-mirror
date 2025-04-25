from llm_web_kit.input.pre_data_json import PreDataJson, PreDataJsonKey
from llm_web_kit.main_html_parser.parser.parser import BaseMainHtmlParser


class MapItemToHtmlTagsParser(BaseMainHtmlParser):
    def parse(self, pre_data: PreDataJson) -> PreDataJson:
        """将item_id与原html网页tag进行映射.

        Args:
            pre_data (PreDataJson): 包含LLM抽取结果的PreDataJson对象

        Returns:
            PreDataJson: 包含映射结果的PreDataJson对象
        """
        # tag映射逻辑
        # ...

        # 设置输出数据
        pre_data[PreDataJsonKey.HTML_ELEMENT_LIST] = []

        return pre_data
