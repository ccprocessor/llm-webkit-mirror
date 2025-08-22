# llm_web_kit/extractor/html/main_html_parser.py

import os
from abc import ABC, abstractmethod
from typing import Tuple

import commentjson as json

from llm_web_kit.config.cfg_reader import load_config
from llm_web_kit.extractor.html.magic_html import GeneralExtractor
from llm_web_kit.input.datajson import DataJson
# from llm_web_kit.libs.class_loader import ClassLoader
from llm_web_kit.libs.path_lib import get_proj_root_dir, get_py_pkg_root_dir


class HTMLPageLayoutType:
    """HTML页面布局类型常量."""
    LAYOUT_ARTICLE = 'article'
    LAYOUT_FORUM = 'forum'
    LAYOUT_LIST = 'list'


class AbstractMainHtmlParser(ABC):
    """主要内容解析器的抽象基类."""
    def __init__(self, config: dict):
        self.config = config

    def parse(self, data_json: DataJson) -> DataJson:
        """解析和处理主要内容.

        Args:
            data_json: 包含原始HTML的数据

        Returns:
            DataJson: 处理后的数据，包含main_html字段

        Raises:
            MainHtmlParserBaseException: 当解析失败时抛出
        """
        return self._do_parse(data_json)

    @abstractmethod
    def _do_parse(self, data_json: DataJson) -> DataJson:
        """具体的解析实现."""
        raise NotImplementedError


class LLMMainHtmlParser(AbstractMainHtmlParser):
    """使用LLM解析主要内容."""
    def _do_parse(self, data_json: DataJson) -> DataJson:
        # TODO: 实现LLM的解析逻辑
        # 1. 调用LLM服务
        # 2. 解析结果
        # 3. 设置main_html字段
        data_json['main_html'] = data_json['html']
        return data_json


class LayoutBatchMainHtmlParser(AbstractMainHtmlParser):
    """使用布局批量解析主要内容."""
    def _do_parse(self, data_json: DataJson) -> DataJson:
        # TODO: 实现布局批量解析主要内容(反推)
        # 1. 调用布局批量解析主要内容
        # 2. 解析结果
        # 3. 设置main_html字段
        data_json['main_html'] = data_json['html']
        return data_json


class MagicHTMLMainHtmlParser(AbstractMainHtmlParser):
    """使用magic-html解析主要内容."""

    def __init__(self, config: dict):
        """初始化MagicHTML解析器.

        Args:
            config: 配置字典
        """
        super().__init__(config)
        self.__magic_html_extractor = self.__build_extractor()

    def _do_parse(self, data_json: DataJson) -> DataJson:
        """使用magic-html提取主要内容.

        Args:
            data_json: 包含原始HTML的数据

        Returns:
            DataJson: 处理后的数据，包含main_html和title字段
        """
        raw_html: str = data_json['html']
        base_url: str = data_json['url']
        page_layout_type: str = data_json.get('page_layout_type', HTMLPageLayoutType.LAYOUT_ARTICLE)

        # 使用magic-html提取主要内容
        main_html, xp_num, title = self._extract_main_html(raw_html, base_url, page_layout_type)

        # 设置提取结果
        data_json['main_html'] = main_html
        data_json['title'] = title

        return data_json

    def _extract_main_html(self, raw_html: str, base_url: str, page_layout_type: str) -> Tuple[str, str, str]:
        """从html文本中提取主要的内容.

        Args:
            raw_html: html文本
            base_url: html文本的网页地址
            page_layout_type: 网页的布局类型

        Returns:
            Tuple[str, str, str]: (主要内容, xpath匹配数量, 标题)
        """
        dict_result = self.__magic_html_extractor.extract(
            raw_html,
            base_url=base_url,
            precision=False,
            html_type=page_layout_type
        )
        return dict_result['html'], dict_result['xp_num'], dict_result.get('title', '')

    def __build_extractor(self) -> GeneralExtractor:
        """构建magic-html抽取器.

        结合自定义域名规则，构建一个抽取器。
        自定义的规则先从python包内自带的规则中获取，然后使用用户在.llm-web-kit.jsonc中定义的规则覆盖。

        Returns:
            GeneralExtractor: magic-html通用抽取器实例
        """
        build_in_rule = self.__get_build_in_rule()
        custom_rule = self.__get_custom_rule()
        if custom_rule:
            build_in_rule.update(custom_rule)

        return GeneralExtractor(custom_rule=build_in_rule)

    def __get_build_in_rule(self) -> dict:
        """获取内置的规则，也就是python包内自带的规则，这些规则是通用的，适用于大多数网站.

        Returns:
            dict: 内置规则字典
        """
        pypkg_dir = get_py_pkg_root_dir()
        rule_file_path = os.path.join(pypkg_dir, 'extractor', 'html', 'magic_html', 'custome_rule.jsonc')
        with open(rule_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def __get_custom_rule(self) -> dict:
        """获取用户自定义的规则.

        这个规则位于.llm-web-kit.jsonc文件中，用户可以在这个文件中定义自己的规则，
        随时修改并覆盖内置规则。

        Returns:
            dict: 自定义规则字典
        """
        config = load_config(suppress_error=True)
        return config.get('magic-html-custom-rule', {})


class TestHTMLFileFormatFilterMainHtmlParser(AbstractMainHtmlParser):
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

    def _do_parse(self, data_json: DataJson) -> DataJson:
        """对输入的单个html拼装到DataJson中，形成标准输入格式."""
        proj_root_dir = get_proj_root_dir()
        html_file_path = os.path.join(proj_root_dir, self.__html_parent_path, data_json.get('path'))

        with open(html_file_path, 'r', encoding='utf-8') as f:
            html = f.read()
            data_json['html'] = html
            data_json['main_html'] = html
            del data_json['path']
        return data_json
