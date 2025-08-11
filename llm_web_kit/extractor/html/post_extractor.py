from overrides import override

from llm_web_kit.extractor.post_extractor import BaseFileFormatPostExtractor
from llm_web_kit.input.datajson import DataJson, DataJsonKey
from llm_web_kit.libs.doc_element_type import DocElementType, ParagraphTextType
from llm_web_kit.libs.statics import Statics
from llm_web_kit.libs.text_utils import normalize_text_segment


class HTMLFileFormatPostExtractor(BaseFileFormatPostExtractor):
    """一个从html文件中提取数据的提取器.

    Args:
        BaseFileFormatPostExtractor (_type_): 一个基础的规则过滤提取器
    """

    @override
    def _filter_by_rule(self, data_json: DataJson) -> bool:
        """根据规则过滤content_list.

        Args:
            data_json (DataJson): 判断content_list是否是自己想要拦截处理的数据

        Returns:
            bool: 如果是希望处理的数据，返回True，否则返回False
        """
        return self.is_html_format(data_json)

    @override
    def _do_post_extract(self, data_json: DataJson) -> DataJson:
        """实现真正的数据提取.

        Args:
            data_json (DataJson): 需要处理的数据集
        """
        # TODO
        raise NotImplementedError('Subclass must implement abstract method')


class ContentListStripSpacePostExtractor(BaseFileFormatPostExtractor):
    """对段落文本进行处理：
    1. 连续的多个空格转换成1个
    2. 连续的\t转换成1个
    3. 连续的\n转换成1个
    4. 连续的\r转换成1个
    5. 连续的\f转换成1个
    6. 连续的\v转换成1个
    7. 去掉不可见字符、乱码

    Args:
        BaseFileFormatPostExtractor (_type_): 一个基础的规则过滤提取器
    """
    @override
    def _filter_by_rule(self, data_json: DataJson) -> bool:
        """根据规则过滤content_list.

        Args:
            data_json (DataJson): 判断content_list是否是自己想要拦截处理的数据

        Returns:
            bool: 如果是希望处理的数据，返回True，否则返回False
        """
        content_list = data_json.get_content_list()
        return content_list.length() >= 1  # 需要有内容才进行处理

    @override
    def _do_post_extract(self, data_json: DataJson) -> DataJson:
        """对content_list中的文本数据进行标准化。

        Args:
            data_json (DataJson): 需要处理的数据集
        """
        contnet_list = data_json.get_content_list()
        for page in contnet_list:
            for content_node in page:
                # 只对list和paragraph进行处理
                if content_node['type'] == DocElementType.PARAGRAPH:
                    content_node['content'] = self.__do_normalize_text(content_node['content'])
                elif content_node['type'] == DocElementType.TITLE:
                    content_node['content']['title_content'] = normalize_text_segment(content_node['content']['title_content'])
        return data_json

    def __do_normalize_text(self, paragraph: list[dict]) -> list[dict]:
        """对文本进行标准化处理.

        Args:
            text (str): 需要处理的文本

        Returns:
            str: 处理后的文本
        """
        for segment in paragraph:
            text = segment['c']
            text_type = segment['t']
            if text_type not in [ParagraphTextType.CODE_INLINE]:  # skip code & math
                segment['c'] = normalize_text_segment(text)
        return paragraph


class ContentListStaticsPostExtractor(BaseFileFormatPostExtractor):
    """对content_list中的元素进行统计.

    Args:
        BaseFileFormatPostExtractor (_type_): 一个基础的规则过滤提取器
    Returns:
        DataJson: 返回处理后的数据集，新增statics字段，示例：
        {
            "meta_data": {
                "statics": {
                    "list": 1,
                    "list.text": 2,
                    "list.equation-inline": 1,
                    "paragraph": 2,
                    "paragraph.text": 2,
                    "equation-interline": 1
                }
            }
        }
    """

    @override
    def _filter_by_rule(self, data_json: DataJson) -> bool:
        """根据规则过滤content_list.

        Args:
            data_json (DataJson): 判断content_list是否是自己想要拦截处理的数据

        Returns:
            bool: 如果是希望处理的数据，返回True，否则返回False
        """
        return True

    @override
    def _do_post_extract(self, data_json: DataJson) -> DataJson:
        """对content_list中的元素进行统计.

        Args:
            data_json (DataJson): 需要处理的数据集
        """
        content_list = data_json.get_content_list()
        statics_obj = Statics()
        meta_data = data_json.get(DataJsonKey.METAINFO, {})
        meta_data[DataJsonKey.STATICS] = statics_obj.get_statics(content_list)
        data_json.__setitem__(DataJsonKey.METAINFO, meta_data)
        return data_json
