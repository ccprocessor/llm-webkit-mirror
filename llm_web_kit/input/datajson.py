import json


class DataJsonKey(object):
    """DataJson的键值key常量定义."""
    DATASET_NAME = 'dataset_name'
    FILE_FORMAT = 'data_source_category'
    CONTENT_LIST = 'content_list'


class DataSourceCategory(object):
    """数据源类型常量定义.

    这是对我们将要处理的数据的一种分类：
    """
    HTML = 'HTML'
    CC = 'CC'
    LAB_CC = 'LAB_CC'
    EBOOK = 'EBOOK'
    PDF = 'PDF'
    # audio 和video目前没有做任何处理
    AUDIO = 'AUDIO'
    VIDEO = 'VIDEO'
    # txt和md基本是从网上直接下载的开源数据
    TXT = 'TXT'
    MD = 'MD'


class StructureMapper(object):
    """作用是把contentList结构组合转化为另外一个结构 例如，从contentList转化为html, txt, md等等.

    Args:
        object (_type_): _description_
    """

    def to_html(self):
        pass

    def to_txt(self):
        pass

    def to_md(self):
        pass

    def to_nlp_md(self):
        pass

    def to_mm_md(self):
        pass

    def to_x_format(self, exclude_nodes=[], include_nodes=[]):
        pass

    def to_json(self) -> str:
        return json.dumps(self.__content_list, ensure_ascii=False)


class StructureChecker(object):

    def _validate(self, json_obj: dict):
        """校验json_obj是否符合要求 如果不符合要求就抛出异常.

        Args:
            json_obj (dict): _description_
        """
        if not isinstance(json_obj, dict):
            raise ValueError('json_obj must be a dict type.')
        if DataJsonKey.CONTENT_LIST in json_obj:
            if not isinstance(json_obj[DataJsonKey.CONTENT_LIST], list):
                raise ValueError('content_list must be a list type.')


class ContentList(StructureMapper):
    """content_list格式的工具链实现."""

    def __init__(self, json_data_lst: list):
        if json_data_lst is None:
            json_data_lst = []
        self.__content_list = json_data_lst

    def length(self) -> int:
        return len(self.__content_list)

    def append(self, content: dict):
        self.__content_list.append(content)


class DataJson(StructureMapper, StructureChecker):
    """从json文件中读取数据."""

    def __init__(self, input_data: dict):
        """初始化DataJson对象，对象必须满足一定的格式，这里进行一些校验.

        Args:
            input_data (dict): _description_
        """
        self._validate(input_data)
        self.__json_data = input_data
        if DataJsonKey.CONTENT_LIST in input_data:
            self.__json_data[DataJsonKey.CONTENT_LIST] = ContentList(input_data[DataJsonKey.CONTENT_LIST])
        if DataJsonKey.CONTENT_LIST not in self.__json_data:
            self.__json_data[DataJsonKey.CONTENT_LIST] = ContentList([])

    def __getitem__(self, key):
        return self.__json_data[key]  # 提供读取功能

    def __setitem__(self, key, value):
        self.__json_data[key] = value  # 提供设置功能

    def __delitem__(self, key):
        del self.__json_data[key]

    def get_dataset_name(self) -> str:
        return self.__json_data[DataJsonKey.DATASET_NAME]

    def get_file_format(self) -> str:
        return self.__json_data[DataJsonKey.FILE_FORMAT]

    def get_content_list(self) -> ContentList:
        cl = self.__json_data[DataJsonKey.CONTENT_LIST]
        return cl

    def get(self, key:str, default=None):
        return self.__json_data.get(key, default)
