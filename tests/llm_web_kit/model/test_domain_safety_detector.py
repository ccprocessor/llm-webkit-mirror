import unittest

from llm_web_kit.model.domain_safety_detector import DomainFilter


class TestDomainFilter(unittest.TestCase):
    def setUp(self):
        self.filter = DomainFilter()

    # 测试基础过滤逻辑
    def test_filter_basic_case(self):
        result = self.filter.filter(
            content_str='Valid content',
            language='en',
            url='https://example.com',
            language_details='formal',
            content_style='professional'
        )
        self.assertTrue(result[0])  # 预期允许通过
        self.assertEqual(result[1], {})  # 预期无附加信息


if __name__ == '__main__':
    unittest.main()
