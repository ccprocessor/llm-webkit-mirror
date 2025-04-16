import copy
import json
from ast import List
from typing import Any, Dict


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
    TYPICAL_SIMPLIFIED_HTML = 'typical_simplified_html'
    LLM_RESPONSE = 'llm_response'
    HTML_ELEMENT_LIST = 'html_element_list'
    HTML_TARGET_LIST = 'html_target_list'
    MAIN_HTML = 'main_html'
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
        copied_data = copy.deepcopy(input_data)
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
        return self._data.get(key, default)

    def keys(self):
        """返回所有键名的迭代器.

        Returns:
            Iterator[str]: 键名迭代器
        """
        return self.__pre_data.keys()

    def values(self):
        """返回所有值的迭代器.

        Returns:
            Iterator[Any]: 值迭代器
        """
        return self.__pre_data.values()

    def items(self):
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
