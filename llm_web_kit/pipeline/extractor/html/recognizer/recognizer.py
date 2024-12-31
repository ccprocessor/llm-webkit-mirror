"""基本的元素解析类."""
from abc import ABC, abstractmethod
from typing import List, Tuple

from lxml import etree
from lxml.etree import _Element as HtmlElement

from llm_web_kit.libs.logger import mylogger


class CCTag:
    CC_CODE = 'cccode'
    CC_MATH = 'ccmath'
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
    """基本的元素解析类."""
    @abstractmethod
    def recognize(self, base_url:str, main_html_lst: List[Tuple[str,str]], raw_html:str) -> List[Tuple[str,str]]:
        """父类，解析html中的元素.

        Args:
            base_url: str: 基础url
            main_html_lst: main_html在一层一层的识别过程中，被逐步分解成不同的元素
            raw_html: 原始完整的html

        Returns:
        """
        raise NotImplementedError

    @abstractmethod
    def to_content_list_node(self, base_url:str, parsed_content: str, raw_html_segment:str) -> dict:
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

    @staticmethod
    def html_split_by_tags(html_segment: str, split_tag_names:str | list) -> List[Tuple[str,str]]:
        """根据split_tag_name将html分割成不同的部分.

        Args:
            html_segment: str: 要分割的html源码
            split_tag_names: str|list: 分割标签名, 例如 'p' 或者 'div' 或者 ['p', 'div']
        """
        parser = etree.HTMLParser(collect_ids=False, encoding='utf-8', remove_comments=True, remove_pis=True)
        root = etree.HTML(html_segment, parser)
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
                copied = parser.makeelement(elem.tag, elem.attrib)
                if i > 0:
                    path[i - 1].append(copied)
                path[i] = copied

        def __copy_tree(elem: HtmlElement):
            """deep copy w/o root's tail."""
            copied = parser.makeelement(elem.tag, elem.attrib)
            copied.text = elem.text
            for sub_elem in elem:
                sub_copied = __copy_tree(sub_elem)
                sub_copied.tail = sub_elem.tail
                copied.append(sub_copied)
            return copied

        def __split_node(elem: HtmlElement):
            copied = parser.makeelement(elem.tag, elem.attrib)
            if elem.text and elem.text.strip():
                copied.text = elem.text

            if path:
                path[-1].append(copied)

            path.append(copied)

            for sub_elem in elem:
                if sub_elem.tag in split_tag_names:
                    # previous elements
                    nodes = raw_nodes = etree.tostring(path[0], encoding='utf-8').decode()
                    if not __is_element_text_empty(path[0]):
                        yield nodes, raw_nodes

                    # current sub element
                    __rebuild_empty_parent_nodes_path()
                    path[-1].append(__copy_tree(sub_elem))
                    html_source_segment = sub_elem.attrib.get('html')
                    if not html_source_segment:
                        mylogger.error(f'{sub_elem.tag} has no html attribute')
                        # TODO raise exception
                    nodes, raw_nodes = etree.tostring(path[0], encoding='utf-8').decode(), html_source_segment
                    yield nodes, raw_nodes

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
                nodes = raw_nodes = etree.tostring(copied, encoding='utf-8').decode()
                yield nodes, raw_nodes

        rtn = list(__split_node(root))
        return rtn

    @staticmethod
    def is_cc_html(html: str, tag_name: str | list = None) -> bool:
        """判断html片段是否是cc标签. 判断的时候由于自定义ccmath等标签可能会含有父标签，因此要逐层判断tagname. 含有父html
        完整路径的如：<html><body><ccmath>...</ccmath></body></html>，这种情况也会被识别为cc标签.

        Args:
            html: str: html片段
            tag_name: str|list: cc标签，如ccmath, cccode, 如果指定了那么就只检查这几个标签是否在html里，否则检查所有cc标签
        """
        parser = etree.HTMLParser(collect_ids=False, encoding='utf-8', remove_comments=True, remove_pis=True)
        # cc标签是指自定义标签，例如<ccmath>，<ccimage>，<ccvideo>等，输入html片段，判断是否是cc标签
        tree = etree.HTML(html, parser)
        if tree is None:
            return False

        if tag_name:
            if isinstance(tag_name, str):
                tag_to_check = [tag_name]
            else:
                tag_to_check = tag_name
        else:
            tag_to_check = [CCTag.CC_CODE, CCTag.CC_MATH, CCTag.CC_IMAGE, CCTag.CC_VIDEO, CCTag.CC_AUDIO, CCTag.CC_TABLE, CCTag.CC_LIST, CCTag.CC_TEXT, CCTag.CC_TITLE]

        for tag in tag_to_check:
            if tree.xpath(f'.//{tag}'):
                return True
        return False
