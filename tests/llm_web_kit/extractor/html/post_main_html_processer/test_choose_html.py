import unittest
from pathlib import Path

from llm_web_kit.extractor.html.post_main_html_processer.choose_html import \
    select_typical_htmls

base_dir = Path(__file__).parent


class TestChooseHtml(unittest.TestCase):

    def test_select_typical_html_with_complex_and_simple_html(self):
        """测试select_typical_html函数能正确选择最复杂的HTML."""

        # 简单HTML示例
        simple_html = """
        <html>
            <head>
                <title>Simple</title>
            </head>
            <body>
                <div>
                    <p>Simple content1</p>
                    <p>Simple content2</p>
                </div>
            </body>
        </html>
        """

        # 复杂HTML示例
        complex_html = """
        <html>
            <head>
                <title>Complex Test</title>
                <meta charset="utf-8">
                <link rel="stylesheet" href="style.css">
            </head>
            <body>
                <header>
                    <nav>
                        <ul>
                            <li><a href="#">Home</a></li>
                            <li><a href="#">About</a></li>
                            <li><a href="#">Contact</a></li>
                        </ul>
                    </nav>
                </header>
                <main>
                    <article>
                        <h1>Title</h1>
                        <p>Paragraph 1</p>
                        <p>Paragraph 2</p>
                        <section>
                            <h2>Section Title</h2>
                            <p>Section content</p>
                            <div>
                                <span>Text</span>
                                <span>More text</span>
                            </div>
                        </section>
                    </article>
                    <aside>
                        <h3>Sidebar</h3>
                        <p>Sidebar content</p>
                    </aside>
                </main>
                <footer>
                    <p>Footer content</p>
                </footer>
            </body>
        </html>
        """

        # 空HTML示例
        empty_html = """
        <html>
            <head>
                <title>Empty</title>
            </head>
            <body>
            </body>
        </html>
        """

        html_lst = list()
        html_lst.append({'html': simple_html, 'filename': 'xxx0'})
        html_lst.append({'html': complex_html, 'filename': 'xxx1'})
        html_lst.append({'html': empty_html, 'filename': 'xxx2'})

        result = select_typical_htmls(html_lst, 1)

        # 验证返回的不是None
        self.assertIsNotNone(result)
        # 应该返回最复杂的HTML
        self.assertEqual(result[0]['html'], complex_html)

    def test_select_typical_html_with_similar_htmls(self):
        """测试select_typical_html处理相似HTML的情况."""
        html2 = base_dir.joinpath('assets/0.html').read_text(encoding='utf-8')

        html_lst = list()
        for i in range(3):
            filename = f'assets/{i}.html'
            html_lst.append({'html': base_dir.joinpath(filename).read_text(encoding='utf-8'), 'filename': filename})

        result = select_typical_htmls(html_lst, 1)

        # 验证返回的不是None
        self.assertIsNotNone(result)
        # 由于HTML复杂度相似，应返回第一个HTML
        self.assertEqual(result[0]['html'], html2)

    def test_select_typical_html_with_empty_input(self):
        """测试select_typical_html处理空输入."""

        html_lst = [{'html': '', 'filename': 'xxx'}]

        result = select_typical_htmls(html_lst, 1)

        self.assertEqual(result, [])

    def test_select_typical_html_with_single_html(self):
        """测试select_typical_html处理只有一个HTML的情况."""

        single_html = base_dir.joinpath('assets/1.html').read_text(encoding='utf-8')

        html_lst = [{'html': single_html, 'filename': 'xxx'}]

        result = select_typical_htmls(html_lst, 1)

        # 验证返回的就是这个HTML
        self.assertIsNotNone(result)
        self.assertEqual(result[0]['html'], single_html)

    def test_select_typical_html_with_invalid_html(self):
        """测试select_typical_html处理无效HTML的情况."""

        single_html = base_dir.joinpath('assets/1.html').read_text(encoding='utf-8')
        invalid_html = '<html></html>'  # 无效的HTML

        html_lst = list()
        html_lst.append({'html': invalid_html, 'filename': 'xxx0'})
        html_lst.append({'html': single_html, 'filename': 'xxx1'})

        result = select_typical_htmls(html_lst, 1)

        # 应该跳过无效HTML，返回有效HTML
        self.assertIsNotNone(result)
        self.assertEqual(result[0]['html'], single_html)

    def test_select_typical_html_with_zero(self):
        """测试输入为空的情况."""
        html_lst = list()

        result = select_typical_htmls(html_lst, 1)

        # 应该跳过无效HTML，返回有效HTML
        self.assertIsNotNone(result)
