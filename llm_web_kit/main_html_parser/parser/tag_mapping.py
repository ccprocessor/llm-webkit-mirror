from hashlib import sha256

from lxml import html

from llm_web_kit.exception.exception import TagMappingParserException
from llm_web_kit.input.pre_data_json import PreDataJson, PreDataJsonKey
from llm_web_kit.main_html_parser.parser.parser import BaseMainHtmlParser


class MapItemToHtmlTagsParser(BaseMainHtmlParser):
    def parse(self, pre_data: PreDataJson) -> PreDataJson:
        """将正文的item_id与原html网页tag进行映射, 找出正文内容, 并构造出正文树结构的字典html_element_list
           字典结构
                    {
                     layer_no: {
                                (tag, class, id, ele_sha256, layer_no, idx): (
                                                                  main_label, (parent_tag, parent_class, parent_id)
                                                                  )
                                }
                    }
           e.g. {1: {('head', None, None, 'ida37c725374fc21e', 1, 0): ('green', ('html', None, None)), ('body', 'post-template-default', None, 'idb421920acb189b3d, 1, 1): ('red', ('html', None, None))}}

        Args:
            pre_data (PreDataJson): 包含LLM抽取结果的PreDataJson对象

        Returns:
            PreDataJson: 包含映射结果的PreDataJson对象
        """
        # tag映射逻辑
        try:
            template_html = pre_data[PreDataJsonKey.TYPICAL_RAW_TAG_HTML]
            response_json = pre_data[PreDataJsonKey.LLM_RESPONSE]
            root = html.fromstring(template_html)
            content_list = self.tag_main_html(response_json, root)
            element_dict = self.construct_main_tree(root)
            pre_data[PreDataJsonKey.HTML_TARGET_LIST] = content_list
            pre_data[PreDataJsonKey.HTML_ELEMENT_LIST] = element_dict
        except Exception as e:
            raise TagMappingParserException(e)
        return pre_data

    def get_element_id(self, element):
        """生成稳定的短哈希ID."""
        element_html = html.tostring(element, encoding='unicode', method='html')
        return f'id{sha256(element_html.encode()).hexdigest()}'  # 10位哈希

    def deal_element_direct(self, item_id, test_root):
        # 对正文内容赋予属性magic_main_html
        elements = test_root.xpath(f'//*[@_item_id="{item_id}"]')
        deal_element = elements[0]
        deal_element.set('magic_main_html', 'True')

    def tag_parent(self, pre_root):
        for elem in pre_root.iter():
            magic_main_html = elem.get('magic_main_html', None)
            if not magic_main_html:
                continue
            cur = elem
            while True:
                parent = cur.getparent()
                if not parent:
                    break
                parent_main = parent.get('magic_main_html', None)
                if parent_main:
                    break
                parent.set('magic_main_html', 'True')
                cur = parent

    def tag_main_html(self, response, pre_root):
        content_list = []
        for elem in pre_root.iter():
            item_id = elem.get('_item_id')
            option = f'item_id {item_id}'
            if option in response:
                res = response[option]
                if res == 1:
                    self.deal_element_direct(item_id, pre_root)
                    content_list.append(elem.text)
        # 完善父节点路径
        self.tag_parent(pre_root)
        return content_list

    def construct_main_tree(self, pre_root):
        all_dict = {}
        layer_index_counter = {}
        self.process_tree(pre_root, 0, layer_index_counter, all_dict)

        return all_dict

    def process_tree(self, element, depth, layer_index_counter, all_dict):
        if element is None:
            return
        if depth not in layer_index_counter:
            layer_index_counter[depth] = 0
        else:
            layer_index_counter[depth] += 1
        if depth not in all_dict:
            all_dict[depth] = {}
        is_main_html = element.get('magic_main_html', None)
        current_dict = all_dict[depth]
        ele_id = self.get_element_id(element)
        tag = element.tag
        class_id = element.get('class', None)
        idd = element.get('id', None)
        keyy = (tag, class_id, idd, ele_id, depth, layer_index_counter[depth])
        parent = element.getparent()
        if parent is not None:
            parent_tag = parent.tag
            parent_class_id = parent.get('class', None)
            parent_idd = parent.get('id', None)
            parent_keyy = (parent_tag, parent_class_id, parent_idd)
        else:
            parent_keyy = None
        if is_main_html:
            current_dict[keyy] = ('red', parent_keyy)

        else:
            current_dict[keyy] = ('green', parent_keyy)

        for ele in element:
            self.process_tree(ele, depth + 1, layer_index_counter, all_dict)
