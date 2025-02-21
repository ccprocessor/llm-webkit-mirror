import base64
import gzip
import html
import json
import re
from typing import List, Tuple
from urllib.parse import urljoin, urlparse

import cairosvg
from lxml.html import HtmlElement
from overrides import override

from llm_web_kit.libs.doc_element_type import DocElementType
from llm_web_kit.libs.logger import mylogger
from llm_web_kit.pipeline.extractor.html.recognizer.recognizer import (
    BaseHTMLElementRecognizer, CCTag)


class ImageRecognizer(BaseHTMLElementRecognizer):
    """解析图片元素."""
    IMG_LABEL = ['.jpg', '.jpeg', '.png', '.gft', '.webp', '.bmp', '.svg', 'data:image', '.gif']  # '.pdf'

    @override
    def to_content_list_node(self, base_url: str, parsed_content: str, raw_html_segment: str) -> dict:
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
        html_obj = self._build_html_tree(parsed_content)
        if html_obj is None:
            raise ValueError(f'Failed to load html: {parsed_content}')

        if html_obj.tag == CCTag.CC_IMAGE:
            return self.__ccimg_to_content_list(raw_html_segment, html_obj)
        else:
            raise ValueError(f'No ccimage element found in content: {parsed_content}')

    def __ccimg_to_content_list(self, raw_html_segment: str, html_obj: HtmlElement) -> dict:
        result = {
            'type': DocElementType.IMAGE,
            'raw_content': raw_html_segment,
            'content': {
                'url': html_obj.text if html_obj.get('format') == 'url' else None,
                'data': html_obj.text if html_obj.get('format') == 'base64' else None,
                'alt': html_obj.get('alt'),
                'title': html_obj.get('title'),
                'caption': html_obj.get('caption')
            }
        }
        # print(f'content: {result["content"]}')
        return result

    @override
    def recognize(self, base_url: str, main_html_lst: List[Tuple[str, str]], raw_html: str) -> List[Tuple[str, str]]:
        """父类，解析图片元素.

        Args:
            base_url: str: 基础url
            main_html_lst: main_html在一层一层的识别过程中，被逐步分解成不同的元素
            raw_html: 原始完整的html

        Returns:
        """
        ccimg_html = list()
        for html_li in main_html_lst:
            try:
                if self.is_cc_html(html_li[0]):
                    ccimg_html.append(html_li)
                else:
                    new_html_li = self.__parse_html_img(base_url, html_li)
                    if new_html_li:
                        ccimg_html.extend(new_html_li)
                    else:
                        ccimg_html.append(html_li)
            except Exception as e:
                mylogger.exception(f'recognizer image failed: {e}')
                raise Exception(f'recognizer image failed: {e}')
        return ccimg_html

    def __parse_html_img(self, base_url: str, html_str: Tuple[str, str]) -> List[Tuple[str, str]]:
        """解析html，获取img标签."""
        html_obj = self._build_html_tree(html_str[0])
        image_related_selectors = [
            '//*[contains(@class, "image-embed") or contains(@id, "image-embed")]',  # 可能包含嵌入图片的自定义标签
            '//*[starts-with(@src, "data:image/") and not(self::img)]',
            # 带有内嵌base64图片的标签,data:image/png;base64,eg:img, svg/image
            '//iframe[not(ancestor::noscript) and not(ancestor::iframe) and not(ancestor::object)]',
            '//embed[not(ancestor::object)]',
            '//figure[not(ancestor::figure)]',
            '//object[not(ancestor::object)]',  # object标签，通常用于嵌入多媒体内容
            '//picture[not(ancestor::figure) and not(ancestor::object)]',
            '//canvas',  # canvas标签，可能用于绘制图形或展示图片
            '//svg[not(ancestor::figure)]',  # svg标签，用于矢量图形
            '//video',
            '//audio',
            '//img[not(ancestor::noscript) and not(ancestor::picture) and not(ancestor::figure) and not(ancestor::object) and not(ancestor::table)]',
        ]
        # 合并XPath表达式
        combined_xpath = '|'.join(image_related_selectors)
        # 使用XPath选择所有相关标签
        img_elements = html_obj.xpath(combined_xpath)
        base_img = html_obj.xpath('//*[starts-with(@xlink:href, "data:image/") and not(self::img)]', namespaces={
            'xlink': 'http://www.w3.org/1999/xlink'})
        if base_img:
            img_elements.extend(base_img)
        if img_elements:
            update_html, img_tag = self.__parse_img_elements(base_url, img_elements, html_obj)
            if img_tag:
                return self.html_split_by_tags(update_html, CCTag.CC_IMAGE)

    def __parse_img_elements(self, base_url: str, img_elements: HtmlElement, html_obj: HtmlElement) -> HtmlElement:
        """解析img标签."""
        img_tag = []
        is_valid_img = False
        for elem in img_elements:
            tag = elem.tag
            raw_img_html = self._element_to_html(elem)
            # mylogger.info(f'raw_img_html: {raw_img_html}')
            attributes = {
                'by': tag,
                'html': raw_img_html,  # 保留原始 <img> 标签作为属性值
                'format': 'url',  # 指定图片格式，url|base
            }
            if elem.text and elem.text.strip():
                attributes['caption'] = elem.text.strip()
            if tag in ['embed', 'object', 'iframe', 'video', 'audio', 'canvas']:
                if not [img_elem for img_elem in self.IMG_LABEL if
                        img_elem in raw_img_html.lower()]:
                    continue
                elif elem.xpath('.//img|.//image'):
                    if len(elem.xpath('.//img|.//image')) == 1:
                        self.__parse_img_attr(base_url, elem.xpath('.//img|.//image')[0], attributes)
                    else:
                        continue
                else:
                    self.__parse_img_attr(base_url, elem, attributes)
            elif tag in ['picture', 'figure']:
                if elem.xpath('.//img|.//image'):
                    self.__parse_img_attr(base_url, elem.xpath('.//img|.//image')[0], attributes)
                else:
                    continue
            elif tag == 'svg':
                if elem.xpath('.//path|.//circle'):
                    self.__parse_svg_img_attr(elem, attributes)
                elif elem.xpath('.//img|.//image'):
                    self.__parse_img_attr(base_url, elem.xpath('.//img|.//image')[0], attributes)
                else:
                    continue
            else:
                self.__parse_img_attr(base_url, elem, attributes)
            if not attributes.get('text'):
                continue

            img_tag.append(CCTag.CC_IMAGE)
            is_valid_img = True
            # attributes = {k: self.__clean_xml_string(v) for k, v in attributes.items()}
            img_text, img_tail = self.__parse_text_tail(attributes)
            try:
                new_ccimage = self._build_cc_element(CCTag.CC_IMAGE, img_text, img_tail, **attributes)
            except Exception as e:
                mylogger.exception(f'build_cc_element failed: {e}')
                raise Exception(f'build_cc_element failed: {e}')
            # mylogger.info(f'new_ccimage:{self._element_to_html(new_ccimage)}')
            try:
                self._replace_element(elem, new_ccimage)
            except Exception as e:
                mylogger.exception(f'replace img element fail: {e}')
                raise Exception(f'replace img element fail: {e}')

        if is_valid_img:
            updated_html = self._element_to_html(html_obj)
            return (updated_html, img_tag)
        else:
            return (None, None)

    def __parse_img_attr(self, base_url: str, elem: HtmlElement, attributes: dict):
        """解析获取img标签属性值."""
        elem_attributes = {k: v for k, v in elem.attrib.items() if v and v.strip()}
        text = self.__parse_img_text(elem_attributes)
        if text:
            if text.startswith('data:image'):
                attributes['text'] = text
                attributes['format'] = 'base64'
                # attributes['text'] = re.search(r'base64[, ]?(.*)', text).group(1)
            else:
                attributes['text'] = self.__get_full_image_url(base_url, text)
        common_attributes = ['alt', 'title', 'width', 'height']  # , 'src', 'style', 'data-src', 'srcset'
        attributes.update({attr: elem_attributes.get(attr) for attr in common_attributes if elem_attributes.get(attr)})
        if elem.tail and elem.tail.strip():
            attributes['tail'] = elem.tail.strip()

    def __parse_img_text(self, elem_attributes: dict):
        text = ''
        src = elem_attributes.get('src')
        data_src = [v.split(' ')[0] for k, v in elem_attributes.items() if k.startswith('data')]
        if src and data_src:
            src = src if not src.startswith('data:image') else data_src[0]
        if src and any(img_label for img_label in self.IMG_LABEL if img_label in src.lower()):
            text = src
        else:
            for k, v in elem_attributes.items():
                if any(img_label for img_label in self.IMG_LABEL if img_label in v.lower().split('?')[0]):
                    if 'http' in v.strip()[1:-1]:
                        continue
                    text = v
        return text

    def __parse_svg_img_attr(self, elem: HtmlElement, attributes: dict):
        svg_img = self.__svg_to_base64(attributes['html'])
        if svg_img:
            attributes['text'] = svg_img
            attributes['format'] = 'base64'
            if elem.tail and elem.tail.strip():
                attributes['tail'] = elem.tail.strip()
            common_attributes = ['alt', 'title', 'width', 'height']
            for attr in common_attributes:
                if elem.get(attr) is not None:
                    attributes[attr] = elem.get(attr)

    def __clean_xml_string(self, s):
        """清洗html数据，统一标准的unicode编码，移除NULL字节和其他控制字符."""
        s = html.unescape(s)
        return ''.join(c for c in s if ord(c) >= 32)

    def __parse_text_tail(self, attributes: dict) -> Tuple[str, str]:
        """解析img标签的text&tail值."""
        if not attributes:
            raise ZeroDivisionError
        text = attributes.pop('text') if attributes.get('text') else ''
        tail = attributes.pop('tail') if attributes.get('tail') else ''
        return (text, tail)

    def __get_full_image_url(self, base_url: str, relative_src: str) -> str:
        parsed_base = urlparse(base_url)
        base_domain = f'{parsed_base.scheme}://{parsed_base.netloc}'

        if relative_src.startswith('http'):
            return relative_src
        elif relative_src.startswith('/'):
            return urljoin(base_domain, relative_src)
        elif relative_src.startswith('//'):
            return urljoin(parsed_base.scheme, relative_src)
        else:
            return urljoin(base_url, relative_src)

    def __svg_to_base64(self, svg_content: str) -> str:
        try:
            if not svg_content.strip().endswith('svg>'):
                svg_content = re.search(r'(<svg.*svg>)', svg_content).group(1)
            image_data = cairosvg.svg2png(bytestring=svg_content)
            base64_data = base64.b64encode(image_data).decode('utf-8')
            mime_type = 'image/png'
            return (
                f'data:{mime_type};'
                f'base64,{base64_data}'
            )
        except ValueError:
            mylogger.info(f'value error, The SVG size is undefined: {svg_content}')
        except Exception as e:
            mylogger.exception(f'svg_to_base64 failed: {e}, error data: {svg_content}')
            raise Exception(f'svg_to_base64 failed: {e}')


def read_gz_and_parse_json_line_by_line(file_path):
    try:
        # 使用 gzip.open() 读取 .gz 文件
        with gzip.open(file_path, 'rt', encoding='utf-8') as gz_file:
            for line in gz_file:
                # 解析每一行 JSON 数据
                json_line = json.loads(line)
                yield json_line
    except Exception as e:
        print(f'Error reading or parsing the file: {e}')


if __name__ == '__main__':
    img = ImageRecognizer()
    path = r'C:\Users\renpengli\Downloads\CC_benchmark_test_v014_part-676e680976e0-000000.jsonl.gz'

    idx = 0
    num = 0
    for html_d in read_gz_and_parse_json_line_by_line(path):
        idx += 1
        # if idx < num:
        #     continue
        # if idx > num:
        #     break
        if idx < num:
            continue
        if idx > 5000:
            break
        print(f"start analysis idx: {idx}, url: {html_d['url']}")
        # print(html_d['html'])
        res = img.recognize(html_d['url'], [(html_d['html'], html_d['html'])], html_d['html'])
        # parsed_content = """<ccimage by="img" html='&lt;img style="margin:0;padding:0;border:0;" alt="Hosted by uCoz" src="http://s201.ucoz.net/img/cp/6.gif" width="80" height="15" title="Hosted by uCoz"&gt;' format="url" alt="Hosted by uCoz">http://s201.ucoz.net/img/cp/6.gif</ccimage>"""
        # res = img.to_content_list_node(html_d["url"], parsed_content, html_d["html"])
        print(f'res size: {len(res)}')
# 43 svg, figure -- 21, 92 picture --53, 69 base64--186, 62 svg--26, table -- 1
