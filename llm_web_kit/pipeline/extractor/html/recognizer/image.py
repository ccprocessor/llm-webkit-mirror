import gzip
import html
import json
from typing import List, Tuple

from lxml.html import HtmlElement, fromstring, tostring
from overrides import override

from llm_web_kit.libs.doc_element_type import DocElementType
from llm_web_kit.libs.logger import mylogger
from llm_web_kit.pipeline.extractor.html.recognizer.recognizer import (
    BaseHTMLElementRecognizer, CCTag)


class ImageRecognizer(BaseHTMLElementRecognizer):
    """解析图片元素."""

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
        html_obj = fromstring(parsed_content)
        if html_obj is None:
            raise ValueError(f'Failed to load html: {parsed_content}')

        if html_obj.tag == CCTag.CC_IMAGE:
            result = {
                'type': DocElementType.IMAGE,
                'raw_content': raw_html_segment,
                'content': {
                    'image_content': html_obj.text,
                    'language': 'python',
                    'by': html_obj.get('by')
                }
            }
            # print(f"content: {result['content']}")
            return result
        else:
            raise ValueError(f'No ccmath element found in content: {parsed_content}')

    @override
    def recognize(self, base_url: str, main_html_lst: List[Tuple[str, str]], raw_html: str) -> List[Tuple[str, str]]:
        """父类，解析图片元素.

        Args:
            base_url: str: 基础url
            main_html_lst: main_html在一层一层的识别过程中，被逐步分解成不同的元素
            raw_html: 原始完整的html

        Returns:
        """
        if not main_html_lst:
            raise ZeroDivisionError
        ccimg_html = list()
        for html_li in main_html_lst:
            if self.is_cc_html(html_li[0]):
                ccimg_html.append(html_li)
            else:
                new_html_li = self.__parse_html_img(html_li)
                if new_html_li:
                    # print(f'new_html_li: {len(new_html_li)}')
                    ccimg_html.extend(new_html_li)
                else:
                    ccimg_html.append(html_li)
        return ccimg_html

    def __parse_html_img(self, html_str: Tuple[str, str]) -> List[Tuple[str, str]]:
        """解析html，获取img标签."""
        html_obj = self._build_html_tree(html_str[0])
        image_related_selectors = [
            '//*[contains(@class, "image-embed") or contains(@id, "image-embed")]',  # 可能包含嵌入图片的自定义标签
            '//iframe[not(ancestor::noscript)]',
            '//embed',
            '//figure[not(ancestor::figure)]',
            '//object',  # object标签，通常用于嵌入多媒体内容
            '//picture[not(ancestor::figure)]',
            '//canvas',  # canvas标签，可能用于绘制图形或展示图片
            '//svg',  # svg标签，用于矢量图形
            '//video',
            '//audio',
            # '//img[not(ancestor::noscript) and not(ancestor::picture) and not(ancestor::figure)]',
            '//img[not(ancestor::noscript) and not(ancestor::picture) and not(ancestor::figure) and not(ancestor::table)]',
        ]
        # 合并XPath表达式
        combined_xpath = '|'.join(image_related_selectors)
        # 使用XPath选择所有相关标签
        img_elements = html_obj.xpath(combined_xpath)
        base_img = html_obj.xpath('//*[starts-with(@xlink:href, "data:image/") or starts-with(@src, "data:image/")]',
                                  namespaces={
                                      'xlink': 'http://www.w3.org/1999/xlink'})  # 带有内嵌base64图片的标签,data:image/png;base64,eg:img, svg/image,
        if base_img:
            img_elements.extend(base_img)
        if img_elements:
            # print(f'img_elements size: {len(img_elements)}')
            update_html, img_tag = self.__parse_img_elements(img_elements, html_obj)
            if img_tag:
                return self.html_split_by_tags(update_html, CCTag.CC_IMAGE)

    def __parse_img_elements(self, img_elements: HtmlElement, html_obj: HtmlElement) -> HtmlElement:
        """解析img标签."""
        img_tag = []
        is_valid_img = False
        for elem in img_elements:
            tag = elem.tag
            # raw_img_html = self._element_to_html(elem)
            raw_img_html = tostring(elem).decode('utf-8')
            # print(f'raw_img_html: {raw_img_html}')
            if tag in ['embed', 'object', 'iframe', 'video', 'audio']:
                # print(f'elem_tag is {tag}')
                if not [img_elem for img_elem in ['.jpg', '.jpeg', '.png', '.webp'] if
                        img_elem in raw_img_html] or not elem.get('src'):
                    continue
            elif tag == 'svg' and elem.xpath('.//path|.//image') is None:
                continue

            img_tag.append(CCTag.CC_IMAGE)
            attributes = {
                'by': tag,
                'html': raw_img_html,  # 保留原始 <img> 标签作为属性值
            }
            if elem.text and elem.text.replace('\n', '').replace('\\n', '').strip():
                attributes['caption'] = elem.text.strip()
            if tag in ['picture', 'figure']:
                if elem.xpath('.//img'):
                    attributes = self.__parse_img_attr(elem.xpath('.//img')[-1], attributes)
                else:
                    # print('picture & figure img tag but no img data')
                    img_tag.pop()
                    continue
            elif tag == 'svg' and elem.xpath('.//image'):
                attributes = self.__parse_img_attr(elem.xpath('.//image')[-1], attributes)
            else:
                attributes = self.__parse_img_attr(elem, attributes)

            is_valid_img = True
            attributes = {k: self.__clean_xml_string(v) for k, v in attributes.items()}
            text, tail = self.__parse_text_tail(attributes)
            new_ccimage = self._build_cc_element(CCTag.CC_IMAGE, text, tail, **attributes)
            # print(f"new_ccimage:{tostring(new_ccimage, pretty_print=True, encoding='unicode')}")
            try:
                self._replace_element(elem, new_ccimage)
            except Exception as e:
                mylogger.error(f'replace img element fail: {e}')
            # elem.getparent().replace(elem, new_ccimage)  # 替换原始 <img> 标签

        if is_valid_img:
            updated_html = self._element_to_html(html_obj)
            # print(f'updated_html: {updated_html}')
            return (updated_html, img_tag)
        else:
            return (None, None)

    def __parse_img_attr(self, elem: HtmlElement, attributes: dict) -> dict:
        """解析获取img标签属性值."""
        src = elem.get('src')
        if src:
            attributes['src'] = src
            attributes['text'] = src

        common_attributes = ['alt', 'title', 'width', 'height']  # 'style', 'data-src', 'srcset'
        for attr in common_attributes:
            if elem.get(attr) is not None:
                attributes[attr] = elem.get(attr)
        # if elem.tail:
        #     attributes['tail'] = elem.tail

        return attributes

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
    path = r'C:\Users\renpengli\Downloads\CC_benchmark_test_v014_object_part-677b7b5416ee-000000.jsonl.gz'
    idx = 0
    for html_d in read_gz_and_parse_json_line_by_line(path):
        idx += 1
        if idx < 1:
            continue
        if idx > 1:
            break
        print(f"start analysis idx: {idx}, url: {html_d['url']}")
        html_d['html'] = """
        <html>
            <head><title>Sample Page</title></head>
            <body>
               <!--  这里是HEAD 注释内容  -->
                <p>Some text before an image.</p>
                first span tail
                <div>
                    div 的TEXT内容
                    <span>
                        <img src="http://example.com/image1.jpg" />
                        这是span
                    </span>
                    span的TAIL内容
                </div>
                这也是DIV的tail内容
                <p>Some text in between images.</p>
                这是P的tail内容
                <img src="http://example.com/image2.jpg" />
                hello
                <img src="http://example.com/image3.jpg" />
                这是img的tail内容
                <p>Some text after the last image.</p>
                这里是TAIL TEXT
                <span>这是span的内容</span>
                span的tail
            </body>
        </html>
        """
        # print(html_d['html'])
        print('-----\n' * 5)
        res = img.recognize(html_d['url'], [(html_d['html'], html_d['html'])], html_d['html'])
        # parsed_content = """<ccimage by="img" html='&lt;img border="0" src="http://wpa.qq.com/pa?p=2:122405331:41" alt="qq" title="qq"&gt;' src="http://wpa.qq.com/pa?p=2:122405331:41" alt="qq" title="qq">http://wpa.qq.com/pa?p=2:122405331:41</ccimage>"""
        # res = img.to_content_list_node(html_d["url"], parsed_content, html_d["html"])
        print('-----\n' * 5)
        from pprint import pprint

        pprint(res)
        print('-----\n' * 5)
        print(len(res))
# 43 svg, figure -- 21, 92 picture --53, 69 base64--186, 62 svg--26, table -- 1
