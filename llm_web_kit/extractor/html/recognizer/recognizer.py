"""基本的元素解析类."""
from abc import ABC, abstractmethod
from typing import List, Tuple

from lxml.html import HtmlElement, HTMLParser

from llm_web_kit.libs.html_utils import (build_cc_element, element_to_html,
                                         element_to_html_unescaped,
                                         html_to_element, replace_element)
from llm_web_kit.libs.logger import mylogger


class CCTag:
    CC_CODE = 'cccode'
    CC_CODE_INLINE = 'cccode-inline'
    CC_MATH_INLINE = 'ccmath-inline'
    CC_MATH_INTERLINE = 'ccmath-interline'
    CC_IMAGE = 'ccimage'
    CC_VIDEO = 'ccvideo'
    CC_AUDIO = 'ccaudio'
    CC_TABLE = 'cctable'
    CC_LIST = 'cclist'
    CC_TEXT = 'cctext'
    CC_TITLE = 'cctitle'


class BaseHTMLElementRecognizer(ABC):
    HTML_PARSER = HTMLParser(collect_ids=False, encoding='utf-8', remove_comments=True, remove_pis=True)

    """基本的元素解析类."""
    @abstractmethod
    def recognize(self, base_url:str, main_html_lst: List[Tuple[HtmlElement, HtmlElement]], raw_html:str, language:str) -> List[Tuple[HtmlElement, HtmlElement]]:
        """父类，解析html中的元素.

        Args:
            base_url: str: 基础url
            main_html_lst: main_html在一层一层的识别过程中，被逐步分解成不同的元素
            raw_html: 原始完整的html

        Returns:
            List[Tuple[HtmlElement, HtmlElement]]: 处理后的HTML元素列表
        """
        raise NotImplementedError

    @abstractmethod
    def to_content_list_node(self, base_url:str, parsed_content: HtmlElement, raw_html_segment:str) -> dict:
        """将content转换成content_list_node.
        每种类型的html元素都有自己的content-list格式：参考 docs/specification/output_format/content_list_spec.md
        例如代码的返回格式：
        ```json
        {
            "type": "code",
            "bbox": [0, 0, 50, 50],
            "raw_content": "<code>def add(a, b):\n    return a + b</code>" // 原始的html代码
            "content": {
                  "code_content": "def add(a, b):\n    return a + b",
                  "language": "python",
                  "by": "hilightjs"
            }
        }
        ```

        Args:
            base_url: str: 基础url
            parsed_content: str: 被解析后的内容<ccmath ...>...</ccmath>等
            raw_html_segment: str: 原始html片段

        Returns:
            dict: content_list_node
        """
        raise NotImplementedError

    def _build_html_tree(self, html_source:str) -> HtmlElement:
        """从一个字符串构造html DOM树.

        Args:
            html_source: str: html字符串

        Returns:
            etree._Element: html树
        """
        return html_to_element(html_source)

    def _element_to_html(self, element: HtmlElement) -> str:
        """将element转换成html字符串.

        Args:
            element: etree._Element: element

        Returns:
            str: html字符串
        """
        return element_to_html(element)

    def _element_to_html_entity(self, element: HtmlElement) -> str:
        """将element转换成html字符串."""
        return element_to_html_unescaped(element)

    def _build_cc_element(self, html_tag_name: str, text: str, tail: str, **kwargs) -> HtmlElement:
        """构建cctitle的html. 例如：<cctitle level=1>标题1</cctitle>

        Args:
            html_tag_name: str: html标签名称，例如 'cctitle'
            text: str: 标签的文本内容
            tail: str: 标签后的文本内容
            **kwargs: 标签的其他属性，例如 level='1', html='<h1>标题</h1>' 等

        Returns:
            str: cctitle的html
        """
        return build_cc_element(html_tag_name, text, tail, **kwargs)

    def _replace_element(self, element:HtmlElement, cc_element:HtmlElement) -> None:
        """Replaces element with cc_element.

        Args:
            element: The element to be replaced
            cc_element: The element to replace with
        """
        replace_element(element, cc_element)

    @staticmethod
    def html_split_by_tags(root: HtmlElement, split_tag_names:str | list) -> List[Tuple[HtmlElement,HtmlElement]]:
        """根据split_tag_name将html分割成不同的部分.

        Args:
            html_segment: str: 要分割的html源码
            split_tag_names: str|list: 分割标签名, 例如 'p' 或者 'div' 或者 ['p', 'div']
        """
        copy_attri = True  # 是否copy 父节点的属性
        # root = html_to_element(html_segment)
        if isinstance(split_tag_names, str):  # 如果参数是str，转换成list
            split_tag_names = [split_tag_names]

        """root is not considered"""
        path: List[HtmlElement] = []

        def __is_element_text_empty(element):
            """"""
            if element.text is not None and element.text.strip():
                return False
            # 遍历所有子元素，检查它们的文本和尾随文本
            for child in element.iter():
                # 检查子元素的文本
                if child.text is not None and child.text.strip():
                    return False
                # 检查子元素的尾随文本
                if child.tail is not None and child.tail.strip():
                    return False
            # 如果没有找到文本，返回 True
            return True

        def __rebuild_empty_parent_nodes_path():
            """rebuild path with only tag & attrib."""
            for i in range(len(path)):
                elem = path[i]
                attrib = elem.attrib if copy_attri else {}
                copied = BaseHTMLElementRecognizer.HTML_PARSER.makeelement(elem.tag, attrib)
                if i > 0:
                    path[i - 1].append(copied)
                path[i] = copied

        def __copy_tree(elem: HtmlElement, copy_attr=False):
            """deep copy w/o root's tail."""
            attrib = elem.attrib if copy_attr else {}
            copied = BaseHTMLElementRecognizer.HTML_PARSER.makeelement(elem.tag, attrib)
            copied.text = elem.text
            for sub_elem in elem:
                sub_copied = __copy_tree(sub_elem)
                sub_copied.tail = sub_elem.tail
                copied.append(sub_copied)
            return copied

        def __split_node(elem: HtmlElement):
            attrib = elem.attrib if copy_attri else {}
            copied = BaseHTMLElementRecognizer.HTML_PARSER.makeelement(elem.tag, attrib)
            if elem.text and elem.text.strip():
                copied.text = elem.text

            if path:
                path[-1].append(copied)

            path.append(copied)

            for sub_elem in elem:
                if sub_elem.tag in split_tag_names:
                    # previous elements
                    # nodes = raw_nodes = element_to_html(path[0])
                    nodes = raw_nodes = path[0]
                    if not __is_element_text_empty(path[0]):
                        yield nodes, raw_nodes

                    # current sub element
                    __rebuild_empty_parent_nodes_path()
                    cp_ele = __copy_tree(sub_elem, copy_attr=True)
                    path[-1].append(cp_ele)
                    html_source_segment = sub_elem.attrib.get('html')
                    if not html_source_segment:
                        mylogger.error(f'{sub_elem.tag} has no html attribute')
                        # TODO raise exception
                    # nodes, raw_nodes = element_to_html(path[0]), html_source_segment
                    if html_source_segment:
                        nodes, raw_nodes = path[0], html_to_element(html_source_segment)
                    else:
                        nodes, raw_nodes = path[0], None
                    # if not __is_element_text_empty(path[0]):
                    yield nodes, raw_nodes  # 这个地方无需检查是否为空，因为这个是分割元素，必须返还

                    # following elements
                    __rebuild_empty_parent_nodes_path()
                    if sub_elem.tail and sub_elem.tail.strip():
                        path[-1].text = sub_elem.tail
                    continue

                yield from __split_node(sub_elem)

            copied = path.pop()
            if elem.tail and elem.tail.strip():
                copied.tail = elem.tail

            if not path:
                nodes = raw_nodes = copied
                # raw_nodes = element_to_html(copied)
                if not __is_element_text_empty(copied):
                    yield nodes, raw_nodes

        rtn = list(__split_node(root))
        return rtn

    @staticmethod
    def is_cc_html(el: HtmlElement, tag_name: str | list = None) -> bool:
        """判断html片段是否是cc标签.

        判断的时候由于自定义ccmath等标签可能会含有父标签，因此要逐层判断tagname. 含有父html
        完整路径的如：<html><body><ccmath>...</ccmath></body></html>，这种情况也会被识别为cc标签.

        Args:
            el: str|HtmlElement: html片段或HtmlElement对象
            tag_name: str|list: cc标签，如ccmath, cccode, 如果指定了那么就只检查这几个标签是否在html里，否则检查所有cc标签
        """
        if el is None:
            return False

        # 默认cc标签列表
        default_tag_names = [
            CCTag.CC_CODE, CCTag.CC_MATH_INTERLINE, CCTag.CC_IMAGE, CCTag.CC_VIDEO,
            CCTag.CC_AUDIO, CCTag.CC_TABLE, CCTag.CC_LIST, CCTag.CC_TEXT, CCTag.CC_TITLE
        ]

        # 确定需要检查的标签集合
        if tag_name:
            if isinstance(tag_name, str):
                tags = {tag_name}
            else:
                tags = set(tag_name)
        else:
            tags = set(default_tag_names)

        # 如果当前元素的标签匹配，直接返回True
        if el.tag in tags:
            return True

        # 构建XPath表达式，检查子元素是否包含目标标签
        xpath_expr = ' or '.join([f'self::{tag}' for tag in tags])
        return bool(el.xpath(f'.//*[{xpath_expr}]'))

    @staticmethod
    def is_cc_tag_node(el: HtmlElement) -> bool:
        """判断html片段是否是cc标签.

        在is_cc_html上做修改，只判断该节点是否为cc标签，而不检查其子节点是否包含cc标签，用在mathjax渲染器方法中.

        Args:
            el: str|HtmlElement: html片段或HtmlElement对象
        """
        default_tag_names = [
            CCTag.CC_CODE, CCTag.CC_MATH_INLINE, CCTag.CC_MATH_INTERLINE, CCTag.CC_IMAGE, CCTag.CC_VIDEO,
            CCTag.CC_AUDIO, CCTag.CC_TABLE, CCTag.CC_LIST, CCTag.CC_TEXT, CCTag.CC_TITLE
        ]
        return hasattr(el, 'tag') and isinstance(el.tag, str) and el.tag in default_tag_names
