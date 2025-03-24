import json

from llm_web_kit.input.datajson import ContentList
from llm_web_kit.libs.doc_element_type import DocElementType


class Statics:
    """统计content_list中每个元素的type的数量."""
    def __init__(self, statics: dict = None):
        self.statics = statics if statics else {}
        self._validate(self.statics)

    def _validate(self, statics: dict):
        """校验statics的格式.需要是字典且只有一个为"statics"的key.示例:
            {
                "list": 1,
                "list.text": 2,
                "list.equation-inline": 1,
                "paragraph": 2,
                "paragraph.text": 2,
                "equation-interline": 2
            }
        """
        if not isinstance(statics, dict):
            raise ValueError('statics must be a dict')

    def __additem__(self, key, value):
        self.statics[key] = value

    def __getitem__(self, key):
        return self.statics[key]

    def __getall__(self):
        return self.statics

    def __clear__(self):
        self.statics = {}

    def print(self):
        print(json.dumps(self.statics, indent=4))

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
        self.__clear__()

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
                current_count = self.statics.get(item_type, 0)
                self.statics[item_type] = current_count + 1

        for page in contentlist._get_data():  # page是每一页的内容列表
            for element in page:  # element是每个具体元素
                # 1. 统计基础元素
                element_type = element['type']
                current_count = self.statics.get(element_type, 0)
                self.statics[element_type] = current_count + 1

                # 2. 统计复合元素内部结构
                if element_type == DocElementType.PARAGRAPH:
                    # 段落内部文本类型统计
                    for item in element['content']:
                        item_type = f"{DocElementType.PARAGRAPH}.{item['t']}"
                        current_count = self.statics.get(item_type, 0)
                        self.statics[item_type] = current_count + 1

                elif element_type == DocElementType.LIST:
                    # 使用递归函数处理列表项
                    process_list_items(element['content']['items'], DocElementType.LIST)
                elif element_type == DocElementType.COMPLEX_TABLE:
                    # 统计复杂表格数量
                    if element.get('content', {}).get('is_complex', False):
                        item_type = f'{DocElementType.COMPLEX_TABLE}.complex'
                        current_count = self.statics.get(item_type, 0)
                        self.statics[item_type] = current_count + 1

        return self.statics
