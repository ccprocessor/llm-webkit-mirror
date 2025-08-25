import os

from overrides import override
from selectolax.parser import HTMLParser

from llm_web_kit.extractor.config import INVISIBLE_TAGS
from llm_web_kit.extractor.pre_extractor import \
    BaseFileFormatFilterPreExtractor
from llm_web_kit.input.datajson import DataJson
from llm_web_kit.libs.html_utils import (element_to_html, html_to_element,
                                         remove_element)
from llm_web_kit.libs.path_lib import get_proj_root_dir


class HTMLFileFormatFilterPreExtractor(BaseFileFormatFilterPreExtractor):
    """实现一个基础的HTML文件格式预处理类 例如，根据文件名的后缀拦截数据并进行基础的预处理.

    Args:
        BaseFileFormatFilterPreExtractor (_type_): _description_
    """

    def __init__(self, config: dict):
        super().__init__(config)

    @override
    def _filter_by_rule(self, data_json: DataJson) -> bool:
        return self.is_html_format(data_json)

    @override
    def _do_pre_extract(self, data_json: DataJson) -> DataJson:
        data_json = self._ensure_main_html(data_json)
        return data_json

    def _ensure_main_html(self, data_json: DataJson) -> DataJson:
        """确保DataJson对象包含main_html字段.

        如果main_html字段不存在或为空，则使用html字段的值作为main_html。

        Args:
            data_json: 要处理的DataJson对象

        Returns:
            处理后的DataJson对象
        """
        if 'main_html' not in data_json or not data_json['main_html']:
            data_json['main_html'] = data_json['html']
        return data_json


class HTMLFileFormatNoClipFilterTablePreExtractor(HTMLFileFormatFilterPreExtractor):
    def __init__(self, config: dict):
        super().__init__(config)

    @override
    def _filter_by_rule(self, data_json: DataJson) -> bool:
        if self.__remove_format_table(data_json):
            return True
        else:
            return False

    @override
    def _do_pre_extract(self, data_json: DataJson) -> DataJson:
        pass  # TODO
        return data_json

    def __remove_format_table(self, data_json: DataJson):
        """remove 排版table."""
        html_content = self._get_html_content(data_json)
        return self.__do_remove_layout_table(html_content)

    def _get_html_content(self, data_json: DataJson):
        return data_json['html']

    def __do_remove_layout_table(self, html_content: str):
        """remove 排版table."""
        html_str = html_to_element(html_content)
        first_structure = html_str.xpath('/html/body/table') != []
        second_structure = html_str.xpath('/html/body/center/table') != []
        if bool(first_structure and second_structure):
            return True
        else:
            return False


class HTMLFileFormatNoClipCleanTagsPreExtractor(HTMLFileFormatFilterPreExtractor):
    """清理html中隐藏标签."""

    def __init__(self, config: dict):
        super().__init__(config)

    @override
    def _do_pre_extract(self, data_json: DataJson) -> DataJson:
        data_json = self._ensure_main_html(data_json)
        html_content = data_json['main_html']
        data_json['main_html'] = self._clean_invisible_elements(html_content, data_json)
        return data_json

    def _clean_invisible_elements(self, html_content: str, data_json: DataJson) -> str:
        """清理隐藏标签."""
        tree = html_to_element(html_content)
        # 遍历所有配置的隐藏标签规则
        for tag in INVISIBLE_TAGS:
            # 如果url是通配符*或者匹配当前url
            if tag['url'] == '*' or (data_json['url'] and tag['url'] in data_json['url']):
                # 查找所有匹配xpath的节点
                elements = tree.xpath(tag['tag'])
                for element in elements:
                    remove_element(element)
        return element_to_html(tree)


class TestHTMLFileToDataJsonPreExtractor(HTMLFileFormatFilterPreExtractor):
    """为了方便noclip管线对测试数据进行测试，根据路径读取html文件和main_html文件，然后转换为DataJson格式。"""

    def __init__(self, config: dict, html_parent_dir: str):
        """
        初始化函数
        Args:
            config:
            html_parent_dir:
        """
        super().__init__(config)
        self.__html_parent_path = html_parent_dir

    @override
    def _do_pre_extract(self, data_json: DataJson) -> DataJson:
        """对输入的html和main_html拼装到DataJson中，形成标准输入格式."""
        proj_root_dir = get_proj_root_dir()
        html_file_path = os.path.join(proj_root_dir, self.__html_parent_path, data_json.get('path'))
        main_html_file_path = os.path.join(proj_root_dir, self.__html_parent_path, data_json.get('main_path'))

        with open(html_file_path, 'r', encoding='utf-8') as f:
            html = f.read()
            data_json['html'] = html
            del data_json['path']

        with open(main_html_file_path, 'r', encoding='utf-8') as f:
            main_html = f.read()
            data_json['main_html'] = main_html
            del data_json['main_path']
        return data_json


class HTMLFileFormatNoClipPreExtractor(HTMLFileFormatFilterPreExtractor):
    """noclip管线对main_html预处理."""
    def __init__(self, config: dict):
        super().__init__(config)

    @override
    def _do_pre_extract(self, data_json: DataJson) -> DataJson:
        data_json = self._ensure_main_html(data_json)
        data_json['main_html'] = self.__clean_interactive_elements(data_json)
        return data_json

    def __clean_interactive_elements(self, data_json: DataJson) -> str:
        """清除main_html中交互式元素."""
        html_content = data_json['main_html']
        selectolax_tree = HTMLParser(html_content)
        fixed_html = selectolax_tree.html
        tree = html_to_element(fixed_html)
        # 删除main_html中的script和style标签
        for script_element in tree.xpath('//script'):
            remove_element(script_element)
        for style_element in tree.xpath('//style'):
            remove_element(style_element)
        interactive_tags = ['input', 'select', 'textarea', 'button']
        # 删除<body>内的交互标签及关联label
        for tag in interactive_tags:
            for element in tree.xpath(f'//body//{tag}'):
                # 删除标签本身
                parent = element.getparent()
                if parent is not None:
                    parent.remove(element)

                # 删除关联的label（通过for属性匹配）
                if 'id' in element.attrib:
                    for label in tree.xpath(f'//body//label[@for="{element.attrib["id"]}"]'):
                        label.getparent().remove(label)

        # 处理<form>内的交互标签及关联label
        for form in tree.xpath('//form'):
            # 删除表单内所有交互标签
            form_elements = form.xpath('.//input | .//select | .//textarea | .//button | .//label | .//img')
            for element in form_elements:
                element.getparent().remove(element)

            # 检查表单是否为空（无子元素或仅剩空白文本）
            if len(form.getchildren()) == 0 or not form.text_content().strip():
                form.getparent().remove(form)
        return element_to_html(tree)
