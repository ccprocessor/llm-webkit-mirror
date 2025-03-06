import unittest

from llm_web_kit.extractor.html.pre_extractor import \
    HTMLFileFormatCleanTagsPreExtractor
from llm_web_kit.input.datajson import DataJson

TEST_CASES = [
    # 基本测试：保留不匹配的内容
    {
        'input': {
            'content_list': [],
            'data_source_category': 'html',
            'url': 'https://example.com/page',
            'html': '<html><body><div class="normal">visible content</div></body></html>',
        },
        'expected_html': '<html><body><div class="normal">visible content</div></body></html>'
    },

    # 测试广告标签移除 - class以advert开头
    {
        'input': {
            'content_list': [],
            'data_source_category': 'html',
            'url': 'https://example.com/page',
            'html': '<html><body><div class="advertisement">广告内容</div><p>正常内容</p></body></html>',
        },
        'expected_html': '<html><body><p>正常内容</p></body></html>'
    },

    # 测试广告标签移除 - id以advert开头
    {
        'input': {
            'content_list': [],
            'data_source_category': 'html',
            'url': 'https://anysite.org/article',
            'html': '<html><body><div id="advert-banner">广告横幅</div><p>正常内容</p></body></html>',
        },
        'expected_html': '<html><body><p>正常内容</p></body></html>'
    },

    # 测试广告标签移除 - name以advert开头
    {
        'input': {
            'content_list': [],
            'data_source_category': 'html',
            'url': 'https://blog.example.com/post',
            'html': '<html><body><div name="advertiser-info">赞助商信息</div><p>正常内容</p></body></html>',
        },
        'expected_html': '<html><body><p>正常内容</p></body></html>'
    },

    # 测试display:none样式移除 - 带空格
    {
        'input': {
            'content_list': [],
            'data_source_category': 'html',
            'url': 'https://example.com/page',
            'html': '<html><body><div style="color: red; display: none;">隐藏内容</div><p>可见内容</p></body></html>',
        },
        'expected_html': '<html><body><p>可见内容</p></body></html>'
    },

    # 测试display:none样式移除 - 不带空格
    {
        'input': {
            'content_list': [],
            'data_source_category': 'html',
            'url': 'https://example.com/page',
            'html': '<html><body><div style="display:none;font-size:12px;">隐藏内容</div><p>可见内容</p></body></html>',
        },
        'expected_html': '<html><body><p>可见内容</p></body></html>'
    },

    # 测试url匹配 - stackexchange.com的d-none类
    {
        'input': {
            'content_list': [],
            'data_source_category': 'html',
            'url': 'https://stats.stackexchange.com/questions/11544/testing-for-stability-in-a-time-series/11750',  # stackexchange.com子域名
            'html': '<html><body><span class="d-none">隐藏内容</span><p>可见内容</p></body></html>',
        },
        'expected_html': '<html><body><p>可见内容</p></body></html>'
    },

    # 测试特定网站规则 - 非stackexchange网站不应移除d-none类
    {
        'input': {
            'content_list': [],
            'data_source_category': 'html',
            'url': 'https://example.com/page',  # 非stackexchange网站
            'html': '<html><body><span class="d-none">这个不应该被移除</span><p>可见内容</p></body></html>',
        },
        'expected_html': '<html><body><span class="d-none">这个不应该被移除</span><p>可见内容</p></body></html>'
    },

    # 测试多规则组合 - 同时包含多种需要移除的元素
    {
        'input': {
            'content_list': [],
            'data_source_category': 'html',
            'url': 'https://stackexchange.com/questions',
            'html': '''<html><body><div class="advertisement">广告内容</div><p>正常内容1</p><div style="display:none;">隐藏内容</div><p>正常内容2</p><span class="d-none">stackexchange隐藏内容</span><p>正常内容3</p></body></html>''',
        },
        'expected_html': '''<html><body><p>正常内容1</p><p>正常内容2</p><p>正常内容3</p></body></html>'''
    },

    # 测试保留tail文本
    {
        'input': {
            'content_list': [],
            'data_source_category': 'html',
            'url': 'https://example.com/page',
            'html': '<html><body><div class="advertisement">广告</div>这是tail文本<p>正常内容</p></body></html>',
        },
        'expected_html': '<html><body>这是tail文本<p>正常内容</p></body></html>'
    }
]


class TestHTMLFileFormatCleanTagsPreExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = HTMLFileFormatCleanTagsPreExtractor({})

    def test_clean_invisible_tags(self):
        for test_case in TEST_CASES:
            data_json = DataJson(test_case['input'])
            self.extractor.pre_extract(data_json)
            self.assertEqual(data_json['html'], test_case['expected_html'])


if __name__ == '__main__':
    unittest.main()
