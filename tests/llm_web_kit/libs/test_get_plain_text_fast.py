"""测试get_plain_text_fast函数."""
import unittest

from llm_web_kit.libs.html_utils import get_plain_text_fast


class TestGetPlainTextFast(unittest.TestCase):
    """测试get_plain_text_fast函数的单元测试类."""

    def test_empty_input(self):
        """测试空输入."""
        # 测试空字符串
        self.assertEqual(get_plain_text_fast(""), "")

        # 测试None值
        self.assertEqual(get_plain_text_fast(None), "")

        # 测试只有空白字符的字符串
        self.assertEqual(get_plain_text_fast("   "), "")
        self.assertEqual(get_plain_text_fast("\n\t"), "")

    def test_simple_text(self):
        """测试简单文本提取."""
        html = "<p>Hello World</p>"
        result = get_plain_text_fast(html)
        self.assertEqual(result, "Hello World")

    def test_multiple_elements(self):
        """测试多个元素的文本提取."""
        html = "<div><p>Hello</p><p>World</p></div>"
        result = get_plain_text_fast(html)
        self.assertEqual(result, "Hello World")

    def test_nested_elements(self):
        """测试嵌套元素的文本提取."""
        html = "<div><span>Hello <strong>beautiful</strong> World</span></div>"
        result = get_plain_text_fast(html)
        self.assertEqual(result, "Hello beautiful World")

    def test_remove_script_tags(self):
        """测试移除script标签及其内容."""
        html = """
        <div>
            <p>Visible text</p>
            <script>console.log('should be removed');</script>
            <p>More visible text</p>
        </div>
        """
        result = get_plain_text_fast(html)
        self.assertEqual(result, "Visible text More visible text")
        self.assertNotIn("console.log", result)

    def test_remove_style_tags(self):
        """测试移除style标签及其内容."""
        html = """
        <div>
            <p>Visible text</p>
            <style>body { color: red; }</style>
            <p>More visible text</p>
        </div>
        """
        result = get_plain_text_fast(html)
        self.assertEqual(result, "Visible text More visible text")
        self.assertNotIn("color", result)

    def test_remove_all_noise_tags(self):
        """测试移除所有噪声标签."""
        html = """
        <html>
            <head><title>Test</title></head>
            <body>
                <p>Visible content</p>
                <script>var x = 1;</script>
                <style>.class { margin: 0; }</style>
                <noscript>No JavaScript</noscript>
                <iframe src="test.html"></iframe>
                <embed src="test.swf"></embed>
                <object data="test.pdf"></object>
                <p>More visible content</p>
            </body>
        </html>
        """
        result = get_plain_text_fast(html)
        expected = "Test Visible content More visible content"
        self.assertEqual(result, expected)

        # 确保噪声内容被移除
        noise_content = ["var x = 1", "margin: 0", "No JavaScript", "test.html", "test.swf", "test.pdf"]
        for noise in noise_content:
            self.assertNotIn(noise, result)

    def test_remove_code_tags(self):
        """测试移除代码相关标签."""
        html = """
        <div>
            <p>Regular text</p>
            <code>function test() { return true; }</code>
            <pre>
                def hello():
                    print("world")
            </pre>
            <kbd>Ctrl+C</kbd>
            <samp>$ ls -la</samp>
            <p>More regular text</p>
        </div>
        """
        result = get_plain_text_fast(html)
        self.assertEqual(result, "Regular text More regular text")

        # 确保代码内容被移除
        code_content = ["function test", "def hello", "Ctrl+C", "$ ls -la"]
        for code in code_content:
            self.assertNotIn(code, result)

    def test_malformed_html(self):
        """测试畸形HTML的处理."""
        html = "<p>Unclosed paragraph<div>Nested without closing</p>Some text"
        result = get_plain_text_fast(html)
        # 应该能够提取文本，即使HTML结构不完整
        self.assertIn("Unclosed paragraph", result)
        self.assertIn("Nested without closing", result)
        self.assertIn("Some text", result)

    def test_only_noise_tags(self):
        """测试只包含噪声标签的HTML."""
        html = """
        <script>var x = 1;</script>
        <style>body { margin: 0; }</style>
        <noscript>Enable JavaScript</noscript>
        """
        result = get_plain_text_fast(html)
        self.assertEqual(result, "")

    def test_unicode_content(self):
        """测试Unicode内容."""
        html = "<p>你好世界 🌍 Здравствуй мир</p>"
        result = get_plain_text_fast(html)
        self.assertEqual(result, "你好世界 🌍 Здравствуй мир")

    def test_table_content(self):
        """测试表格内容提取."""
        html = """
        <table>
            <tr>
                <th>Name</th>
                <th>Age</th>
            </tr>
            <tr>
                <td>John</td>
                <td>25</td>
            </tr>
            <tr>
                <td>Jane</td>
                <td>30</td>
            </tr>
        </table>
        """
        result = get_plain_text_fast(html)
        self.assertIn("Name", result)
        self.assertIn("Age", result)
        self.assertIn("John", result)
        self.assertIn("25", result)
        self.assertIn("Jane", result)
        self.assertIn("30", result)

    def test_image_alt_text(self):
        """测试图片alt文本不会被提取（因为是属性而非文本内容）"""
        html = '<div><img src="test.jpg" alt="Description"><p>Text content</p></div>'
        result = get_plain_text_fast(html)
        self.assertEqual(result, "Text content")
        # alt属性不应该被提取为文本内容
        self.assertNotIn("Description", result)

    def test_comments_handling(self):
        """测试HTML注释处理（应该被HTMLParser移除）"""
        html = """
        <div>
            <!-- This is a comment -->
            <p>Visible text</p>
            <!-- Another comment -->
        </div>
        """
        result = get_plain_text_fast(html)
        self.assertEqual(result, "Visible text")
        self.assertNotIn("comment", result)


if __name__ == '__main__':
    unittest.main()
