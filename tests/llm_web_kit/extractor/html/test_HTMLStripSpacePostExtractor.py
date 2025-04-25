import json
import unittest

from llm_web_kit.extractor.html.post_extractor import \
    HTMLStripSpacePostExtractor
from llm_web_kit.input.datajson import DataJson


class TestHTMLStripSpacePostExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = HTMLStripSpacePostExtractor({})
        self.data_json = {  # 构造一个测试数据，检测是否把文本中的连续空格字符转换为1个空格字符
            'content_list': [
                [
                    {
                        'type': 'paragraph',
                        'bbox': [0, 0, 50, 50],
                        'raw_content': '',
                        'content': [
                            {'c': '爱因斯坦的质量   方程公式是', 't': 'text'},
                            {'c': 'E=mc^2  ', 't': 'equation-inline'},
                            {'c': '，其中E是能量，m是质量，c是光速 ', 't': 'text'}
                        ]
                    }

                ]
            ]
        }

    def test_space_post_extractor(self):
        # Test basic text normalization
        data_json = DataJson(self.data_json)
        processed = self.extractor.post_extract(data_json).get_content_list()._get_data()
        print('============= processed', json.dumps(processed, ensure_ascii=False))
        # 再看段落的情况
        text_4_processed = processed[0][0]['content'][0]['c']
        text_4_expected = '爱因斯坦的质量 方程公式是'
        self.assertEqual(text_4_processed, text_4_expected)

        text_5_processed = processed[0][0]['content'][1]['c']
        text_5_expected = 'E=mc^2 '
        self.assertEqual(text_5_processed, text_5_expected)

        text_6_processed = processed[0][0]['content'][2]['c']
        text_6_expected = '，其中E是能量，m是质量，c是光速 '
        self.assertEqual(text_6_processed, text_6_expected)
