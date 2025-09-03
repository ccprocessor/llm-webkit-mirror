import unittest

from llm_web_kit.extractor.html.post_main_html_processer.post_mapping import \
    mapping_html_by_rules


class TestMappingHtmlByRules(unittest.TestCase):

    def setUp(self):
        """测试前的准备工作."""
        self.html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Page</title>
        </head>
        <body>
            <div class="header">
                <h1>Website Header</h1>
                <nav>Navigation Menu</nav>
            </div>
            <div class="main-content">
                <h2>Main Content Title</h2>
                <p>This is the main content that should be preserved.</p>
                <div class="advertisement">
                    <span>Ad content</span>
                </div>
                <p>More main content here.</p>
            </div>
            <div class="footer">
                <p>Footer content with copyright information.</p>
                <div class="social-links">Social media links</div>
            </div>
        </body>
        </html>
        """

        # 用于测试的XPath规则
        self.xpaths_to_remove = [
            {
                'xpath': "//div[@class='header']",
                'parent_tag': 'body',
                'parent_attributes': {},
                'reson': 'Header is non-core content at the beginning'
            },
            {
                'xpath': "//div[@class='footer']",
                'parent_tag': 'body',
                'parent_attributes': {},
                'reson': 'Footer is non-core content at the end'
            }
        ]

    def test_mapping_html_by_rules_with_valid_input(self):
        """测试使用有效输入参数的情况."""
        result, is_success = mapping_html_by_rules(self.html_content, self.xpaths_to_remove)

        # 验证结果是字符串
        self.assertIsInstance(result, str)
        self.assertEqual(is_success, True)

        # 验证header被删除（位于开始位置）
        self.assertNotIn('Website Header', result)
        self.assertNotIn('Navigation Menu', result)
        self.assertNotIn('class="header"', result)

        # 验证footer被删除（位于结束位置）
        self.assertNotIn('Footer content with copyright', result)
        self.assertNotIn('Social media links', result)
        self.assertNotIn('class="footer"', result)

        # 验证中间主要内容仍然存在
        self.assertIn('Main Content Title', result)
        self.assertIn('main content that should be preserved', result)
        self.assertIn('More main content here', result)

        # 验证中间元素未被删除（即使在规则中）
        self.assertIn('advertisement', result)
        self.assertIn('Ad content', result)

    def test_mapping_html_by_rules_with_empty_html_content(self):
        """测试空HTML内容的情况."""
        empty_html = ''
        result, is_success = mapping_html_by_rules(empty_html, self.xpaths_to_remove)

        # 空HTML应该返回空字符串或处理后的结果
        self.assertIsInstance(result, str)
        self.assertEqual(is_success, False)

    def test_mapping_html_by_rules_with_none_html_content(self):
        """测试None作为HTML内容的情况."""
        result, is_success = mapping_html_by_rules(None, self.xpaths_to_remove)
        # 空HTML应该返回空字符串或处理后的结果
        self.assertIsNone(result)
        self.assertEqual(is_success, False)

    def test_mapping_html_by_rules_with_empty_xpaths_list(self):
        """测试空XPath规则列表."""
        empty_xpaths = []
        result, is_success = mapping_html_by_rules(self.html_content, empty_xpaths)

        # 结果应该与原始HTML基本一致（去除格式差异）
        self.assertIsInstance(result, str)
        self.assertEqual(is_success, False)
        # 应该保留所有原始内容
        self.assertIn('Website Header', result)
        self.assertIn('Main Content Title', result)
        self.assertIn('Footer content', result)

    def test_mapping_html_by_rules_with_none_xpaths_list(self):
        """测试None作为XPath规则列表的情况."""
        with self.assertRaises(TypeError):
            mapping_html_by_rules(self.html_content, None)

    def test_mapping_html_by_rules_with_invalid_xpath(self):
        """测试包含无效XPath的规则列表."""
        invalid_xpaths = [
            {
                'xpath': "//div[@class='nonexistent']",
                'parent_tag': 'body',
                'parent_attributes': {},
                'reson': 'Non-existent element'
            }
        ]

        # 应该不会抛出异常
        try:
            result, is_success = mapping_html_by_rules(self.html_content, invalid_xpaths)
            self.assertIsInstance(result, str)
            self.assertEqual(is_success, False)
            # 内容应该基本保持不变
            self.assertIn('Main Content Title', result)
        except Exception as e:
            self.fail(f'mapping_html_by_rules raised Exception unexpectedly: {e}')

    def test_mapping_html_by_rules_with_malformed_html(self):
        """测试格式不正确的HTML."""
        malformed_html = "<html><div class='main'>Unclosed div<div class='content'>Content</div>"
        result, is_success = mapping_html_by_rules(malformed_html, self.xpaths_to_remove)

        # 应该返回处理后的字符串，不会抛出异常
        self.assertIsInstance(result, str)
        self.assertEqual(is_success, False)

    def test_mapping_html_by_rules_partial_match_xpath(self):
        """测试部分匹配的XPath."""
        partial_xpaths = [
            {
                'xpath': "//div[contains(@class, 'header')]",
                'parent_tag': 'body',
                'parent_attributes': {},
                'reson': 'Partial match header'
            }
        ]

        result, is_success = mapping_html_by_rules(self.html_content, partial_xpaths)
        self.assertEqual(is_success, True)

        # 验证匹配的header被删除
        self.assertNotIn('Website Header', result)
        self.assertNotIn('Navigation Menu', result)

    def test_mapping_html_by_rules_multiple_matches_same_xpath(self):
        """测试XPath匹配多个元素的情况."""
        html_with_duplicates = """
        <html>
        <body>
            <div class="remove-me">First div to remove</div>
            <p>Main content here</p>
            <div class="remove-me">Second div to remove</div>
            <p>More content</p>
            <div class="keep-me">Div to keep</div>
        </body>
        </html>
        """

        remove_rules = [
            {
                'xpath': "//div[@class='remove-me']",
                'parent_tag': 'body',
                'parent_attributes': {},
                'reson': 'Remove all elements with this class'
            }
        ]

        result, is_success = mapping_html_by_rules(html_with_duplicates, remove_rules)
        self.assertEqual(is_success, True)

        # 验证所有匹配的元素都被删除
        self.assertNotIn('Second div to remove', result)

        # 验证未匹配的元素仍然存在
        self.assertIn('Main content here', result)
        self.assertIn('More content', result)
        self.assertIn('Div to keep', result)

    def test_mapping_html_by_rules_middle_position_elements_not_removed(self):
        """测试中间位置的元素不会被删除."""
        middle_element_rules = [
            {
                'xpath': "//div[@class='advertisement']",
                'parent_tag': 'div',
                'parent_attributes': {'class': 'main-content'},
                'reson': 'Advertisement is in middle position'
            }
        ]

        result, is_success = mapping_html_by_rules(self.html_content, middle_element_rules)
        self.assertEqual(is_success, False)

        # 验证广告元素未被删除（因为它在中间位置）
        self.assertIn('advertisement', result)
        self.assertIn('Ad content', result)
