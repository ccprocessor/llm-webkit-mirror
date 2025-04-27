from llm_web_kit.exception.exception import TypicalHtmlSelectorParserException
from llm_web_kit.input.pre_data_json import PreDataJson, PreDataJsonKey
from llm_web_kit.main_html_parser.parser.parser import BaseMainHtmlParser
from llm_web_kit.main_html_parser.typical_html.typical_html import \
    select_representative_html


class TypicalHtmlSelectorParser(BaseMainHtmlParser):
    def parse(self, pre_data: PreDataJson) -> PreDataJson:
        """以layout粒度，找出当前批次layout中1个具有代表性的网页（内容区域深度、宽度最大的最优）

        Args:
            pre_data (PreDataJson): 包含layout信息的PreDataJson对象

        Returns:
            PreDataJson: 包含代表性网页的PreDataJson对象
        """
        # 选择代表性网页逻辑
        layout_file_list = pre_data.get(PreDataJsonKey.LAYOUT_FILE_LIST, [])
        try:
            typical_html = select_representative_html(layout_file_list)
        except TypicalHtmlSelectorParserException as e1:
            raise e1
        except Exception as e2:
            raise e2
        # 设置输出数据
        pre_data[PreDataJsonKey.TYPICAL_RAW_HTML] = typical_html

        return pre_data
