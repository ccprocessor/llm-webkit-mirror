from llm_web_kit.pipeline.extractor.html.recognizer.code.testcase import (
    geeksforgeeks,
    prismjs,
    stackoverflow,
    react,
)
from llm_web_kit.pipeline.extractor.html.recognizer.code import CodeRecognizer
from magic_html import GeneralExtractor

from types import ModuleType

ge = GeneralExtractor()
cr = CodeRecognizer()
testcases: list[ModuleType] = [geeksforgeeks, prismjs, stackoverflow, react]
for testcase in testcases:
    filename = testcase.__name__.split(".")[-1] + ".txt"
    codes = cr.recognize(
        testcase.base_url,
        [(testcase.html, testcase.html)],
        testcase.html,
    )
    with open(filename, "w") as f:
        for code in codes:
            f.write("-------------------------------------\n")
            f.write(code[0] + "\n")
            f.write("-------------------------------------\n")
