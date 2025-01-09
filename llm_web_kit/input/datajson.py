import json


class DataJsonKey(object):
    """DataJson的键值常量定义."""
    DATASET_NAME = 'dataset_name'
    FILE_FORMAT = 'file_format'
    CONTENT_LIST = 'content_list'


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
        pass  # TODO: 实现这个方法, 根据不同的输入标准进行检查


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
        if DataJsonKey.CONTENT_LIST not in self.__json_data:  # 保证content_list一定存在
            self.__json_data[DataJsonKey.CONTENT_LIST] = ContentList([])
        else:
            self.__json_data[DataJsonKey.CONTENT_LIST] = ContentList(self.__json_data[DataJsonKey.CONTENT_LIST])

    def __getitem__(self, key):
        return self.__json_data[key]  # 提供读取功能

    def __setitem__(self, key, value):
        self.__json_data[key] = value  # 提供设置功能

    def get_dataset_name(self) -> str:
        return self.__json_data[DataJsonKey.DATASET_NAME]

    def get_file_format(self) -> str:
        return self.__json_data[DataJsonKey.FILE_FORMAT]

    def get_content_list(self) -> ContentList:
        cl = self.__json_data[DataJsonKey.CONTENT_LIST]
        return cl
