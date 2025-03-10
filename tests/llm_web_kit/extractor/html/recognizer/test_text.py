# 测试text识别器
import os
from llm_web_kit.extractor.html.recognizer.text import TextParagraphRecognizer


def test_text_recognizer():
    with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/recognizer/text.html', 'r') as file:
        html_content = file.read()

    result = TextParagraphRecognizer().recognize('http://www.baidu.com', [(html_content, html_content)], html_content)
    assert result[909][0][1413:1422] == '知识乱象\\n 中共'
