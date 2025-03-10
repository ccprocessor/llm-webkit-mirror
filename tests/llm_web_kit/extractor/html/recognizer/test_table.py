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
            parts = self.rec.recognize(base_url, [(raw_html, raw_html)], raw_html)
            self.assertEqual(len(parts), 4)

    def test_not_involve_table(self):
        """不包含表格."""
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][1])
            base_url = test_case['input'][1]
            raw_html = raw_html_path.read_text(encoding='utf-8')
            parts = self.rec.recognize(base_url, [(raw_html, raw_html)], raw_html)
            self.assertEqual(len(parts), 1)

    def test_only_involve_table(self):
        """只包含表格的Html解析."""
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][2])
            base_url = test_case['input'][1]
            raw_html = raw_html_path.read_text()
            parts = self.rec.recognize(base_url, [(raw_html, raw_html)], raw_html)
            self.assertEqual(len(parts), 2)
            table_body = html_to_element(parts[1][0]).text_content()
            assert table_body == r'<table><tr><td>Mrs S Hindle</td></tr><tr><td>Show</td><td>CC</td><td>RCC</td></tr><tr><td>Driffield 5th October 2006</td><td>CH. Ricksbury Royal Hero</td><td>CH. Keyingham Branwell</td></tr><tr><td>Manchester 16th January 2008</td><td>CH. Lochbuie Geordie</td><td>Merryoth Maeve</td></tr><tr><td>Darlington 20th September 2009</td><td>CH. Maibee Make Believe</td><td>CH. Loranka Just Like Heaven JW</td></tr><tr><td>Blackpool 22nd June 2012</td><td>CH. Loranka Sherrie Baby</td><td>Dear Magic Touch De La Fi Au Songeur</td></tr><tr><td>Welsh Kennel Club 2014</td><td>Brymarden Carolina Sunrise</td><td>Ch. Wandris Evan Elp Us</td></tr><tr><td>Welsh Kennel Club 2014</td><td>Ch. Charnell Clematis of Salegreen</td><td>CH. Byermoor Queens Maid</td></tr></table>'

    def test_table_include_img_label(self):
        """table是否包含img标签."""
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][6])
            base_url = test_case['input'][1]
            raw_html = raw_html_path.read_text()
            parts = self.rec.recognize(base_url, [(raw_html, raw_html)], raw_html)
            assert len(parts) == 3
            simple_table_tag = html_to_element(parts[1][0]).xpath(f'.//{CCTag.CC_TABLE}')[0]
            simple_table_type = simple_table_tag.attrib
            assert simple_table_type['table_type'] == 'simple'

    def test_cc_simple_table(self):
        """cc中简单表格."""
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][7])
            base_url = test_case['input'][8]
            raw_html = raw_html_path.read_text(encoding='utf-8')
            parts = self.rec.recognize(base_url, [(raw_html, raw_html)], raw_html)
            assert len(parts) == 3
            content = html_to_element(parts[1][0]).text_content()
            assert content == r'<table><tbody><tr><td>Рейтинг:</td><td>Рейтинг 5.00 из 5 на основе опроса 3 пользователей</td></tr><tr><td>Тип товара:</td><td>Препараты для омоложения</td></tr><tr><td>Форма:</td><td>Крем</td></tr><tr><td>Объем:</td><td>50 мл</td></tr><tr><td>Рецепт:</td><td>Отпускается без рецепта</td></tr><tr><td>Способ хранения:</td><td>Хранить при температуре 4-20°</td></tr><tr><td>Примечание:</td><td>Беречь от детей</td></tr><tr><td>Оплата:</td><td>Наличными/банковской картой</td></tr><tr><td>Доступность в Северске:</td><td>В наличии</td></tr><tr><td>Доставка:</td><td>2-7 Дней</td></tr><tr><td>Цена:</td><td>84 ₽</td></tr></tbody></table>'

    def test_cc_complex_table(self):
        """cc跨行跨列的表格."""
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][8])
            base_url = test_case['input'][8]
            raw_html = raw_html_path.read_text(encoding='utf-8')
            parts = self.rec.recognize(base_url, [(raw_html, raw_html)], raw_html)
            assert len(parts) == 3
            content = html_to_element(parts[1][0]).text_content()
            assert content == r'<table><caption>ফেব্রুয়ারি ২০২৪</caption><thead><tr><th>সোম</th><th>মঙ্গল</th><th>বুধ</th><th>বৃহ</th><th>শুক্র</th><th>শনি</th><th>রবি</th></tr></thead><tfoot><tr><td colspan="3">« জানুয়ারি</td><td></td><td colspan="3"></td></tr></tfoot><tbody><tr><td colspan="3"></td><td>১</td><td>২</td><td>৩</td><td>৪</td></tr><tr><td>৫</td><td>৬</td><td>৭</td><td>৮</td><td>৯</td><td>১০</td><td>১১</td></tr><tr><td>১২</td><td>১৩</td><td>১৪</td><td>১৫</td><td>১৬</td><td>১৭</td><td>১৮</td></tr><tr><td>১৯</td><td>২০</td><td>২১</td><td>২২</td><td>২৩</td><td>২৪</td><td>২৫</td></tr><tr><td>২৬</td><td>২৭</td><td>২৮</td><td>২৯</td><td colspan="3"></td></tr></tbody></table>'
            table_type = html_to_element(parts[1][0]).xpath(f'.//{CCTag.CC_TABLE}')[0]
            assert table_type.attrib['table_type'] == 'complex'

    def test_simple_complex_table(self):
        """包含简单和复杂table."""
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][3])
            base_url = test_case['input'][1]
            raw_html = raw_html_path.read_text(encoding='utf-8')
            parts = self.rec.recognize(base_url, [(raw_html, raw_html)], raw_html)
            simple_table_tag = html_to_element(parts[1][0]).xpath(f'.//{CCTag.CC_TABLE}')[0]
            simple_table_type = simple_table_tag.attrib
            assert simple_table_type['table_type'] == 'simple'
            assert simple_table_type == {'table_type': 'simple', 'table_nest_level': '1', 'html': '<table>\n    <tr>\n        <td>1</td>\n        <td>2</td>\n    </tr>\n    <tr>\n        <td>3</td>\n        <td>4</td>\n    </tr>\n</table>\n\n'}
            complex_table_tag = html_to_element(parts[2][0]).xpath(f'.//{CCTag.CC_TABLE}')[0]
            complex_table_type = complex_table_tag.attrib
            assert complex_table_type['table_type'] == 'complex'
            assert complex_table_type == {'table_type': 'complex', 'table_nest_level': '1', 'html': '<table>\n        <tr>\n            <td rowspan="2">1</td>\n            <td>2</td>\n            <td>3</td>\n        </tr>\n        <tr>\n            <td colspan="2">4</td>\n        </tr>\n        <tr>\n            <td>5</td>\n            <td>6</td>\n            <td>7</td>\n        </tr>\n    </table>\n    '}

    def test_table_to_content_list_node_simple(self):
        """测试table的 to content list node方法."""
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][4])
            base_url = test_case['input'][1]
            raw_html = raw_html_path.read_text(encoding='utf-8')
            parsed_content = raw_html
            result = self.rec.to_content_list_node(base_url, parsed_content, raw_html)
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
            result = self.rec.to_content_list_node(expect_path, raw_html, raw_html)
            fr = open(expect_path, 'r', encoding='utf-8')
            expect_result = json.loads(fr.read())
            assert result == expect_result

    def test_table_involve_equation(self):
        """involve equation table,待解决嵌套问题."""
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][9])
            base_url = 'https://en.m.wikipedia.org/wiki/Variance'
            raw_html = raw_html_path.read_text(encoding='utf-8')
            parts = self.rec.recognize(base_url, [(raw_html, raw_html)], raw_html)
            complex_table_tag = html_to_element(parts[1][0]).xpath(f'.//{CCTag.CC_TABLE}')
            assert complex_table_tag[0].text == r'<table><tbody><tr><th>Name of the probability distribution</th><th>Probability distribution function</th><th>Mean</th><th>Variance</th></tr><tr><td>Binomial distribution</td><td>${\displaystyle \Pr \,(X=k)={\binom {n}{k}}p^{k}(1-p)^{n-k}}$</td><td>${\displaystyle np}$</td><th>${\displaystyle np(1-p)}$</th></tr><tr><td>Geometric distribution</td><td>${\displaystyle \Pr \,(X=k)=(1-p)^{k-1}p}$</td><td>${\displaystyle {\frac {1}{p}}}$</td><th>${\displaystyle {\frac {(1-p)}{p^{2}}}}$</th></tr><tr><td>Normal distribution</td><td>${\displaystyle f\left(x\mid \mu ,\sigma ^{2}\right)={\frac {1}{\sqrt {2\pi \sigma ^{2}}}}e^{-{\frac {(x-\mu )^{2}}{2\sigma ^{2}}}}}$</td><td>${\displaystyle \mu }$</td><th>${\displaystyle \sigma ^{2}}$</th></tr><tr><td>Uniform distribution (continuous)</td><td>${\displaystyle f(x\mid a,b)={\begin{cases}{\frac {1}{b-a}}&amp;{\text{for }}a\leq x\leq b,\\[3pt]0&amp;{\text{for }}x&lt;a{\text{ or }}x&gt;b\end{cases}}}$</td><td>${\displaystyle {\frac {a+b}{2}}}$</td><th>${\displaystyle {\frac {(b-a)^{2}}{12}}}$</th></tr><tr><td>Exponential distribution</td><td>${\displaystyle f(x\mid \lambda )=\lambda e^{-\lambda x}}$</td><td>${\displaystyle {\frac {1}{\lambda }}}$</td><th>${\displaystyle {\frac {1}{\lambda ^{2}}}}$</th></tr><tr><td>Poisson distribution</td><td>${\displaystyle f(k\mid \lambda )={\frac {e^{-\lambda }\lambda ^{k}}{k!}}}$</td><td>${\displaystyle \lambda }$</td><th>${\displaystyle \lambda }$</th></tr></tbody></table>'

    def test_table_involve_after_code(self):
        """test table involve code, code被提取出去了，过滤掉空的和坏的table."""
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][10])
            base_url = 'https://en.m.wikipedia.org/wiki/Variance'
            raw_html = raw_html_path.read_text(encoding='utf-8')
            parts = self.rec.recognize(base_url, [(raw_html, raw_html)], raw_html)
            assert html_to_element(parts[0][0]).xpath(f'.//{CCTag.CC_TABLE}')[0].text is None

    @unittest.skip(reason='在code模块解决了table嵌套多行代码问题')
    def test_table_involve_code(self):
        """table involve code."""
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][11])
            base_url = 'https://en.m.wikipedia.org/wiki/Variance'
            raw_html = raw_html_path.read_text(encoding='utf-8')
            parts = self.rec.recognize(base_url, [(raw_html, raw_html)], raw_html)
            complex_table_tag = html_to_element(parts[1][0]).xpath(f'.//{CCTag.CC_TABLE}')
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
            parts = self.rec.recognize(base_url, [(raw_html, raw_html)], raw_html)
            complex_table_tag = html_to_element(parts[1][0]).xpath(f'.//{CCTag.CC_TABLE}')
            expect_path = base_dir.joinpath(test_case['expected'][3])
            content = open(expect_path, 'r', encoding='utf-8').read()
            assert complex_table_tag[0].text == content.strip('\n')
