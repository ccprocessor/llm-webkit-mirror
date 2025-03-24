import json
import os
import unittest

from llm_web_kit.extractor.html.recognizer.text import TextParagraphRecognizer
from llm_web_kit.libs.html_utils import html_to_element


class TestTextParagraphRecognizer(unittest.TestCase):
    """测试文本段落识别器."""

    def setUp(self):
        self.recognizer = TextParagraphRecognizer()
        self.test_data_dir = f'{os.path.dirname(os.path.abspath(__file__))}/assets/recognizer'

    def test_recognize_simple_para(self):
        """测试识别简单段落."""
        # 准备测试数据
        with open(os.path.join(self.test_data_dir, 'simple_para.html'), 'r', encoding='utf-8') as f:
            html = f.read()

        # 执行识别
        result = self.recognizer.recognize('', [(html_to_element(html), html_to_element(html))], html)

        # 验证结果
        self.assertEqual(len(result), 2)  # 应该识别出2个段落

        # 验证第一个段落
        first_para = result[0][0]
        ccel = first_para
        jso = json.loads(ccel.text)
        self.assertEqual(jso[0]['c'], '质量方程')
        self.assertEqual(jso[0]['t'], 'text')

        # 验证第二个段落
        second_para = result[1][0]
        text = second_para.text
        jso = json.loads(text)
        self.assertEqual(jso[0]['c'], '爱因斯坦的方程')
        self.assertEqual(jso[0]['t'], 'text')
        self.assertEqual(jso[1]['c'], 'E=MC^2')
        self.assertEqual(jso[1]['t'], 'equation-inline')
        self.assertTrue(jso[2]['c'].endswith('请访问'))
        self.assertEqual(jso[3]['c'], 'https://abc.com')
        self.assertEqual(jso[3]['t'], 'code-inline')
        self.assertEqual(jso[4]['c'], '.')
