import json

from llm_web_kit.input.datajson import ContentList
from llm_web_kit.libs.doc_element_type import DocElementType


class Statics:
    def __init__(self):
        self.statics = {}

    def add(self, key, value):
        self.statics[key] = value

    def get(self, key):
        return self.statics[key]

    def get_all(self):
        return self.statics

    def clear(self):
        self.statics = {}

    def print(self):
        for key, value in self.statics.items():
            print(f'{key}: {value}')

    def save(self, path):
        with open(path, 'w') as f:
            json.dump(self.statics, f)

    def merge_statics(self, statics: dict) -> dict:
        """合并多个contentlist的统计结果.

        Args:
            statics: 每个contentlist的统计结果
        Returns:
            dict: 合并后的统计结果
        """
        for key, value in statics.items():
            if isinstance(value, (int, float)):
                self.statics[key] = self.statics.get(key, 0) + value

        return self.statics

    def get_statics(self, contentlist: ContentList) -> dict:
        """
        统计contentlist中每个元素的type的数量
        Returns:
            dict: 每个元素的类型的数量
        """
        result = {}

        def process_list_items(items, parent_type):
            """递归处理列表项
            Args:
                items: 列表项
                parent_type: 父元素类型（用于构建统计key）
            """
            if isinstance(items, list):
                for item in items:
                    process_list_items(item, parent_type)
            elif isinstance(items, dict) and 't' in items:
                # 到达最终的文本/公式元素
                item_type = f"{parent_type}.{items['t']}"
                current_count = result.get(item_type, 0)
                result[item_type] = current_count + 1

        for page in contentlist._get_data():  # page是每一页的内容列表
            for element in page:  # element是每个具体元素
                # 1. 统计基础元素
                element_type = element['type']
                current_count = result.get(element_type, 0)
                result[element_type] = current_count + 1

                # 2. 统计复合元素内部结构
                if element_type == DocElementType.PARAGRAPH:
                    # 段落内部文本类型统计
                    for item in element['content']:
                        item_type = f"{DocElementType.PARAGRAPH}.{item['t']}"
                        current_count = result.get(item_type, 0)
                        result[item_type] = current_count + 1

                elif element_type == DocElementType.LIST:
                    # 使用递归函数处理列表项
                    process_list_items(element['content']['items'], DocElementType.LIST)
        self.merge_statics(result)
        return result
