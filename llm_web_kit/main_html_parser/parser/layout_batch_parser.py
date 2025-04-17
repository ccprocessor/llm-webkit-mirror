from llm_web_kit.input.pre_data_json import PreDataJson, PreDataJsonKey
from llm_web_kit.main_html_parser.parser.parser import BaseMainHtmlParser


class LayoutBatchParser(BaseMainHtmlParser):
    def parse(self, pre_data: PreDataJson) -> PreDataJson:
        """根据子树结构，推理同批次layout上的所有网页，输出main_html.

        Args:
            pre_data (PreDataJson): 包含子树结构的PreDataJson对象

        Returns:
            PreDataJson: 包含处理结果的PreDataJson对象
        """
        # 批处理逻辑
        # ...

        # 设置输出数据
        pre_data[PreDataJsonKey.MAIN_HTML] = ''

        return pre_data
