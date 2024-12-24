from types import ModuleType

from llm_web_kit.pipeline.extractor.html.magic_html import GeneralExtractor
from llm_web_kit.pipeline.extractor.html.recognizer.cccode import \
    CodeRecognizer
from llm_web_kit.pipeline.extractor.html.recognizer.code.testcase import (
    geeksforgeeks, homemade, prismjs, react, stackoverflow, telerik)

ge = GeneralExtractor()
cr = CodeRecognizer()
testcases: list[ModuleType] = [
    geeksforgeeks,
    homemade,
    prismjs,
    react,
    stackoverflow,
    telerik,
]
for testcase in testcases:
    filename = testcase.__name__.split('.')[-1] + '.txt'
    print(filename)
    codes = cr.recognize(
        testcase.base_url,
        [(testcase.html, testcase.html)],
        testcase.html,
    )
    with open(filename, 'wt') as f:
        for code in codes:
            f.write('-------------------------------------\n')
            f.write(code[1] + '\n')
            f.write('-------------------------------------\n')
