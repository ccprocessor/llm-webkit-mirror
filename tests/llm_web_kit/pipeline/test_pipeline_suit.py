"""
测试pipeline_suit.py， 集成测试：
测试方法是：
1. 设定一个场景：从一些散落的html中提取content_list
2. 定义test_pipline_suit_html.jsonc，定义pipeline的执行顺序和模块，数据路径
3. 准备一些html文件，按照零散html的输入标准组织成jsonl数据
4. 执行解析，得到content_list，并比对期望结果

测试需要涵盖：
1. 正确提取时候的content_list是否符合期望
2. 各类异常的抛出是否符合期望
"""
import json
import os
import unittest

from llm_web_kit.input.datajson import DataJson
from llm_web_kit.libs.doc_element_type import DocElementType, ParagraphTextType
from llm_web_kit.pipeline.extractor.html.recognizer.cc_math.common import \
    MathType
from llm_web_kit.pipeline.pipeline_suit import PipelineSuit


class TestPipelineSuitHTML(unittest.TestCase):
    """Test pipeline suit with HTML data."""

    def setUp(self):
        """Set up test fixtures."""
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.html_data_path = os.path.join(
            self.base_path,
            'assets/pipline_suit_input/good_data/html_data_input.jsonl'
        )
        self.pipeline_config = os.path.join(
            self.base_path,
            'assets/pipline_suit_input/html_pipeline_formatter_disable.jsonc'
        )

    def test_html_pipeline(self):
        """Test HTML pipeline with sample data."""
        # Initialize pipeline
        pipeline = PipelineSuit(self.pipeline_config)
        self.assertIsNotNone(pipeline)

        # Read test data
        with open(self.html_data_path, 'r') as f:
            test_data = json.loads(f.readline().strip())

        # Create DataJson from test data
        input_data = DataJson(test_data)

        # Test extraction
        result = pipeline.extract(input_data)

        # Verify basic properties
        self.assertEqual(result.get_dataset_name(), 'test_pipeline_suit')
        self.assertEqual(result.get_file_format(), 'HTML')
        self.assertEqual(result['track_id'], 'f7b3b1b4-0b1b')

        html_content_list = result.get_content_list()[0]
        # Verify content_list
        self.assertEqual(result.get_content_list().length(), 1)
        html_content = html_content_list[0]
        # 首先是h1
        self.assertEqual(html_content['type'], DocElementType.TITLE)
        self.assertEqual(html_content['content']['level'], '1')
        self.assertEqual(html_content['content']['title_content'], 'Heading 1')
        # 然后是p
        html_content = html_content_list[1]
        self.assertEqual(html_content['type'], DocElementType.PARAGRAPH)
        self.assertEqual(html_content['content'][0]['c'], 'Paragraph 1')
        self.assertEqual(html_content['content'][0]['t'], ParagraphTextType.TEXT)
        # 然后是img
        html_content = html_content_list[2]
        self.assertEqual(html_content['type'], DocElementType.IMAGE)
        self.assertEqual(html_content['content']['title'], 'image-title')
        self.assertEqual(html_content['content']['alt'], 'image-alt')
        self.assertEqual(html_content['content']['url'], 'https://www.test.com/test.png')
        self.assertEqual(html_content['content']['caption'], None)

        # 然后是simple table
        html_content = html_content_list[4]
        self.assertEqual(html_content['type'], DocElementType.TABLE)
        self.assertEqual(html_content['content']['is_complex'], False)
        assert html_content['content']['html'].startswith('<table')

        # 然后是complex table
        html_content = html_content_list[5]
        self.assertEqual(html_content['type'], DocElementType.TABLE)
        self.assertEqual(html_content['content']['is_complex'], True)

        # 然后是list
        html_content = html_content_list[6]
        self.assertEqual(html_content['type'], DocElementType.LIST)
        self.assertEqual(len(html_content['content']['items']), 2)
        self.assertEqual(html_content['content']['ordered'], False)
        self.assertEqual(html_content['content']['items'][0][0][0]['c'], '1')
        self.assertEqual(html_content['content']['items'][0][0][0]['t'], ParagraphTextType.TEXT)
        self.assertEqual(html_content['content']['items'][1][0][0]['c'], '2')
        self.assertEqual(html_content['content']['items'][1][0][0]['t'], ParagraphTextType.TEXT)

        # 嵌套list
        html_content = html_content_list[7]
        self.assertEqual(html_content['type'], DocElementType.LIST)
        self.assertEqual(len(html_content['content']['items']), 2)
        self.assertEqual(len(html_content['content']['items'][0][0]), 3)
        self.assertEqual(html_content['content']['items'][0][0][1]['c'], '1.1')
        self.assertEqual(html_content['content']['items'][0][0][1]['t'], ParagraphTextType.TEXT)
        self.assertEqual(html_content['content']['items'][1][0][1]['c'], '2.1')
        self.assertEqual(html_content['content']['items'][1][0][1]['t'], ParagraphTextType.TEXT)

        # 行间公式
        html_content = html_content_list[8]
        self.assertEqual(html_content['type'], DocElementType.EQUATION_INTERLINE)
        self.assertEqual(html_content['content']['math_content'], 'x=\\frac{-b±\\sqrt{{b}^{2}-4ac}}{2a}\\text{.}')
        self.assertEqual(html_content['content']['math_type'], MathType.MATHML)

        # 代码
        html_content = html_content_list[9]
        self.assertEqual(html_content['type'], DocElementType.CODE)
        self.assertEqual(len(html_content['content']['code_content']), 251)
        self.assertEqual(html_content['content']['by'], 'tag_pre_code')

        # 有序列表
        html_content = html_content_list[10]
        self.assertEqual(html_content['type'], DocElementType.LIST)
        self.assertEqual(html_content['content']['ordered'], True)
        self.assertEqual(len(html_content['content']['items']), 2)
        self.assertEqual(html_content['content']['items'][0][0][0]['c'], '100')
        self.assertEqual(html_content['content']['items'][0][0][0]['t'], ParagraphTextType.TEXT)
        self.assertEqual(html_content['content']['items'][1][0][0]['c'], '200')
        self.assertEqual(html_content['content']['items'][1][0][0]['t'], ParagraphTextType.TEXT)
