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

        # Verify content_list
        pass
