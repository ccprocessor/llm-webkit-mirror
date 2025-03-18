import json
import string
from typing import List, Tuple

from lxml import etree
from lxml.html import HtmlElement
from overrides import override

from llm_web_kit.extractor.html.recognizer.recognizer import (
    BaseHTMLElementRecognizer, CCTag)
from llm_web_kit.libs.doc_element_type import DocElementType, ParagraphTextType
from llm_web_kit.libs.html_utils import element_to_html

special_symbols = [  # TODO 从文件读取
    '®',  # 注册商标符号
    '™',  # 商标符号
    '©',  # 版权符号
    '$',   # 美元符号
    '€',   # 欧元符号
    '£',   # 英镑符号
    '¥',   # 日元符号
    '₹',   # 印度卢比符号
    '∑',   # 求和符号
    '∞',   # 无穷大符号
    '√',   # 平方根符号
    '≠',   # 不等于符号
    '≤',   # 小于等于符号
    '•',   # 项目符号
    '¶',   # 段落符号
    '†',   # 匕首符号
    '‡',   # 双匕首符号
    '—',   # 长破折号
    '–',   # 短破折号
    '♥',   # 爱心符号
    '★',   # 星星符号
    '☀',   # 太阳符号
    '☁'    # 云符号
]


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

    def __combine_text(self, text1:str, text2:str, lang='en') -> str:
        """将两段文本合并，中间加空格.

        Args:
            text1: str: 第一段文本
            text2: str: 第二段文本
            lang: str: 语言  TODO 实现根据语言连接文本的不同方式, 还有就是一些特殊符号开头的连接不加空格。
        """
        text1 = text1.strip(' ') if text1 else ''
        text2 = text2.strip(' ') if text2 else ''
        if lang == 'zh':
            txt = text1 + text2
            return txt.strip().replace('\\r\\n', '\n').replace('\\n', '\n')
        else:
            words_sep = '' if text2[0] in string.punctuation or text2[0] in special_symbols else ' '
            txt = text1 + words_sep + text2
            return txt.strip().replace('\\r\\n', '\n').replace('\\n', '\n')

    def __get_paragraph_text(self, root: HtmlElement) -> List[dict]:
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
        para_text = []

        def __get_paragraph_text_recusive(el: HtmlElement, text: str) -> str:
            if el.tag == CCTag.CC_MATH_INLINE:
                if text:
                    para_text.append({'c':text, 't':ParagraphTextType.TEXT})
                    text = ''
                para_text.append({'c':el.text, 't':ParagraphTextType.EQUATION_INLINE})
            elif el.tag == CCTag.CC_CODE_INLINE:
                if text:
                    para_text.append({'c': text, 't': ParagraphTextType.TEXT})
                    text = ''
                para_text.append({'c': el.text, 't': ParagraphTextType.CODE_INLINE})
            elif el.tag in ['br']:
                text += '\n'
            else:
                if el.text and el.text.strip():
                    text = self.__combine_text(text, el.text.strip())
                for child in el:
                    text = __get_paragraph_text_recusive(child, text)

            if el.tail and el.tail.strip():
                text = self.__combine_text(text, el.tail.strip())

            return text

        if final := __get_paragraph_text_recusive(root, ''):
            para_text.append({'c':final, 't':ParagraphTextType.TEXT})

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
