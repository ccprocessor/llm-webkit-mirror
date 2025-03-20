# 测试text识别器
import os
import unittest
from pathlib import Path

from llm_web_kit.config.cfg_reader import load_pipe_tpl
from llm_web_kit.extractor.extractor_chain import ExtractSimpleFactory
from llm_web_kit.extractor.html.recognizer.recognizer import \
    BaseHTMLElementRecognizer
from llm_web_kit.extractor.html.recognizer.text import TextParagraphRecognizer
from llm_web_kit.input.datajson import DataJson


class TestTextParagraphRecognize(unittest.TestCase):
    def setUp(self):
        self.text_recognize = TextParagraphRecognizer()
        # Config for HTML extraction
        self.config = load_pipe_tpl('html-test')

    def test_text_1(self):
        """
        测试1  s3://llm-pdf-text-1/qa/quyuan/output/part-67c01310620e-000064.jsonl
        Returns:

        """
        with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/recognizer/text.html', 'r') as file:
            html_content = file.read()
        assert self.text_recognize._TextParagraphRecognizer__combine_text('知识乱象\n',
                                                                          '中共中央政治局召开会议审议《成-2020年10月16日新闻联播',
                                                                          'zh')[:7] == '知识乱象\n中共'
        result = self.text_recognize.recognize('http://www.baidu.com', [(html_content, html_content)], html_content)
        assert result[909][0][1413:1422] == '知识乱象\\n 中共'

    def test_text_2(self):
        """
        测试2  s3://llm-pdf-text-1/qa/quyuan/output/part-67c01310620e-004720.jsonl
        Returns:

        """
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = {
            'track_id': 'text_md',
            'dataset_name': 'text_md',
            'url': 'https://www.aircraftspruce.com/catalog/pnpages/AT108AR-5_32.php',
            'data_source_category': 'HTML',
            'path': 'text2.html',
            'file_bytes': 1000,
            'meta_info': {'input_datetime': '2020-01-01 00:00:00'}
        }
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        content_md = result.get_content_list().to_mm_md()
        assert content_md[:130] == '''For Swivel Hand Rivet Squeezer or any snap Type .187 Shank Diameter Squeezer\n \n\n Instructions for Selecting Rivet Sets:\n\nTo develo'''

    def test_text_3(self):
        """
        测试3  s3://llm-pdf-text-1/qa/quyuan/mathout/part-67c05902108f-001066.jsonl
        Returns:

        """
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = {
            'track_id': 'text_md',
            'dataset_name': 'text_md',
            'url': 'https://www.physicsforums.com/threads/how-do-convex-mirrors-affect-image-location-and-size.240850/',
            'data_source_category': 'HTML',
            'path': 'text3.html',
            'file_bytes': 1000,
            'meta_info': {'input_datetime': '2020-01-01 00:00:00'}
        }
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        content_md = result.get_content_list().to_mm_md()
        assert content_md[371:584] == '''2.\n The speed of light in a material is 2.50x10^8 meters per second. What is the index of refraction of the\n material?\n\n\n\n\n\n 2. Relevant equations\n\n\n\n\n\n\n\n 3. The\n attempt at a solution\n\n1. di=22.22\n\n\n\n2. Dont know'''

    def test_text_4(self):
        """
        测试4  s3://llm-pdf-text-1/qa/quyuan/mathout/part-67c05902108f-000050.jsonl
        Returns:

        """
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = {
            'track_id': 'text_md',
            'dataset_name': 'text_md',
            'url': 'https://www.physicsforums.com/threads/isnt-the-normal-acceleration-always-towards-the-center.157291/',
            'data_source_category': 'HTML',
            'path': 'text4.html',
            'file_bytes': 1000,
            'meta_info': {'input_datetime': '2020-01-01 00:00:00'}
        }
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        content_md = result.get_content_list().to_mm_md()
        assert content_md[46:475] == '''1. The problem statement, all variables and given/known data\n\n 2. Relevant equations\n\n\n\nSee attachment\n\n\n\n 3. The attempt at a solution\n\nI solved the problem (on the same page as problem, written in pencil) but the direction of the acceleration that I calculated is different, I dont understand why my answer is wrong if the normal acceleration always towards the center and the tangent acceleration is suppossed to be clockwise.'''

    def test_text_5(self):
        """
        测试5  s3://llm-pdf-text-1/qa/quyuan/output/part-67c01310620e-007988.jsonl
        Returns:

        """
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = {
            'track_id': 'text_md',
            'dataset_name': 'text_md',
            'url': 'https://shopnado.com.au/product/rigo-ride-on-car-tractor-toy-kids-electric-cars-12v-battery-child-toddlers-blue/',
            'data_source_category': 'HTML',
            'path': 'text5.html',
            'file_bytes': 1000,
            'meta_info': {'input_datetime': '2020-01-01 00:00:00'}
        }
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        content_md = result.get_content_list().to_mm_md()
        assert content_md[1214:1449] == '''Please Note:\n\n 1. Charge the battery on receiving even if it will not be used soon.\n\n 2. Charge the battery EVERY MONTH if not in use for long periods to prevent over-discharging of the battery. This can cause irreparable damage to it.'''

    def test_text_6(self):
        """
        测试6  s3://llm-pdf-text-1/qa/quyuan/output/part-67c01310620e-012288.jsonl
        Returns:

        """
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = {
            'track_id': 'text_md',
            'dataset_name': 'text_md',
            'url': 'https://adelanta.biz/kuplu-knigi/the-experience-of-russian-bibliography-copikova-part-2-l/',
            'data_source_category': 'HTML',
            'path': 'text6.html',
            'file_bytes': 1000,
            'meta_info': {'input_datetime': '2020-01-01 00:00:00'}
        }
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        content_md = result.get_content_list().to_mm_md()
        assert content_md[255:450] == '''1813 года\n\n5864.\\t Лабиринт волшебства, или удивительные приключения восточных принцев, сочинение В. Протопоповича; Москва, 1786 г. - в 8°. \n\n\n\n\n\n 5865.\\t Лакировальщик, или ясное и подробное нас'''

    def test_text_7(self):
        """
        测试7  s3://llm-pdf-text-1/qa/quyuan/mathout/part-67c05902108f-001871.jsonl
        ps：badcase未保留行是因为走的cc
        Returns:

        """
        with open(Path(__file__).parent.parent.parent / 'assets/extractor_chain_input/good_data/html/text7.html', 'r') as file:
            html_content = file.read()
        result = self.text_recognize.recognize('http://www.baidu.com', [(html_content, html_content)], html_content)
        assert '1) A man takes 5 hrs and 45 mins to walk to a certain place and ride back' in result[0][0] and BaseHTMLElementRecognizer.is_cc_html(result[0][0])

    def test_text_8(self):
        """
        测试8  s3://llm-pdf-text-1/qa/quyuan/mathout/part-67c05902108f-001477.jsonl
        ps：badcase未保留行是因为走的cc
        Returns:

        """
        with open(Path(__file__).parent.parent.parent / 'assets/extractor_chain_input/good_data/html/text8.html', 'r') as file:
            html_content = file.read()
        result = self.text_recognize.recognize('http://www.baidu.com', [(html_content, html_content)], html_content)
        assert "40xy' -ln(x^8) = 0\\n\\n\\nInitial Condition: y(1)=31" in result[0][0] and BaseHTMLElementRecognizer.is_cc_html(result[0][0])

    def test_text_9(self):
        """
        测试9  s3://llm-pdf-text-1/qa/quyuan/mathout/part-67c05902108f-000073.jsonl
        ps：badcase未保留行是因为走的cc
        Returns:

        """
        with open(Path(__file__).parent.parent.parent / 'assets/extractor_chain_input/good_data/html/text9.html', 'r') as file:
            html_content = file.read()
        result = self.text_recognize.recognize('http://www.baidu.com', [(html_content, html_content)], html_content)
        assert '1) Consider the formula f(x)=lim(n--&gt;infinity)((x^n)/(1+x^n)).\\n Let D={x:f(x) is an element of R}. Calculate f(x) for all x elements of D and determine where f: D--&gt;R is continuous.\\n\\n 2) Let f: D--&gt;R and suppose that f(x) greater than equal 0 for all x elements of D. Define sqrt(f)--&gt;R by (sqrt(f))(x) = sqrt(f(x)). If f is continuous at c elements of D, prove that sqrt(f) is continuous at c.' in result[50][0] and BaseHTMLElementRecognizer.is_cc_html(result[50][0])

    def test_text_10(self):
        """
        测试10  s3://llm-pdf-text-1/qa/quyuan/mathout/part-67c05902108f-000620.jsonl
        Returns:

        """
        chain = ExtractSimpleFactory.create(self.config)
        self.assertIsNotNone(chain)
        test_data = {
            'track_id': 'text_md',
            'dataset_name': 'text_md',
            'url': 'https://www.physicsforums.com/threads/questions-about-parallel-worlds-by-michio-kaku-the-big-bang.612643/',
            'data_source_category': 'HTML',
            'path': 'text10.html',
            'file_bytes': 1000,
            'meta_info': {'input_datetime': '2020-01-01 00:00:00'}
        }
        input_data = DataJson(test_data)
        result = chain.extract(input_data)
        content_md = result.get_content_list().to_mm_md()
        assert content_md[306:450] == '''So far I have 2 sets of questions (but I\'m onlin in the 2nd chapter now\n\n![\\":smile:\\"]( "\\"Smile")\n\n)\n\n\n\n1)\n\nIn the book, Michio Kaku says the '''
