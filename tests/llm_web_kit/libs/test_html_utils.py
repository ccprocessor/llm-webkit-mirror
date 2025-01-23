
import unittest

from lxml.html import HtmlElement

from llm_web_kit.libs.html_utils import (element_to_html, html_to_element,
                                         html_to_markdown_table,
                                         replace_element, table_cells_count)


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

    def test_replace_element_with_parent(self):
        """Test replacing one element with another."""
        # Create parent element containing old element
        parent_html = '<main><div>Old content</div></main>'
        parent_element = html_to_element(parent_html)
        old_element = parent_element.find('div')

        # Create new element
        new_html = '<p>New content</p>'
        new_element = html_to_element(new_html)

        # Replace old with new
        replace_element(old_element, new_element)

        # Verify replacement
        self.assertEqual(parent_element.find('p').text, 'New content')
        self.assertIsNone(parent_element.find('div'))

    def test_replace_element_without_parent(self):
        """Test replacing root element (element with no parent)."""
        # Create root element to replace
        old_html = '<div>Old content</div>'
        old_element = html_to_element(old_html)
        self.assertEqual(old_element.tag, 'div')

        # Create new element
        new_html = '<p a="1" b="a">New content</p>'
        new_element = html_to_element(new_html)
        self.assertEqual(new_element.tag, 'p')

        # Replace root element
        replace_element(old_element, new_element)

        # Verify replacement
        self.assertEqual(old_element.tag, 'p')
        self.assertEqual(old_element.text, 'New content')
        self.assertEqual(old_element.get('a'), '1')
        self.assertEqual(old_element.get('b'), 'a')

    def test_table_cells_count(self):
        """测试表格单元格数量."""
        html = '<table><tr><td>1</td><td>2</td></tr></table>'
        self.assertEqual(table_cells_count(html), 2)

    def test_table_cells_count_2(self):
        """测试表格单元格数量."""
        html = '<table><tr><td>1</td></tr></table>'
        self.assertEqual(table_cells_count(html), 1)

    def test_table_cells_count_3(self):
        """测试表格单元格数量."""
        html = '<table><tr><td>1</td><td>2</td></tr><tr><td>3</td><td>4</td></tr></table>'
        self.assertEqual(table_cells_count(html), 4)

    def test_table_cells_count_4(self):
        """测试表格单元格数量."""
        html = '<table><tr><th>1</th><td>2</td></tr><tr><th>3</th><td>4</td></tr></table>'
        self.assertEqual(table_cells_count(html), 4)

    def test_html_to_markdown_table(self):
        """测试html转换成markdown表格."""
        html = '<table><tr><th>1</th><td>2</td></tr></table>'
        self.assertEqual(html_to_markdown_table(html), '| 1 | 2 |\n|---|---|')

    def test_html_to_markdown_table2(self):
        """测试html转换成markdown表格."""
        html = '<table><tr><th>1</th><th>2</th></tr><tr><td>3</td><td>4</td></tr></table>'
        self.assertEqual(html_to_markdown_table(html), '| 1 | 2 |\n|---|---|\n| 3 | 4 |')

    def test_html_to_markdown_table3(self):
        """测试html转换成markdown表格."""
        html = '<table><tr><th>1</th><th>2</th></tr><tr><td>3</td><td>4</td></tr><tr><td>5</td><td>6</td></tr></table>'
        self.assertEqual(html_to_markdown_table(html), '| 1 | 2 |\n|---|---|\n| 3 | 4 |\n| 5 | 6 |')

    def test_table4(self):
        """测试html转换成markdown表格.测试空表格."""
        html = """
        <table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom:3px">
    <tr valign="bottom">

    \t

        </tr>
        </table>
        """
        cell_count = table_cells_count(html)
        self.assertEqual(cell_count, 0)
        self.assertEqual(html_to_markdown_table(html), '')

    def test_table5(self):
        """测试html转换成markdown表格.测试空表格."""
        html = """
        <table><tr><th>Rank</th><th>Product Name</th><th>Score</th></tr><tr><td>1</td><td>Car Underglow Lights,EJ's SUPER CAR Underglow Underbody System Neon Strip Lights Kit,8 Color</td><td>9.7</td></tr><tr><td>2</td><td>4pcs 8 Colors LED Strip Under Car Tube Underglow Underbody System Neon Accent</td><td>9.5</td></tr><tr><td>3</td><td>Xprite Car Underglow Neon Accent Strip Lights Kit 8 Color Sound Active Function</td><td>9.1</td></tr><tr><td>4</td><td>Car Underglow Lights, Bluetooth Dream Color Chasing Strip Lights Kit, 6 PCS Waterproof</td><td>8.8</td></tr><tr><td>5</td><td>GOODRUN Underglow Underbody Lighting Kit, Multicolored LED Strip Light with Light Bulbs,Neon Accent</td><td>8.6</td></tr><tr><td>6</td><td>OPT7 Aura 4pc Pickup Truck Underglow LED Lighting Kit w/remote - Soundsync</td><td>8.3</td></tr><tr><td>7</td><td>Xprite Car Underglow RGB Dancing Light Kit with Wireless Remote Control 6PC Underbody</td><td>8.1</td></tr><tr><td>8</td><td>LEDGlow 4pc Multi-Color Slimline LED Underbody Underglow Accent Neon Lighting Kit for Cars</td><td>7.8</td></tr><tr><td>9</td><td>KORJO Car Underglow Lights, 6 Pcs Bluetooth Led Strip Lights with Dream Color</td><td>7.5</td></tr><tr><td>10</td><td>XTAUTO 4Pcs Car 72 LED Neon Undercar Underglow Glow Atmosphere Decorative Bar Light</td><td>7.2</td></tr></table>
        """
        cell_count = table_cells_count(html)
        self.assertEqual(cell_count, 33)
