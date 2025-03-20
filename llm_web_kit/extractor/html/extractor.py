import os
from typing import List, Tuple

import commentjson as json
from overrides import override

from llm_web_kit.config.cfg_reader import load_config
from llm_web_kit.exception.exception import HtmlFileExtractorException
from llm_web_kit.extractor.extractor import BaseFileFormatExtractor
from llm_web_kit.extractor.html.magic_html import GeneralExtractor
from llm_web_kit.extractor.html.recognizer.audio import AudioRecognizer
from llm_web_kit.extractor.html.recognizer.cccode import CodeRecognizer
from llm_web_kit.extractor.html.recognizer.ccmath import MathRecognizer
from llm_web_kit.extractor.html.recognizer.image import ImageRecognizer
from llm_web_kit.extractor.html.recognizer.list import ListRecognizer
from llm_web_kit.extractor.html.recognizer.recognizer import (
    BaseHTMLElementRecognizer, CCTag)
from llm_web_kit.extractor.html.recognizer.table import TableRecognizer
from llm_web_kit.extractor.html.recognizer.text import TextParagraphRecognizer
from llm_web_kit.extractor.html.recognizer.title import TitleRecognizer
from llm_web_kit.extractor.html.recognizer.video import VideoRecognizer
from llm_web_kit.input.datajson import ContentList, DataJson
from llm_web_kit.libs.html_utils import element_to_html, html_to_element
from llm_web_kit.libs.path_lib import get_py_pkg_root_dir


class HTMLPageLayoutType:
    """网页的布局类型."""
    LAYOUT_ARTICLE = 'article'
    LAYOUT_QA = 'forum'
    LAYOUT_LIST = 'list'


class HTMLFileFormatExtractor(BaseFileFormatExtractor):
    """一个从html文件中提取数据的提取器."""

    def __init__(self, config: dict):
        """从参数指定的配置中初始化这个流水线链.

        Args:
            config (dict): 配置字典
        """
        super().__init__(config)
        self.__code_recognizer:BaseHTMLElementRecognizer = CodeRecognizer()
        self.__math_recognizer:BaseHTMLElementRecognizer = MathRecognizer()
        self.__image_recognizer:BaseHTMLElementRecognizer = ImageRecognizer()
        self.__audio_recognizer:BaseHTMLElementRecognizer = AudioRecognizer()
        self.__video_recognizer:BaseHTMLElementRecognizer = VideoRecognizer()
        self.__table_recognizer:BaseHTMLElementRecognizer = TableRecognizer()
        self.__list_recognizer:BaseHTMLElementRecognizer = ListRecognizer()
        self.__title_recognizer:BaseHTMLElementRecognizer = TitleRecognizer()
        self.__paragraph_recognizer:BaseHTMLElementRecognizer = TextParagraphRecognizer()

        self.__to_content_list_mapper = {
            CCTag.CC_CODE: self.__code_recognizer,
            CCTag.CC_MATH_INTERLINE: self.__math_recognizer,
            CCTag.CC_IMAGE: self.__image_recognizer,
            CCTag.CC_AUDIO: self.__audio_recognizer,
            CCTag.CC_VIDEO: self.__video_recognizer,
            CCTag.CC_TABLE: self.__table_recognizer,
            CCTag.CC_LIST: self.__list_recognizer,
            CCTag.CC_TITLE: self.__title_recognizer,
            CCTag.CC_TEXT: self.__paragraph_recognizer
        }

        self.__magic_html_extractor = self.__build_extractor()

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
    def _do_extract(self, data_json: DataJson) -> DataJson:
        """实现真正的数据提取.

        Args:
            data_json (DataJson): 需要处理的数据集
        """
        # 第一步使用magic-html框选html正文部分
        # 第二步逐步精细解析特定的html标签
        # 第三步将解析结果存入content_list中
        raw_html:str = data_json['html']
        base_url:str = data_json['url']
        page_layout_type:str = data_json.get('page_layout_type', HTMLPageLayoutType.LAYOUT_ARTICLE)  # 默认是文章类型

        main_html, method, title = self._extract_main_html(raw_html, base_url, page_layout_type)
        parsed_html = [(main_html,raw_html)]
        for extract_func in [self._extract_code, self._extract_table, self._extract_math, self._extract_list,
                             self._extract_image,
                             self._extract_title, self._extract_paragraph]:
            parsed_html = extract_func(base_url, parsed_html, raw_html)

        content_list:ContentList = self._export_to_content_list(base_url, parsed_html, raw_html)
        data_json['content_list'] = content_list
        data_json['title'] = title

        return data_json

    def _extract_main_html(self, raw_html:str, base_url:str, page_layout_type:str) -> Tuple[str, str, str]:
        """从html文本中提取主要的内容.

        Args:
            raw_html (str): html文本
            base_url (str): html文本的网页地址
            page_layout_type (str): 网页的布局类型

        Returns:
            str1: 主要的内容
            str2: 获得内容的方式，可对质量进行评估
        """
        dict_result = self.__magic_html_extractor.extract(raw_html, base_url=base_url, precision=False, html_type=page_layout_type)
        return dict_result['html'], dict_result['xp_num'], dict_result.get('title', '')

    def _extract_code(self, base_url:str, html_lst:List[Tuple[str,str]], raw_html:str) -> List[Tuple[str,str]]:
        """从html文本中提取代码.

        Args:
            base_url (str): html文本的网页地址
            html_lst (List[Tuple[str,str]]): html文本
            raw_html (str): html文本
        Returns:
        """

        lst = self.__code_recognizer.recognize(base_url, html_lst, raw_html)
        return lst

    def _extract_math(self, base_url:str, html_lst:List[Tuple[str,str]], raw_html:str) -> List[Tuple[str,str]]:
        """从html文本中提取数学公式.

        Args:
            base_url (str): html文本的网页地址
            html_lst (List[Tuple[str,str]]): html文本
            raw_html (str): html文本

        Returns:
        """

        lst = self.__math_recognizer.recognize(base_url, html_lst, raw_html)
        return lst

    def _extract_image(self, base_url:str, html_lst:List[Tuple[str,str]], raw_html:str) -> List[Tuple[str,str]]:
        """从html文本中提取图片.

        Args:
            base_url (str): html文本的网页地址
            html_lst (List[Tuple[str,str]]): html文本
            raw_html (str): html文本

        Returns:
        """

        lst = self.__image_recognizer.recognize(base_url, html_lst, raw_html)
        return lst

    def _extract_audio(self, base_url:str, html_lst:List[Tuple[str,str]], raw_html:str) -> List[Tuple[str,str]]:
        """从html文本中提取音频.

        Args:
            base_url (str): html文本的网页地址
            html_lst (List[Tuple[str,str]]): html文本
            raw_html (str): html文本

        Returns:
        """

        lst = self.__audio_recognizer.recognize(base_url, html_lst, raw_html)
        return lst

    def _extract_video(self, base_url:str, html_lst:List[Tuple[str,str]], raw_html:str) -> List[Tuple[str,str]]:
        """从html文本中提取视频.

        Args:
            base_url (str): html文本的网页地址
            html_lst (List[Tuple[str,str]]): html文本
            raw_html (str): html文本

        Returns:
        """

        lst = self.__video_recognizer.recognize(base_url, html_lst, raw_html)
        return lst

    def _extract_table(self, base_url:str, html_lst:List[Tuple[str,str]], raw_html:str) -> List[Tuple[str,str]]:
        """从html文本中提取表格.

        Args:
            base_url (str): html文本的网页地址
            html_lst (List[Tuple[str,str]]): html文本
            raw_html (str): html文本

        Returns:
        """

        lst = self.__table_recognizer.recognize(base_url, html_lst, raw_html)
        return lst

    def _extract_list(self, base_url:str, html_lst:List[Tuple[str,str]], raw_html:str) -> List[Tuple[str,str]]:
        """从html文本中提取列表.

        Args:
            base_url (str): html文本的网页地址
            html_lst (List[Tuple[str,str]]): html文本
            raw_html (str): html文本

        Returns:
        """

        lst = self.__list_recognizer.recognize(base_url, html_lst, raw_html)
        return lst

    def _extract_title(self, base_url:str, html_lst:List[Tuple[str,str]], raw_html:str) -> List[Tuple[str,str]]:
        """从html文本中提取标题.

        Args:
            base_url (str): html文本的网页地址
            html_lst (List[Tuple[str,str]]): html文本
            raw_html (str): html文本

        Returns:
        """

        lst = self.__title_recognizer.recognize(base_url, html_lst, raw_html)
        return lst

    def _extract_paragraph(self, base_url:str, html_lst:List[Tuple[str,str]], raw_html:str) -> List[Tuple[str,str]]:
        """从html文本中提取段落.

        Args:
            base_url (str): html文本的网页地址
            html_lst (List[Tuple[str,str]]): html文本
            raw_html (str): html文本

        Returns:
        """

        lst = self.__paragraph_recognizer.recognize(base_url, html_lst, raw_html)
        return lst

    def __is_valid_node(self, node: dict) -> bool:
        """检查节点是否有效(不为空).

        Args:
            node (dict): 内容节点

        Returns:
            bool: 如果节点有效返回True,否则返回False
        """
        if not node:
            raise HtmlFileExtractorException('node is empty')
        node_type = node.get('type')
        valid_types = {'list', 'code', 'equation-interline', 'image', 'table', 'title', 'paragraph'}
        if node_type not in valid_types:
            raise HtmlFileExtractorException(f'Invalid node type: {node_type}')
        # 检查列表类型的节点
        if node.get('type') == 'list':
            items = node.get('content', {}).get('items', [])
            # 过滤掉None、空列表，以及只包含None或空值的列表
            return bool(items) and any(
                isinstance(item, (dict, list)) and bool(item)
                for item in items)
        # 检测code类型的节点
        if node.get('type') == 'code':
            code_content = node.get('content', {}).get('code_content')
            # 如果代码内容为None或空字符串，则视为无效节点
            return bool(code_content and code_content.strip())
        # 检测行间公式类型的节点
        if node.get('type') == 'equation-interline':
            math_content = node.get('content', {}).get('math_content')
            # 如果公式内容为None或空字符串，则视为无效节点
            return bool(math_content and math_content.strip())
        # 检测image类型的节点
        if node.get('type') == 'image':
            content = node.get('content', {})
            # 检查url、path或data字段是否至少有一个不为空
            return bool(content.get('url') or content.get('path') or content.get('data'))
        # 检测table类型的节点
        if node.get('type') == 'table':
            html = node.get('content', {}).get('html')
            # 如果表格的html内容为None或空字符串，则视为无效节点
            return bool(html and html.strip())
        # 检测title类型的节点
        if node.get('type') == 'title':
            title_content = node.get('content', {}).get('title_content')
            # 如果标题内容为None或空字符串，则视为无效节点
            return bool(title_content and title_content.strip())
        # 检测段落类型的节点
        if node.get('type') == 'paragraph':
            content = node.get('content', [])
            # 检查content列表是否存在且不为空，并且至少有一个非空的内容项
            return bool(content) and any(
                item.get('c') and item.get('c').strip()
                for item in content
            )
        return True

    def _export_to_content_list(self, base_url:str, html_lst:List[Tuple[str,str]], raw_html:str) -> ContentList:
        """将解析结果存入content_list格式中.

        Args:
            base_url (str): html文本的网页地址
            html_lst (List[Tuple[str,str]]): html文本
            raw_html (str): html文本

        Returns:
        """
        # 在这个地方，根据tuple中的第一个元素的类型，将其转换为content_list中的元素，转换之后如果还有剩余的元素，则证明解析出现问题，有内容缺失的风险。

        one_page = []
        for parsed_html, raw_html in html_lst:
            ccnode_html, cc_tag = self.__get_cc_node(parsed_html)
            parser:BaseHTMLElementRecognizer = self.__to_content_list_mapper.get(cc_tag)
            if parser:
                node = parser.to_content_list_node(base_url, ccnode_html, raw_html)
                if node and self.__is_valid_node(node):
                    one_page.append(node)
            else:
                raise HtmlFileExtractorException(f'无法识别的html标签：{cc_tag}, {parsed_html}')
        content_list = ContentList([one_page])  # 对于网页来说仅有一页，如果多页，则剩下的每个都是一个论坛的回复
        return content_list

    def __get_cc_node(self, html:str) -> (str, str):
        """获取html文本的根标签名。只获取一个，如果html文本中包含多个cc标签，则抛异常。

        Args:
            html (str): html文本

        Returns:
            str: 根标签名
        """
        el = html_to_element(html)
        if el.tag in self.__to_content_list_mapper.keys():
            return html, el.tag
        else:
            # 查找子节点，包括节点自己。  self::tag | .//tag 这是xpath的写法，表示查找自己和子节点中的tag标签，如果只写./tag则只查找子节点中的tag标签
            xpath_expr = ' | '.join(f'self::{tag} | .//{tag}' for tag in self.__to_content_list_mapper.keys())
            nodes = el.xpath(xpath_expr)
            if len(nodes) == 0:
                raise HtmlFileExtractorException(f'html文本中没有cc标签: {html}')
            if len(nodes) > 3:
                raise HtmlFileExtractorException(f'html文本中包含多个cc标签: {html}')
            return element_to_html(nodes[0]), nodes[0].tag

    def __build_extractor(self):
        """
        结合自定义域名规则，构建一个抽取器。
        自定义的规则先从python包内自带的规则中获取，然后使用用户在.llm-web-kit.jsonc中定义的规则覆盖。
        Returns:

        """
        build_in_rule = self.__get_build_in_rule()
        custom_rule = self.__get_custom_rule()
        if custom_rule:
            build_in_rule.update(custom_rule)

        return GeneralExtractor(custom_rule=build_in_rule)

    def __get_build_in_rule(self) -> dict:
        """
        获取内置的规则，也就是python包内自带的规则，这些规则是通用的，适用于大多数网站。
        Returns:

        """
        pypkg_dir = get_py_pkg_root_dir()
        rule_file_path = os.path.join(pypkg_dir, 'extractor', 'html', 'magic_html', 'custome_rule.jsonc')
        with open(rule_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def __get_custom_rule(self) -> dict:
        """
        获取用户自定义的规则，这个规则位于.llm-web-kit.jsonc文件中，用户可以在这个文件中定义自己的规则，随时修改并覆盖内置规则。
        Returns:

        """
        config = load_config(suppress_error=True)
        return config.get('magic-html-custom-rule', {})
