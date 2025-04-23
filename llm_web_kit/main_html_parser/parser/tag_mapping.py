from llm_web_kit.exception.exception import TagMappingParserException
from llm_web_kit.input.pre_data_json import PreDataJson, PreDataJsonKey
from llm_web_kit.main_html_parser.parser.parser import BaseMainHtmlParser
from html_alg_lib.simplify import general_simplify
from html_alg_lib.base_funcs import document_fromstring
from html_alg_lib.normalize import (
    pre_normalize_html,
)

from lxml import html
from hashlib import sha256
import copy

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
        # ...
        try:
            template_html = pre_data['html_source']
            response_json = pre_data['response_json']
            root = document_fromstring(template_html)
            title, simplified_root = general_simplify(root)
            root = document_fromstring(template_html)
            pre_root = pre_normalize_html(root)
            if isinstance(simplified_root, tuple):
                simplified_root, mapp = simplified_root
            test_root = copy.deepcopy(pre_root)
            test_sim_root = copy.deepcopy(simplified_root)
            content_list = self.tag_main_html(response_json, mapp, test_root, test_sim_root)
            element_dict = self.construct_main_tree(test_root)

            # 设置输出数据
            pre_data[PreDataJsonKey.HTML_TARGET_LIST] = content_list
            pre_data[PreDataJsonKey.HTML_ELEMENT_LIST] = element_dict
        except Exception as e:
            raise TagMappingParserException(e)
        return pre_data


    def get_element_id(self, element):
        """生成稳定的短哈希ID"""
        element_html = html.tostring(element, encoding='unicode', method='html')
        return f"id{sha256(element_html.encode()).hexdigest()}"  # 10位哈希


    def find_affected_element_after_drop(self, element):
        prev_sibling = element.getprevious()
        parent = element.getparent()

        element.drop_tag()

        if prev_sibling is not None:
            return prev_sibling
        else:
            return parent


    def process_element(self, element):
        # 前序遍历元素树（先处理子元素）
        for child in list(element):  # 使用list()创建副本，因为我们会修改原元素
            self.process_element(child)

        # 如果是cc-alg-uc-text标签，用drop_tag()删除标签但保留子元素
        if element.tag == 'cc-alg-uc-text':
            is_main = element.get('magic_main_html', None)
            affected = self.find_affected_element_after_drop(element)
            if is_main:
                affected.set('magic_main_html', "True")

        # 删除指定属性
        for attr in ['cc-alg-node-tags', 'cc-alg-node-ids']:
            if attr in element.attrib:
                del element.attrib[attr]
        return


    def deal_element_direct(self, item_id, mapp, test_root):
        node_ids = mapp[item_id].split(' ')
        # 对正文内容赋予属性magic_main_html
        for node_id in node_ids:
            elements = test_root.xpath(f'//*[@cc-alg-node-ids="{node_id}"]')
            deal_element = elements[0]
            deal_element.set('magic_main_html', "True")



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
                parent.set('magic_main_html', "True")
                cur = parent

    def tag_main_html(self, response, mapp, pre_root, sim_root):
        content_list = []
        for elem in sim_root.iter():
            item_id = elem.get('_item_id')
            option = f'Option {item_id}'
            if option in response:
                res = response[option]['isMain']
                if res.lower() in ['yes', 'may yes']:
                    self.deal_element_direct(item_id, mapp, pre_root)
                    content_list.append(elem.text)


        # 恢复到原网页结构
        self.process_element(pre_root)
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
