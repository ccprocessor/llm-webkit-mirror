import unittest

from lxml import html

from llm_web_kit.model.html_lib.base_func import (document_fromstring,
                                                  extract_tag_text, get_title,
                                                  remove_blank_text)


class TestExtractTagText(unittest.TestCase):
    def test_img_tag(self):
        element = html.fromstring('<img alt="test alt">')
        self.assertEqual(extract_tag_text(element), 'test alt')

    def test_img_tag_no_alt(self):
        element = html.fromstring('<img>')
        self.assertEqual(extract_tag_text(element), '')

    def test_plain_text(self):
        element = html.fromstring('<p>Hello World</p>')
        self.assertEqual(extract_tag_text(element), 'Hello World')

    def test_nested_elements(self):
        element = html.fromstring('<div>Text <span>inside span</span> tail</div>')
        self.assertEqual(extract_tag_text(element), 'Text inside span tail')

    def test_newline_tags(self):
        element = html.fromstring('<div><p>Line1</p><br/><p>Line2</p></div>')
        result = extract_tag_text(element)
        # Expect "Line1\nLine2\n" after newline processing
        self.assertEqual(result.replace('\n', '|'), 'Line1|Line2|')

    def test_mixed_content(self):
        element = html.fromstring(
            """
            <div>
                Before
                <b>bold text</b>
                <span>
                    <i>italic</i>
                    tail
                </span>
                after
            </div>
        """
        )
        # Some problem here. But now the web classification model is trained with this behavior.
        # TODO Fix this bug and retrain the model
        # expected = "Before bold text italic tail after"
        expected = 'Before                 bold text italic                     tail                                  after'
        self.assertEqual(extract_tag_text(element).replace('\n', ' ').strip(), expected)

    def test_whitespace_handling(self):
        # Some problem here. But now the web classification model is trained with this behavior.
        # TODO Fix this bug and retrain the model
        # expected = "\n"
        element = html.fromstring('<div>   \t\n  </div>')
        self.assertEqual(extract_tag_text(element), '   \t\n  ')


class TestGetTitle(unittest.TestCase):
    def test_has_title(self):
        root = html.fromstring('<html><head><title>Test Title</title></head></html>')
        self.assertEqual(get_title(root), 'Test Title')

    def test_no_title(self):
        root = html.fromstring('<html><head></head></html>')
        self.assertIsNone(get_title(root))

    def test_multiple_titles(self):
        root = html.fromstring(
            '<html><head><title>First</title><title>Second</title></head></html>'
        )
        self.assertEqual(get_title(root), 'First')


class TestRemoveBlankText(unittest.TestCase):
    def test_remove_whitespace_nodes(self):
        root = html.fromstring(
            """
            <div>
                <p>   </p>
                <pre>  </pre>
                <code> </code>
                <span>  </span>
            </div>
        """
        )
        processed = remove_blank_text(root)

        # Check normal elements
        p = processed.find('.//p')
        self.assertIsNone(p.text)

        span = processed.find('.//span')
        self.assertIsNone(span.text)

        # Check preserved elements
        pre = processed.find('.//pre')
        self.assertEqual(pre.text.strip(), '', 'Pre text should preserve whitespace')
        self.assertEqual(pre.text, '  ')

        code = processed.find('.//code')
        self.assertEqual(code.text, ' ')

    def test_keep_trailing_text(self):
        root = html.fromstring('<div>Hello <b> </b>World</div>')
        processed = remove_blank_text(root)
        b = processed.find('.//b')
        self.assertIsNone(b.text)
        self.assertEqual(b.tail, 'World')


class TestDocumentFromString(unittest.TestCase):
    def test_basic_parsing(self):
        html_str = """
            <!DOCTYPE html>
            <html>
            <head><title>Test</title></head>
            <body>
                <p>Content</p>
            </body>
            </html>
        """
        root = document_fromstring(html_str)
        self.assertEqual(root.tag, 'html')
        self.assertIsNotNone(root.find('.//body/p'))

    def test_whitespace_removal(self):
        html_str = '<div>  <p>   </p>  </div>'
        root = document_fromstring(html_str)
        div = root.find('.//div')
        self.assertIsNone(div.text)
        p = div.find('.//p')
        self.assertIsNone(p.text)


if __name__ == '__main__':
    unittest.main()
