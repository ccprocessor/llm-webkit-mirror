from abc import abstractmethod
from typing import List, Tuple

from overrides import override

from llm_web_kit.input.datajson import ContentList, DataJson
from llm_web_kit.pipeline.extractor.extractor import BaseFileFormatExtractor
from llm_web_kit.pipeline.extractor.html.recognizer.audio import \
    AudioRecognizer
from llm_web_kit.pipeline.extractor.html.recognizer.code import CodeRecognizer
from llm_web_kit.pipeline.extractor.html.recognizer.image import \
    ImageRecognizer
from llm_web_kit.pipeline.extractor.html.recognizer.list import ListRecognizer
from llm_web_kit.pipeline.extractor.html.recognizer.math import MathRecognizer
from llm_web_kit.pipeline.extractor.html.recognizer.recognizer import \
    BaseHTMLElementRecognizer
from llm_web_kit.pipeline.extractor.html.recognizer.table import \
    TableRecognizer
from llm_web_kit.pipeline.extractor.html.recognizer.text import \
    TextParagraphRecognizer
from llm_web_kit.pipeline.extractor.html.recognizer.title import \
    TitleRecognizer
from llm_web_kit.pipeline.extractor.html.recognizer.video import \
    VideoRecognizer


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

        main_html, method = self._extract_main_html(raw_html, base_url)
        parsed_html = [(main_html,main_html)]
        for extract_func in [self._extract_code, self._extract_math, self._extract_image, self._extract_audio,
                             self._extract_video, self._extract_table, self._extract_list,
                             self._extract_title, self._extract_paragraph]:
            parsed_html = extract_func(base_url, parsed_html, raw_html)

        content_list = self._export_to_content_list(base_url, parsed_html, raw_html)
        data_json['content_list'] = content_list

        return data_json

    @abstractmethod
    def _extract_main_html(self, raw_html:str, base_url:str) -> (str, str):
        """从html文本中提取主要的内容.

        Args:
            raw_html (str): html文本
            base_url (str): html文本的网页地址

        Returns:
            str1: 主要的内容
            str2: 获得内容的方式，可对质量进行评估
        """
        # TODO: 从html文本中提取主要的内容
        raise NotImplementedError

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
    def _export_to_content_list(self, base_url:str, html_lst:List[Tuple[str,str]], raw_html:str) -> ContentList:
        """将解析结果存入content_list格式中.

        Args:
            base_url (str): html文本的网页地址
            html_lst (List[Tuple[str,str]]): html文本
            raw_html (str): html文本

        Returns:
        """

        raise NotImplementedError
