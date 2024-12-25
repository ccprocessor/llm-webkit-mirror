import unittest

from pathlib import Path

from lxml import etree

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
        "expected": [
            "assets/cccode/geeksforgeeks-0.java",
            "assets/cccode/geeksforgeeks-1.java",
            "assets/cccode/geeksforgeeks-2.java",
            "assets/cccode/geeksforgeeks-3.java",
            "assets/cccode/geeksforgeeks-4.java",
        ],
    },
    {
        "input": (
            "assets/cccode/homemade.html",
            "https://www.test.com/",
        ),
        "expected": [
            "assets/cccode/homemade-0.py",
            "assets/cccode/homemade-1.py",
            "assets/cccode/homemade-2.py",
        ],
    },
    {
        "input": (
            "assets/cccode/prismjs.html",
            "https://prismjs.com/",
        ),
        "expected": [
            "assets/cccode/prismjs-0.html",
            "assets/cccode/prismjs-1.html",
            "assets/cccode/prismjs-2.html",
            "assets/cccode/prismjs-3.html",
            "assets/cccode/prismjs-4.html",
            "assets/cccode/prismjs-5.html",
            "assets/cccode/prismjs-6.sh",
            "assets/cccode/prismjs-7.ts",
            "assets/cccode/prismjs-8.js",
            "assets/cccode/prismjs-9.js",
        ],
    },
    {
        "input": (
            "assets/cccode/react.html",
            "https://react.dev/reference/react/Fragment",
        ),
        "expected": [
            "assets/cccode/react-0.html",
            "assets/cccode/react-1.js",
            "assets/cccode/react-2.js",
            "assets/cccode/react-3.js",
            "assets/cccode/react-4.js",
            "assets/cccode/react-5.js",
        ],
    },
    {
        "input": (
            "assets/cccode/stackoverflow.html",
            "https://stackoverflow.com/questions/35302978/how-to-get-current-value-of-androids-proximity-sensor",
        ),
        "expected": [
            "assets/cccode/stackoverflow-0.java",
            "assets/cccode/stackoverflow-1.xml",
            "assets/cccode/stackoverflow-2.java",
        ],
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
            print(base_url)
            raw_html = raw_html_path.read_text()
            parts = self.rec.recognize(base_url, [(raw_html, raw_html)], raw_html)
            parts = [part for part in parts if "cccode" in part]
            # self.assertEqual(len(parts), len(test_case["expected"]))
            print(len(test_case["expected"]))
            for answer_path in test_case["expected"]:
                answer = base_dir.joinpath(answer_path).read_text()
                # self.assertEqual()


if __name__ == "__main__":
    r = TestMathRecognizer()
    r.setUp()
    r.test_code_rec()
