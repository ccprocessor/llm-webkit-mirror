# 测试text识别器
import os

from llm_web_kit.extractor.html.recognizer.text import TextParagraphRecognizer


def test_text_recognizer():
    with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/recognizer/text.html', 'r') as file:
        html_content = file.read()

    text_recognizer = TextParagraphRecognizer()

    assert text_recognizer._TextParagraphRecognizer__combine_text('知识乱象\n', '中共中央政治局召开会议审议《成-2020年10月16日新闻联播', 'zh')[:7] == '知识乱象\n中共'
    result = text_recognizer.recognize('http://www.baidu.com', [(html_content, html_content)], html_content)
    assert result[909][0][1413:1422] == '知识乱象\\n 中共'
