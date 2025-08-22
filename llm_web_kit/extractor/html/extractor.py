from typing import List, Tuple

from lxml.html import HtmlElement
from overrides import override

from llm_web_kit.exception.exception import HtmlFileExtractorException
from llm_web_kit.extractor.extractor import BaseFileFormatExtractor
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
from llm_web_kit.libs.doc_element_type import DocElementType
from llm_web_kit.libs.html_utils import element_to_html, html_to_element


class HTMLPageLayoutType:
    """网页的布局类型."""
    LAYOUT_ARTICLE = 'article'
    LAYOUT_QA = 'forum'
    LAYOUT_LIST = 'list'


class NoClipHTMLFIleFormatorExtractor(BaseFileFormatExtractor):
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
        data_json = self._ensure_main_html(data_json)
        raw_html:str = data_json['html']
        base_url:str = data_json['url']
        main_html:str = data_json['main_html']
        language:str = data_json.get('language', 'en')
        # page_layout_type:str = data_json.get('page_layout_type', HTMLPageLayoutType.LAYOUT_ARTICLE)  # 默认是文章类型

        # main_html, method, title = self._extract_main_html(raw_html, base_url, page_layout_type)
        main_html_element = html_to_element(main_html)
        parsed_html = [(main_html_element, main_html)]
        for extract_func in [self._extract_code, self._extract_table, self._extract_math, self._extract_list,
                             self._extract_image,
                             self._extract_title, self._extract_paragraph]:
            parsed_html = extract_func(base_url, parsed_html, raw_html, language)

        content_list:ContentList = self._export_to_content_list(base_url, parsed_html, raw_html)
        data_json['content_list'] = content_list
        # data_json['title'] = title
        return data_json

    def _ensure_main_html(self, data_json: DataJson) -> DataJson:
        """确保DataJson对象包含main_html字段.

        如果main_html字段不存在或为空，则使用html字段的值作为main_html。
        这个方法应该在所有HTML处理器的处理逻辑开始前调用。

        Args:
            data_json: 要处理的DataJson对象

        Returns:
            处理后的DataJson对象
        """
        if 'main_html' not in data_json or not data_json['main_html']:
            data_json['main_html'] = data_json['html']
        return data_json

    def _extract_code(self, base_url:str, html_lst:List[Tuple[HtmlElement, HtmlElement]], raw_html:str, language:str) -> List[Tuple[HtmlElement,HtmlElement]]:
        """从html文本中提取代码.

        Args:
            base_url (str): html文本的网页地址
            html_lst (List[Tuple[str,str]]): html文本
            raw_html (str): html文本
        Returns:
        """

        lst = self.__code_recognizer.recognize(base_url, html_lst, raw_html, language)
        return lst

    def _extract_math(self, base_url:str, html_lst:List[Tuple[str,str]], raw_html:str, language:str) -> List[Tuple[str,str]]:
        """从html文本中提取数学公式.

        Args:
            base_url (str): html文本的网页地址
            html_lst (List[Tuple[str,str]]): html文本
            raw_html (str): html文本

        Returns:
        """

        lst = self.__math_recognizer.recognize(base_url, html_lst, raw_html, language)
        return lst

    def _extract_image(self, base_url:str, html_lst:List[Tuple[str,str]], raw_html:str, language:str) -> List[Tuple[str,str]]:
        """从html文本中提取图片.

        Args:
            base_url (str): html文本的网页地址
            html_lst (List[Tuple[str,str]]): html文本
            raw_html (str): html文本

        Returns:
        """

        lst = self.__image_recognizer.recognize(base_url, html_lst, raw_html, language)
        return lst

    def _extract_audio(self, base_url:str, html_lst:List[Tuple[str,str]], raw_html:str, language:str) -> List[Tuple[str,str]]:
        """从html文本中提取音频.

        Args:
            base_url (str): html文本的网页地址
            html_lst (List[Tuple[str,str]]): html文本
            raw_html (str): html文本

        Returns:
        """

        lst = self.__audio_recognizer.recognize(base_url, html_lst, raw_html, language)
        return lst

    def _extract_video(self, base_url:str, html_lst:List[Tuple[str,str]], raw_html:str, language:str) -> List[Tuple[str,str]]:
        """从html文本中提取视频.

        Args:
            base_url (str): html文本的网页地址
            html_lst (List[Tuple[str,str]]): html文本
            raw_html (str): html文本

        Returns:
        """

        lst = self.__video_recognizer.recognize(base_url, html_lst, raw_html, language)
        return lst

    def _extract_table(self, base_url:str, html_lst:List[Tuple[str,str]], raw_html:str, language:str) -> List[Tuple[str,str]]:
        """从html文本中提取表格.

        Args:
            base_url (str): html文本的网页地址
            html_lst (List[Tuple[str,str]]): html文本
            raw_html (str): html文本

        Returns:
        """

        lst = self.__table_recognizer.recognize(base_url, html_lst, raw_html, language)
        return lst

    def _extract_list(self, base_url:str, html_lst:List[Tuple[str,str]], raw_html:str, language:str) -> List[Tuple[str,str]]:
        """从html文本中提取列表.

        Args:
            base_url (str): html文本的网页地址
            html_lst (List[Tuple[str,str]]): html文本
            raw_html (str): html文本

        Returns:
        """

        lst = self.__list_recognizer.recognize(base_url, html_lst, raw_html, language)
        return lst

    def _extract_title(self, base_url:str, html_lst:List[Tuple[str,str]], raw_html:str, language:str) -> List[Tuple[str,str]]:
        """从html文本中提取标题.

        Args:
            base_url (str): html文本的网页地址
            html_lst (List[Tuple[str,str]]): html文本
            raw_html (str): html文本

        Returns:
        """

        lst = self.__title_recognizer.recognize(base_url, html_lst, raw_html, language)
        return lst

    def _extract_paragraph(self, base_url:str, html_lst:List[Tuple[str,str]], raw_html:str, language:str) -> List[Tuple[str,str]]:
        """从html文本中提取段落.

        Args:
            base_url (str): html文本的网页地址
            html_lst (List[Tuple[str,str]]): html文本
            raw_html (str): html文本

        Returns:
        """

        lst = self.__paragraph_recognizer.recognize(base_url, html_lst, raw_html, language)
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
        valid_types = {DocElementType.TITLE, DocElementType.LIST, DocElementType.CODE, DocElementType.EQUATION_INTERLINE, DocElementType.IMAGE, DocElementType.SIMPLE_TABLE, DocElementType.COMPLEX_TABLE, DocElementType.IMAGE, DocElementType.PARAGRAPH}
        if node_type not in valid_types:
            raise HtmlFileExtractorException(f'Invalid node type: {node_type}')
        # 检查列表类型的节点
        if node.get('type') == DocElementType.LIST:
            items = node.get('content', {}).get('items', [])
            if len(items) == 0:
                return False
            if items and isinstance(items[0], dict) and 'c' in items[0]:
                valid_items = []
                for item in items:
                    # 检查c是否有内容
                    has_content = False
                    if item.get('c'):
                        if isinstance(item['c'], str) and item['c'].strip():
                            has_content = True
                        elif isinstance(item['c'], list) and any(bool(c_item) for c_item in item['c']):
                            has_content = True

                    # 检查child_list是否有内容
                    has_child_list = False
                    child_list = item.get('child_list', {})
                    if isinstance(child_list, dict) and child_list.get('item') and len(child_list.get('item', [])) > 0:
                        has_child_list = True

                    # 如果c或child_list有内容，则认为是有效项
                    if has_content or has_child_list:
                        valid_items.append(item)

                # 如果没有有效项，则返回False
                return len(valid_items) > 0
        # 检测code类型的节点
        if node.get('type') == DocElementType.CODE:
            code_content = node.get('content', {}).get('code_content')
            # 如果代码内容为None或空字符串，则视为无效节点
            return bool(code_content and code_content.strip())
        # 检测行间公式类型的节点
        if node.get('type') == DocElementType.EQUATION_INTERLINE:
            math_content = node.get('content', {}).get('math_content')
            # 如果公式内容为None或空字符串，则视为无效节点
            return bool(math_content and math_content.strip())
        # 检测image类型的节点
        if node.get('type') == DocElementType.IMAGE:
            content = node.get('content', {})
            # 检查url、path或data字段是否至少有一个不为空
            return bool(content.get('url') or content.get('path') or content.get('data'))
        # 检测table类型的节点
        if node.get('type') == DocElementType.SIMPLE_TABLE or node.get('type') == DocElementType.COMPLEX_TABLE:
            html = node.get('content', {}).get('html')
            # 如果表格的html内容为None或空字符串，则视为无效节点
            return bool(html and html.strip())
        # 检测title类型的节点
        if node.get('type') == DocElementType.TITLE:
            title_content = node.get('content', {}).get('title_content')
            # 如果标题内容为None或空字符串，则视为无效节点
            return bool(title_content and title_content.strip())
        # 检测段落类型的节点
        if node.get('type') == DocElementType.PARAGRAPH:
            content = node.get('content', [])
            # 检查content列表是否存在且不为空，并且至少有一个非空的内容项
            return bool(content) and any(
                item.get('c') and item.get('c').strip()
                for item in content
            )
        return True

    def _export_to_content_list(self, base_url:str, html_lst:List[Tuple[HtmlElement,HtmlElement]], raw_html:str) -> ContentList:
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
                raw_html_str = element_to_html(raw_html)
                # raw_html_str = raw_html
                node = parser.to_content_list_node(base_url, ccnode_html, raw_html_str)
                if node and self.__is_valid_node(node):
                    one_page.append(node)
            else:
                raise HtmlFileExtractorException(f'无法识别的html标签：{cc_tag}, {parsed_html}')
        content_list = ContentList([one_page])  # 对于网页来说仅有一页，如果多页，则剩下的每个都是一个论坛的回复
        return content_list

    def __get_cc_node(self, html:HtmlElement) -> Tuple[HtmlElement, str]:
        """获取html文本的根标签名。只获取一个，如果html文本中包含多个cc标签，则抛异常。

        Args:
            html (str): html文本

        Returns:
            str: 根标签名
        """
        # el = html_to_element(html)
        el = html
        if el.tag in self.__to_content_list_mapper.keys():
            return html, el.tag
        else:
            # 查找子节点，包括节点自己。  self::tag | .//tag 这是xpath的写法，表示查找自己和子节点中的tag标签，如果只写./tag则只查找子节点中的tag标签
            xpath_expr = ' | '.join(f'self::{tag} | .//{tag}' for tag in self.__to_content_list_mapper.keys())
            nodes = el.xpath(xpath_expr)
            if len(nodes) == 0:
                raise HtmlFileExtractorException(f'html文本中没有cc标签: {html}')
            # if len(nodes) > 5:
            #     raise HtmlFileExtractorException(f'html文本中包含多个cc标签: {html}')
            # return element_to_html(nodes[0]), nodes[0].tag
            return nodes[0], nodes[0].tag
