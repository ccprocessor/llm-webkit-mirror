import os
import unittest

from llm_web_kit.extractor.html.recognizer.list import ListRecognizer
from llm_web_kit.libs.html_utils import html_to_element


class TestSimpleListRecognize(unittest.TestCase):
    def setUp(self):
        self.__list_recognize = ListRecognizer()
        self.__simple_list_content = None
        self.__complex_list_content = None
        self.__with_empty_list_item_content = None
        self.__list_with_sub_sup_content = None
        self.__list_with_sub_sup_simple_content = None

        with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/recognizer/simple_list.html', 'r') as file:
            self.__simple_list_content = file.read()

        with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/recognizer/complex_list.html', 'r') as file:
            self.__complex_list_content = file.read()

        with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/recognizer/test-list-item.html', 'r') as file:
            self.__with_empty_list_item_content = file.read()

        with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/recognizer/list_sub_sup.html', 'r') as file:
            self.__list_with_sub_sup_content = file.read()

        with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/recognizer/list_sub_sup_simple.html', 'r') as file:
            self.__list_with_sub_sup_simple_content = file.read()

    def test_simple_list(self):
        html_part = self.__list_recognize.recognize('http://url.com', [(html_to_element(self.__simple_list_content), html_to_element(self.__simple_list_content))], self.__simple_list_content)
        assert len(html_part) == 6

    def test_complex_list(self):
        # TODO: Fix this test
        html_part = self.__list_recognize.recognize('http://url.com', [(html_to_element(self.__complex_list_content), html_to_element(self.__complex_list_content))], self.__complex_list_content)
        assert len(html_part) == 6

    def test_with_empty_list_item_content(self):
        html_part = self.__list_recognize.recognize('http://url.com', [(html_to_element(self.__with_empty_list_item_content), html_to_element(self.__with_empty_list_item_content))], self.__with_empty_list_item_content)
        assert len(html_part) == 33

    def test_list_with_sub_sup_tags(self):
        """测试列表中的下标和上标标签是否正确处理为GitHub Flavored Markdown格式."""
        # 验证原始HTML中是否包含sub/sup标签
        assert '<sub>' in self.__list_with_sub_sup_content or '<sup>' in self.__list_with_sub_sup_content, '测试HTML中没有sub或sup标签'

        html_part = self.__list_recognize.recognize(
            'http://url.com',
            [(html_to_element(self.__list_with_sub_sup_content), html_to_element(self.__list_with_sub_sup_content))],
            self.__list_with_sub_sup_content
        )

        # 验证能够正确识别列表
        assert len(html_part) > 0, '没有识别出任何HTML部分'

        # 验证process_sub_sup_tags函数已被调用和集成
        # 通过检查html_part中是否有任何元素包含转换后的标记
        any_part_contains_markdown = False
        for element, _ in html_part:
            element_text = element.text_content() if hasattr(element, 'text_content') else (element.text or '')
            if '~' in element_text or '^' in element_text:
                any_part_contains_markdown = True
                break

        # 只要验证至少一个元素中包含可能的转换标记
        assert any_part_contains_markdown, '没有元素包含已转换的sub/sup标记'

    def test_list_with_sub_sup_tags_simple(self):
        """使用简化HTML测试列表中的下标和上标标签处理."""
        # 验证原始HTML中是否包含sub/sup标签
        assert '<sub>' in self.__list_with_sub_sup_simple_content, '测试HTML中没有sub标签'
        assert '<sup>' in self.__list_with_sub_sup_simple_content, '测试HTML中没有sup标签'

        html_part = self.__list_recognize.recognize(
            'http://url.com',
            [(html_to_element(self.__list_with_sub_sup_simple_content), html_to_element(self.__list_with_sub_sup_simple_content))],
            self.__list_with_sub_sup_simple_content
        )

        # 验证能够正确识别列表
        assert len(html_part) > 0, '没有识别出任何HTML部分'

        # 检查html_part中是否有任何元素包含转换后的标记
        any_part_contains_markdown = False
        for element, _ in html_part:
            element_text = element.text_content() if hasattr(element, 'text_content') else (element.text or '')
            if '~' in element_text or '^' in element_text:
                any_part_contains_markdown = True
                break

        # 只要验证至少一个元素中包含可能的转换标记
        assert any_part_contains_markdown, '没有元素包含已转换的sub/sup标记'
