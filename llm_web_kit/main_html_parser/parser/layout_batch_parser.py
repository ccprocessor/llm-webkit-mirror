import json
import re
from hashlib import sha256

import nltk
from lxml import html
from lxml.html import etree
from nltk.tokenize import word_tokenize

from llm_web_kit.input.pre_data_json import PreDataJson, PreDataJsonKey
from llm_web_kit.libs.html_utils import element_to_html, html_to_element
from llm_web_kit.main_html_parser.parser.parser import BaseMainHtmlParser

nltk.download('punkt', quiet=True)  # 静默模式避免日志干扰

MAX_LENGTH = 10


class LayoutBatchParser(BaseMainHtmlParser):
    """完整处理流程."""
    def __init__(self, template_data: str | dict):
        # 确保模板数据的键是整数类型
        self.template_data = template_data

    def parse_tuple_key(self, key_str):
        if key_str.startswith('(') and key_str.endswith(')'):
            try:
                return eval(key_str)  # WARNING: eval is unsafe for untrusted data!
            except (SyntaxError, ValueError):
                return key_str  # Fallback if parsing fails
        return key_str

    def parse(self, pre_data: PreDataJson) -> PreDataJson:
        # 支持输入字符串和tag mapping后的dict对象
        html_source = pre_data['html_source']
        template_data_str = pre_data['html_element_dict']
        template_data = dict()
        if isinstance(template_data_str, str):
            template_data_str = json.loads(template_data_str)
            for layer, layer_dict in template_data_str.items():
                layer_dict_json = {self.parse_tuple_key(k): v for k, v in layer_dict.items()}
                template_data[int(layer)] = layer_dict_json
        elif isinstance(template_data_str, dict):
            template_data = template_data_str
        else:
            raise ValueError(f'template_data 类型错误: {type(template_data_str)}')
        pipeline = LayoutBatchParser(template_data)
        content, body = pipeline.process(html_source)
        pre_data[PreDataJsonKey.MAIN_HTML] = content
        pre_data[PreDataJsonKey.MAIN_HTML_BODY] = body
        return pre_data

    def get_element_id(self, element):
        """生成稳定的短哈希ID."""
        element_html = html.tostring(element, encoding='unicode', method='html')
        return f'id{sha256(element_html.encode()).hexdigest()}'  # 10位哈希

    def process(self, html_source: str) -> str:
        # 根据颜色删减html_source
        processed_html = self.drop_node_element(html_source, self.template_data)
        content, body = self.htmll_to_content2(processed_html)
        return content, body

    def get_tokens(self, content):
        tokens = word_tokenize(content)
        return tokens

    def normalize_key(self, tup):
        if not tup:
            return None
        tag, class_id, idd = tup
        # 如果有id，则无需判断class，因为有的网页和模版id相同，但是class不同
        if tag in ['body', 'html']:
            return (tag, None, None)
        if idd:
            return (tag, None, self.replace_post_number(idd))
        return (tag, self.replace_post_number(class_id), self.replace_post_number(idd))

    def replace_post_number(self, text):
        if not text:
            return None
        # 匹配 "post-数字" 或 "postid-数字"（不区分大小写），并替换数字部分为空
        pattern = r'(post|postid)-(\d+)'
        # 使用 \1 保留前面的 "post" 或 "postid"，但替换数字部分
        return re.sub(pattern, lambda m: f'{m.group(1)}-', text, flags=re.IGNORECASE)

    def find_blocks_drop(self, element, depth, element_dict, parent_keyy, parent_label):
        # 判断这个tag是否有id
        if isinstance(element, etree._Comment):
            return
        length = len(self.get_tokens(element.text_content().strip()))
        length_tail = 0
        if element.tail:
            length_tail = len(element.tail.strip())
        idd = element.get('id')
        tag = element.tag
        layer_nodes = element_dict[depth]
        class_tag = element.get('class')
        element_id = self.get_element_id(element)
        keyy = (tag, class_tag, idd, element_id)
        keyy = self.normalize_key((tag, class_tag, idd))
        # 如果有id，则找到root下面一层子节点对应id的节点，如找不到，则新增一个子节点
        # TODO 目前只搜索下面一层，而不是搜索全部，如果更改搜索逻辑，树结构也会受到影响，当前逻辑可能会导致有多个id相同但层级不同的节点（在这一批html 的id结构不完全一致的情况下），全部从头搜索会产出id唯一的节点
        has_red = False
        layer_nodes_list = []
        layer_nodes_dict = dict()
        for node_keyy, node_value in layer_nodes.items():
            node_parent_keyy = self.normalize_key(node_value[1])
            if node_parent_keyy is not None:
                node_parent_keyy = tuple(node_parent_keyy)
            node_label = node_value[0]
            if node_parent_keyy == parent_keyy:
                layer_nodes_list.append((node_keyy[:3], node_label))
                if self.normalize_key(node_keyy[:3]) in layer_nodes_dict:
                    layer_nodes_dict[self.normalize_key(node_keyy[:3])].append(node_label)
                else:
                    layer_nodes_dict[self.normalize_key(node_keyy[:3])] = [node_label]

            if node_label == 'red' and node_parent_keyy == parent_keyy:
                has_red = True
        if not has_red and parent_label != 'red':
            parent = element.getparent()
            if parent is not None:
                parent.remove(element)
            return
        # 当前层无红色节点，但父节点是红的，则整体输出这一层
        elif not has_red and parent_label == 'red':
            return
        label = None
        if keyy in layer_nodes_dict:
            if 'red' not in layer_nodes_dict[keyy]:
                parent = element.getparent()
                if parent is not None:
                    parent.remove(element)
                return
            else:
                label = 'red'
        elif length > 0 or length_tail > 0:
            return

        for child in element:
            self.find_blocks_drop(child, depth + 1, element_dict, keyy, label)

    def drop_node_element(self, html_source, element_dict):
        # 解析 HTML 内容
        tree = html_to_element(html_source)
        self.find_blocks_drop(tree, 0, element_dict, None, '')
        return element_to_html(tree)

    def htmll_to_content2(self, body_str):
        body = html.fromstring(body_str)
        tags_to_remove = ['header', 'footer', 'nav', 'aside', 'script', 'style']
        for tag in tags_to_remove:
            for element in body.xpath(f'//{tag}'):
                element.getparent().remove(element)
        self.add_newline_after_tags(body, ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'br', 'span', 'div', 'p', 'li'])
        output = []
        main_content = re.split(r'\n{1,}', self.get_text_with_newlines(body))
        for line in main_content:
            if line.strip():
                output.append(line)
        return '\n\n'.join(output), element_to_html(body)

    def add_newline_after_tags(self, element, tags):
        # Find all specified tags
        for tag in tags:
            for elem in element.xpath(f'//{tag}'):
                # Add a newline character after each specified tag
                if elem.tail:
                    elem.tail = '\n' + elem.tail
                else:
                    elem.tail = '\n'

    def get_text_with_newlines(self, element):
        text = []
        for item in element.iter():
            if item.tag in ['br', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'tr', 'div']:
                text.append(item.text if item.text else '')
                text.append('\n')
            elif item.tag in ['td', 'th']:
                text.append(item.text if item.text else '')
                text.append('\t')
            else:
                text.append(item.text if item.text else '')

            if item.tail:
                text.append(item.tail)

        return ''.join(text)
