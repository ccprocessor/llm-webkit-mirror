import unittest
from unittest.mock import MagicMock, patch

import pytest
from lxml.html import HtmlElement, fromstring

from llm_web_kit.exception.exception import MagicHtmlExtractorException
from llm_web_kit.libs.html_utils import (element_to_html, extract_magic_html,
                                         html_to_element,
                                         html_to_markdown_table,
                                         process_sub_sup_tags, remove_element,
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
        new_html = '<p a="1" b="a">New content<span>child1</span>span1 tail<span>child2</span>span2 tail</p>'
        new_element = html_to_element(new_html)
        self.assertEqual(new_element.tag, 'p')

        # Replace root element
        replace_element(old_element, new_element)

        # Verify replacement
        self.assertEqual(old_element.tag, 'p')
        self.assertEqual(old_element.text, 'New content')
        self.assertEqual(old_element.get('a'), '1')
        self.assertEqual(old_element.get('b'), 'a')
        self.assertEqual(element_to_html(old_element[0]),'<span>child1</span>span1 tail')
        self.assertEqual(element_to_html(old_element[1]),'<span>child2</span>span2 tail')

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

    def test_html_to_markdown_table_table5(self):
        """测试tr一行只有一个单元格，补充空列."""
        table_html = '<table><tr><td>Mrs S Hindle</td></tr><tr><td>Show</td><td>CC</td><td>RCC</td></tr><tr><td>Driffield 5th October 2006</td><td>CH. Ricksbury Royal Hero</td><td>CH. Keyingham Branwell</td></tr><tr><td>Manchester 16th January 2008</td><td>CH. Lochbuie Geordie</td><td>Merryoth Maeve</td></tr><tr><td>Darlington 20th September 2009</td><td>CH. Maibee Make Believe</td><td>CH. Loranka Just Like Heaven JW</td></tr><tr><td>Blackpool 22nd June 2012</td><td>CH. Loranka Sherrie Baby</td><td>Dear Magic Touch De La Fi Au Songeur</td></tr><tr><td>Welsh Kennel Club 2014</td><td>Brymarden Carolina Sunrise</td><td>Ch. Wandris Evan Elp Us</td></tr><tr><td>Welsh Kennel Club 2014</td><td>Ch. Charnell Clematis of Salegreen</td><td>CH. Byermoor Queens Maid</td></tr></table>'
        result = html_to_markdown_table(table_html)
        assert result == '| Mrs S Hindle |  |  |\n|---|---|---|\n| Show | CC | RCC |\n| Driffield 5th October 2006 | CH. Ricksbury Royal Hero | CH. Keyingham Branwell |\n| Manchester 16th January 2008 | CH. Lochbuie Geordie | Merryoth Maeve |\n| Darlington 20th September 2009 | CH. Maibee Make Believe | CH. Loranka Just Like Heaven JW |\n| Blackpool 22nd June 2012 | CH. Loranka Sherrie Baby | Dear Magic Touch De La Fi Au Songeur |\n| Welsh Kennel Club 2014 | Brymarden Carolina Sunrise | Ch. Wandris Evan Elp Us |\n| Welsh Kennel Club 2014 | Ch. Charnell Clematis of Salegreen | CH. Byermoor Queens Maid |'

    def test_html_to_markdown_table6(self):
        """没有表头的table转md."""
        table_html = '<table><tr></tr><tr><td>4</td></tr></table>'
        result = html_to_markdown_table(table_html)
        assert result == '|  |\n|---|\n| 4 |'

    def test_html_to_markdown_table7(self):
        """"""
        html = """
        <table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom:3px">
<tr valign="bottom">

\t

    </tr><tr><td>xxx</td><td>ttt</td></tr>
    </table>
        """
        result = html_to_markdown_table(html)
        assert result == '|  |  |\n|---|---|\n| xxx | ttt |'

    def test_table5(self):
        """测试html转换成markdown表格.测试空表格."""
        html = """
        <table><tr><th>Rank</th><th>Product Name</th><th>Score</th></tr><tr><td>1</td><td>Car Underglow Lights,EJ's SUPER CAR Underglow Underbody System Neon Strip Lights Kit,8 Color</td><td>9.7</td></tr><tr><td>2</td><td>4pcs 8 Colors LED Strip Under Car Tube Underglow Underbody System Neon Accent</td><td>9.5</td></tr><tr><td>3</td><td>Xprite Car Underglow Neon Accent Strip Lights Kit 8 Color Sound Active Function</td><td>9.1</td></tr><tr><td>4</td><td>Car Underglow Lights, Bluetooth Dream Color Chasing Strip Lights Kit, 6 PCS Waterproof</td><td>8.8</td></tr><tr><td>5</td><td>GOODRUN Underglow Underbody Lighting Kit, Multicolored LED Strip Light with Light Bulbs,Neon Accent</td><td>8.6</td></tr><tr><td>6</td><td>OPT7 Aura 4pc Pickup Truck Underglow LED Lighting Kit w/remote - Soundsync</td><td>8.3</td></tr><tr><td>7</td><td>Xprite Car Underglow RGB Dancing Light Kit with Wireless Remote Control 6PC Underbody</td><td>8.1</td></tr><tr><td>8</td><td>LEDGlow 4pc Multi-Color Slimline LED Underbody Underglow Accent Neon Lighting Kit for Cars</td><td>7.8</td></tr><tr><td>9</td><td>KORJO Car Underglow Lights, 6 Pcs Bluetooth Led Strip Lights with Dream Color</td><td>7.5</td></tr><tr><td>10</td><td>XTAUTO 4Pcs Car 72 LED Neon Undercar Underglow Glow Atmosphere Decorative Bar Light</td><td>7.2</td></tr></table>
        """
        cell_count = table_cells_count(html)
        self.assertEqual(cell_count, 33)

    def test_html_to_element_without_xml_declaration(self):
        """测试普通HTML解析（无XML声明）"""
        # 普通HTML字符串
        html_simple = '<html><body><p>普通HTML</p></body></html>'

        # 解析HTML
        element = html_to_element(html_simple)

        # 验证解析结果
        self.assertIsInstance(element, HtmlElement)
        self.assertEqual(element.tag, 'html')
        self.assertEqual(element.find('.//p').text, '普通HTML')

    def test_html_to_element_with_complex_xml_declaration(self):
        """测试带有复杂DOCTYPE和XML声明的HTML解析."""
        # 复杂HTML字符串
        complex_html = '''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-gb" lang="en-gb" dir="ltr">
<head>
  <title>测试标题</title>
</head>
<body>
  <p>复杂HTML测试</p>
</body>
</html>'''

        # 解析HTML
        element = html_to_element(complex_html)

        # 验证解析结果
        self.assertIsInstance(element, HtmlElement)
        self.assertEqual(element.find('.//title').text, '测试标题')
        self.assertEqual(element.find('.//p').text, '复杂HTML测试')

    def test_html_to_element_with_malformed_xml(self):
        """测试畸形XML处理."""
        # 带有不完整XML声明的HTML
        malformed_html = '<?xml version="1.0" encoding="utf-8"?><html><unclosed><p>畸形XML</p></html>'

        # 解析HTML (不应抛出异常)
        element = html_to_element(malformed_html)

        # 验证解析结果 (应该尽可能解析)
        self.assertIsInstance(element, HtmlElement)
        # self.assertEqual(element.tag, 'html')
        self.assertIsNotNone(element.find('.//p'))
        self.assertEqual(element.find('.//p').text, '畸形XML')

    def test_process_sub_sup_tags(self):
        """测试处理HTML中的上标和下标标签."""
        # 1. 测试单个sub标签
        html_el = fromstring('<sub>2</sub>')
        result = process_sub_sup_tags(html_el)
        self.assertEqual(result, '<sub>2</sub>')

        # 2. 测试单个sup标签
        html_el = fromstring('<sup>2</sup>')
        result = process_sub_sup_tags(html_el)
        self.assertEqual(result, '<sup>2</sup>')

        # 3. 测试非sub/sup标签
        html_el = fromstring('<div>普通文本</div>')
        result = process_sub_sup_tags(html_el)
        self.assertEqual(result, '')

        # 4. 测试带初始文本的process_sub_sup_tags
        html_el = fromstring('<sub>2</sub>')
        result = process_sub_sup_tags(html_el, 'H')
        self.assertEqual(result, 'H<sub>2</sub>')

        # 5. 测试包含sub标签的父元素 - 递归处理
        html_el = fromstring('<div>H<sub>2</sub>O</div>')
        result = process_sub_sup_tags(html_el)
        self.assertEqual(result, 'H<sub>2</sub>O')

        # 6. 测试包含sub标签的父元素 - 非递归处理
        html_el = fromstring('<div>H<sub>2</sub>O</div>')
        result = process_sub_sup_tags(html_el, recursive=False)
        self.assertEqual(result, '')

        # 7. 测试带运算符的公式
        html_el = fromstring('<div>x<sup>2</sup> + y<sup>2</sup> = z<sup>2</sup></div>')
        result = process_sub_sup_tags(html_el)
        self.assertEqual(result, 'x<sup>2</sup> + y<sup>2</sup> = z<sup>2</sup>')

        # 8. 测试混合公式
        html_el = fromstring('<div>f(x) = x<sup>2</sup> - 3x + 2</div>')
        result = process_sub_sup_tags(html_el)
        self.assertEqual(result, 'f(x) = x<sup>2</sup> - 3x + 2')

        # 9. 测试复杂的化学公式
        html_el = fromstring('<div>C<sub>6</sub>H<sub>12</sub>O<sub>6</sub></div>')
        result = process_sub_sup_tags(html_el)
        self.assertEqual(result, 'C<sub>6</sub>H<sub>12</sub>O<sub>6</sub>')

        # 10. 测试混合上下标
        html_el = fromstring('<div>∫<sub>a</sub><sup>b</sup> f(x) dx</div>')
        result = process_sub_sup_tags(html_el)
        self.assertEqual(result, '∫<sub>a</sub><sup>b</sup> f(x) dx')

        # 11. 测试电路公式
        html_el = fromstring('<div>RI = R<sub>S</sub>R<sub>P</sub>/(R<sub>S</sub> - R<sub>P</sub>)</div>')
        result = process_sub_sup_tags(html_el)
        self.assertEqual(result, 'RI = R<sub>S</sub>R<sub>P</sub>/(R<sub>S</sub> - R<sub>P</sub>)')

    def test_process_sub_sup_tags_recursive_false(self):
        """测试process_sub_sup_tags函数的recursive=False参数."""
        # 测试带有子元素的元素，但recursive=False，应该不处理子元素
        html_el = fromstring('<div><sub>test</sub></div>')
        result = process_sub_sup_tags(html_el, current_text='', lang='en', recursive=False)
        self.assertEqual(result, '')

        html_el = fromstring('<div>test</div>')
        result = process_sub_sup_tags(html_el, current_text='prefix ', lang='en', recursive=False)
        self.assertEqual(result, 'prefix')

    def test_process_sub_sup_tags_with_children(self):
        """测试process_sub_sup_tags函数处理包含子元素的元素."""
        # 测试包含非sub/sup子元素的元素
        html_el = fromstring('<div>parent<span>child</span><sub>test</sub></div>')
        from llm_web_kit.extractor.html.recognizer.text import \
            TextParagraphRecognizer
        text_recognize = TextParagraphRecognizer()
        result = text_recognize._TextParagraphRecognizer__get_paragraph_text(html_el)
        self.assertEqual(result[0]['c'], 'parent child<sub>test</sub>')

        # 非sub/sup上下文下，子元素没有处理结果的情况
        html_el = fromstring('<div>parent<span></span><sub>test</sub></div>')
        result = text_recognize._TextParagraphRecognizer__get_paragraph_text(html_el)
        self.assertEqual(result[0]['c'], 'parent<sub>test</sub>')

        # is_sub_sup_context为真的情况下处理子元素结果
        html_el = fromstring('<sup>parent<span><sub>nested</sub></span></sup>')
        result = text_recognize._TextParagraphRecognizer__get_paragraph_text(html_el)
        self.assertEqual(result[0]['c'], '<sup>parent<sub>nested</sub></sup>')

    def test_process_sub_sup_tags_with_tail(self):
        """测试process_sub_sup_tags函数处理带有尾部文本的子元素."""
        # 子元素有尾部文本但is_sub_sup_context为假的情况
        html_el = fromstring('<div><span>child</span> tail text<sub>test</sub></div>')
        from llm_web_kit.extractor.html.recognizer.text import \
            TextParagraphRecognizer
        text_recognize = TextParagraphRecognizer()
        result = text_recognize._TextParagraphRecognizer__get_paragraph_text(html_el)
        self.assertEqual(result[0]['c'], 'child tail text<sub>test</sub>')

        # 子元素有尾部文本且is_sub_sup_context为真的情况
        html_el = fromstring('<sub><span>child</span> tail text</sub>')
        result = text_recognize._TextParagraphRecognizer__get_paragraph_text(html_el)
        self.assertEqual(result[0]['c'], '<sub>child tail text</sub>')

    def test_process_sub_sup_tags_edge_cases(self):
        """测试process_sub_sup_tags函数的边缘情况，特别针对代码覆盖行数367, 382, 389."""
        # 使用sub/sup上下文中处理非sub/sup子元素并确保结果为空
        div_el = fromstring('<sub>parent<span></span></sub>')
        from llm_web_kit.extractor.html.recognizer.text import \
            TextParagraphRecognizer
        text_recognize = TextParagraphRecognizer()
        result = text_recognize._TextParagraphRecognizer__get_paragraph_text(div_el)
        self.assertEqual(result[0]['c'], '<sub>parent</sub>')

        # 确保子元素的处理结果在is_sub_sup_context下被添加
        div_el = fromstring('<div><span><sub>test</sub></span>after</div>')
        span_el = div_el.find('.//span')
        span_result = process_sub_sup_tags(span_el)
        self.assertTrue(span_result)  # 确保span的处理有结果
        result = process_sub_sup_tags(div_el)
        self.assertEqual(result, '<sub>test</sub>after')

        # 测试当子元素的处理结果为空的情况
        # 注意：这个测试的div_el没有任何sub/sup标签，所以函数会返回空字符串
        div_el = fromstring('<div>parent<span></span>after</div>')
        result = process_sub_sup_tags(div_el)
        self.assertEqual(result, '')  # 没有sub/sup元素，返回空字符串

        # 尝试使用有sub标签的元素
        div_el = fromstring('<div>parent<span><sub></sub></span>after<sub>x</sub></div>')
        result = process_sub_sup_tags(div_el)
        self.assertEqual(result, 'parent<sub></sub>after<sub>x</sub>')

        # 确保子元素尾部文本在非sub/sup上下文中得到处理
        div_el = fromstring('<div><span></span> tail text</div>')
        result = process_sub_sup_tags(div_el)
        self.assertEqual(result, '')

        # 测试子元素有尾巴文本且有sub/sup元素
        div_el = fromstring('<div>text<span></span> tail<sub>x</sub></div>')
        result = process_sub_sup_tags(div_el)
        self.assertEqual(result, 'text tail<sub>x</sub>')

    def test_process_sub_sup_tags_text_combining(self):
        """测试process_sub_sup_tags函数处理文本拼接的情况."""
        # 非sub/sup上下文下的文本拼接
        html_el = fromstring('<div>prefix<sub>test</sub></div>')
        result = process_sub_sup_tags(html_el)
        self.assertEqual(result, 'prefix<sub>test</sub>')

        # 中文文本拼接
        html_el = fromstring('<div>前缀<span>子元素</span><sub>测试</sub></div>')
        result = process_sub_sup_tags(html_el, lang='zh')
        self.assertEqual(result, '前缀<sub>测试</sub>')

        # 测试标点符号情况
        html_el = fromstring('<div>prefix<span>!child</span><sub>test</sub></div>')
        result = process_sub_sup_tags(html_el)

        from llm_web_kit.extractor.html.recognizer.text import \
            TextParagraphRecognizer
        text_recognize = TextParagraphRecognizer()
        result = text_recognize._TextParagraphRecognizer__get_paragraph_text(html_el)
        self.assertEqual(result[0]['c'], 'prefix!child<sub>test</sub>')

        # 测试仅处理标点符号
        html_el = fromstring('<div>prefix!<sub>test</sub></div>')
        result = process_sub_sup_tags(html_el)
        self.assertEqual(result, 'prefix!<sub>test</sub>')


# 测试用例数据
TEST_REMOVE_ELEMENT_CASES = [
    # 基本的元素删除
    {
        'input': '<div><p>要删除的段落</p></div>',
        'xpath': './/p',
        'expect': '<div></div>'
    },
    # 删除带有tail文本的元素
    {
        'input': '<div><p>要删除的段落</p>这是tail文本</div>',
        'xpath': './/p',
        'expect': '<div>这是tail文本</div>'
    },
    # 删除有前置兄弟节点且带tail的元素
    {
        'input': '<div><span>前置元素</span><p>要删除的段落</p>这是tail文本</div>',
        'xpath': './/p',
        'expect': '<div><span>前置元素</span>这是tail文本</div>'
    },
    # 删除没有父节点的元素（根元素）
    {
        'input': '<p>根元素</p>',
        'xpath': '.',
        'expect': '<p>根元素</p>'  # 不应该变化
    },
    # 嵌套结构中删除元素
    {
        'input': '<div><section><p>要删除的段落</p>段落后文本</section></div>',
        'xpath': './/p',
        'expect': '<div><section>段落后文本</section></div>'
    },
    # 删除包含子元素的元素
    {
        'input': '<div><article>文章开始<p>段落<span>重点</span></p>文章结束</article></div>',
        'xpath': './/p',
        'expect': '<div><article>文章开始文章结束</article></div>'
    },
    # 删除带属性的元素
    {
        'input': '<div><p class="important" id="p1">带属性的段落</p>后续文本</div>',
        'xpath': './/p',
        'expect': '<div>后续文本</div>'
    },
    # 有多个兄弟节点的情况
    {
        'input': '<div><span>第一个</span><p>要删除的</p>中间文本<span>最后一个</span></div>',
        'xpath': './/p',
        'expect': '<div><span>第一个</span>中间文本<span>最后一个</span></div>'
    },
    # 父节点已有文本且删除元素有tail的情况
    {
        'input': '<div>父节点文本<p>要删除的段落</p>tail文本</div>',
        'xpath': './/p',
        'expect': '<div>父节点文本tail文本</div>'
    },
    # 删除第一个子元素且有tail的情况
    {
        'input': '<div><p>第一个子元素</p>tail文本<span>其他元素</span></div>',
        'xpath': './/p',
        'expect': '<div>tail文本<span>其他元素</span></div>'
    },
    # 删除多个元素中的一个
    {
        'input': '<div><p>段落1</p><p>段落2</p><p>段落3</p></div>',
        'xpath': './/p[2]',
        'expect': '<div><p>段落1</p><p>段落3</p></div>'
    },
    # 删除带有HTML实体的元素
    {
        'input': '<div><p>段落&nbsp;带有&lt;实体&gt;</p>后文本</div>',
        'xpath': './/p',
        'expect': '<div>后文本</div>'
    }
]


class TestRemoveElement(unittest.TestCase):
    """测试remove_element函数."""
    def setUp(self):
        self.test_cases = TEST_REMOVE_ELEMENT_CASES

    def test_remove_element(self):
        """使用测试用例数据测试remove_element函数."""
        for case in self.test_cases:
            with self.subTest(case=case):
                # 解析HTML
                root = html_to_element(case['input'])
                # 查找要删除的元素
                element = root.xpath(case['xpath'])[0]
                # 执行删除
                remove_element(element)
                # 验证结果
                result = element_to_html(root)
                self.assertEqual(result, case['expect'])


class TestExtractMagicHtml(unittest.TestCase):

    @patch('llm_web_kit.extractor.html.extractor.HTMLFileFormatExtractor')
    def test_extract_magic_html_success(self, mock_extractor_class):
        mock_extractor_instance = MagicMock()
        mock_extractor_class.return_value = mock_extractor_instance

        expected_html = '<body><div>Test Content</div></body>'
        mock_extractor_instance._extract_main_html.return_value = (expected_html, 'metadata', 'content_type')

        html = '<html><body><div>Test Content</div></body></html>'
        base_url = 'https://example.com'
        page_layout_type = 'article'

        result = extract_magic_html(html, base_url, page_layout_type)

        mock_extractor_class.assert_called_once_with({})
        mock_extractor_instance._extract_main_html.assert_called_once_with(html, base_url, page_layout_type)
        self.assertEqual(result, expected_html)

    @patch('llm_web_kit.extractor.html.extractor.HTMLFileFormatExtractor')
    def test_extract_magic_html_exception(self, mock_extractor_class):
        mock_extractor_instance = MagicMock()
        mock_extractor_class.return_value = mock_extractor_instance
        mock_extractor_instance._extract_main_html.side_effect = MagicHtmlExtractorException('Test error')

        html = '<html><body><div>Test Content</div></body></html>'
        base_url = 'https://example.com'
        page_layout_type = 'article'

        with pytest.raises(MagicHtmlExtractorException) as excinfo:
            extract_magic_html(html, base_url, page_layout_type)

        self.assertIn('Magic HTML extractor exception#Test error', str(excinfo.value))
