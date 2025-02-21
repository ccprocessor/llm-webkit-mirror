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

        assert len(self.data_json) == 11

        # Config for HTML extraction
        self.config = {
            'extractor_pipe': {
                'enable': True,
                'validate_input_format': False,
                'pre_extractor': [
                    {
                        'enable': True,
                        'python_class': 'llm_web_kit.extractor.html.pre_extractor.TestHTMLFileFormatFilterPreExtractor',
                        'class_init_kwargs': {
                            'html_parent_dir': 'tests/llm_web_kit/extractor/assets/extractor_chain_input/good_data/html/',
                        },
                    },
                    {
                        'enable': True,
                        'python_class': 'llm_web_kit.extractor.html.pre_extractor.HTMLFileFormatFilterTablePreExtractor',
                    },
                ],
                'extractor': [
                    {
                        'enable': True,
                        'python_class': 'llm_web_kit.extractor.html.extractor.HTMLFileFormatExtractor',
                        'class_init_kwargs': {},
                    }
                ],
                'post_extractor': [
                    {
                        'enable': False,
                        'python_class': 'llm_web_kit.extractor.html.post_extractor.HTMLFileFormatPostExtractor',
                        'class_init_kwargs': {},
                    }
                ],
            }
        }

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
        self.assertEqual(html_content['type'], DocElementType.TABLE)
        self.assertEqual(html_content['content']['is_complex'], False)
        assert html_content['content']['html'].startswith('<table')

        # 然后是complex table
        html_content = html_content_list[5]
        self.assertEqual(html_content['type'], DocElementType.TABLE)
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
        self.assertIn('![點(diǎn)擊進(jìn)入下一頁(yè)]( "")', result.get_content_list().to_mm_md())
        self.assertIn('![點(diǎn)擊進(jìn)入下一頁(yè)]( "")', result.get_content_list().to_txt([]))

    # def test_lineno_detect(self):
    #     chain = ExtractSimpleFactory.create(self.config)
    #     self.assertIsNotNone(chain)
    #     test_data = self.data_json[7]
    #     # Create DataJson from test data
    #     input_data = DataJson(test_data)
    #     result = chain.extract(input_data)
    #     self.assertEqual(result.get_content_list().to_mm_md(), self.csdn_lineno_expected_content)

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
        main_html = result.get_content_list().to_main_html()
        assert 'public int hashCode()' in main_html
