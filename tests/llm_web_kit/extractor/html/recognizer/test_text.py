# 测试text识别器
import os
from llm_web_kit.extractor.html.recognizer.text import TextParagraphRecognizer


def test_text_recognizer():
    with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/recognizer/text.html', 'r') as file:
        html_content = file.read()

    result = TextParagraphRecognizer().recognize('http://www.baidu.com', [(html_content, html_content)], html_content)
    for i in result:
        if "知识乱象" in i[1]:
            print(i[0])
            print(i[1])
