import json
from typing import List, Tuple

from lxml import etree
from lxml.etree import _Element as HtmlElement
from overrides import override

from llm_web_kit.libs.doc_element_type import DocElementType, ParagraphTextType
from llm_web_kit.libs.html_utils import element_to_html
from llm_web_kit.pipeline.extractor.html.recognizer.recognizer import (
    BaseHTMLElementRecognizer, CCTag)


class TextParagraphRecognizer(BaseHTMLElementRecognizer):
    """解析文本段落元素."""

    @override
    def to_content_list_node(self, base_url: str, parsed_content: str, raw_html_segment: str) -> dict:
        """
        把文本段落元素转换为content list node.
        Args:
            base_url:
            parsed_content:
            raw_html_segment:

        Returns:

        """
        el = self._build_html_tree(parsed_content)
        node = {
            'type': DocElementType.PARAGRAPH,
            'raw_content': el.attrib.get('html', ''),
            'content': json.loads(el.text),
        }
        return node

    @override
    def recognize(self, base_url:str, main_html_lst: List[Tuple[str,str]], raw_html:str) -> List[Tuple[str,str]]:
        """父类，解析文本段落元素.

        Args:
            base_url: str: 基础url
            main_html_lst: main_html在一层一层的识别过程中，被逐步分解成不同的元素
            raw_html: 原始完整的html

        Returns:
        """
        new_html_lst = []
        for html, raw_html in main_html_lst:
            if self.is_cc_html(html):
                new_html_lst.append((html, raw_html))
            else:
                root_el = self._build_html_tree(html)
                lst = list(self.__extract_paragraphs(root_el))
                # 然后对lst[Element, raw_html] 进行处理. 提出Element里的文字，做成<<cctext>>标签
                new_lst = self.__to_cctext_lst(lst)
                new_html_lst.extend(new_lst)
        return new_html_lst

    def __to_cctext_lst(self, lst: List[Tuple[HtmlElement, str]]) -> List[Tuple[str, str]]:
        """将lst[Element, raw_html] 进行处理. 提出Element里的文字，做成<<cctext>>标签.

        Args:
            lst: List[Tuple[HtmlElement, str]]: Element和raw_html组成的列表
        """
        new_lst = []
        for el, raw_html in lst:
            para_text = self.__get_paragraph_text(el)
            if para_text:
                cctext_el = self._build_cc_element(CCTag.CC_TEXT, json.dumps(para_text, ensure_ascii=False, indent=4), '', html=raw_html)
                cc_node_html = self._element_to_html(cctext_el)
                new_lst.append((cc_node_html, raw_html))

        return new_lst

    def __get_paragraph_text(self, el: HtmlElement) -> List[dict]:
        """
        获取段落全部的文本.
        对于段落里的行内公式<equation-inline>需要特定处理，转换为段落格式：
        [
          {"c":"content text", "t":"text"},
          {"c": "equation text", "t":"equation"},
          {"c":"content text", "t":"text"}
        ]

        Args:
            el: 代表一个段落的html元素
        """
        type_text = ParagraphTextType.TEXT
        type_equation_inline = ParagraphTextType.EQUATION_INLINE

        para_text = []
        text = ''
        for child in el.iter():
            if child.tag == CCTag.CC_MATH_INLINE:
                if text:
                    para_text.append({'c':text, 't':type_text})
                    text = ''
                para_text.append({'c':child.text, 't':type_equation_inline})
            else:
                text += child.text or ''
                text += child.tail or ''

        if text:
            para_text.append({'c':text, 't':type_text})

        return para_text

    def __extract_paragraphs(self, root: HtmlElement):
        """解析文本段落元素.

        Args:
            root: 根元素

        Returns:
            解析后的文本段落元素
        """
        path: List[HtmlElement] = []
        parser = etree.HTMLParser(collect_ids=False, encoding='utf-8', remove_comments=True, remove_pis=True)

        def is_contain_readable_text(text):
            return text.strip() if text else text

        def rebuild_path():
            """rebuild path with only tag & attrib."""
            for i in range(len(path)):
                elem = path[i]
                copied = parser.makeelement(elem.tag, elem.attrib)
                if i > 0:
                    path[i - 1].append(copied)
                path[i] = copied

        def copy_helper(elem: HtmlElement):
            """deep copy w/o root's tail."""
            copied = parser.makeelement(elem.tag, elem.attrib)
            copied.text = elem.text
            for sub_elem in elem:
                sub_copied = copy_helper(sub_elem)
                sub_copied.tail = sub_elem.tail
                copied.append(sub_copied)
            return copied

        def has_direct_text(elem: HtmlElement):
            # hr is not considered
            # <br> return false
            # &nbsp; return false
            if is_contain_readable_text(elem.text):
                return True
            for sub_elem in elem:
                if is_contain_readable_text(sub_elem.tail):
                    return True
            return False

        def has_text(elem: HtmlElement):
            if has_direct_text(elem):
                return True
            for sub_elem in elem:
                if has_text(sub_elem):
                    return True
            return False

        def helper(elem: HtmlElement):
            copied = parser.makeelement(elem.tag, elem.attrib)
            copied.text = elem.text

            if path:
                path[-1].append(copied)

            path.append(copied)
            for sub_elem in elem:
                if has_direct_text(sub_elem) or (sub_elem.tag == 'p' and has_text(sub_elem)):
                    rebuild_path()
                    path[-1].append(copy_helper(sub_elem))
                    yield path[0], element_to_html(path[0])

                    # detach the yielded tree
                    rebuild_path()
                    continue

                yield from helper(sub_elem)

            copied = path.pop()
            copied.tail = elem.tail

        return helper(root)
