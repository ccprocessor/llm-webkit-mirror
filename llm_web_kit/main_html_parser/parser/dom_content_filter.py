from llm_web_kit.input.pre_data_json import PreDataJson, PreDataJsonKey
from llm_web_kit.main_html_parser.parser.parser import BaseMainHtmlParser


class DomContentFilterParser(BaseMainHtmlParser):
    def parse(self, pre_data: PreDataJson) -> PreDataJson:
        """根据头尾、重复率，删除头尾的导航、广告等节点.

        Args:
            pre_data (PreDataJson): 包含main_html的PreDataJson对象

        Returns:
            PreDataJson: 包含过滤后内容的PreDataJson对象
        """
        # DOM过滤逻辑
        # ...

        # 设置输出数据
        pre_data[PreDataJsonKey.FILTERED_MAIN_HTML] = ''

        return pre_data
