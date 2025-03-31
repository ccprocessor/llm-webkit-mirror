import unittest
from pathlib import Path

from llm_web_kit.config.cfg_reader import load_pipe_tpl
from llm_web_kit.extractor.extractor_chain import ExtractSimpleFactory
from llm_web_kit.extractor.html.recognizer.cccode import CodeRecognizer
from llm_web_kit.extractor.html.recognizer.recognizer import CCTag
from llm_web_kit.input.datajson import DataJson
from llm_web_kit.libs.html_utils import get_element_text, html_to_element

TEST_CASES = [
    {
        'input': (
            'assets/cccode/mathorg.html',
            'https://www.mathorg.cn/forum.php?mod=viewthread&tid=36798&extra=page%3D1',
        ),
        'expected': [
            'assets/cccode/mathorg-0.py',
        ],
    },
    {
        'input': (
            'assets/cccode/cprograming.html',
            'https://cboard.cprogramming.com/c-programming/96288-one-question-about-array-function-prototype-declaration-printable-thread.html',
        ),
        'expected': [
            'assets/cccode/cprograming.c',
            'int a[]',
        ],
    },
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
    {
        'input': (
            'assets/cccode/table-code.html',
            'https://git.znc.in/Dessa/gentoo/src/commit/d8bae05997012bacefdf65cb1f273a437c448129/sys-process/audit/audit-2.6.4.ebuild',
        ),
        'expected': [
            'assets/cccode/table-code-1.sh',
        ],
    }
]

base_dir = Path(__file__).parent


class TestCodeRecognizer(unittest.TestCase):
    def setUp(self):
        self.rec = CodeRecognizer()
        self.chain_config = load_pipe_tpl('html')

    def compare_code(self, expect: str, answer: str) -> None:
        if expect != answer:
            print(expect, answer)
        self.assertEqual(expect, answer)
        # expect_lines = [line for line in expect.split('\n') if line]
        # answer_lines = [line for line in answer.split('\n') if line]
        # self.assertEqual(len(expect_lines), len(answer_lines))
        # for x, y in zip(expect_lines, answer_lines):
        #     self.assertEqual(x, y)

    def test_inline_code_output(self):
        chain = ExtractSimpleFactory.create(self.chain_config)
        self.assertIsNotNone(chain)
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

        resp = chain.extract(input_data)
        answer = resp.get_content_list().to_mm_md().strip('\n')
        expect = base_dir.joinpath('assets/cccode/mathworks.md').read_text().strip('\n')
        self.assertEqual(expect, answer)
        answer = resp.get_content_list().to_txt().strip('\n')
        expect = (
            base_dir.joinpath('assets/cccode/mathworks.txt').read_text().strip('\n')
        )
        self.assertEqual(expect, answer)

    def test_code_rec(self):
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][0])
            base_url = test_case['input'][1]
            print(base_url)
            raw_html = raw_html_path.read_text()
            parts = self.rec.recognize(base_url, [(html_to_element(raw_html), html_to_element(raw_html))], raw_html)
            # parts = [
            #    part[0]
            #    for part in parts
            #    if CCTag.CC_CODE in part[0] or CCTag.CC_CODE_INLINE in part[0]
            # ]
            # for part in parts:
            #     part_el = html_to_element(part)
            #     answer = get_element_text(part_el).strip()
            #     print("--------------------------------------------------")
            #     print(answer)
            #     print("--------------------------------------------------")
            answers = []
            for part in parts:
                part_el = part[0]
                cccodes = part_el.xpath(f'.//{CCTag.CC_CODE}') + part_el.xpath(
                    f'.//{CCTag.CC_CODE_INLINE}'
                )
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

    def test_inclusion(self):
        chain = ExtractSimpleFactory.create(self.chain_config)
        self.assertIsNotNone(chain)
        raw_html = base_dir.joinpath('assets/cccode/telerik-case-2.html').read_text()
        input_data = DataJson(
            {
                'track_id': 'f7b3b1b4-0b1b',
                'dataset_name': 'news',
                'url': 'https://www.telerik.com/forums/set-style-of-root-radmenuitem-when-child-item-is-selected',
                'data_source_category': 'HTML',
                'html': raw_html,
                'file_bytes': 1000,
                'meta_info': {'input_datetime': '2020-01-01 00:00:00'},
            }
        )

        resp = chain.extract(input_data)
        answer = resp.get_content_list()
        count = 0
        for page in answer:
            for item in page:
                if item['type'] == 'code':
                    count += 1
        self.assertEqual(count, 1)

    def test_to_md_first_line_spaces(self):
        html = """<pre><code>  •	Review your business objectives
  •	Uncover your challenges and problems
  •	Visualize solutions to help move your organization forward
</code></pre>
"""
        chain = ExtractSimpleFactory.create(self.chain_config)
        self.assertIsNotNone(chain)
        input_data = DataJson(
            {
                'track_id': 'f7b3b1b4-0b1b',
                'dataset_name': 'news',
                'url': 'https://www.telerik.com/forums/set-style-of-root-radmenuitem-when-child-item-is-selected',
                'data_source_category': 'HTML',
                'html': html,
                'file_bytes': 1000,
                'meta_info': {'input_datetime': '2020-01-01 00:00:00'},
            }
        )

        resp = chain.extract(input_data)
        answer = resp.get_content_list().to_mm_md()
        self.assertEqual(
            answer,
            """```
•\tReview your business objectives
•\tUncover your challenges and problems
•\tVisualize solutions to help move your organization forward
```
""",
        )

    """
    测试用例来源：
    http://terra.polydev.org/config/development/config-system.html
    CC-MAIN-2024-30/segments/1720763514387.30/warc/CC-MAIN-20240712094214-20240712124214-00117.warc.gz?bytes=23736586,11582
    """

    def test_lineno(self):
        html = """<pre><span></span><span class="linenos"> 1</span><span class="p">{</span>
<span class="hll"><span class="linenos"> 2</span><span class="w">   </span><span class="nt">"type"</span><span class="p">:</span><span class="w"> </span><span class="s2">"ZOO"</span><span class="p">,</span>
</span><span class="linenos"> 3</span><span class="w">   </span><span class="nt">"description"</span><span class="p">:</span><span class="w"> </span><span class="s2">"A zoo of Australian animals."</span><span class="p">,</span>
<span class="linenos"> 4</span><span class="w">   </span><span class="nt">"animals"</span><span class="p">:</span><span class="w"> </span><span class="p">{</span>
<span class="linenos"> 5</span><span class="w">      </span><span class="nt">"koala"</span><span class="p">:</span><span class="w"> </span><span class="p">{</span>
<span class="linenos"> 6</span><span class="w">         </span><span class="nt">"color"</span><span class="p">:</span><span class="w"> </span><span class="s2">"grey"</span><span class="p">,</span>
<span class="linenos"> 7</span><span class="w">         </span><span class="nt">"legs"</span><span class="p">:</span><span class="w"> </span><span class="mi">4</span>
<span class="linenos"> 8</span><span class="w">      </span><span class="p">},</span>
<span class="linenos"> 9</span><span class="w">      </span><span class="nt">"kangaroo"</span><span class="p">:</span><span class="w"> </span><span class="p">{</span>
<span class="linenos">10</span><span class="w">         </span><span class="nt">"color"</span><span class="p">:</span><span class="w"> </span><span class="s2">"brown"</span><span class="p">,</span>
<span class="linenos">11</span><span class="w">         </span><span class="nt">"legs"</span><span class="p">:</span><span class="w"> </span><span class="mi">2</span>
<span class="linenos">12</span><span class="w">      </span><span class="p">}</span>
<span class="linenos">13</span><span class="w">   </span><span class="p">}</span>
<span class="linenos">14</span><span class="p">}</span>
</pre>
"""
        chain = ExtractSimpleFactory.create(self.chain_config)
        self.assertIsNotNone(chain)
        input_data = DataJson(
            {
                'track_id': 'f7b3b1b4-0b1b',
                'dataset_name': 'news',
                'url': 'https://www.telerik.com/forums/set-style-of-root-radmenuitem-when-child-item-is-selected',
                'data_source_category': 'HTML',
                'html': html,
                'file_bytes': 1000,
                'meta_info': {'input_datetime': '2020-01-01 00:00:00'},
            }
        )

        resp = chain.extract(input_data)
        answer = resp.get_content_list().to_mm_md()

        self.assertEqual(answer, """```
{
   "type": "ZOO",
   "description": "A zoo of Australian animals.",
   "animals": {
      "koala": {
         "color": "grey",
         "legs": 4
      },
      "kangaroo": {
         "color": "brown",
         "legs": 2
      }
   }
}
```
""")

    def test_lineno_2(self):
        html = """
<div>
<div class="linenumber index41"><span style="width: 50px; display: inline-block;">7</span><code>package</code>&nbsp;<code>com.servlet;</code></div>
<div class="linenumber index42"><span style="width: 50px; display: inline-block;">8</span></div>
<div class="linenumber index43"><span style="width: 50px; display: inline-block;">9</span><code>import</code>&nbsp;<code>java.io.IOException;</code></div>
<div class="linenumber index44"><span style="width: 50px; display: inline-block;">10</span><code>import</code>&nbsp;<code>java.io.PrintWriter;</code></div>
<div class="linenumber index45"><span style="width: 50px; display: inline-block;">11</span></div>
<div class="linenumber index46"><span style="width: 50px; display: inline-block;">12</span><code>import</code>&nbsp;<code>javax.servlet.ServletException;</code></div>
<div class="linenumber index47"><span style="width: 50px; display: inline-block;">13</span><code>import</code>&nbsp;<code>javax.servlet.http.HttpServlet;</code></div>
<div class="linenumber index48"><span style="width: 50px; display: inline-block;">14</span><code>import</code>&nbsp;<code>javax.servlet.http.HttpServletRequest;</code></div>
<div class="linenumber index49"><span style="width: 50px; display: inline-block;">15</span><code>import</code>&nbsp;<code>javax.servlet.http.HttpServletResponse;</code></div>
<div class="linenumber index51"><span style="width: 50px; display: inline-block;">16</span></div>
<div class="linenumber index50"><span style="width: 50px; display: inline-block;">100</span><code>import</code>&nbsp;<code>com.dao.UsersDao;</code></div>
</div>
"""
        chain = ExtractSimpleFactory.create(self.chain_config)
        self.assertIsNotNone(chain)
        input_data = DataJson(
            {
                'track_id': 'f7b3b1b4-0b1b',
                'dataset_name': 'news',
                'url': 'https://www.telerik.com/forums/set-style-of-root-radmenuitem-when-child-item-is-selected',
                'data_source_category': 'HTML',
                'html': html,
                'file_bytes': 1000,
                'meta_info': {'input_datetime': '2020-01-01 00:00:00'},
            }
        )

        resp = chain.extract(input_data)
        answer = resp.get_content_list().to_mm_md()

        self.assertEqual(answer, """```
package com.servlet;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.dao.UsersDao;
```
""")

    def test_lineno_3(self):
        html = """<div>
<div style="display: inline-block">
<div class="linenumber index41" style="height: 2em;">7</div>
<div class="linenumber index42" style="height: 2em;">8</div>
<div class="linenumber index43" style="height: 2em;">9</div>
<div class="linenumber index44" style="height: 2em;">10</div>
<div class="linenumber index45" style="height: 2em;">11</div>
<div class="linenumber index46" style="height: 2em;">12</div>
<div class="linenumber index47" style="height: 2em;">13</div>
<div class="linenumber index48" style="height: 2em;">14</div>
<div class="linenumber index49" style="height: 2em;">15</div>
<div class="linenumber index51" style="height: 2em;">16</div>
<div class="linenumber index50" style="height: 2em;">100</div>
</div>
<div style="display: inline-block">
<div class="linenumber index41" style="height: 2em;"><code>package</code>&nbsp;<code>com.servlet;</code><br></div>
<div class="linenumber index42" style="height: 2em;"><br></div>
<div class="linenumber index43" style="height: 2em;"><code>import</code>&nbsp;<code>java.io.IOException;</code><br></div>
<div class="linenumber index44" style="height: 2em;"><code>import</code>&nbsp;<code>java.io.PrintWriter;</code><br></div>
<div class="linenumber index45" style="height: 2em;"><br></div>
<div class="linenumber index46" style="height: 2em;"><code>import</code>&nbsp;<code>javax.servlet.ServletException;</code><br></div>
<div class="linenumber index47" style="height: 2em;"><code>import</code>&nbsp;<code>javax.servlet.http.HttpServlet;</code><br></div>
<div class="linenumber index48" style="height: 2em;"><code>import</code>&nbsp;<code>javax.servlet.http.HttpServletRequest;</code><br></div>
<div class="linenumber index49" style="height: 2em;"><code>import</code>&nbsp;<code>javax.servlet.http.HttpServletResponse;</code><br></div>
<div class="linenumber index51" style="height: 2em;"><br></div>
<div class="linenumber index50" style="height: 2em;"><code>import</code>&nbsp;<code>com.dao.UsersDao;</code><br></div>
</div>
</div>"""
        chain = ExtractSimpleFactory.create(self.chain_config)
        self.assertIsNotNone(chain)
        input_data = DataJson(
            {
                'track_id': 'f7b3b1b4-0b1b',
                'dataset_name': 'news',
                'url': 'https://www.telerik.com/forums/set-style-of-root-radmenuitem-when-child-item-is-selected',
                'data_source_category': 'HTML',
                'html': html,
                'file_bytes': 1000,
                'meta_info': {'input_datetime': '2020-01-01 00:00:00'},
            }
        )

        resp = chain.extract(input_data)
        answer = resp.get_content_list().to_mm_md()

        self.assertEqual(answer, """```
package com.servlet;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.dao.UsersDao;
```
""")

    def test_lineno_4(self):
        """行内代码尝试寻找行号删除导致代码节点顺序发生变化。 原代码路径为：/div[2]/code, /div[3]/code
        在删除行号后为：/div[1]/cccode, /div[2]/code."""
        html = """<div>
<p>1<p>
<p>2<p>
<p>3<p>
<p>4<p>
<p>5<p>
</div>
<div>This is inline <code>code</code>.<div>
<div>
<code>line one</code><br>
<code>line two</code><br>
<code>line three</code><br>
<code>line four</code><br>
<code>line five</code><br>
</div>
<div>
<code>A<code>
</div>
"""
        # 无须检查内容，只要不爆错就可以了
        _ = self.rec.recognize('', [(html_to_element(html), html_to_element(html))], html)
