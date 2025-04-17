from llm_web_kit.input.pre_data_json import PreDataJson, PreDataJsonKey
from llm_web_kit.main_html_parser.parser.parser import BaseMainHtmlParser


class LayoutSubtreeParser(BaseMainHtmlParser):
    def parse(self, pre_data: PreDataJson) -> PreDataJson:
        """根据上一步映射html的tag，抽取layout代表网页的子树.

        Args:
            pre_data (PreDataJson): 包含tag映射结果的PreDataJson对象

        Returns:
            PreDataJson: 包含子树结构的PreDataJson对象
        """
        # 子树抽取逻辑
        # ...

        # 设置输出数据
        pre_data[PreDataJsonKey.HTML_TARGET_LIST] = []

        return pre_data
