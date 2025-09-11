import unittest
from pathlib import Path

from llm_web_kit.extractor.html.post_main_html_processer.post_llm import (
    clean_json_data, get_llm_response)

base_dir = Path(__file__).parent


class TestGetLLMResponse(unittest.TestCase):

    def setUp(self):
        """测试前的准备工作."""
        self.api_key = ''
        self.url = ''
        self.model_name = ''

        # 模拟的LLM输出
        self.mock_response_content = [
            {
                'xpath': "//div[@class='et_pb_section_1 et_pb_with_background et_section_regular']",
                'parent_tag': 'div',
                'parent_attributes': {'id': 'main-content'},
                'reson': 'This section contains contact information and social media links, which are typically non-core content placed at the bottom of a webpage.'
            },
            {
                'xpath': "//ul[@class='et_pb_module et_pb_social_media_follow et_pb_social_media_follow_0 clearfix  et_pb_text_align_center et_pb_bg_layout_light']",
                'parent_tag': 'div',
                'parent_attributes': {'class': 'et_pb_section_1 et_pb_with_background et_section_regular'},
                'reson': 'This is a social media follow block, commonly considered non-core content and usually found at the bottom of pages.'
            },
            {
                'xpath': "//form[@class='et_pb_contact_form clearfix']",
                'parent_tag': 'div',
                'parent_attributes': {'class': 'et_pb_section_1 et_pb_with_background et_section_regular'},
                'reson': 'This is a contact form, often used for user interaction but not central to the main page content.'
            }
        ]

    def test_get_llm_response_success(self):
        """测试成功获取LLM响应的情况."""
        test_input = []
        for i in range(3):
            filename = f'assets/html{i}.html'
            test_input.append(base_dir.joinpath(filename).read_text(encoding='utf-8'))

        # 调用被测试的方法
        result = get_llm_response(test_input, self.api_key, self.url, self.model_name, is_llm=False)

        # 验证结果
        self.assertEqual(len(result), len(self.mock_response_content))
        self.assertEqual(True, bool("//form[@class='et_pb_contact_form clearfix']" in str(result)))

    def test_get_llm_response_fail(self):
        """测试获取LLM响应失败的情况."""
        test_input = []
        for i in range(3):
            filename = f'assets/html{i}.html'
            test_input.append(base_dir.joinpath(filename).read_text(encoding='utf-8'))

        # 调用被测试的方法
        result = get_llm_response(test_input, self.api_key, self.url, self.model_name)

        # 验证结果
        self.assertIsNone(result)

    def test_valid_json_without_markdown_wrapping(self):
        """测试不带 Markdown 包裹的合法 JSON."""
        input_text = '{"key": "value"}'
        expected = {'key': 'value'}
        result = clean_json_data(input_text)
        self.assertEqual(result, expected)

    def test_invalid_json_syntax(self):
        """测试语法错误的 JSON."""
        input_text = '{"key": value}'
        result = clean_json_data(input_text)
        self.assertIsNone(result)

    def test_empty_content(self):
        """测试空内容."""
        input_text = ''
        result = clean_json_data(input_text)
        self.assertIsNone(result)

    def test_completely_invalid_string(self):
        """测试完全不相关的字符串."""
        input_text = 'this is not json'
        result = clean_json_data(input_text)
        self.assertIsNone(result)
