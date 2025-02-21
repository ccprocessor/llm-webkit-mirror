import unittest

from llm_web_kit.extractor.html.post_extractor import \
    ContentListStaticsPostExtractor
from llm_web_kit.input.datajson import DataJson, DataJsonKey


class TestContentListStaticsPostExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = ContentListStaticsPostExtractor({})
        self.data_json = {  # 构造一个测试数据，检测是否把文本中的连续空格字符转换为1个空格字符
            'content_list': [
                [
                    {
                        'type': 'list',
                        'raw_content': '',
                        'content': {
                            'items': [
                                [
                                    [
                                        {'c': '爱因斯坦的   质量方差公式是', 't': 'text'},
                                        {'c': 'E=mc^2   ', 't': 'equation-inline'},
                                        {'c': '，其中E是\t\t能量，m是质量，c是光速  ', 't': 'text'}
                                    ]
                                ],
                                [
                                    [
                                        {'c': '爱因斯坦的质量方差公式是', 't': 'text'},
                                        {'c': 'E=mc^2  ', 't': 'equation-inline'},
                                        {'c': '，其中E是  能量，m是质量，c是光速 ', 't': 'text'}
                                    ]
                                ]
                            ],
                            'ordered': True
                        }
                    },
                    {
                        'type': 'paragraph',
                        'bbox': [0, 0, 50, 50],
                        'raw_content': '',
                        'content': [
                            {'c': '爱因斯坦的质量   方程公式是', 't': 'text'},
                            {'c': 'E=mc^2  ', 't': 'equation-inline'},
                            {'c': '，其中E是能量，m是质量，c是光速 ', 't': 'text'}
                        ]
                    },
                    {
                        'type': 'equation-interline',
                        'bbox': [0, 0, 50, 50],
                        'raw_content': 'a^2 + b^2 = c^2',
                        'content': {
                            'math_content': 'a^2 + b^2 = c^2',
                            'math_type': 'kelatex|mathml|asciimath'
                        }
                    },
                    {
                        'type': 'table',
                        'raw_content': '',
                        'content': {
                            'html': '<table><tr><td>1</td><td>2</td></tr></table>',
                            'is_complex': True
                        }
                    }
                ]
            ]
        }

    def test_content_list_statics_post_extractor(self):
        data_json = DataJson(self.data_json)
        self.extractor.post_extract(data_json)
        self.assertEqual(data_json.get(DataJsonKey.METAINFO, {}).get(DataJsonKey.STATICS, {}).get('list'), 1)
        self.assertEqual(data_json.get(DataJsonKey.METAINFO, {}).get(DataJsonKey.STATICS, {}).get('list.text'), 4)
        self.assertEqual(data_json.get(DataJsonKey.METAINFO, {}).get(DataJsonKey.STATICS, {}).get('list.equation-inline'), 2)
        self.assertEqual(data_json.get(DataJsonKey.METAINFO, {}).get(DataJsonKey.STATICS, {}).get('paragraph'), 1)
        self.assertEqual(data_json.get(DataJsonKey.METAINFO, {}).get(DataJsonKey.STATICS, {}).get('paragraph.text'), 2)
        self.assertEqual(data_json.get(DataJsonKey.METAINFO, {}).get(DataJsonKey.STATICS, {}).get('paragraph.equation-inline'), 1)
        self.assertEqual(data_json.get(DataJsonKey.METAINFO, {}).get(DataJsonKey.STATICS, {}).get('equation-interline'), 1)
        self.assertEqual(data_json.get(DataJsonKey.METAINFO, {}).get(DataJsonKey.STATICS, {}).get('table'), 1)
        self.assertEqual(data_json.get(DataJsonKey.METAINFO, {}).get(DataJsonKey.STATICS, {}).get('table.complex'), 1)
