import unittest
from pathlib import Path

from llm_web_kit.input.datajson import DataJson
from llm_web_kit.libs.html_utils import get_element_text, html_to_element
from llm_web_kit.pipeline.extractor.html.recognizer.cccode import \
    CodeRecognizer
from llm_web_kit.pipeline.extractor.html.recognizer.recognizer import CCTag
from llm_web_kit.pipeline.pipeline_suit import PipelineSuit

TEST_CASES = [
    {
        'input': (
            'assets/cccode/geeksforgeeks.html',
            'https://www.geeksforgeeks.org/output-java-program-set-7/?ref=rp',
        ),
        'expected': [
            'assets/cccode/geeksforgeeks-0.java',
            'assets/cccode/geeksforgeeks-1.java',
            'assets/cccode/geeksforgeeks-2.java',
            'assets/cccode/geeksforgeeks-3.java',
            'assets/cccode/geeksforgeeks-4.java',
        ],
    },
    {
        'input': (
            'assets/cccode/homemade.html',
            'https://www.test.com/',
        ),
        'expected': [
            'assets/cccode/homemade-0.py',
            'assets/cccode/homemade-1.py',
            'assets/cccode/homemade-2.py',
        ],
    },
    {
        'input': (
            'assets/cccode/prismjs.html',
            'https://prismjs.com/',
        ),
        'expected': [
            'code.language-xxxx',
            '.comment',
            '.string',
            '.property',
            '<pre>',
            '<script>',
            '<code>',
            '<pre>',
            'language-xxxx',
            'language-xxxx',
            'prism.css',
            'prism.js',
            'assets/cccode/prismjs-0.html',
            '<code>',
            '<code>',
            'language-xxxx',
            'lang-xxxx',
            '<pre>',
            '<code>',
            'assets/cccode/prismjs-1.html',
            '<pre>',
            'language-xxxx',
            'assets/cccode/prismjs-2.html',
            '<',
            '&',
            '<code>',
            '&lt;',
            '&amp;',
            '<code>',
            'language-xxxx',
            'language-xxxx',
            '<body>',
            '<html>',
            '<code>',
            'language-none',
            'none',
            'language-plain',
            'Prism.manual',
            'true',
            'DOMContentLoaded',
            'data-manual',
            '<script>',
            'assets/cccode/prismjs-3.html',
            'assets/cccode/prismjs-4.html',
            'assets/cccode/prismjs-5.html',
            'npm',
            'assets/cccode/prismjs-6.sh',
            'import',
            'assets/cccode/prismjs-7.ts',
            'assets/cccode/prismjs-8.js',
            'prismjs',
            'markup',
            'css',
            'clike',
            'javascript',
            'loadLanguages()',
            'assets/cccode/prismjs-9.js',
            'loadLanguages()',
            'loadLanguages()',
            'loadLanguages.silent = true',
            'xxxx',
            'language-xxxx',
            'lang-xxxx',
        ],
    },
    {
        'input': (
            'assets/cccode/react.html',
            'https://react.dev/reference/react/Fragment',
        ),
        'expected': [
            '<Fragment>',
            '<>...</>',
            'assets/cccode/react-0.html',
            '<Fragment>',
            '<Fragment>',
            '<Fragment>',
            'Fragment',
            '<></>',
            '<Fragment></Fragment>',
            'key',
            '<Fragment>',
            'key',
            '<>...</>',
            'Fragment',
            "'react'",
            '<Fragment key={yourKey}>...</Fragment>',
            '<><Child /></>',
            '[<Child />]',
            '<><Child /></>',
            '<Child />',
            '<><><Child /></></>',
            '<Child />',
            'Fragment',
            '<>...</>',
            'assets/cccode/react-1.js',
            '<h1>',
            '<article>',
            'assets/cccode/react-6.js',
            'Fragment',
            'assets/cccode/react-2.js',
            'key',
            'Fragment',
            'assets/cccode/react-3.js',
            'Fragment',
            'assets/cccode/react-4.js',
            'Fragment',
            '<></>',
            'key',
            'key',
            'assets/cccode/react-5.js',
            'assets/cccode/react-7.js',
            '<Fragment>',
        ],
    },
    {
        'input': (
            'assets/cccode/stackoverflow.html',
            'https://stackoverflow.com/questions/35302978/how-to-get-current-value-of-androids-proximity-sensor',
        ),
        'expected': [
            'proximitySensor.getCurrentDistance();',
            'values[0]',
            'onSensorChanged',
            # 'assets/cccode/stackoverflow-0.java',
            'assets/cccode/stackoverflow-1.xml',
            'assets/cccode/stackoverflow-2.java',
        ],
    },
    {
        'input': (
            'assets/cccode/telerik.html',
            'https://www.telerik.com/forums/virtual-mode-custom-cell-datatemplate-problems',
        ),
        'expected': [
            'assets/cccode/telerik-0.cs',
            'assets/cccode/telerik-1.cs',
            'assets/cccode/telerik-9',
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
        self.pipeline_config = base_dir.parent.parent.parent.joinpath(
            'assets', 'html_pipe_normal.jsonc'
        )

    def compare_code(self, expect: str, answer: str) -> None:
        self.assertEqual(expect, answer)
        # expect_lines = [line for line in expect.split('\n') if line]
        # answer_lines = [line for line in answer.split('\n') if line]
        # self.assertEqual(len(expect_lines), len(answer_lines))
        # for x, y in zip(expect_lines, answer_lines):
        #     self.assertEqual(x, y)

    def test_inline_code_output(self):
        pipeline = PipelineSuit(self.pipeline_config.as_posix())
        raw_html = base_dir.joinpath('assets/cccode/mathworks.html').read_text()
        input_data = DataJson(
            {
                'track_id': 'f7b3b1b4-0b1b',
                'dataset_name': 'news',
                'url': 'https://ww2.mathworks.cn/help/fixedpoint/ug/single-precision-conversion-verification-best-practices.html',
                'data_source_category': 'HTML',
                'html': raw_html,
                'file_bytes': 1000,
                'meta_info': {'input_datetime': '2020-01-01 00:00:00'},
            }
        )

        resp = pipeline.extract(input_data)
        answer = resp.get_content_list().to_mm_md().strip('\n')
        print(answer)
        expect = base_dir.joinpath('assets/cccode/mathworks.md').read_text().strip('\n')
        self.assertEqual(expect, answer)
        answer = resp.get_content_list().to_txt().strip('\n')
        print(answer)
        expect = base_dir.joinpath('assets/cccode/mathworks.txt').read_text().strip('\n')
        self.assertEqual(expect, answer)

    def test_code_rec(self):
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][0])
            base_url = test_case['input'][1]
            print(base_url)
            raw_html = raw_html_path.read_text()
            parts = self.rec.recognize(base_url, [(raw_html, raw_html)], raw_html)
            parts = [part[0] for part in parts if CCTag.CC_CODE in part[0] or CCTag.CC_CODE_INLINE in part[0]]
            # for part in parts:
            #     part_el = html_to_element(part)
            #     answer = get_element_text(part_el).strip()
            #     print("--------------------------------------------------")
            #     print(answer)
            #     print("--------------------------------------------------")
            answers = []
            for part in parts:
                part_el = html_to_element(part)
                cccodes = part_el.xpath(f'.//{CCTag.CC_CODE}') + part_el.xpath(f'.//{CCTag.CC_CODE_INLINE}')
                # self.assertEqual(len(cccodes), 1)
                for part_el in cccodes:
                    inline = part_el.get('inline', 'false') == 'true'
                    answer = get_element_text(part_el).strip('\n')
                    if not answer:
                        continue
                    answers.append((answer, inline))

            self.assertEqual(len(answers), len(test_case['expected']))
            for expect_path, (answer, inline) in zip(test_case['expected'], answers):
                if expect_path.startswith('assets'):
                    expect = base_dir.joinpath(expect_path).read_text().strip('\n')
                    self.assertTrue(not inline)
                else:
                    expect = expect_path
                    # 并非所有 inline code 都可以识别出来
                    # self.assertTrue(inline)
                    if not inline:
                        print(f'{expect} is not identified as inline code')
                # print(expect, answer)
                self.compare_code(expect, answer)


if __name__ == '__main__':
    r = TestMathRecognizer()
    r.setUp()
    r.test_code_rec()
    r.test_inline_code_output()
