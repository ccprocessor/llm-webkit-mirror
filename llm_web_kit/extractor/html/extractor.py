import os
from typing import Tuple

import commentjson as json
from overrides import override

from llm_web_kit.config.cfg_reader import load_config
from llm_web_kit.extractor.html.magic_html import GeneralExtractor
from llm_web_kit.extractor.html.pure_extractor import \
    PureHTMLFileFormatExtractor
from llm_web_kit.input.datajson import DataJson
from llm_web_kit.libs.path_lib import get_py_pkg_root_dir


class HTMLPageLayoutType:
    """网页的布局类型."""
    LAYOUT_ARTICLE = 'article'
    LAYOUT_QA = 'forum'
    LAYOUT_LIST = 'list'


class HTMLFileFormatExtractor(PureHTMLFileFormatExtractor):
    """一个从html文件中提取数据的提取器."""

    def __init__(self, config: dict):
        """从参数指定的配置中初始化这个流水线链.

        Args:
            config (dict): 配置字典
        """
        super().__init__(config)
        self.__magic_html_extractor = self.__build_extractor()

    @override
    def _do_extract(self, data_json: DataJson) -> DataJson:
        """实现真正的数据提取.

        Args:
            data_json (DataJson): 需要处理的数据集
        """
        raw_html:str = data_json['html']
        base_url:str = data_json['url']
        page_layout_type:str = data_json.get('page_layout_type', HTMLPageLayoutType.LAYOUT_ARTICLE)  # 默认是文章类型

        # 使用magic-html提取主要内容
        main_html, method, title = self._extract_main_html(raw_html, base_url, page_layout_type)
        data_json['main_html'] = main_html
        # 调用父类的提取方法
        data_json = super()._do_extract(data_json)
        # 添加标题
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
