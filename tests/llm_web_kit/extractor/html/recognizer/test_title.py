# 测试title识别器
import os

import pytest

from llm_web_kit.extractor.html.recognizer.title import TitleRecognizer
from llm_web_kit.libs.html_utils import element_to_html


@pytest.fixture
def title_recognizer():
    return TitleRecognizer()


def test_title_recognizer(title_recognizer):
    with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/recognizer/title.html', 'r') as file:
        html_content = file.read()

    result = title_recognizer.recognize('http://www.baidu.com', [(html_content, html_content)], html_content)
    assert len(result) == 10
    assert element_to_html(result[0][0]) == """<html><body><cctitle level="1" html="&lt;h1&gt;大模型好，大模型棒1&lt;/h1&gt;">大模型好，大模型棒1</cctitle></body></html>"""
    assert element_to_html(result[6][0]) == """<html><body><cctitle level="3" html="&lt;h3&gt;大模型好，大模型棒5&lt;span&gt;大模型很棒&lt;/span&gt;&lt;/h3&gt;">大模型好，大模型棒5 大模型很棒</cctitle></body></html>"""


def test_title_tails_and_levels(title_recognizer):
    html_content = """<h4>TEST:<cccode-inline>import *</cccode-inline>TEST</h4>Tail<p>aaa</p>"""
    result = title_recognizer.recognize('http://www.baidu.com', [(html_content, html_content)], html_content)
    assert len(result) == 2
    assert element_to_html(result[0][0]) == '<div><cctitle level="4" html="&lt;h4&gt;TEST:&lt;cccode-inline&gt;import *&lt;/cccode-inline&gt;TEST&lt;/h4&gt;">TEST: `import *` TEST</cctitle></div>'
    pass


def test_title1(title_recognizer):
    """
    测试修复标题被隔断
    Args:
        title_recognizer:

    Returns:

    """
    with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/recognizer/title1_main.html', 'r') as file:
        main_html_content = file.read()

    with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/recognizer/title1.html', 'r') as file:
        html_content = file.read()
    result = title_recognizer.recognize('http://www.baidu.com', [(main_html_content, main_html_content)], html_content)
    assert 'Compare vibrational frequencies for two calculations for C&lt;sub&gt;3&lt;/sub&gt; (carbon trimer)' in element_to_html(result[1][0])


def test_title_has_formula(title_recognizer):
    """
    标题含有公式
    Args:
        title_recognizer:

    Returns:

    """
    html_content = r"""<h4 class="record-header" data-anno-uid="anno-uid-ak93kqpj44f">
    <a cc-select="true" class="mark-selected" data-anno-uid="anno-uid-37umi9vq7o2" href="https://www.hepdata.net/record/ins228250" style="">
                                                Vector Meson Production in the Final State $K^+ K^- \pi^+ \pi^-$ Photon-photon Collisions
                                            </a>
    </h4>"""
    result = title_recognizer.recognize('http://www.baidu.com', [(html_content, html_content)], html_content)
    assert r"Vector Meson Production in the Final State $K^+ K^- \pi^+ \pi^-$ Photon-photon Collisions" in element_to_html(result[0][0])
