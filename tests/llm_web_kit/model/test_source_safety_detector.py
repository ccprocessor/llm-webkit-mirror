import unittest

from llm_web_kit.model.source_safety_detector import SourceFilter


class TestSourceFilter(unittest.TestCase):
    def setUp(self):
        self.filter = SourceFilter()

    # 测试非法来源
    def test_unsafe_source(self):
        result = self.filter.filter(
            content_str='Unverified data',
            language='en',
            data_source='http://unknown-site.com',
            language_details='informal',
            content_style='user-generated'
        )
        self.assertFalse(result['from_safe_source'])
        self.assertFalse(result['from_domestic_source'])


if __name__ == '__main__':
    unittest.main()
