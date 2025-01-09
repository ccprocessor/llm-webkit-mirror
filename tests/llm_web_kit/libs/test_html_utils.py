
import unittest

from lxml.html import HtmlElement

from llm_web_kit.libs.html_utils import element_to_html, html_to_element


class TestHtmlUtils(unittest.TestCase):
    """Test html utility functions."""

    def test_build_html_tree(self):
        """Test building HTML tree from string."""
        html = '<html><body><p>Test</p></body></html>'
        tree = html_to_element(html)
        self.assertIsInstance(tree, HtmlElement)
        self.assertEqual(tree.tag, 'html')
        self.assertEqual(tree.find('.//p').text, 'Test')

    def test_build_html_tree_2(self):
        """这里测试一个自定义的标签."""
        html = '<cctitle level=1>标题1</cctitle>'
        tree = html_to_element(html)
        self.assertIsInstance(tree, HtmlElement)
        self.assertEqual(tree.tag, 'cctitle')
        self.assertEqual(tree.get('level'), '1')
        self.assertEqual(tree.text, '标题1')

    def test_build_html_element_from_string(self):
        """Test building HTML element from string."""
        html = '<div>Hello <b>World</b></div>'
        element = html_to_element(html)
        self.assertIsInstance(element, HtmlElement)
        self.assertEqual(element.tag, 'div')
        self.assertEqual(element.find('b').text, 'World')

    def test_element_to_html(self):
        """Test converting element back to HTML string."""
        html = '<p>Test paragraph</p>'
        element = html_to_element(html)
        result = element_to_html(element)
        self.assertEqual(result.strip(), html)

    def test_build_html_tree_with_comments(self):
        """Test building HTML tree removes comments."""
        html = '<div><!-- comment -->Content</div>'
        tree = html_to_element(html)
        result = element_to_html(tree)
        self.assertNotIn('comment', result)

    def test_build_html_tree_with_encoding(self):
        """Test building HTML tree with non-ASCII characters."""
        html = '<p>测试中文</p>'
        tree = html_to_element(html)
        result = element_to_html(tree)
        self.assertIn('测试中文', result)
