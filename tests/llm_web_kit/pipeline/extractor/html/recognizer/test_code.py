import unittest
from pathlib import Path

from llm_web_kit.libs.html_utils import get_element_text, html_to_element
from llm_web_kit.pipeline.extractor.html.recognizer.cccode import \
    CodeRecognizer

TEST_CASES = [{'input': ('assets/cccode/geeksforgeeks.html',
                         'https://www.geeksforgeeks.org/output-java-program-set-7/?ref=rp',
                         ),
               'expected': ['assets/cccode/geeksforgeeks-0.java',
                            'assets/cccode/geeksforgeeks-1.java',
                            'assets/cccode/geeksforgeeks-2.java',
                            'assets/cccode/geeksforgeeks-3.java',
                            'assets/cccode/geeksforgeeks-4.java',
                            ],
               },
              {'input': ('assets/cccode/homemade.html',
               'https://www.test.com/',
                         ),
               'expected': ['assets/cccode/homemade-0.py',
                            'assets/cccode/homemade-1.py',
                            'assets/cccode/homemade-2.py',
                            ],
               },
              {'input': ('assets/cccode/prismjs.html',
               'https://prismjs.com/',
                         ),
               'expected': ['assets/cccode/prismjs-0.html',
                            'assets/cccode/prismjs-1.html',
                            'assets/cccode/prismjs-2.html',
                            'assets/cccode/prismjs-3.html',
                            'assets/cccode/prismjs-4.html',
                            'assets/cccode/prismjs-5.html',
                            'assets/cccode/prismjs-6.sh',
                            'assets/cccode/prismjs-7.ts',
                            'assets/cccode/prismjs-8.js',
                            'assets/cccode/prismjs-9.js',
                            ],
               },
              {'input': ('assets/cccode/react.html',
               'https://react.dev/reference/react/Fragment',
                         ),
               'expected': ['assets/cccode/react-0.html',
                            'assets/cccode/react-1.js',
                            'assets/cccode/react-2.js',
                            'assets/cccode/react-3.js',
                            'assets/cccode/react-4.js',
                            'assets/cccode/react-5.js',
                            ],
               },
              {'input': ('assets/cccode/stackoverflow.html',
               'https://stackoverflow.com/questions/35302978/how-to-get-current-value-of-androids-proximity-sensor',
                         ),
               'expected': ['assets/cccode/stackoverflow-0.java',
                            'assets/cccode/stackoverflow-1.xml',
                            'assets/cccode/stackoverflow-2.java',
                            ],
               },
              {'input': ('assets/cccode/telerik.html',
               'https://www.telerik.com/forums/virtual-mode-custom-cell-datatemplate-problems',
                         ),
               'expected': ['assets/cccode/telerik-0.cs',
                            'assets/cccode/telerik-1.cs',
                            'assets/cccode/telerik-2.xml',
                            'assets/cccode/telerik-3.cs',
                            'assets/cccode/telerik-4.xml',
                            'assets/cccode/telerik-5.cs',
                            'assets/cccode/telerik-6.cs',
                            'assets/cccode/telerik-7.xml',
                            'assets/cccode/telerik-8.cs',
                            ],
               },
              ]

base_dir = Path(__file__).parent


class TestMathRecognizer(unittest.TestCase):
    def setUp(self):
        self.rec = CodeRecognizer()

    def compare_code(self, expect: str, answer: str) -> None:
        self.assertEqual(expect, answer)
        # expect_lines = [line for line in expect.split('\n') if line]
        # answer_lines = [line for line in answer.split('\n') if line]
        # self.assertEqual(len(expect_lines), len(answer_lines))
        # for x, y in zip(expect_lines, answer_lines):
        #     self.assertEqual(x, y)

    def test_code_rec(self):
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][0])
            base_url = test_case['input'][1]
            print(base_url)
            raw_html = raw_html_path.read_text()
            parts = self.rec.recognize(
                base_url, [(raw_html, raw_html)], raw_html)
            parts = [part[0] for part in parts if 'cccode' in part[0]]
            self.assertEqual(len(parts), len(test_case['expected']))
            for expect_path, part in zip(test_case['expected'], parts):
                expect = base_dir.joinpath(expect_path).read_text().strip()
                part_el = html_to_element(part)
                answer = get_element_text(part_el).strip()
                self.compare_code(expect, answer)


if __name__ == '__main__':
    r = TestMathRecognizer()
    r.setUp()
    r.test_code_rec()
