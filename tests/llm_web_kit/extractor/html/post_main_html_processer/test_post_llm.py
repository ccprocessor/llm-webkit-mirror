import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

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

    def test_get_llm_response_success_f(self):
        """测试成功获取默认LLM响应的情况."""
        test_input = []
        for i in range(3):
            filename = f'assets/html{i}.html'
            test_input.append(base_dir.joinpath(filename).read_text(encoding='utf-8'))

        # 调用被测试的方法
        result = get_llm_response(test_input, self.api_key, self.url, self.model_name, is_llm=False)

        # 验证结果
        self.assertEqual(len(result), len(self.mock_response_content))
        self.assertEqual(True, bool("//form[@class='et_pb_contact_form clearfix']" in str(result)))

    @patch('llm_web_kit.extractor.html.post_main_html_processer.post_llm.request_model')
    def test_get_llm_response_success_t(self, mock_request_model):
        """测试成功获取LLM响应的情况."""
        mock_res = '{"choices": [{"message": {"content": "[\\n    {\\n        \\"xpath\\": \\"//section[@class=\'et_pb_with_border et_pb_module et_pb_fullwidth_header et_pb_fullwidth_header_0 et_animated et_hover_enabled et_pb_text_align_center et_pb_bg_layout_dark et_pb_fullscreen\']\\",\\n        \\"parent_tag\\": \\"div\\",\\n        \\"parent_attributes\\": {\\"class\\": \\"et_pb_section et_pb_section_0 et_pb_with_background et_pb_fullwidth_section et_section_regular\\"},\\n        \\"reason\\": \\"This section represents a header banner with branding and subhead information, which is non-core content as it does not contribute to the main page body.\\"\\n    },\\n    {\\n        \\"xpath\\": \\"//ul[@class=\'et_pb_module et_pb_social_media_follow et_pb_social_media_follow_0 clearfix  et_pb_text_align_center et_pb_bg_layout_light\']\\",\\n        \\"parent_tag\\": \\"div\\",\\n        \\"parent_attributes\\": {\\"class\\": \\"et_pb_column et_pb_column_1_3 et_pb_column_5  et_pb_css_mix_blend_mode_passthrough\\"},\\n        \\"reason\\": \\"This section contains social media links and icons, which are typically non-core content placed in the footer or sidebar for engagement purposes.\\"\\n    },\\n    {\\n        \\"xpath\\": \\"//form[@class=\'et_pb_contact_form clearfix\' and @action=\'https://gillgrencommunication.com/?\']\\",\\n        \\"parent_tag\\": \\"div\\",\\n        \\"parent_attributes\\": {\\"class\\": \\"et_pb_column et_pb_column_2_3 et_pb_column_6  et_pb_css_mix_blend_mode_passthrough et-last-child\\"},\\n        \\"reason\\": \\"This contact form is part of the page layout but is more related to user interaction rather than the core content being presented on the page.\\"\\n    }\\n]"}}]}'
        mock_request_model.return_value = mock_res

        test_input = []
        for i in range(3):
            filename = f'assets/html{i}.html'
            test_input.append(base_dir.joinpath(filename).read_text(encoding='utf-8'))

        result = get_llm_response(test_input, self.api_key, self.url, self.model_name)
        self.assertIn(
            "//section[@class='et_pb_with_border et_pb_module et_pb_fullwidth_header et_pb_fullwidth_header_0 et_animated et_hover_enabled et_pb_text_align_center et_pb_bg_layout_dark et_pb_fullscreen']",
            str(result))

    @patch('llm_web_kit.extractor.html.post_main_html_processer.post_llm.request_model')
    def test_get_llm_response_fail_b(self, mock_request_model):
        """测试成功获取LLM响应的情况."""
        from openai import BadRequestError
        message = 'Range of input length should be [1, 32768]'
        response = MagicMock()
        response.status_code = 400
        response.json.return_value = {
            'error': {
                'message': message,
                'type': 'invalid_request_error',
                'param': None,
                'code': None
            }
        }

        # 创建异常实例
        error = BadRequestError(
            message=message,
            response=response,
            body={}
        )
        mock_request_model.side_effect = error

        test_input = []
        for i in range(3):
            filename = f'assets/html{i}.html'
            test_input.append(base_dir.joinpath(filename).read_text(encoding='utf-8'))

        result = get_llm_response(test_input, self.api_key, self.url, self.model_name)

        self.assertIsNone(result)

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
