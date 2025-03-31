"""
测试extractor_chain.py， 集成测试：
测试方法是：
1. 设定一个场景：从一些散落的html中提取content_list
2. 定义extractor_pipe的config配置文件，定义chain的执行顺序和模块，数据路径
3. 准备一些html文件，按照零散html的输入标准组织成jsonl数据
4. 执行解析，得到content_list，并比对期望结果

测试需要涵盖：
1. 正确提取时候的content_list是否符合期望
2. 各类异常的抛出是否符合期望
"""
import json
import os
import unittest

from lxml import html

from llm_web_kit.config.cfg_reader import load_pipe_tpl
from llm_web_kit.extractor.extractor_chain import ExtractSimpleFactory
from llm_web_kit.extractor.html.recognizer.cc_math.common import MathType
from llm_web_kit.input.datajson import DataJson
from llm_web_kit.libs.doc_element_type import DocElementType, ParagraphTextType


def normalize_html(html_string:str) -> str:
    # 解析 HTML
    tree = html.fromstring(html_string)
    # 转换为字符串并去除空白
    return html.tostring(tree, pretty_print=True, encoding='utf-8').strip()


class TestExtractorChain(unittest.TestCase):
    """Test extractor suit with HTML data."""

    def setUp(self):
        """Set up test fixtures."""
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.html_data_path = os.path.join(self.base_path, 'assets/extractor_chain_input/good_data/html_data_input.jsonl')
        self.md_output_file_path = os.path.join(self.base_path, 'assets/extractor_chain_input/good_data/output_expected/1.md')
        self.txt_output_file_path = os.path.join(self.base_path, 'assets/extractor_chain_input/good_data/output_expected/1.txt')
        self.main_html_output_file_path = os.path.join(
            self.base_path, 'assets/extractor_chain_input/good_data/output_expected/1.main_html.html'
        )
        self.csdn_lineno_output_file_path = os.path.join(
            self.base_path, 'assets/extractor_chain_input/good_data/output_expected/csdn_lineno.md'
        )
        self.oracle_doc_main_html_path = os.path.join(
            self.base_path, 'assets/extractor_chain_input/good_data/output_expected/oracle_doc.main_html.html'
        )

        self.md_expected_content = open(self.md_output_file_path, 'r').read()
        self.txt_expected_content = open(self.txt_output_file_path, 'r').read()
        self.main_html_expected_content = open(self.main_html_output_file_path, 'r').read()
        self.csdn_lineno_expected_content = open(self.csdn_lineno_output_file_path, 'r').read()
        self.oracle_doc_main_html_content = open(self.oracle_doc_main_html_path, 'r').read()

        self.data_json = []
        with open(self.html_data_path, 'r') as f:
            for line in f:
                self.data_json.append(json.loads(line.strip()))

        assert len(self.data_json) == 39

        # Config for HTML extraction
        self.config = load_pipe_tpl('html-test')

    def test_html_pipeline(self):
        """Test HTML extractor with sample data."""
        # Initialize extractor
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[0]
        # Create DataJson from test data
        input_data = DataJson(test_data)

        # Test extraction
        result = chain.extract(input_data)

        # Verify basic properties
        self.assertEqual(result.get_dataset_name(), 'test_pipeline_suit')
        self.assertEqual(result.get_file_format(), 'HTML')
        self.assertEqual(result['track_id'], 'f7b3b1b4-0b1b')

        html_content_list = result.get_content_list()[0]
        # Verify content_list
        self.assertEqual(result.get_content_list().length(), 1)
        html_content = html_content_list[0]
        # 首先是h1
        self.assertEqual(html_content['type'], DocElementType.TITLE)
        self.assertEqual(html_content['content']['level'], '1')
        self.assertEqual(html_content['content']['title_content'], 'Heading 1')
        # 然后是p
        html_content = html_content_list[1]
        self.assertEqual(html_content['type'], DocElementType.PARAGRAPH)
        self.assertEqual(html_content['content'][0]['c'], 'Paragraph 1')
        self.assertEqual(html_content['content'][0]['t'], ParagraphTextType.TEXT)
        # 然后是img
        html_content = html_content_list[2]
        self.assertEqual(html_content['type'], DocElementType.IMAGE)
        self.assertEqual(html_content['content']['title'], 'image-title')
        self.assertEqual(html_content['content']['alt'], 'image-alt')
        self.assertEqual(html_content['content']['url'], 'https://www.test.com/test.png')
        self.assertEqual(html_content['content']['caption'], None)

        # 然后是simple table
        html_content = html_content_list[4]
        self.assertEqual(html_content['type'], DocElementType.SIMPLE_TABLE)
        self.assertEqual(html_content['content']['is_complex'], False)
        assert html_content['content']['html'].startswith('<table')

        # 然后是complex table
        html_content = html_content_list[5]
        self.assertEqual(html_content['type'], DocElementType.COMPLEX_TABLE)
        self.assertEqual(html_content['content']['is_complex'], True)

        # 然后是list
        html_content = html_content_list[6]
        self.assertEqual(html_content['type'], DocElementType.LIST)
        self.assertEqual(len(html_content['content']['items']), 2)
        self.assertEqual(html_content['content']['ordered'], False)
        self.assertEqual(html_content['content']['items'][0][0][0]['c'], '1')
        self.assertEqual(html_content['content']['items'][0][0][0]['t'], ParagraphTextType.TEXT)
        self.assertEqual(html_content['content']['items'][1][0][0]['c'], '2')
        self.assertEqual(html_content['content']['items'][1][0][0]['t'], ParagraphTextType.TEXT)

        # 嵌套list
        html_content = html_content_list[7]
        self.assertEqual(html_content['type'], DocElementType.LIST)
        self.assertEqual(len(html_content['content']['items']), 2)
        self.assertEqual(len(html_content['content']['items'][0][0]), 3)
        self.assertEqual(html_content['content']['items'][0][0][1]['c'], '1.1')
        self.assertEqual(html_content['content']['items'][0][0][1]['t'], ParagraphTextType.TEXT)
        self.assertEqual(html_content['content']['items'][1][0][1]['c'], '2.1')
        self.assertEqual(html_content['content']['items'][1][0][1]['t'], ParagraphTextType.TEXT)

        # 行间公式
        html_content = html_content_list[8]
        self.assertEqual(html_content['type'], DocElementType.EQUATION_INTERLINE)
        self.assertEqual(html_content['content']['math_content'], 'x=\\frac{-b±\\sqrt{{b}^{2}-4ac}}{2a}\\text{.}')
        self.assertEqual(html_content['content']['math_type'], MathType.MATHML)

        # 代码
        html_content = html_content_list[9]
        self.assertEqual(html_content['type'], DocElementType.CODE)
        self.assertEqual(len(html_content['content']['code_content']), 251)
        self.assertEqual(html_content['content']['by'], 'tag_pre_code')
        self.assertEqual(html_content['inline'], False)

        # 有序列表
        html_content = html_content_list[10]
        self.assertEqual(html_content['type'], DocElementType.LIST)
        self.assertEqual(html_content['content']['ordered'], True)
        self.assertEqual(len(html_content['content']['items']), 2)
        self.assertEqual(html_content['content']['items'][0][0][0]['c'], '100')
        self.assertEqual(html_content['content']['items'][0][0][0]['t'], ParagraphTextType.TEXT)
        self.assertEqual(html_content['content']['items'][1][0][0]['c'], '200')
        self.assertEqual(html_content['content']['items'][1][0][0]['t'], ParagraphTextType.TEXT)

        # code 前的文本
        html_content = html_content_list[11]
        self.assertEqual(html_content['type'], DocElementType.PARAGRAPH)
        self.assertEqual(len(html_content['content']), 2)
        self.assertEqual(html_content['content'][0]['c'], 'reference:')
        self.assertEqual(html_content['content'][0]['t'], ParagraphTextType.TEXT)
        self.assertEqual(html_content['content'][1]['c'], '#include<xxxx.hpp>')
        self.assertEqual(html_content['content'][1]['t'], ParagraphTextType.CODE_INLINE)

        # txt格式
        txt_content = result.get_content_list().to_txt()
        self.assertEqual(txt_content, self.txt_expected_content)
        self.assertNotEqual(txt_content[-2], '\n')
        self.assertEqual(txt_content[-1], '\n')

        # md格式
        md_content = result.get_content_list().to_nlp_md()
        print('md_content', md_content)
        self.assertEqual(md_content, self.md_expected_content)
        self.assertNotEqual(md_content[-2], '\n')
        self.assertEqual(md_content[-1], '\n')

        # main_html
        main_html = result.get_content_list().to_main_html()  # 获取main_html内容
        self.assertEqual(normalize_html(main_html), normalize_html(self.main_html_expected_content))  # 如果遇到嵌套的html, 则返回原始html的时候还是应当拼接替换一下 TODO

    def test_html_pipeline_suit_2(self):
        """测试第二个数据：这个数据会丢失一些文本信息."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[1]
        # Create DataJson from test data
        input_data = DataJson(test_data)
        result = chain.extract(input_data)

        # Verify basic properties
        self.assertEqual(result.get_dataset_name(), 'test_pipeline_suit')
        self.assertEqual(result['track_id'], 'stackoverflow_math')

        html_content_list = result.get_content_list()[0]
        assert len(html_content_list) == 22

    def test_mathlab_html_to_md(self):
        """测试第二个数据：这个数据会丢失一些文本信息."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[2]  # matlab网页
        # Create DataJson from test data
        input_data = DataJson(test_data)
        result = chain.extract(input_data)

        # Verify basic properties
        self.assertEqual(result['track_id'], 'mathlab_code')
        md_content = result.get_content_list().to_nlp_md()
        self.assertIn('### Use Integers for Index Variables', md_content)
        self.assertIn('### Limit Use of `assert` Statements', md_content)

    def test_list_to_md(self):
        """测试第三个数据：这个数据会丢失一些文本信息."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[3]
        # Create DataJson from test data
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        self.assertEqual(result['track_id'], 'educba_com_list')
        md_content = result.get_content_list().to_nlp_md()
        self.assertIn('- Exception: All exceptions base class', md_content)

    def test_code_mix_in_list(self):
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[4]
        # Create DataJson from test data
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        md_content = result.get_content_list().to_nlp_md()
        self.assertIn('The descendant of `StandardizerActionRunner` interface has to provide', md_content)

    def test_code_pre_mixed(self):
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)

        test_data = self.data_json[5]
        # Create DataJson from test data
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        # print("code_pre_mixed", result.get_content_list().to_mm_md())
        self.assertIn("""```
this (DEFAULT_SERVER_NAME, DEFAULT_SERVER_PORT);
```

Test Test Test

```
ABC
DEF
```""", result.get_content_list().to_mm_md())

    def test_image_without_path(self):
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)

        test_data = self.data_json[6]
        # Create DataJson from test data
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        print(result.get_content_list()._get_data())
        self.assertIn('![點(diǎn)擊進(jìn)入下一頁(yè)]( "")', result.get_content_list().to_mm_md())
        self.assertNotIn('![點(diǎn)擊進(jìn)入下一頁(yè)]( "")', result.get_content_list().to_txt())

    def test_lineno_detect(self):
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[7]
        # Create DataJson from test data
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        code_content = result.get_content_list()[0][0]['content']['code_content']
        self.assertEqual(code_content, self.csdn_lineno_expected_content)

    def test_lineno_detect_2(self):
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[8]
        # Create DataJson from test data
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        self.assertIn('12.1.  Normative References', result.get_content_list().to_mm_md())

    def test_legato_docs_code_with_comment(self):
        """
        magic-html 抽代码时候把注释抽没了
        Returns:

        """
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[9]
        # Create DataJson from test data
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        assert result is not None
        # TODO magic-html修改完毕后，再来完善断言

    def test_oracle_doc_comment(self):
        """
        把末尾部分抽没了
        Returns:

        """
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[10]
        # Create DataJson from test data
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        main_html = result.get_content_list().to_mm_md()
        assert 'public int hashCode()' in main_html

    def test_table_involve_inline_code(self):
        """
        table里面包含行内code
        Returns:

        """
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[11]
        # Create DataJson from test data
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        content_list = result.get_content_list()._get_data()[0][0]['content']['html']
        assert content_list == r"""<table><tr><th>Function</th><th>Description</th><th>Example</th></tr><tr><td>`print()`</td><td>Prints a message to the console.</td><td>`print("Hello, World!")`</td></tr><tr><td>`len()`</td><td>Returns the length of an object.</td><td>`len([1, 2, 3])`</td></tr><tr><td>`range()`</td><td>Generates a sequence of numbers.</td><td>`range(1, 10)`</td></tr></table>"""

    def test_table_tail_text(self):
        """table的tail文本保留."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[12]
        # Create DataJson from test data
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        content_md = result.get_content_list().to_mm_md()
        assert '| ID: 975' in content_md

    def test_table_element_include_enter(self):
        """table的元素中间有换行."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[13]
        # Create DataJson from test data
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        content_md = result.get_content_list().to_mm_md()
        assert """| عنوان فارسی | توسعه مالی و هزینه سرمایه حقوق سهامداران: شواهدی از چین |
|---|---|
| عنوان انگلیسی | Financial development and the cost of equity capital: Evidence from China |
| کلمات کلیدی : | &nbsp  توسعه مالی؛ هزینه سرمایه حقوق سهامداران؛ قانون و امور مالی؛ چین |
| درسهای مرتبط | حسابداری |""" in content_md

    def test_list_empty(self):
        """list抽取为空，原因是嵌套的img标签没有text."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[14]
        # Create DataJson from test data
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        list_type = result.get_content_list()._get_data()[0][0]['type']
        assert list_type != 'list'

    def test_table_include_math_p(self):
        """table包含math和其他内容."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[15]
        # Create DataJson from test data
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        content_list = result.get_content_list()._get_data()
        assert len(content_list[0]) == 17
        assert content_list[0][3]['content']['html'] == r"<table><tr><td>up vote 17 down vote favorite 5</td><td>I'm having problems with exercises on proving whether or not a given number is prime. Is $83^{27} + 1$ prime? prime-numbers factoring</td></tr><tr><td></td><td></td></tr></table>"

    def test_table_include_math_p_2(self):
        """table包含math和其他内容."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[16]
        # Create DataJson from test data
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        content_list = result.get_content_list()._get_data()
        assert content_list[0][2]['content']['html'] == '<table><tr><td>单位换算：</td><td>$1 \\text{km} = 10^3 \\text{m}$<table><tr><td>长度</td><td>质量</td><td>时间</td></tr><tr><td>$1m=10^2cm$</td><td>$1kg=10^3g$</td><td>$1h=3600s$</td></tr></table></td></tr><tr><td>运动学：</td><td>$v = \\frac{dx}{dt}$ $a = \\frac{dv}{dt}$</td></tr></table>'

    def test_clean_tags(self):
        """测试clean_tag的preExtractor是否生效."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[17]
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        content_md = result.get_content_list().to_mm_md()
        self.assertNotIn('begingroup', content_md)

    def test_list_nest_three(self):
        """测试列表嵌套三层."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[18]
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        result_content_list = result.get_content_list()._get_data()
        assert int(result_content_list[0][0]['content']['list_nest_level']) == 3

    def test_table_include_entity(self):
        """测试table包含实体."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[19]
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        result_md = result.get_content_list().to_mm_md()
        assert '&amp;' not in result_md
        assert '&nbsp;' not in result_md

    def test_content_list_empty(self):
        """测试content_list为空."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[20]
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        content_mmd = result.get_content_list().to_mm_md()
        assert '京大平层，奶油风浪漫到家！' in content_mmd

    def test_nlp_md_exclude_node_types(self):
        """测试nlp_md排除节点类型."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[21]
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        content_txt = result.get_content_list().to_nlp_md(exclude_nodes=[DocElementType.COMPLEX_TABLE])
        assert '<table>' not in content_txt
        assert '</table>' not in content_txt

    def test_para_is_short(self):
        """测试para识别后内容太短."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[22]
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        content_txt = result.get_content_list().to_nlp_md()
        print('content_txt', content_txt)
        assert len(content_txt) == 2022

    def test_xml_tag(self):
        """测试xml标签."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[23]
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        result_md = result.get_content_list().to_mm_md()
        self.assertIn('Every child that attends a CHICKS break has a deserving story', result_md)

    def test_math_dollar(self):
        """测试math美元符号."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[24]
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        result_md = result.get_content_list().to_nlp_md()
        self.assertIn(r'\$16.8 million', result_md)

    def test_math_non_asciimath(self):
        """测试普通文本中的``不应该被识别为asciimath."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[25]
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        result_md = result.get_content_list().to_nlp_md()
        self.assertIn(r'\`Queen Helena\`', result_md)

    def test_more_nt(self):
        """测试去除单元格的\n\t.\n保留下来."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[26]
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        result_content_list = result.get_content_list()._get_data()
        result = result_content_list[0][2]['content']['html']
        assert '\n\t' not in result
        assert len(result) == 1878

    def test_math_physicsforums(self):
        """测试math_physicsforums网页中数学公式是[tex]和[itex]包裹的，且中间还有<br>标签分割."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[27]
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        result_md = result.get_content_list().to_nlp_md()
        self.assertIn('$\\Delta K = (dd^{\\dagger} + d^{\\dagger}d)K$', result_md)
        self.assertIn('$$\\Delta K = \\Bigl( \\frac{1}{3!}\\epsilon^{klm}\\epsilon^n_{\\ ij}\\partial_k \\partial_n K_{lm} - \\frac{1}{4}\\partial_{i}\\partial^k K_{jk} \\Bigr) dx^i \\wedge dx^j$$', result_md)

    def test_table_only_include_tr(self):
        """测试table的表头只包含tr标签."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[28]
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        result_md = result.get_content_list().to_nlp_md()
        assert 'List Price:$11.80' in result_md

    def test_table_only_one_td(self):
        """测试table只有一个td."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[29]
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        result_md = result.get_content_list().to_nlp_md()
        assert '|  | Shooting on DEWEY AVENUE AND GLENDALE PARK., ROCHESTER |\n|---|---|' not in result_md

    def test_math_broken_label(self):
        """测试math标签包含属性缺失的情况."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[30]
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        result_md = result.get_content_list().to_nlp_md()
        self.assertIn(r'$alpha = \left(alpha_1, alpha_2, ldots, alpha_n\right) ,!$', result_md)

    def test_table_span_error(self):
        """测试table的span标签错误."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[31]
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        result_flag = result.get_content_list()._get_data()[0][0]['content']['is_complex']
        assert result_flag is True

    def test_table_colspan_error(self):
        """测试table的colspan标签为字符串引起的异常错误."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[32]
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        result_flag = result.get_content_list()._get_data()[0][15]['content']['is_complex']
        assert result_flag is False

    def test_table_colspan_percent_err(self):
        """测试table的colspan标签为百分数引起的异常错误."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[33]
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        result_flag = result.get_content_list()._get_data()[0][0]['content']['is_complex']
        assert result_flag is True

    def test_table_colspan_str_error(self):
        """测试table的colspan标签为字符串引起的异常错误."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[34]
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        result_flag = result.get_content_list()._get_data()[0][37]['content']['is_complex']
        assert result_flag is False

    def test_table_invalid_percent(self):
        """测试table的colspan标签为百分数引起的异常错误."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[35]
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        result_flag = result.get_content_list()._get_data()[0][0]['content']['is_complex']
        assert result_flag is False

    def test_maigc_html(self):
        """测试magic-html."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[36]
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        result_md = result.get_magic_html()
        assert len(result_md) > 0

    def test_table_tail_repeat(self):
        """测试table的tail重复."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[37]
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        result_md = result.get_content_list().to_mm_md()
        text = """
A few explanations on why certain things in business are so.
        """
        assert result_md.count(text.strip()) == 1

    def test_title_include_special_char(self):
        """测试title包含特殊字符."""
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = self.data_json[38]
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        result_md = result.get_content_list()._get_data()
        assert result_md[0][0]['content']['title_content'] == 'View source for Semi-continuous decomposition'
