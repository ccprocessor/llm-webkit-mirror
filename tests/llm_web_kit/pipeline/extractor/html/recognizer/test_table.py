import unittest
from pathlib import Path

from lxml import etree

from llm_web_kit.pipeline.extractor.html.recognizer.table import \
    TableRecognizer

TEST_CASES = [
    {
        'input': (
            'assets/recognizer/table.html',
            'assets/recognizer/table_exclude.html',
        ),
        'expected':[
            ('<cccode>hello</cccode>', '<code>hello</code>'), ('<html><body><p>段落2</p></body></html>', '<html><body><p>段落2</p></body></html>'), ('<html><body><cctable type="complex" html="<table><tr><td rowspan="2">1</td><td>2</td></tr><tr><td>3</td></tr></table>">\'<tr><td rowspan="2">1</td><td>2</td></tr><tr><td>3</td></tr>\'</cctable></body></html>', '<table><tr><td rowspan="2">1</td><td>2</td></tr><tr><td>3</td></tr></table>'), ('<html><body><p>段落2</p></body></html>', '<html><body><p>段落2</p></body></html>'), ('<html><body><cctable type="complex" html="<table><tr><td rowspan="2">1</td><td>2</td></tr><tr><td>3</td></tr></table>">\'<tr><td rowspan="2">1</td><td>2</td></tr><tr><td>3</td></tr>\'</cctable></body></html>', '<table><tr><td rowspan="2">1</td><td>2</td></tr><tr><td>3</td></tr></table>')
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
            raw_html = raw_html_path.read_text()
            parts = self.rec.recognize(base_url, [(raw_html, raw_html)], raw_html)
            self.assertEqual(len(parts), len(test_case['expected']))


    def test_not_involve_table(self):
        """
        不包含表格
        """
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][1])
            base_url = test_case['input'][1]
            raw_html = raw_html_path.read_text()
            parts = self.rec.recognize(base_url, [(raw_html, raw_html)], raw_html)
            self.assertEqual(len(parts), 2)


if __name__ == '__main__':
    r = TestTableRecognizer()
    r.setUp()
    r.test_not_involve_table()
