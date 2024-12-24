"""基本的元素解析类."""
import inspect
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import List, Tuple

from lxml import etree
from lxml.etree import _Element as HtmlElement

from llm_web_kit.libs.logger import mylogger


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
    def to_content_list_node(self, content: str) -> dict:
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
            content: str: 要转换的content

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
            parent: bool: False时候，只分割split_tag_name标签，True时候，分割split_tag_name标签的所有上级标签以及属性

        Returns:
             List[Tuple[HtmlElement,str]]: 分割后的html(html节点，原始html字符串)
        """
        def __contain_wanted_tag(el: HtmlElement, tags_to_check:list) -> bool:
            # 遍历需要检查的标签列表
            for tag in tags_to_check:
                if el.tag == tag:  # 如果当前节点就是我们想要的标签，直接返回即可
                    mylogger.info(f'{el.tag} is wanted tag: {tag}')
                    return True
                # 使用XPath查找当前节点下是否包含我们想要的标签
                elements = el.xpath(f'.//{tag}')
                if elements:
                    mylogger.info(f'{el.tag} contain wanted tag: {tag}')
                    return True

            mylogger.info(f'{el.tag} not contain wanted tag: {tags_to_check}')
            return False

        def __push_el(lst: List[Tuple[HtmlElement,str]], el: HtmlElement, split_tail=False) -> List[Tuple[HtmlElement,str]]:
            """将节点和节点的html字符串添加到列表中, 此处着重处理了节点的text和tail部分 ```html.

            <p>
            这里没有在任何内部标签中，出现在p的开头，叫做p的text属性
            <img src="http..."/> 这里是img的tail属性
            </p>
            这里呢也是p的tail属性
            ```

            Args:
                lst: list: 要添加的列表
                el: HtmlElement: 节点
                split_tail: bool: tail 是否单独作为一个节点

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

            lst.append((new_el, html_source_segment))
            if tail_text and split_tail and tail_text.strip():
                lst.append((tail_text.strip(), tail_text.strip()))

            return lst

        def __split_html(root_el: HtmlElement, wanted_tag_names:list) -> List[Tuple[HtmlElement,str]]:
            """递归分割html.

            Args:
                root_el: HtmlElement: html节点
                wanted_tag_names: str: 分割标签名

            Returns:
                List[Tuple[HtmlElement,str]]: 分割后的html(html节点，原始html字符串)
            """
            assert isinstance(wanted_tag_names, list), f'{__file__}:{inspect.currentframe().f_back.f_lineno} wanted_tag_names must be a list'
            parts = []
            if not __contain_wanted_tag(root_el, wanted_tag_names):  # 这个节点里没有包含想要分割的标签，就原样返回
                __push_el(parts, root_el, split_tail=False)
            else:  # 这个节点里肯定包含了我们想要分割的标签
                if root_el.tag in wanted_tag_names:  # 如果这个节点就是我们想要的标签，直接返回即可
                    __push_el(parts, root_el, split_tail=True)
                else:  # 继续逐层分割
                    # 先将当前节点的text部分添加到列表中
                    if root_el.text and root_el.text.strip():
                        parts.append((root_el.text.strip(), root_el.text))
                    for child_el in root_el.iterchildren():  # 遍历直接子节点
                        lst = __split_html(child_el, wanted_tag_names)
                        parts = parts + lst  # 将子节点的分割结果合并到当前节点
                    if root_el.tail and root_el.tail.strip():  # 将当前节点的tail部分添加到列表中
                        parts.append((root_el.tail.strip(), root_el.tail))

            return parts

        if isinstance(split_tag_name, str):  # 如果参数是str，转换成list
            split_tag_name = [split_tag_name]
        parser = etree.HTMLParser(collect_ids=False, encoding='utf-8', remove_comments=True, remove_pis=True)
        root = etree.HTML(html_segment, parser)
        html_parts = __split_html(root, split_tag_name)
        return_parts = []
        for p in html_parts:
            if isinstance(p[0], str):
                return_parts.append([p[0], p[1]])
            else:
                return_parts.append((etree.tostring(p[0], encoding='utf-8').decode(), p[1]))
        return return_parts
