from llm_web_kit.input.pre_data_json import PreDataJson, PreDataJsonKey
from llm_web_kit.main_html_parser.parser.parser import BaseMainHtmlParser


class LayoutClusteringParser(BaseMainHtmlParser):
    """将同一domain下的HTML按layout结构进行聚类处理器."""

    def parse(self, pre_data: PreDataJson) -> PreDataJson:
        """将同一个domain下layout结构相同的html进行聚类分组.

        Args:
            pre_data (PreDataJson): 包含domain信息的PreDataJson对象

        Returns:
            PreDataJson: 包含layout聚类结果的PreDataJson对象
        """
        # 获取domain信息
        # domain_name = pre_data.get(PreDataJsonKey.DOMAIN_NAME, '')
        # domain_id = pre_data.get(PreDataJsonKey.DOMAIN_ID, '')

        # 处理layout聚类逻辑
        # ...

        # 设置输出数据
        pre_data[PreDataJsonKey.LAYOUT] = ''
        pre_data[PreDataJsonKey.LAYOUT_FILE_LIST] = []

        return pre_data
