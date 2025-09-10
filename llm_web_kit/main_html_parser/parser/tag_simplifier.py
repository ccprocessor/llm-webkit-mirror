from llm_web_kit.exception.exception import TagSimplifiedParserException
from llm_web_kit.input.pre_data_json import PreDataJson, PreDataJsonKey
from llm_web_kit.main_html_parser.parser.parser import BaseMainHtmlParser
from llm_web_kit.main_html_parser.simplify_html.simplify_html import \
    simplify_html


class HtmlTagSimplifierParser(BaseMainHtmlParser):
    """HTML标签简化处理器."""

    def parse(self, pre_data: PreDataJson) -> PreDataJson:
        """简化HTML结构.

        Args:
            pre_data (PreDataJson): 包含原始HTML的PreDataJson对象

        Returns:
            PreDataJson: 包含简化后HTML的PreDataJson对象
        """
        # 获取输入数据
        typical_raw_html = pre_data.get(PreDataJsonKey.TYPICAL_RAW_HTML, '')
        # layout_file_list = pre_data.get(PreDataJsonKey.LAYOUT_FILE_LIST, [])

        # 执行HTML标签简化逻辑
        try:
            simplified_html, original_html = simplify_html(typical_raw_html)
        except TagSimplifiedParserException as e1:
            raise e1
        except Exception as e2:
            raise e2

        # 设置输出数据
        pre_data[PreDataJsonKey.TYPICAL_RAW_TAG_HTML] = original_html  # 保存原始标签HTML
        pre_data[PreDataJsonKey.TYPICAL_SIMPLIFIED_HTML] = simplified_html  # 保存简化后的HTML

        return pre_data
