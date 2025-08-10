import copy
import json
from typing import Any, Dict, Iterator, List, Tuple


class PreDataJsonKey:
    """PreDataJson的键值key常量定义."""
    DOMAIN_NAME = 'domain_name'
    DOMAIN_ID = 'domain_id'
    DOMAIN_FILE_LIST = 'domain_file_list'
    LAYOUT_NAME = 'layout_name'
    LAYOUT_ID = 'layout_id'
    LAYOUT_FILE_LIST = 'layout_file_list'
    RECORD_COUNT = 'record_count'

    TYPICAL_RAW_HTML = 'typical_raw_html'
    TYPICAL_RAW_TAG_HTML = 'typical_raw_tag_html'
    IS_XPATH = 'is_xpath'
    XPATH_MAPPING = 'xpath_mapping'
    TYPICAL_SIMPLIFIED_HTML = 'typical_simplified_html'
    # 模型打标字典
    LLM_RESPONSE = 'llm_response'
    # 模型结果都为0
    LLM_RESPONSE_EMPTY = 'llm_response_empty'
    # 映射模版正文树结构的元素字典
    HTML_ELEMENT_DICT = 'html_element_dict'
    # 映射模版正文时的文本列表
    HTML_TARGET_LIST = 'html_target_list'
    # 相似度计算层数
    SIMILARITY_LAYER = 'similarity_layer'
    # 模版网页提取的正文html
    TYPICAL_MAIN_HTML = 'typical_main_html'
    # 模版网页提取正文成功标签, bool类型
    TYPICAL_MAIN_HTML_SUCCESS = 'typical_main_html_success'
    # similarity between typical main html and html
    TYPICAL_MAIN_HTML_SIM = 'typical_main_html_sim'
    # 用于生成element dict的html
    TYPICAL_DICT_HTML = 'typical_dict_html'
    # 动态id开关
    DYNAMIC_ID_ENABLE = 'dynamic_id_enable'
    # 动态classid开关
    DYNAMIC_CLASSID_ENABLE = 'dynamic_classid_enable'
    # 动态classid相似度阈值
    DYNAMIC_CLASSID_SIM_THRESH = 'dynamic_classid_similarity_threshold'
    # 正文噪音开关
    MORE_NOISE_ENABLE = 'more_noise_enable'
    # 推广原网页
    HTML_SOURCE = 'html_source'
    # 推广网页提取正文成功标签, bool类型
    MAIN_HTML_SUCCESS = 'main_html_success'
    # similarity between main html and typical main html
    MAIN_HTML_SIM = 'main_html_sim'
    # 推广网页提取正文文本
    MAIN_HTML = 'main_html'
    # 推广网页提取正文树
    MAIN_HTML_BODY = 'main_html_body'
    FILTERED_MAIN_HTML = 'filtered_main_html'


class PreDataJson:
    """数据结构PreDataJson，用于存储HTML解析过程中的中间数据.

    该类实现了类似字典的访问方式，可以通过obj[key]方式读写数据
    """

    def __init__(self, input_data: dict = None):
        """初始化PreDataJson对象.

        Args:
            input_data (dict): 初始数据
        """
        copied_data = copy.deepcopy(input_data) if input_data else {}
        self.__pre_data = copied_data
        if PreDataJsonKey.LAYOUT_FILE_LIST not in self.__pre_data:
            self.__pre_data[PreDataJsonKey.LAYOUT_FILE_LIST] = []

    def __getitem__(self, key: str) -> Any:
        """通过obj[key]方式获取数据.

        Args:
            key (str): 键名

        Returns:
            返回key对应的值

        Raises:
            KeyError: 如果key不存在
        """
        return self.__pre_data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        """通过obj[key] = value方式设置数据

        Args:
            key (str): 键名
            value: 值
        """
        self.__pre_data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """获取数据.

        Args:
            key (str): 键名
            default: 默认返回值，如果key不存在

        Returns:
            返回key对应的值，如果key不存在返回default
        """
        return self.__pre_data.get(key, default)

    def keys(self) -> Iterator[str]:
        """返回所有键名的迭代器.

        Returns:
            Iterator[str]: 键名迭代器
        """
        return self.__pre_data.keys()

    def values(self) -> Iterator[Any]:
        """返回所有值的迭代器.

        Returns:
            Iterator[Any]: 值迭代器
        """
        return self.__pre_data.values()

    def items(self) -> Iterator[Tuple[str, Any]]:
        """返回所有键值对的迭代器.

        Returns:
            Iterator[Tuple[str, Any]]: 键值对迭代器
        """
        return self.__pre_data.items()

    def __contains__(self, key: str) -> bool:
        """通过key in obj方式判断键是否存在.

        Args:
            key (str): 键名

        Returns:
            bool: 如果key存在返回True，否则返回False
        """
        return key in self.__pre_data

    def get_layout_file_list(self) -> List[str]:
        """获取layout_file_list.

        Returns:
            List[str]: layout_file_list
        """
        return self.__pre_data[PreDataJsonKey.LAYOUT_FILE_LIST]

    def to_json(self, pretty: bool = False) -> str:
        """将PreDataJson转换为JSON字符串.

        Args:
            pretty (bool): 是否美化输出的JSON字符串

        Returns:
            str: JSON字符串
        """
        json_dict = self.__pre_data.copy()
        json_dict[PreDataJsonKey.LAYOUT_FILE_LIST] = self.get_layout_file_list()
        if pretty:
            return json.dumps(json_dict, ensure_ascii=False, indent=2)
        return json.dumps(json_dict, ensure_ascii=False)

    def to_dict(self) -> Dict[str, Any]:
        """将PreDataJson转换为字典.

        Returns:
            Dict[str, Any]: 包含所有数据的字典
        """
        json_dict = self.__pre_data.copy()
        json_dict[PreDataJsonKey.LAYOUT_FILE_LIST] = self.get_layout_file_list().to_dict()
        return json_dict
