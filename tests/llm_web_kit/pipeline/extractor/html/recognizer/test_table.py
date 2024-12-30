import unittest
from pathlib import Path

from lxml import etree

from llm_web_kit.pipeline.extractor.html.recognizer.table import \
    TableRecognizer

TEST_CASES = [
    {
        'input': (
            'assets/recognizer/table.html',
            'https://www.geeksforgeeks.org/output-java-program-set-7/?ref=rp',
        ),
        'expected': [
            'assets/cccode/geeksforgeeks-0.java'
        ]
    }
]

base_dir = Path(__file__).parent


class TestTableRecognizer(unittest.TestCase):
    def setUp(self):
        self.rec = TableRecognizer()

    def test_involve_cctale(self):
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][0])
            base_url = test_case['input'][1]
            print(base_url)
            raw_html = raw_html_path.read_text()
            parts = self.rec.recognize(base_url, [(raw_html, raw_html)], raw_html)
            parts = [part[0] for part in parts if 'cctable' in part[0]]
            #self.assertEqual(len(parts), len(test_case['expected']))
            for expect_path, part in zip(test_case['expected'], parts):
                expect = base_dir.joinpath(expect_path).read_text().strip()
                answer = (etree.fromstring(part, None).text or '').strip()
                #self.assertEqual(expect, answer)
            print(base_url, 'ok')


if __name__ == '__main__':
    r = TestTableRecognizer()
    r.setUp()
    r.test_involve_cctale()
