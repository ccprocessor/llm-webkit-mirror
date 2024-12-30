"""基本的元素解析类."""
import inspect
from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Tuple

from lxml import etree
from lxml.etree import _Element as HtmlElement

from llm_web_kit.libs.logger import mylogger
from llm_web_kit.pipeline.extractor.html.magic_html.utils import load_html


class CCTag:
    CC_CODE = "cccode"
    CC_MATH = "ccmath"
    CC_IMAGE = "ccimage"
    CC_VIDEO = "ccvideo"
    CC_AUDIO = "ccaudio"
    CC_TABLE = "cctable"
    CC_LIST = "cclist"
    CC_TEXT = "cctext"
    CC_TITLE = "cctitle"


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
    def html_split_by_tags(html_segment: str, split_tag_name:str | list, parent=False) -> List[Tuple[str,str]]:
        """根据split_tag_name将html分割成不同的部分.

        Args:
            html_segment: str: 要分割的html源码
            split_tag_name: str|list: 分割标签名, 例如 'p' 或者 'div' 或者 ['p', 'div']
            parent: bool: False时候，只返回带内容的叶子标签，True时候，分割html标签的时候会带上所有上级标签以及属性

        Returns:
             List[Tuple[HtmlElement,str]]: 分割后的html(html节点，原始html字符串)

        TODO
        1. <script>和<style>中出现的 <, >, & 等字符会被转义，需要跳过，但是目前没有看到影响正文提取，因此暂时不处理
        """
        parser = etree.HTMLParser(collect_ids=False, encoding='utf-8', remove_comments=True, remove_pis=True)

        def __contain_wanted_tag(el: HtmlElement, tags_to_check:list) -> bool:
            # 遍历需要检查的标签列表
            for tag in tags_to_check:
                if el.tag == tag:  # 如果当前节点就是我们想要的标签，直接返回即可
                    mylogger.debug(f'{el.tag} is wanted tag: {tag}')
                    return True
                # 使用XPath查找当前节点下是否包含我们想要的标签
                elements = el.xpath(f'.//{tag}')
                if elements:
                    mylogger.debug(f'{el.tag} contain wanted tag: {tag}')
                    return True

            mylogger.debug(f'{el.tag} not contain wanted tag: {tags_to_check}')
            return False

        def __push_el(parent_nodes:list[HtmlElement], lst: List[Tuple[HtmlElement,str]], el: HtmlElement, split_tail=False, extra_html=False) -> List[Tuple[HtmlElement,str]]:
            """将节点和节点的html字符串添加到列表中, 此处着重处理了节点的text和tail部分 ```html.

            <p>
            这里没有在任何内部标签中，出现在p的开头，叫做p的text属性
            <img src="http..."/> 这里是img的tail属性
            </p>
            这里呢也是p的tail属性
            ```

            Args:
                parent_nodes: list: 父节点列表
                lst: list: 要添加的列表
                el: HtmlElement: 节点
                split_tail: bool: tail 是否单独作为一个节点
                extra_html: bool: 是否从el中提取html属性，这个html是代表了el的原始html。el节点为自定义标签的那些节点：ccmath, ccimage, ccvideo等

            Returns:
                List[Tuple[HtmlElement,str]]: 节点和节点的html字符串
            """
            tail_text = el.tail
            new_el = deepcopy(el)
            if split_tail:
                new_el.tail = None
                html_source_segment = etree.tostring(new_el, encoding='utf-8').decode()
            else:
                html_source_segment = etree.tostring(el, encoding='utf-8').decode()

            if extra_html:
                html_source_segment = el.attrib.get('html')
                if not html_source_segment:
                    mylogger.error(f'{el.tag} has no html attribute')
                    # TODO 正式生产的时候抛出异常，说明程序有bug

            if parent:
                new_el = __attach_parent_nodes_path(new_el, parent_nodes)
            lst.append((new_el, html_source_segment))
            if tail_text and split_tail and tail_text.strip():
                if parent:
                    new_tail = __attach_parent_nodes_path(tail_text.strip(), parent_nodes)
                    lst.append((new_tail, tail_text.strip()))
                else:
                    lst.append((tail_text.strip(), tail_text.strip()))

            return lst

        def __attach_parent_nodes_path(el: HtmlElement | str, parent_nodes: list[HtmlElement]) -> HtmlElement:
            """将父节点附加到当前节点上，返回一个新的节点.

            Args:
                el: HtmlElement|str: 当前节点, 或者是个text
                parent_nodes: list: 父节点列表

            Returns:
                HtmlElement: 新的节点
            """
            if isinstance(el, HtmlElement):
                new_el = deepcopy(el)
                if parent_nodes and parent:  # 如果有父节点，并且调用方要求返回父节点
                    for p in reversed(parent_nodes):
                        new_p = parser.makeelement(p.tag, p.attrib)
                        new_p.append(new_el)
                        new_el = new_p
            else:
                if parent and parent_nodes:
                    new_el = parser.makeelement(parent_nodes[-1].tag, parent_nodes[-1].attrib)
                    new_el.text = el
                    for p in reversed(parent_nodes[:-1]):
                        new_p = parser.makeelement(p.tag, p.attrib)

                        new_p.append(new_el)
                        new_el = new_p
                else:
                    new_el = el  # 单纯的文字就可以了

            return new_el

        def __split_html(root_el: HtmlElement, wanted_tag_names:list, parent_nodes:list[HtmlElement]) -> List[Tuple[HtmlElement,str]]:
            """递归分割html.

            Args:
                root_el: HtmlElement: html节点
                wanted_tag_names: str: 分割标签名
                parent_nodes: list: 父节点列表

            Returns:
                List[Tuple[HtmlElement,str]]: 分割后的html(html节点，原始html字符串)
            """
            assert isinstance(wanted_tag_names, list), f'{__file__}:{inspect.currentframe().f_back.f_lineno} wanted_tag_names must be a list'
            parts = []
            if not __contain_wanted_tag(root_el, wanted_tag_names):  # 这个节点里没有包含想要分割的标签，就原样返回
                __push_el(parent_nodes, parts, root_el, split_tail=False)
            else:  # 这个节点里肯定包含了我们想要分割的标签
                if root_el.tag in wanted_tag_names:  # 如果这个节点就是我们想要的标签，直接返回即可
                    __push_el(parent_nodes, parts, root_el, split_tail=True, extra_html=True)
                else:  # 继续逐层分割
                    new_parent_nodes = parent_nodes + [root_el]
                    # 先将当前节点的text部分添加到列表中
                    if root_el.text and root_el.text.strip():
                        parts.append((__attach_parent_nodes_path(root_el.text.strip(), new_parent_nodes), root_el.text))
                    for child_el in root_el.iterchildren():  # 遍历直接子节点
                        lst = __split_html(child_el, wanted_tag_names, new_parent_nodes)
                        parts = parts + lst  # 将子节点的分割结果合并到当前节点
                    if root_el.tail and root_el.tail.strip():  # 将当前节点的tail部分添加到列表中
                        parts.append((__attach_parent_nodes_path(root_el.tail.strip(), new_parent_nodes), root_el.tail))

            return parts

        # ########################################################################################################
        if isinstance(split_tag_name, str):  # 如果参数是str，转换成list
            split_tag_name = [split_tag_name]

        root = etree.HTML(html_segment, parser)
        html_parts = __split_html(root, split_tag_name, parent_nodes=[])
        return_parts = []
        for p in html_parts:
            if isinstance(p[0], str):
                return_parts.append([p[0], p[1]])
            else:
                return_parts.append((etree.tostring(p[0], encoding='utf-8').decode(), p[1]))
        return return_parts

    @staticmethod
    def is_cc_html(html: str, tag_name:str | list=None) -> bool:
        """判断html片段是否是cc标签.
        判断的时候由于自定义ccmath等标签可能会含有父标签，因此要逐层判断tagname.
        含有父html完整路径的如：<html><body><ccmath>...</ccmath></body></html>，这种情况也会被识别为cc标签

        Args:
            html: str: html片段
            tag_name: str|list: cc标签，如ccmath, cccode, 如果指定了那么就只检查这几个标签是否在html里，否则检查所有cc标签
        """
        parser = etree.HTMLParser(collect_ids=False, encoding='utf-8', remove_comments=True, remove_pis=True)
        # cc标签是指自定义标签，例如<ccmath>，<ccimage>，<ccvideo>等，输入html片段，判断是否是cc标签
        tree  = etree.HTML(html, parser)
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
