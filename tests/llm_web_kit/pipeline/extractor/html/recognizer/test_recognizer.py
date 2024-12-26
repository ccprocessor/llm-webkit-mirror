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

    def test_html_split_by_tags_2(self):
        with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/cccode.html', 'r') as file:
            html_content = file.read()

        result = BaseHTMLElementRecognizer.html_split_by_tags(html_content, ['cccode'])
        assert len(result) == 3

    def test_html_split_by_tags_3(self):
        with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/raw_html_attr.html', 'r') as file:
            html_content = file.read()

        result = BaseHTMLElementRecognizer.html_split_by_tags(html_content, ['ccmath'])
        assert len(result) == 4
        assert result[0][1] == '$E=MC^2$'
