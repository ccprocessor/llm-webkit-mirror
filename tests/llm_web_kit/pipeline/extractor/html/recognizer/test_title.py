# 测试title识别器
import os

import pytest

from llm_web_kit.pipeline.extractor.html.recognizer.title import \
    TitleRecognizer


@pytest.fixture
def title_recognizer():
    return TitleRecognizer()


def test_title_recognizer(title_recognizer):
    with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/recognizer/title.html', 'r') as file:
        html_content = file.read()

    result = title_recognizer.recognize('http://www.baidu.com', [(html_content, html_content)], html_content)
    assert len(result) == 10
    assert result[0][0].replace('\n', '') == '<html><body><cctitle level="1" html="&lt;h1&gt;&#x5927;&#x6A21;&#x578B;&#x597D;&#xFF0C;&#x5927;&#x6A21;&#x578B;&#x68D2;1&lt;/h1&gt;&#10;        ">大模型好，大模型棒1</cctitle></body></html>'
    assert result[6][0].replace('\n', '') == '<html><body><cctitle level="3" html="&lt;h3&gt;&#x5927;&#x6A21;&#x578B;&#x597D;&#xFF0C;&#x5927;&#x6A21;&#x578B;&#x68D2;5&lt;/h3&gt;&#10;        ">大模型好，大模型棒5</cctitle></body></html>'
