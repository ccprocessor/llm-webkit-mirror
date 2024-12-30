import os
import unittest

from llm_web_kit.pipeline.extractor.html.recognizer.recognizer import \
    BaseHTMLElementRecognizer


class TestBaseHTMLElementRecognizer(unittest.TestCase):
    def test_html_split_by_tags_1(self):
        with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/recognizer/image.html', 'r') as file:
            html_content = file.read()

        result = BaseHTMLElementRecognizer.html_split_by_tags(html_content, ['img'])
        assert len(result) == 7

    def test_html_split_by_tags_2(self):
        with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/recognizer/cccode.html', 'r') as file:
            html_content = file.read()

        result = BaseHTMLElementRecognizer.html_split_by_tags(html_content, ['cccode'])
        assert len(result) == 3

    def test_html_split_by_tags_3(self):
        with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/recognizer/raw_html_attr.html', 'r') as file:
            html_content = file.read()

        result = BaseHTMLElementRecognizer.html_split_by_tags(html_content, ['ccmath'])
        assert len(result) == 2
        assert result[0][1] == '$E=MC^2$'

    def test_html_split_by_tags_with_parent_nodes(self):
        """
        测试是否能够正确带上父节点
        """
        with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/recognizer/with_parent_nodes.html', 'r') as file:
            html_content = file.read()

        result_with_parent = BaseHTMLElementRecognizer.html_split_by_tags(html_content, 'cccode')
        assert len(result_with_parent) == 7
        assert result_with_parent[0][0] == """<html><body><article>
    这里是text
    <span>这里是span</span></article></body></html>"""
        assert result_with_parent[2][0] == '<html><body><article><cccode>print("BBBBBB")</cccode></article></body></html>'
        assert result_with_parent[3][0] == """<html><body><article>
    这里是tail
    <div><p>
            这里是div text
            <span>这里是span2</span></p></div></article></body></html>"""

        result = BaseHTMLElementRecognizer.html_split_by_tags(html_content, 'cccode')
        assert len(result) == 7

    def test_is_cctag(self):
        with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/recognizer/iscctag.html', 'r') as file:
            html_content = file.read()

        assert BaseHTMLElementRecognizer.is_cc_html(html_content, 'cccode')
        assert BaseHTMLElementRecognizer.is_cc_html(html_content, 'ccmath')
        assert BaseHTMLElementRecognizer.is_cc_html(html_content, 'ccimage')
        assert not BaseHTMLElementRecognizer.is_cc_html(html_content, 'ccvideo')
        assert not BaseHTMLElementRecognizer.is_cc_html(html_content, 'cctitle')
        assert  BaseHTMLElementRecognizer.is_cc_html(html_content, ['cccode', 'ccxxx'])
