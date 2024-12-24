import os
import unittest

from llm_web_kit.pipeline.extractor.html.recognizer.recognizer import \
    BaseHTMLElementRecognizer


class TestBaseHTMLElementRecognizer(unittest.TestCase):
    def test_html_split_by_tags_1(self):
        with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/image.html', 'r') as file:
            html_content = file.read()

        result = BaseHTMLElementRecognizer.html_split_by_tags(html_content, ['img'])
        assert len(result) == 14
