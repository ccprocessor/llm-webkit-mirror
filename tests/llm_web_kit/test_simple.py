import unittest

from llm_web_kit.simple import extract_html_to_md, extract_html_to_mm_md


class TestSimple(unittest.TestCase):
    def setUp(self):
        self.url = 'https://example.com'
        self.html_content = '<html><body><h1>Test Content</h1><p>This is a test paragraph.</p><img src="https://example.com/image.jpg" alt="Test Image" /></body></html>'

    def test_extractor_factory(self):
        # Setup mocks
        md = extract_html_to_md(self.url, self.html_content)
        self.assertEqual(md, '# Test Content\n\nThis is a test paragraph.\n')

    def test_extract_html_to_mm_md(self):
        # Setup mock
        mm_md = extract_html_to_mm_md(self.url, self.html_content)
        self.assertEqual(mm_md, '# Test Content\n\nThis is a test paragraph.\n\n![Test Image](e5db82b5bf63d49d80c5533616892d3386f43955369520986d67653c700fc53c)\n')
