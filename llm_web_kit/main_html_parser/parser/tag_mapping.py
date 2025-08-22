from lxml import etree, html
from selectolax.parser import HTMLParser

from llm_web_kit.exception.exception import TagMappingParserException
from llm_web_kit.html_layout.html_layout_cosin import get_feature, similarity
from llm_web_kit.input.pre_data_json import PreDataJson, PreDataJsonKey
from llm_web_kit.main_html_parser.parser.layout_batch_parser import \
    LayoutBatchParser
from llm_web_kit.main_html_parser.parser.parser import BaseMainHtmlParser

SIMILAR_THRESHOLD = 0.92


class MapItemToHtmlTagsParser(BaseMainHtmlParser):
    def parse(self, pre_data: PreDataJson) -> PreDataJson:
        """将正文的item_id与原html网页tag进行映射, 找出正文内容, 并构造出正文树结构的字典html_element_list，使用相似度判断正文抽取效果
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
            template_raw_html = pre_data[PreDataJsonKey.TYPICAL_RAW_HTML]
            selectolax_tree = HTMLParser(template_raw_html)
            template_raw_html = selectolax_tree.html
            template_tag_html = pre_data[PreDataJsonKey.TYPICAL_RAW_TAG_HTML]
            response_json = pre_data[PreDataJsonKey.LLM_RESPONSE]
            root = html.fromstring(template_tag_html)
            tree = etree.ElementTree(root)
            # 抽取正文树结构
            content_list = self.tag_main_html(response_json, root)
            element_dict, template_dict_html = self.construct_main_tree(root, tree)

            # 检查response_json中的所有值是否都为0
            all_values_zero = True
            if isinstance(response_json, dict):
                for value in response_json.values():
                    if value != 0:
                        all_values_zero = False
                        break
            else:
                all_values_zero = False

            # 如果所有值都为0，直接返回空的HTML
            if all_values_zero:
                pre_data[PreDataJsonKey.TYPICAL_MAIN_HTML] = ''
                pre_data[PreDataJsonKey.HTML_TARGET_LIST] = content_list
                pre_data[PreDataJsonKey.HTML_ELEMENT_DICT] = element_dict
                pre_data[PreDataJsonKey.TYPICAL_DICT_HTML] = template_dict_html
                pre_data[PreDataJsonKey.SIMILARITY_LAYER] = 0
                pre_data[PreDataJsonKey.TYPICAL_MAIN_HTML_SUCCESS] = False
                pre_data[PreDataJsonKey.LLM_RESPONSE_EMPTY] = True
                return pre_data

            # 模版抽取正文html
            parser = LayoutBatchParser({})
            extract_info = {PreDataJsonKey.HTML_SOURCE: template_raw_html,
                            PreDataJsonKey.HTML_ELEMENT_DICT: element_dict}
            extract_info_json = PreDataJson(extract_info)
            parts = parser.parse(extract_info_json)
            template_extract_html = parts[PreDataJsonKey.MAIN_HTML_BODY]

            # 检验模版抽取效果
            feature1 = get_feature(template_raw_html)
            feature2 = get_feature(template_extract_html)
            layer = self.__get_max_width_layer(element_dict)
            template_sim = None
            if feature1 is not None and feature2 is not None:
                template_sim = similarity(feature1, feature2, layer_n=layer)
                pre_data[PreDataJsonKey.TYPICAL_MAIN_HTML_SIM] = template_sim

                # 比较模版正文html与原html相似度
            if template_sim is None or template_sim > SIMILAR_THRESHOLD:
                pre_data[PreDataJsonKey.TYPICAL_MAIN_HTML_SUCCESS] = False
            else:
                pre_data[PreDataJsonKey.TYPICAL_MAIN_HTML_SUCCESS] = True

            # 结果返回
            pre_data[PreDataJsonKey.SIMILARITY_LAYER] = layer
            pre_data[PreDataJsonKey.TYPICAL_MAIN_HTML] = template_extract_html
            pre_data[PreDataJsonKey.HTML_TARGET_LIST] = content_list
            pre_data[PreDataJsonKey.HTML_ELEMENT_DICT] = element_dict
            pre_data[PreDataJsonKey.TYPICAL_DICT_HTML] = template_dict_html
        except Exception as e:
            raise TagMappingParserException(e)
        return pre_data

    def parse_single(self, pre_data: PreDataJson) -> PreDataJson:
        """
            skip element dict construct step, remove all non-main tags in template tagged html directly
            for single-html extraction plan
            Args:
                pre_root:
            Returns:
                PreDataJson: 包含映射结果的PreDataJson对象
        """
        try:
            template_tag_html = pre_data[PreDataJsonKey.TYPICAL_RAW_TAG_HTML]
            response_json = pre_data[PreDataJsonKey.LLM_RESPONSE]
            source_html = pre_data[PreDataJsonKey.TYPICAL_RAW_HTML]
            root = html.fromstring(template_tag_html)
            # 直接抽取正文
            content_list = self.tag_main_html(response_json, root)
            template_extract_html = self.__extract_main_directly(root)
            if pre_data.get('success_label_enable', False):
                feature1 = get_feature(source_html)
                feature2 = get_feature(template_extract_html)
                layer = 6
                template_sim = None
                if feature1 is not None and feature2 is not None:
                    template_sim = similarity(feature1, feature2, layer_n=layer)

                # 比较模版正文html与原html相似度
                if template_sim is None or template_sim > SIMILAR_THRESHOLD:
                    pre_data[PreDataJsonKey.TYPICAL_MAIN_HTML_SUCCESS] = False
                else:
                    pre_data[PreDataJsonKey.TYPICAL_MAIN_HTML_SUCCESS] = True

            pre_data[PreDataJsonKey.TYPICAL_MAIN_HTML] = template_extract_html
            pre_data[PreDataJsonKey.HTML_TARGET_LIST] = content_list
        except Exception as e:
            raise TagMappingParserException(e)
        return pre_data

    def __get_max_width_layer(self, element_dict):
        max_length = 0
        max_width_layer = 0
        for layer_n, layer in element_dict.items():
            if len(layer) > max_length:
                max_width_layer = layer_n
                max_length = len(layer)

        return max_width_layer - 2 if max_width_layer > 4 else 3

    def deal_element_direct(self, item_id, test_root):
        # 对正文内容赋予属性magic_main_html
        elements = test_root.xpath(f'//*[@_item_id="{item_id}"]')
        deal_element = elements[0]
        deal_element.set('magic_main_html', 'True')
        for ele in deal_element:
            try:
                ele.set('magic_main_html', 'True')
            except Exception:
                continue

    def find_affected_element_after_drop(self, element):
        prev_sibling = element.getprevious()
        parent = element.getparent()
        is_main = bool(element.get('magic_main_html', None))
        # 包裹子节点的情况返回element父节点
        if len(element) > 0:
            if is_main:
                for ele in element:
                    try:
                        ele.set('magic_main_html', 'True')
                    except Exception:
                        continue

            element.drop_tag()
            # 如果包含子tag并且还有text，text有可能是兄弟节点的tail
            if element.text and element.text.strip():
                if prev_sibling is not None:
                    # 兄弟节点是否drop text， 是否drop tail
                    return prev_sibling, False, not is_main
                else:
                    return parent, not is_main, False
            return parent, False, False

        # 只有文本的情况，返回element前面的兄弟节点或者父节点
        element.drop_tag()

        if prev_sibling is not None:
            return prev_sibling, False, not is_main
        else:
            return parent, not is_main, False

    def process_element(self, element):
        # 前序遍历元素树（先处理子元素）
        for child in list(element):  # 使用list()创建副本，因为我们会修改原元素
            self.process_element(child)

        # 如果是cc-alg-uc-text标签，用drop_tag()删除标签但保留子元素
        if element.tag == 'cc-alg-uc-text':
            is_main = element.get('magic_main_html', None)
            affected, drop_text, drop_tail = self.find_affected_element_after_drop(element)
            if is_main:
                affected.set('magic_main_html', 'True')
            if drop_text:
                affected.set('drop_text', 'True')
            if drop_tail:
                affected.set('drop_tail', 'True')

        return

    def tag_parent(self, pre_root):
        for elem in pre_root.iter():
            magic_main_html = elem.get('magic_main_html', None)
            if not magic_main_html:
                continue
            cur = elem
            while True:
                parent = cur.getparent()
                if parent is None:
                    break
                parent_main = parent.get('magic_main_html', None)
                if parent_main:
                    break
                parent.set('magic_main_html', 'True')
                cur = parent

    def __extract_main_directly(self, pre_root):
        def iter_process(elem):
            if isinstance(elem, etree._Comment):
                return
            magic_main_html = elem.get('magic_main_html', None)
            if magic_main_html:
                # 查找所有子孙节点中 magic_main_html='True' 的元素
                matching_elements = elem.xpath(
                    './/*[@magic_main_html="True"]'
                )
                # 给正文最小单元节点的子孙节点补上正文标识，避免被删除
                if len(matching_elements) == 0:
                    for child in elem.iterdescendants():  # 仅遍历子孙节点（不包括自身）
                        child.set('magic_main_html', 'True')
            else:
                # 非正文节点直接删除
                parent = elem.getparent()
                if parent is not None:
                    parent.remove(elem)
            for elem_child in elem:
                iter_process(elem_child)

        if pre_root is None:
            return None
        iter_process(pre_root)
        return html.tostring(pre_root, encoding='utf-8').decode()

    def tag_main_html(self, response, pre_root):
        content_list = []
        for elem in pre_root.iter():
            item_id = elem.get('_item_id')
            option = f'item_id {item_id}'
            if option in response:
                res = response[option]
                if res == 1:
                    self.deal_element_direct(item_id, pre_root)
                    text_nodes = elem.xpath('.//text()[not(ancestor::style or ancestor::script)]')  # 获取所有文本节点（包括tail）
                    all_text = ' '.join([t.strip() for t in text_nodes if t.strip()])
                    content_list.append(all_text)
        # 恢复到原网页结构
        self.process_element(pre_root)
        # 完善父节点路径
        self.tag_parent(pre_root)
        return content_list

    def process_main_tree(self, element, depth, layer_index_counter, all_dict, all_set, tree):
        if element is None:
            return
        if isinstance(element, etree._Comment):
            return
        if depth not in layer_index_counter:
            layer_index_counter[depth] = 0
        else:
            layer_index_counter[depth] += 1
        if depth not in all_dict:
            all_dict[depth] = {}
            all_set[depth] = {}
        is_main_html = element.get('magic_main_html', None)
        is_drop_tail = element.get('drop_tail', None)
        current_dict = all_dict[depth]
        current_set = all_set[depth]
        tag = element.tag
        class_id = element.get('class', None)
        idd = element.get('id', None)
        keyy = (tag, class_id, idd, depth, layer_index_counter[depth])

        parent = element.getparent()
        if parent is not None:
            parent_tag = parent.tag
            parent_class_id = parent.get('class', None)
            parent_idd = parent.get('id', None)
            parent_keyy = (parent_tag, parent_class_id, parent_idd)
        else:
            parent_keyy = None
        # 为了让element_dict不过大，简化这个字典
        keyy_for_sim = (keyy[:3], parent_keyy)

        if is_main_html:
            color = 'red'
        else:
            color = 'green'
        xpath = tree.getpath(element)
        # 写入该层元素key，如果有重复的green节点，只保留一个
        if keyy_for_sim in current_set:
            if is_main_html and current_set[keyy_for_sim][0] == 'green':
                current_dict[keyy] = ('red', parent_keyy, xpath, bool(is_drop_tail))
                current_set[keyy_for_sim] = ('red', parent_keyy)
        else:
            current_dict[keyy] = (color, parent_keyy, xpath, bool(is_drop_tail))
            current_set[keyy_for_sim] = (color, parent_keyy)

        for ele in element:
            self.process_main_tree(ele, depth + 1, layer_index_counter, all_dict, all_set, tree)

    def construct_main_tree(self, pre_root, tree):
        all_dict = {}
        all_set = {}
        layer_index_counter = {}
        self.process_main_tree(pre_root, 0, layer_index_counter, all_dict, all_set, tree)
        template_dict_html = html.tostring(pre_root, encoding='utf-8').decode()
        return all_dict, template_dict_html
