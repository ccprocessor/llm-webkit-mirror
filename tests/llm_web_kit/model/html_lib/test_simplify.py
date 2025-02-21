import unittest

from lxml import html

from llm_web_kit.model.html_lib.simplify import (general_simplify,
                                                 general_simplify_html_str)


class TestGeneralSimplify(unittest.TestCase):
    def test_general_simplify_with_title(self):
        # 测试带有标题的HTML页面
        html_str = """
        <html>
        <head>
            <title>Test Title</title>
        </head>
        <body>
            <div class="content">
                <h1>Main Heading</h1>
                <p>This is a paragraph.</p>
                <div style="display:none;">
                    <p>Hidden content</p>
                </div>
                <ul>
                    <li>Item 1</li>
                    <li>Item 2</li>
                </ul>
            </div>
        </body>
        </html>
        """
        root = html.fromstring(html_str)
        title, simplified_root = general_simplify(root)
        self.assertEqual(title, 'Test Title')
        # 找到动态变更的`<p>`标签和`<span>`标签
        p_tags = simplified_root.xpath('//p')
        self.assertTrue(all(p.tag == 'p' for p in p_tags))
        # 表结构未被保留
        ul_tag = simplified_root.xpath('//ul')
        self.assertEqual(len(ul_tag), 1)
        # `None`标签结构未被保留
        # 需要进一步检查具体的删除逻辑，但在此处假设所有不可见内容都被移除
        hidden_divs = simplified_root.xpath("//div[@style='display:none;']")
        self.assertEqual(len(hidden_divs), 0)

    def test_general_simplify_no_title(self):
        # 测试没有标题的HTML页面
        html_str = """
        <html>
        <body>
            <div class="content-no-title">
                <h1>No Title Here</h1>
                <p>This is a paragraph without a title.</p>
            </div>
        </body>
        </html>
        """
        root = html.fromstring(html_str)
        title, simplified_root = general_simplify(root)
        self.assertIsNone(title)

    def test_general_simplify_remove_invisible_tags(self):
        # 测试移除不可见的HTML标签
        html_str = """
        <html>
        <body>
            <div>
                <p>Visible content</p>
                <div style="display:none;">
                    <p>Hidden content</p>
                </div>
            </div>
        </body>
        </html>
        """
        root = html.fromstring(html_str)
        title, simplified_root = general_simplify(root)
        hidden_divs = simplified_root.xpath("//div[@style='display:none;']")
        self.assertEqual(len(hidden_divs), 0)

    def test_general_simplify_merge_list(self):
        # 测试合并列表标签
        html_str = """
        <html>
        <body>
            <ul>
                <li>Item 1</li>
                <li>Item 2</li>
            </ul>
            <ol>
                <li>Item A</li>
                <li>Item B</li>
            </ol>
        </body>
        </html>
        """
        root = html.fromstring(html_str)
        title, simplified_root = general_simplify(root)
        ul_tags = simplified_root.xpath('//ul')
        ol_tags = simplified_root.xpath('//ol')
        # 合并后的列表标签应保留
        self.assertEqual(len(ul_tags), 1)
        self.assertEqual(len(ol_tags), 1)
        # 但是li标签应该被移除
        li_tags = simplified_root.xpath('//li')
        self.assertEqual(len(li_tags), 0)

    def test_general_simplify_remove_blank_tags(self):
        # 测试移除空白标签
        html_str = """
        <html>
        <body>
            <div>
                <p> </p>
                <span></span>
                <div>
                    <p>Content</p>
                </div>
            </div>
        </body>
        </html>
        """
        root = html.fromstring(html_str)
        title, simplified_root = general_simplify(root)
        # 检查子节点是否被删除
        p_tags = simplified_root.xpath('//p')
        self.assertEqual(len(p_tags), 1)
        self.assertEqual(p_tags[0].text, 'Content')

    def test_general_simplify_unwrap_tags(self):
        # 测试解包单子节点标签
        html_str = """
        <html>
        <body>
            <div>
                <p>Content</p>
            </div>
            <span>Text</span>
        </body>
        </html>
        """
        root = html.fromstring(html_str)
        title, simplified_root = general_simplify(root)
        # 检查`div`标签是否被解包
        div_tags = simplified_root.xpath('//div')
        self.assertEqual(len(div_tags), 0)
        # 检查`p`标签是否保留
        p_tags = simplified_root.xpath('//p')
        self.assertEqual(len(p_tags), 1)
        self.assertEqual(p_tags[0].text, 'Content')

    def test_general_simplify_html_str(self):
        # 测试`general_simplify_html_str`函数
        html_str = """
        <html>
        <body>
            <div>
                <p>Hello World</p>
                <script>console.log("hidden");</script>
            </div>
        </body>
        </html>
        """
        simplified_html_str = general_simplify_html_str(html_str)
        # 确保脚本标记被移除
        self.assertNotIn('<script>', simplified_html_str)
        # 确保HTML有效
        # 检查基本结构
        self.assertIn('<html>', simplified_html_str)
        self.assertIn('Hello World', simplified_html_str)

    def test_general_simplify_nested_tags(self):
        # 测试嵌套标签的简化
        html_str = """
        <html>
        <body>
            <div>
                <p>
                    <b>Bold text</b>
                    <i>Italic text</i>
                </p>
            </div>
        </body>
        </html>
        """
        root = html.fromstring(html_str)
        title, simplified_root = general_simplify(root)
        # 检查是否保留必要的标签
        b_tags = simplified_root.xpath('//b')
        self.assertEqual(len(b_tags), 0)
        i_tags = simplified_root.xpath('//i')
        self.assertEqual(len(i_tags), 0)
        # 检查文本内容是否完整
        p_text = ''.join(simplified_root.xpath('//p/text()')).strip()
        self.assertEqual(p_text, 'Bold text\n                    Italic text')

    def test_general_simplify_bare_text(self):
        # 测试裸文本的包裹
        html_str = """
        <html>
        <body>
            This is bare text.
            <div>This is also bare text.</div>
        </body>
        </html>
        """
        root = html.fromstring(html_str)
        title, simplified_root = general_simplify(root)
        # 检查文本是否被包裹在span标签中
        body_text = [
            text.strip()
            for text in simplified_root.xpath('//body/text()')
            if text.strip()
        ]
        self.assertEqual(body_text, [])
        span_tags = simplified_root.xpath('//span')
        self.assertTrue(len(span_tags) > 0)


if __name__ == '__main__':
    unittest.main()
