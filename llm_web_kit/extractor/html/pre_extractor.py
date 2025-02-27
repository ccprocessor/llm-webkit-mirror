import os

from overrides import override

from llm_web_kit.extractor.pre_extractor import \
    BaseFileFormatFilterPreExtractor
from llm_web_kit.input.datajson import DataJson
from llm_web_kit.libs.html_utils import html_to_element
from llm_web_kit.libs.path_lib import get_proj_root_dir


class HTMLFileFormatFilterPreExtractor(BaseFileFormatFilterPreExtractor):
    """实现一个基础的HTML文件格式预处理类 例如，根据文件名的后缀拦截数据并进行基础的预处理.

    Args:
        BaseFileFormatFilterPreExtractor (_type_): _description_
    """

    def __init__(self, config: dict):
        super().__init__(config)

    @override
    def _filter_by_rule(self, data_json: DataJson) -> bool:
        return self.is_html_format(data_json)

    @override
    def _do_pre_extract(self, data_json: DataJson) -> DataJson:
        pass  # TODO
        return data_json


class HTMLFileFormatFilterTablePreExtractor(HTMLFileFormatFilterPreExtractor):
    def __init__(self, config: dict):
        super().__init__(config)

    @override
    def _filter_by_rule(self, data_json: DataJson) -> bool:
        if self.__remove_format_table(data_json):
            return True
        else:
            return False

    @override
    def _do_pre_extract(self, data_json: DataJson) -> DataJson:
        pass  # TODO
        return data_json

    def __remove_format_table(self, data_json: DataJson):
        """remove 排版table."""
        html_content = data_json['html']
        html_str = html_to_element(html_content)
        first_structure = html_str.xpath('/html/body/table') != []
        second_structure = html_str.xpath('/html/body/center/table') != []
        if bool(first_structure and second_structure):
            return True
        else:
            return False


class TestHTMLFileFormatFilterPreExtractor(HTMLFileFormatFilterPreExtractor):
    """为了方便对测试数据进行测试，需要吧测试数据的格式转换为处理HTML数据的标准的DataJson格式
    也就是测试数据的html以文件放在磁盘路径下，但是标准的DataJson格式是html以字符串的形式存在于jsonl中的html字段里。
    这个类就是根据路径读取html文件，然后转换为DataJson格式。"""

    def __init__(self, config: dict, html_parent_dir: str):
        """
        初始化函数
        Args:
            config:
            html_parent_dir:
        """
        super().__init__(config)
        self.__html_parent_path = html_parent_dir

    @override
    def _do_pre_extract(self, data_json: DataJson) -> DataJson:
        """对输入的单个html拼装到DataJson中，形成标准输入格式."""
        proj_root_dir = get_proj_root_dir()
        html_file_path = os.path.join(proj_root_dir, self.__html_parent_path, data_json.get('path'))

        with open(html_file_path, 'r', encoding='utf-8') as f:
            html = f.read()
            data_json['html'] = html
            del data_json['path']
        return data_json
