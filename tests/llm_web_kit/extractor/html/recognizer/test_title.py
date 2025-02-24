# 测试title识别器
import os

import pytest

from llm_web_kit.extractor.html.recognizer.title import TitleRecognizer


@pytest.fixture
def title_recognizer():
    return TitleRecognizer()


def test_title_recognizer(title_recognizer):
    with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/recognizer/title.html', 'r') as file:
        html_content = file.read()

    result = title_recognizer.recognize('http://www.baidu.com', [(html_content, html_content)], html_content)
    assert len(result) == 10
    assert result[0][0] == """<html><body><cctitle level="1" html="&lt;h1&gt;大模型好，大模型棒1&lt;/h1&gt;
        ">大模型好，大模型棒1</cctitle></body></html>"""
    assert result[6][0] == """<html><body><cctitle level="3" html="&lt;h3&gt;大模型好，大模型棒5&lt;span&gt;大模型很棒&lt;/span&gt;&lt;/h3&gt;
        ">大模型好，大模型棒5 大模型很棒</cctitle></body></html>"""


def test_title_tails_and_levels(title_recognizer):
    html_content = """<h4>TEST:<cccode-inline>import *</cccode-inline>TEST</h4>Tail<p>aaa</p>"""
    result = title_recognizer.recognize('http://www.baidu.com', [(html_content, html_content)], html_content)
    assert len(result) == 2
    assert result[0][0] == '<div><cctitle level="4" html="&lt;h4&gt;TEST:&lt;cccode-inline&gt;import *&lt;/cccode-inline&gt;TEST&lt;/h4&gt;Tail">TEST: `import *` TEST</cctitle></div>'
    pass
