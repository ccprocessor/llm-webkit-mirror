import unittest

from pathlib import Path

from llm_web_kit.pipeline.extractor.html.recognizer.cccode import (
    CodeRecognizer,
)
from llm_web_kit.pipeline.extractor.html.extractor import HTMLFileFormatExtractor

TEST_CASES = [
    {
        "input": (
            "assets/cccode/geeksforgeeks.html",
            "https://www.geeksforgeeks.org/output-java-program-set-7/?ref=rp",
        ),
        "expected": [],
    },
    {
        "input": (
            "assets/cccode/homemade.html",
            "https://www.test.com/",
        ),
        "expected": [],
    },
    {
        "input": (
            "assets/cccode/prismjs.html",
            "https://prismjs.com/",
        ),
        "expected": [],
    },
    {
        "input": (
            "assets/cccode/react.html",
            "https://react.dev/reference/react/Fragment",
        ),
        "expected": [],
    },
    {
        "input": (
            "assets/cccode/stackoverflow.html",
            "https://stackoverflow.com/questions/35302978/how-to-get-current-value-of-androids-proximity-sensor",
        ),
        "expected": [],
    },
    {
        "input": (
            "assets/cccode/telerik.html",
            "https://www.telerik.com/forums/virtual-mode-custom-cell-datatemplate-problems",
        ),
        "expected": [],
    },
]

base_dir = Path(__file__).parent


class TestMathRecognizer(unittest.TestCase):
    def setUp(self):
        self.rec = CodeRecognizer()

    def test_code_rec(self):
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case["input"][0])
            base_url = test_case["input"][1]
            raw_html = raw_html_path.read_text()
            parts = self.rec.recognize(base_url, [(raw_html, raw_html)], raw_html)
            # TODO: add assertions


if __name__ == "__main__":
    r = TestMathRecognizer()
    r.setUp()
    r.test_code_rec()
