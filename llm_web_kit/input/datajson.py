import json
from abc import ABC, abstractmethod
from typing import Dict, List

from overrides import override

from llm_web_kit.libs.doc_element_type import DocElementType, ParagraphTextType
from llm_web_kit.libs.html_utils import html_to_markdown_table


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


class StructureMapper(ABC):
    """作用是把contentList结构组合转化为另外一个结构 例如，从contentList转化为html, txt, md等等.

    Args:
        object (_type_): _description_
    """
    def __init__(self):
        self.__txt_para_splitter = '\n'
        self.__md_para_splitter = '\n\n'

    def to_html(self):
        raise NotImplementedError('This method must be implemented by the subclass.')

    def to_txt(self, exclude_nodes=DocElementType.MM_NODE_LIST):
        """把content_list转化为txt格式.

        Args:
            exclude_nodes (list): 需要排除的节点类型
        Returns:
            str: txt格式的文本内容
        """
        text_blocks = []  # 每个是个DocElementType规定的元素块之一转换成的文本
        content_lst = self._get_data()
        for page in content_lst:
            for content_lst_node in page:
                if content_lst_node['type'] not in exclude_nodes:
                    txt_content = self.__content_lst_node_2_txt(content_lst_node)
                    if txt_content and len(txt_content) > 0:
                        text_blocks.append(txt_content)

        txt = self.__txt_para_splitter.join(text_blocks)
        txt = txt.strip() + '\n'  # 加上结尾换行符
        return txt

    def to_md(self):
        raise NotImplementedError('This method must be implemented by the subclass.')

    def to_nlp_md(self):
        raise NotImplementedError('This method must be implemented by the subclass.')

    def to_mm_md(self):
        raise NotImplementedError('This method must be implemented by the subclass.')

    def to_x_format(self, exclude_nodes=[], include_nodes=[]):
        raise NotImplementedError('This method must be implemented by the subclass.')

    def to_json(self) -> str:
        content_lst = self._get_data()
        return json.dumps(content_lst, ensure_ascii=False)

    @abstractmethod
    def _get_data(self) -> List[Dict]:
        raise NotImplementedError('This method must be implemented by the subclass.')

    def __content_lst_node_2_txt(self, content_lst_node: dict) -> str:
        """把content_list里定义的每种元素块转化为纯文本格式.

        Args:
            content_lst_node (dict): content_list里定义的每种元素块
        Returns:
            str: 纯文本格式
        """
        node_type = content_lst_node['type']
        if node_type == DocElementType.CODE:
            code = content_lst_node['content']['code_content']
            code = code.strip()
            language = content_lst_node['content'].get('language', '')
            code = f'```{language}\n{code}\n```'
            return code
        elif node_type == DocElementType.EQUATION_INTERLINE:
            math_content = content_lst_node['content']['math_content']
            math_content = math_content.strip()
            math_content = f'$$\n{math_content}\n$$'
            return math_content
        elif node_type == DocElementType.IMAGE:
            image_path = content_lst_node['content']['path']
            image_data = content_lst_node['content']['data']
            image_alt = content_lst_node['content']['alt']
            image_title = content_lst_node['content']['title']
            image_caption = content_lst_node['content']['caption']

            if image_alt:
                image_alt = image_alt.strip()
            if image_title:
                image_title = image_title.strip()
            if image_caption:
                image_caption = image_caption.strip()

            image_des = image_title if image_title else image_caption if image_caption else ''
            # 优先使用data, 其次path.其中data是base64编码的图片，path是图片的url
            if image_data:
                image = f'![{image_alt}]({image_data} "{image_des}")'
            elif image_path:
                image = f'![{image_alt}]({image_path} "{image_des}")'
            else:
                image = f'![{image_alt}]({image_path} "{image_des}")'
            return image
        elif node_type == DocElementType.AUDIO:
            return ''
        elif node_type == DocElementType.VIDEO:
            return ''
        elif node_type == DocElementType.TITLE:
            title_content = content_lst_node['content']['title_content']
            title_content = (title_content or '').strip()
            return title_content
        elif node_type == DocElementType.PARAGRAPH:
            paragraph_el_lst = content_lst_node['content']
            one_para = self.__join_one_para(paragraph_el_lst)
            return one_para
        elif node_type == DocElementType.LIST:
            items_paras = []
            for item in content_lst_node['content']['items']:
                paras_of_item = []
                for para in item:
                    one_para = self.__join_one_para(para)
                    paras_of_item.append(one_para)
                items_paras.append(paras_of_item)
            items_paras = [self.__txt_para_splitter.join(item) for item in items_paras]
            return self.__txt_para_splitter.join(items_paras)   # 对于txt格式来说一个列表项里多个段落没啥问题，但是对于markdown来说，多个段落要合并成1个，否则md格式无法表达。
        elif node_type == DocElementType.TABLE:
            # 对文本格式来说，普通表格直接转为md表格，复杂表格返还原始html
            html_table = content_lst_node['content']['html']
            html_table = html_table.strip()
            is_complex = content_lst_node['content']['is_complex']
            if is_complex:
                return html_table
            else:
                md_table = html_to_markdown_table(html_table)
                return md_table
        elif node_type == DocElementType.EQUATION_INTERLINE:
            math_content = content_lst_node['content']['math_content']
            math_content = math_content.strip()
            math_content = f'$$\n{math_content}\n$$'
            return math_content
        else:
            raise ValueError(f'content_lst_node contains invalid element type: {node_type}')  # TODO: 自定义异常

    def __join_one_para(self, para: list) -> str:
        """把一个段落的元素块连接起来.

        Args:
            para (list): 一个段落的元素块
        Returns:
            str: 连接后的字符串
        """
        one_para = []
        for el in para:
            if el['t'] == ParagraphTextType.TEXT:
                one_para.append(el['c'].strip())
            elif el['t'] == ParagraphTextType.EQUATION_INLINE:
                one_para.append(f" ${el['c'].strip()}$ ")
            else:
                raise ValueError(f'paragraph_el_lst contains invalid element type: {el["t"]}')

        return ''.join(one_para)


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
        super().__init__()
        if json_data_lst is None:
            json_data_lst = []
        self.__content_list = json_data_lst

    def length(self) -> int:
        return len(self.__content_list)

    def append(self, content: dict):
        self.__content_list.append(content)

    def __getitem__(self, key):
        return self.__content_list[key]  # 提供读取功能

    def __setitem__(self, key, value):
        self.__content_list[key] = value  # 提供设置功能

    def __delitem__(self, key):
        del self.__content_list[key]

    @override
    def _get_data(self) -> List[Dict]:
        return self.__content_list


class DataJson(StructureChecker):
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
