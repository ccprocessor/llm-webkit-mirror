import json
import unittest
from pathlib import Path

from llm_web_kit.extractor.html.recognizer.recognizer import CCTag
from llm_web_kit.extractor.html.recognizer.table import TableRecognizer
from llm_web_kit.libs.html_utils import html_to_element

TEST_CASES = [
    {
        'input': (
            'assets/recognizer/table.html',
            'assets/recognizer/table_exclude.html',
            'assets/recognizer/only_table.html',
            'assets/recognizer/table_simple_compex.html',
            'assets/recognizer/table_to_content_list_simple.html',
            'assets/recognizer/table_to_content_list_complex.html',
            'assets/recognizer/table_include_image.html',
            'assets/recognizer/table_simple_cc.html',
            'assets/recognizer/table_include_rowspan_colspan.html',
            'assets/recognizer/table_involve_equation.html',
            'assets/recognizer/table_include_after_code.html',
            'assets/recognizer/table_involve_code.html',
            'assets/recognizer/table_involve_complex_code.html'

        ),
        'expected': [
            ('assets/recognizer/table_to_content_list_simple_res.json'),
            ('assets/recognizer/table_to_content_list_complex_res.json'),
            ('assets/recognizer/table_include_image_expcet.json'),
            ('assets/recognizer/table_include_code_expect.json')
        ],
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
            parts = self.rec.recognize(base_url, [(html_to_element(raw_html), html_to_element(raw_html))], raw_html)
            self.assertEqual(len(parts), 4)

    def test_not_involve_table(self):
        """不包含表格."""
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][1])
            base_url = test_case['input'][1]
            raw_html = raw_html_path.read_text(encoding='utf-8')
            parts = self.rec.recognize(base_url, [(html_to_element(raw_html), html_to_element(raw_html))], raw_html)
            self.assertEqual(len(parts), 1)

    def test_only_involve_table(self):
        """只包含表格的Html解析."""
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][2])
            base_url = test_case['input'][1]
            raw_html = raw_html_path.read_text()
            parts = self.rec.recognize(base_url, [(html_to_element(raw_html), html_to_element(raw_html))], raw_html)
            self.assertEqual(len(parts), 2)
            table_body = parts[1][0].text_content()
            assert table_body == '<table><tr><td><font>Mrs S Hindle</font></td></tr><tr><td><font>Show</font></td><td><font>CC</font></td><td><font>RCC</font></td></tr><tr><td><font>Driffield 5th October 2006</font></td><td><font>CH. Ricksbury Royal Hero</font></td><td><font>CH. Keyingham Branwell</font></td></tr><tr><td><font>Manchester 16th January 2008</font></td><td><font>CH. Lochbuie Geordie</font></td><td><font>Merryoth Maeve</font></td></tr><tr><td><font>Darlington 20th September 2009</font></td><td><font>CH. Maibee Make Believe</font></td><td><font>CH. Loranka Just Like Heaven JW</font></td></tr><tr><td><font>Blackpool 22nd June 2012</font></td><td><font>CH. Loranka Sherrie Baby</font></td><td><font>Dear Magic Touch De La Fi Au Songeur</font></td></tr><tr><td><font>Welsh Kennel Club 2014</font></td><td><font>Brymarden Carolina Sunrise</font></td><td><font>Ch. Wandris Evan Elp Us</font></td></tr><tr><td><font>Welsh Kennel Club 2014</font></td><td><font>Ch. Charnell Clematis of Salegreen</font></td><td><font>CH. Byermoor Queens Maid</font></td></tr></table>'

    def test_table_include_img_label(self):
        """table是否包含img标签."""
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][6])
            base_url = test_case['input'][1]
            raw_html = raw_html_path.read_text()
            parts = self.rec.recognize(base_url, [(html_to_element(raw_html), html_to_element(raw_html))], raw_html)
            assert len(parts) == 3
            simple_table_tag = parts[1][0].xpath(f'.//{CCTag.CC_TABLE}')[0]
            simple_table_type = simple_table_tag.attrib
            assert simple_table_type['table_type'] == 'simple'

    def test_cc_simple_table(self):
        """cc中简单表格."""
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][7])
            base_url = test_case['input'][8]
            raw_html = raw_html_path.read_text(encoding='utf-8')
            parts = self.rec.recognize(base_url, [(html_to_element(raw_html), html_to_element(raw_html))], raw_html)
            assert len(parts) == 3
            content = parts[1][0].text_content()
            assert content == '<table><tbody><tr><td><strong>Рейтинг:</strong></td><td><div>Рейтинг 5.00 из 5 на основе опроса 3 пользователей</div></td></tr><tr><td><strong>Тип товара:</strong></td><td><span>Препараты для омоложения</span></td></tr><tr><td><strong>Форма:</strong></td><td>Крем</td></tr><tr><td><strong>Объем:</strong></td><td>50 мл</td></tr><tr><td><strong>Рецепт:</strong></td><td>Отпускается без рецепта</td></tr><tr><td><strong>Способ хранения:</strong></td><td>Хранить при температуре 4-20°</td></tr><tr><td><strong>Примечание:</strong></td><td>Беречь от детей</td></tr><tr><td><strong>Оплата:</strong></td><td>Наличными/банковской картой</td></tr><tr><td><strong>Доступность в Северске:</strong></td><td>В наличии</td></tr><tr><td><strong>Доставка:</strong></td><td>2-7 Дней</td></tr><tr><td><strong>Цена:</strong></td><td><span>84 ₽</span></td></tr></tbody></table>'

    def test_cc_complex_table(self):
        """cc跨行跨列的表格."""
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][8])
            base_url = test_case['input'][8]
            raw_html = raw_html_path.read_text(encoding='utf-8')
            parts = self.rec.recognize(base_url, [(html_to_element(raw_html), html_to_element(raw_html))], raw_html)
            assert len(parts) == 3
            content = parts[1][0].text_content()
            assert content == '<table><caption>ফেব্রুয়ারি ২০২৪</caption><thead><tr><th>সোম</th><th>মঙ্গল</th><th>বুধ</th><th>বৃহ</th><th>শুক্র</th><th>শনি</th><th>রবি</th></tr></thead>\n\n<tfoot><tr><td colspan="3"><a>« জানুয়ারি</a></td><td></td><td colspan="3"></td></tr></tfoot>\n\n<tbody><tr><td colspan="3"></td><td><a>১</a></td><td><a>২</a></td><td><a>৩</a></td><td><a>৪</a></td></tr><tr><td><a>৫</a></td><td><a>৬</a></td><td><a>৭</a></td><td><a>৮</a></td><td><a>৯</a></td><td><a>১০</a></td><td><a>১১</a></td></tr><tr><td><a>১২</a></td><td><a>১৩</a></td><td><a>১৪</a></td><td><a>১৫</a></td><td><a>১৬</a></td><td><a>১৭</a></td><td><a>১৮</a></td></tr><tr><td><a>১৯</a></td><td><a>২০</a></td><td>২১</td><td>২২</td><td>২৩</td><td>২৪</td><td>২৫</td></tr><tr><td>২৬</td><td>২৭</td><td>২৮</td><td>২৯</td><td colspan="3"></td></tr></tbody></table>'
            table_type = parts[1][0].xpath(f'.//{CCTag.CC_TABLE}')[0]
            assert table_type.attrib['table_type'] == 'complex'

    def test_simple_complex_table(self):
        """包含简单和复杂table."""
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][3])
            base_url = test_case['input'][1]
            raw_html = raw_html_path.read_text(encoding='utf-8')
            parts = self.rec.recognize(base_url, [(html_to_element(raw_html), html_to_element(raw_html))], raw_html)
            simple_table_tag = parts[1][0].xpath(f'.//{CCTag.CC_TABLE}')[0]
            simple_table_type = simple_table_tag.attrib
            assert simple_table_type['table_type'] == 'simple'
            assert simple_table_type == {'table_type': 'simple', 'table_nest_level': '1', 'html': '<table>\n    <tr>\n        <td>1</td>\n        <td>2</td>\n    </tr>\n    <tr>\n        <td>3</td>\n        <td>4</td>\n    </tr>\n</table>'}
            complex_table_tag = parts[2][0].xpath(f'.//{CCTag.CC_TABLE}')[0]
            complex_table_type = complex_table_tag.attrib
            assert complex_table_type['table_type'] == 'complex'
            assert complex_table_type == {'table_type': 'complex', 'table_nest_level': '1', 'html': '<table>\n        <tr>\n            <td rowspan="2">1</td>\n            <td>2</td>\n            <td>3</td>\n        </tr>\n        <tr>\n            <td colspan="2">4</td>\n        </tr>\n        <tr>\n            <td>5</td>\n            <td>6</td>\n            <td>7</td>\n        </tr>\n    </table>'}

    def test_table_to_content_list_node_simple(self):
        """测试table的 to content list node方法."""
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][4])
            base_url = test_case['input'][1]
            raw_html = raw_html_path.read_text(encoding='utf-8')
            parsed_content = raw_html
            result = self.rec.to_content_list_node(base_url, html_to_element(parsed_content), raw_html)
            expect = base_dir.joinpath(test_case['expected'][0])
            expect_json = expect.read_text(encoding='utf-8')
            assert result['type'] == json.loads(expect_json)['type']
            assert result['content']['is_complex'] == json.loads(expect_json)['content']['is_complex']
            assert result['raw_content'] == json.loads(expect_json)['raw_content']
            self.assertTrue(result['content']['html'].startswith('<table>'))
            self.assertTrue(result['content']['html'].endswith('</table>'))

    def test_table_to_content_list_node_complex(self):
        """测试table的 complex table to content list node方法."""
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][5])
            expect_path = base_dir.joinpath(test_case['expected'][1])
            raw_html = raw_html_path.read_text(encoding='utf-8')
            result = self.rec.to_content_list_node(expect_path, html_to_element(raw_html), raw_html)
            fr = open(expect_path, 'r', encoding='utf-8')
            expect_result = json.loads(fr.read())
            assert result == expect_result

    def test_table_involve_equation(self):
        """involve equation table,待解决嵌套问题."""
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][9])
            base_url = 'https://en.m.wikipedia.org/wiki/Variance'
            raw_html = raw_html_path.read_text(encoding='utf-8')
            parts = self.rec.recognize(base_url, [(html_to_element(raw_html), html_to_element(raw_html))], raw_html)
            complex_table_tag = parts[1][0].xpath(f'.//{CCTag.CC_TABLE}')
            assert complex_table_tag[0].text == '<table><tbody><tr><th>Name of the probability distribution</th><th>Probability distribution function</th><th>Mean</th><th>Variance</th></tr><tr><td><a>Binomial distribution</a></td><td><span>${\\displaystyle \\Pr \\,(X=k)={\\binom {n}{k}}p^{k}(1-p)^{n-k}}$ \n\n</span></td><td><span>${\\displaystyle np}$ \n\n</span></td><th><span>${\\displaystyle np(1-p)}$ \n\n</span></th></tr><tr><td><a>Geometric distribution</a></td><td><span>${\\displaystyle \\Pr \\,(X=k)=(1-p)^{k-1}p}$ \n\n</span></td><td><span>${\\displaystyle {\\frac {1}{p}}}$ \n\n</span></td><th><span>${\\displaystyle {\\frac {(1-p)}{p^{2}}}}$ \n\n</span></th></tr><tr><td><a>Normal distribution</a></td><td><span>${\\displaystyle f\\left(x\\mid \\mu ,\\sigma ^{2}\\right)={\\frac {1}{\\sqrt {2\\pi \\sigma ^{2}}}}e^{-{\\frac {(x-\\mu )^{2}}{2\\sigma ^{2}}}}}$ \n\n</span></td><td><span>${\\displaystyle \\mu }$ \n\n</span></td><th><span>${\\displaystyle \\sigma ^{2}}$ \n\n</span></th></tr><tr><td><a>Uniform distribution (continuous)</a></td><td><span>${\\displaystyle f(x\\mid a,b)={\\begin{cases}{\\frac {1}{b-a}}&{\\text{for }}a\\leq x\\leq b,\\\\[3pt]0&{\\text{for }}x<a{\\text{ or }}x>b\\end{cases}}}$ \n\n</span></td><td><span>${\\displaystyle {\\frac {a+b}{2}}}$ \n\n</span></td><th><span>${\\displaystyle {\\frac {(b-a)^{2}}{12}}}$ \n\n</span></th></tr><tr><td><a>Exponential distribution</a></td><td><span>${\\displaystyle f(x\\mid \\lambda )=\\lambda e^{-\\lambda x}}$ \n\n</span></td><td><span>${\\displaystyle {\\frac {1}{\\lambda }}}$ \n\n</span></td><th><span>${\\displaystyle {\\frac {1}{\\lambda ^{2}}}}$ \n\n</span></th></tr><tr><td><a>Poisson distribution</a></td><td><span>${\\displaystyle f(k\\mid \\lambda )={\\frac {e^{-\\lambda }\\lambda ^{k}}{k!}}}$ \n\n</span></td><td><span>${\\displaystyle \\lambda }$ \n\n</span></td><th><span>${\\displaystyle \\lambda }$ \n\n</span></th></tr></tbody></table>'
            parts = self.rec.recognize(base_url, [(html_to_element(raw_html), html_to_element(raw_html))], raw_html)
            complex_table_tag = parts[1][0].xpath(f'.//{CCTag.CC_TABLE}')
            assert complex_table_tag[0].text == '<table><tbody><tr><th>Name of the probability distribution</th><th>Probability distribution function</th><th>Mean</th><th>Variance</th></tr><tr><td><a>Binomial distribution</a></td><td><span>${\\displaystyle \\Pr \\,(X=k)={\\binom {n}{k}}p^{k}(1-p)^{n-k}}$ \n\n</span></td><td><span>${\\displaystyle np}$ \n\n</span></td><th><span>${\\displaystyle np(1-p)}$ \n\n</span></th></tr><tr><td><a>Geometric distribution</a></td><td><span>${\\displaystyle \\Pr \\,(X=k)=(1-p)^{k-1}p}$ \n\n</span></td><td><span>${\\displaystyle {\\frac {1}{p}}}$ \n\n</span></td><th><span>${\\displaystyle {\\frac {(1-p)}{p^{2}}}}$ \n\n</span></th></tr><tr><td><a>Normal distribution</a></td><td><span>${\\displaystyle f\\left(x\\mid \\mu ,\\sigma ^{2}\\right)={\\frac {1}{\\sqrt {2\\pi \\sigma ^{2}}}}e^{-{\\frac {(x-\\mu )^{2}}{2\\sigma ^{2}}}}}$ \n\n</span></td><td><span>${\\displaystyle \\mu }$ \n\n</span></td><th><span>${\\displaystyle \\sigma ^{2}}$ \n\n</span></th></tr><tr><td><a>Uniform distribution (continuous)</a></td><td><span>${\\displaystyle f(x\\mid a,b)={\\begin{cases}{\\frac {1}{b-a}}&{\\text{for }}a\\leq x\\leq b,\\\\[3pt]0&{\\text{for }}x<a{\\text{ or }}x>b\\end{cases}}}$ \n\n</span></td><td><span>${\\displaystyle {\\frac {a+b}{2}}}$ \n\n</span></td><th><span>${\\displaystyle {\\frac {(b-a)^{2}}{12}}}$ \n\n</span></th></tr><tr><td><a>Exponential distribution</a></td><td><span>${\\displaystyle f(x\\mid \\lambda )=\\lambda e^{-\\lambda x}}$ \n\n</span></td><td><span>${\\displaystyle {\\frac {1}{\\lambda }}}$ \n\n</span></td><th><span>${\\displaystyle {\\frac {1}{\\lambda ^{2}}}}$ \n\n</span></th></tr><tr><td><a>Poisson distribution</a></td><td><span>${\\displaystyle f(k\\mid \\lambda )={\\frac {e^{-\\lambda }\\lambda ^{k}}{k!}}}$ \n\n</span></td><td><span>${\\displaystyle \\lambda }$ \n\n</span></td><th><span>${\\displaystyle \\lambda }$ \n\n</span></th></tr></tbody></table>'

    def test_table_involve_after_code(self):
        """test table involve code, code被提取出去了，过滤掉空的和坏的table."""
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][10])
            base_url = 'https://en.m.wikipedia.org/wiki/Variance'
            raw_html = raw_html_path.read_text(encoding='utf-8')
            parts = self.rec.recognize(base_url, [(html_to_element(raw_html), html_to_element(raw_html))], raw_html)
            assert len(parts[0][0].xpath(f'.//{CCTag.CC_TABLE}')[0]) == 0

    @unittest.skip(reason='在code模块解决了table嵌套多行代码问题')
    def test_table_involve_code(self):
        """table involve code."""
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][11])
            base_url = 'https://en.m.wikipedia.org/wiki/Variance'
            raw_html = raw_html_path.read_text(encoding='utf-8')
            parts = self.rec.recognize(base_url, [(html_to_element(raw_html), html_to_element(raw_html))], raw_html)
            complex_table_tag = parts[1][0].xpath(f'.//{CCTag.CC_TABLE}')
            expect_path = base_dir.joinpath(test_case['expected'][3])
            content = open(expect_path, 'r', encoding='utf-8').read()
            assert complex_table_tag[0].text == content.strip('\n')

    @unittest.skip(reason='在code模块解决了这个问题')
    def test_table_involve_complex_code(self):
        """table involve complex code."""
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][12])
            base_url = 'https://en.m.wikipedia.org/wiki/Variance'
            raw_html = raw_html_path.read_text(encoding='utf-8')
            parts = self.rec.recognize(base_url, [(html_to_element(raw_html), html_to_element(raw_html))], raw_html)
            complex_table_tag = parts[1][0].xpath(f'.//{CCTag.CC_TABLE}')
            expect_path = base_dir.joinpath(test_case['expected'][3])
            content = open(expect_path, 'r', encoding='utf-8').read()
            assert complex_table_tag[0].text == content.strip('\n')

    def test_nested_table1(self):
        """复杂嵌套表格."""
        raw_html_path = base_dir.joinpath('assets/recognizer/nested_table1.html')
        base_url = 'https://en.m.wikipedia.org/wiki/Variance'
        raw_html = raw_html_path.read_text(encoding='utf-8')
        parts = self.rec.recognize(base_url, [(html_to_element(raw_html), html_to_element(raw_html))], raw_html)
        assert len(parts) == 3
        content = parts[2][0].text_content()
        assert '<table><tr><td><form><table><tr><td><table><tr><td><label>Search APO</label></td></tr><tr><td><input><input>\n\n<br><a>Advanced Search</a></td></tr></table></td></tr></table></form>\n\n<table><tr><td><img></td>\n\n<td><a>Home</a></td></tr>\n\n<tr><td colspan="2"></td></tr>\n\n<tr><td colspan="2">Browse</td></tr>\n\n<tr><td><img></td><td><a>Communities \n\n & Collections</a></td></tr>\n\n<tr><td><img></td><td><a>Issue Date</a></td></tr>\n\n<tr><td><img></td><td><a>Author</a></td></tr>\n\n<tr><td><img></td><td><a>Title</a></td></tr>\n\n<tr><td><img></td><td><a>Subject</a></td></tr>\n\n<tr><td colspan="2"></td></tr>\n\n<tr><td colspan="2">Sign on to:</td></tr>\n\n<tr><td><img></td><td><a>Receive email \n\n updates</a></td></tr>\n\n<tr><td><img></td><td><a>My APO</a>\n\n<br><small>authorized users</small></td></tr>\n\n<tr><td><img></td><td><a>Edit Profile</a></td></tr>\n\n<tr><td colspan="2"></td></tr>\n\n<tr><td><img></td><td><script><!-- Javascript starts here\ndocument.write(\'<a href="#" onClick="var popupwin = window.open(\\\'/dspace/help/index.html\\\',\\\'dspacepopup\\\',\\\'height=600,width=550,resizable,scrollbars\\\');popupwin.focus();return false;">Help<\\/a>\');\n// --></script><noscript>Help</noscript></td></tr>\n\n<tr><td><img></td><td><a>About DSpace</a></td></tr></table>\n\n</td>\n\n<td><p>ANSTO Publications Online > \n\n Journal Publications > \n\n Journal Articles ></p><table><tr><td><strong>Please use this identifier to cite or link to this item: http://apo.ansto.gov.au/dspace/handle/10238/2935</strong></td>\n\n</tr></table>\n\n<br><center><table><tr><td>Title:</td><td>An investigation into transition metal ion binding properties of silk fibers and particles using radioisotopes.</td></tr><tr><td>Authors:</td><td><a>Rajkhowa, R</a>\n\n<br><a>Naik, R</a>\n\n<br><a>Wang, L</a>\n\n<br><a>Smith, SV</a>\n\n<br><a>Wang, X</a></td></tr><tr><td>Keywords:</td><td>Radioisotopes \n\n Transition Elements<br>\n\nBinding Energy<br>\n\nFibers<br>\n\nAbsorption<br>\n\nIons<br></td></tr><tr><td>Issue Date:</td><td>15-Mar-2011</td></tr><tr><td>Publisher:</td><td>Wiley-Blackwell</td></tr><tr><td>Citation:</td>' in content

    def test_nested_table2(self):
        """复杂嵌套表格."""
        raw_html_path = base_dir.joinpath('assets/recognizer/nested_table2.html')
        base_url = 'https://en.m.wikipedia.org/wiki/Variance'
        raw_html = raw_html_path.read_text(encoding='utf-8')
        parts = self.rec.recognize(base_url, [(html_to_element(raw_html), html_to_element(raw_html))], raw_html)
        assert len(parts) == 2
        content = parts[1][0].text_content()
        assert '<table><tr><td colspan="2"><div>jQuery(document).ready( function($) { if ($(\'#gateway-page\').length) { jQuery("body").addClass("fontyourface layout-one-sidebar layout-sidebar-first wide hff-43 pff-43 sff-43 slff-43 fixed-header-enabled slideout-side-right transparent-header-active path-node page-node-type-page"); }}); \n\n .acalog-custom .region--light-typography.region--dark-background a {font-weight:normal;} .acalog-custom ul.icons-list {margin:0} .acalog-custom ul.icons-list li {margin:5px 12px 5px 0;} #gateway-footer-copyright {background:#f6f8f9; font-family:\'Libre Franklin\', Helvetica Neue, Arial, sans-serif; padding:20px;} \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag(\'js\', new Date()); gtag(\'config\', \'G-L4J2WT8RM8\'); \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n Main Numbers: \n\n (615) 452-8600 \n\n (888) 335-8722 \n\n \n\n \n\n \n\n \n\n  facebook \n\n  instagram \n\n  twitter \n\n  youtube \n\n \n\n \n\n \n\n \n\n Campuses \n\n \n\n Gallatin \n\n Cookeville \n\n Livingston \n\n Springfield \n\n \n\n \n\n \n\n \n\n \n\n Academic Divisions \n\n \n\n Business & Technology \n\n Health Sciences \n\n Humanities & Fine Arts \n\n Mathematics & Science \n\n Nursing \n\n Social Science & Education \n\n \n\n \n\n \n\n \n\n \n\n Resources \n\n \n\n Accreditation \n\n Bookstore \n\n Campus Police \n\n Contact Us \n\n Employee Directory \n\n IT Help Desk \n\n Library \n\n Marketing & Communications</div></td></tr><tr><td></td><td><span>Volunteer State Community College</span></td></tr><tr><td></td><td><table><tr><td></td><td><span>May 24, 2024</span></td><td></td><td><table><tr><td><span>2013-2014 VSCC Catalog</span></td><td><form><table><tr><td><div>Select a Catalog \n\n 2024-2025 Undergraduate Catalog \n\n 2023-2024 Undergraduate Catalog [ARCHIVED CATALOG] \n\n 2022-2023' in content

    def test_nested_table3(self):
        """复杂嵌套表格."""
        raw_html_path = base_dir.joinpath('assets/recognizer/nested_table3.html')
        base_url = 'https://en.m.wikipedia.org/wiki/Variance'
        raw_html = raw_html_path.read_text(encoding='utf-8')
        parts = self.rec.recognize(base_url, [(html_to_element(raw_html), html_to_element(raw_html))], raw_html)
        assert len(parts) == 3
        content = parts[2][0].text_content()
        assert "<table><tr><td><table><tr><td><div>What's New - Recent Content \n\n \n\n Members' Peak Updates \n\n Recent Trip Reports \n\n Recent Trip Report Comments \n\n Recently added Images \n\n Recently added Peaks \n\n List Completers \n\n \n\n Height List Completers \n\n Elevation List Completers \n\n County Summit Completers \n\n Wilderness Area Completers \n\n Member Profiles & Stats \n\n \n\n Member Profiles - Summary Stats \n\n Member Stats by Date Range & Charts \n\n Calendar Grid Completions \n\n Peaks Repeated \n\n Most Climbed Peaks \n\n Unclimbed Peaks \n\n US Peak Totals by State \n\n Member Tools \n\n \n\n Closest 50 Peaks by Member \n\n \n\n Closest 50 Map \n\n Closest 50 List \n\n Download your Peak List \n\n Search Trip Reports \n\n Unclimbed by Custom Group \n\n Export CSV, GPX, POI, TOPO! Files \n\n Elevation Threshold Progress Maps \n\n State Highest # Progress Maps \n\n County Summit Progress Maps \n\n Statewide County Summit Maps \n\n Prominence Progress Maps \n\n State Quads Progress Maps \n\n Quadrangle Lookup \n\n Distance Calculator \n\n Slope Angle Calculator \n\n Stats Category Leaders \n\n US Highest 1,000 Peaks \n\n \n\n US Highest 1,000 Member Area \n\n 1,000 Highest Peak List \n\n US Steepest 1,000 Peaks \n\n \n\n Steepness Member Area \n\n View 1,000 Steepest List \n\n US 2,000' Prominence \n\n \n\n US Prominence Member Area \n\n View US Prominence Peak Profiles \n\n View Member 5k Completion Maps \n\n Prominence Progress Maps \n\n US County Highpoints \n\n \n\n County Highpoints Member Area \n\n Highpoint Profiles - By State \n\n View Member's Completion Maps \n\n US State Highpoints \n\n \n\n US State Highpoints Member Area \n\n View State Highpoints List \n\n View Member's Completion Maps \n\n US Wilderness Area Peaks \n\n \n\n Wilderness Summits Member Area \n\n Wilderness Area Detail by State \n\n Wilderness HPs Member Area \n\n US National Park Peaks \n\n \n\n National Park Peaks Member Area \n\n National Park Peaks Detail by State" in content

    def test_nested_table4(self):
        """复杂嵌套表格."""
        raw_html_path = base_dir.joinpath('assets/recognizer/nested_table4.html')
        base_url = 'https://en.m.wikipedia.org/wiki/Variance'
        raw_html = raw_html_path.read_text(encoding='utf-8')
        parts = self.rec.recognize(base_url, [(html_to_element(raw_html), html_to_element(raw_html))], raw_html)
        assert len(parts) == 4
        content = parts[2][0].text_content()
        assert '<table><tr><td><h1>Molecular line emissions from pre main sequence objects</h1><div><div></div><div></div><div></div><div><p>Saraceno, P. ; Benedettini, M. ; Caux, E. ; Ceccarelli, M. C. ; Clegg, P. E. ; Correia, J. C. ; di Giorgio, A. M. ; Giannini, T. ; Griffin, M. J. ; Leeks, S. J. ; Liseau, R. ; Lorenzetti, D. ; Molinari, S. ; Nisini, B. ; Smith, H. ; Spinoglio, L. ; Tomassi, E. and White, G. J. (1997). \n\n Molecular line emissions from pre main sequence objects. \n\n In: The first ISO workshop on Analytical Spectroscopy , 6-8 October 1997, Madrid, Spain, p. 291. \n\n Full text available as:</p><table><tr><td><a></a><div><table><tr><td><img><div>Preview</div></td></tr></table></div>\n\n</td><td><span>PDF (Version of Record) - Requires a PDF viewer such as</span><a>GSview ,</a><a>Xpdf or</a><a>Adobe Acrobat Reader</a>\n\n<br><a>Download (239Kb)</a><ul></ul></td></tr>\n\n</table>\n\n<table><tr><th>URL:</th><td><a>http://cdsads.u-strasbg.fr/abs/1997ESASP.419..291S</a></td></tr>\n\n<tr><th>Google Scholar:</th><td><a>Look up in Google Scholar</a></td></tr></table>\n\n<h2>Abstract</h2><p>We present some preliminary results obtained with the LWS G.T. programme on the study of young objects driving molecular outflows. In particular, we discuss the importance of molecular emission in these sources and address the role of the H <sub>2</sub> 0 cooling.</p><table><tr><th>Item Type:</th><td>Conference Item</td></tr>\n\n<tr><th>Copyright Holders:</th><td>1997 European Space Agency</td></tr>\n\n<tr><th>Extra Information:</th><td>Proceedings of the first ISO workshop on Analytical Spectroscopy, Madrid, Spain, 6-8 October 1997. Editors: A.M. Heras, K. Leech, N. R. Trams, and Michael Perry. Noordwijk, The Netherlands : ESA Publications Division, c1997. (ESA SP-419), 1997., pp.291-292</td></tr>\n\n<tr><th>Academic Unit/Department:</th><td><a>Science > Physical Sciences</a></td></tr>\n\n<tr><th>Interdisciplinary Research Centre:</th><td><a>Centre for Earth, Planetary, Space and Astronomical Research (CEPSAR)</a></td></tr>\n\n<tr><th>Item ID:</th><td>32696</td></tr>\n\n<tr><th>Depositing User:</th><td><span>Glenn White</span></td></tr>\n\n<tr>' in content
