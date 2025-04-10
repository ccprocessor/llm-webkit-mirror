import os
import unittest

from llm_web_kit.exception.exception import HtmlListRecognizerException
from llm_web_kit.extractor.html.recognizer.list import ListRecognizer
from llm_web_kit.extractor.html.recognizer.recognizer import CCTag
from llm_web_kit.libs.html_utils import build_cc_element, html_to_element


class TestSimpleListRecognize(unittest.TestCase):
    def setUp(self):
        self.__list_recognize = ListRecognizer()
        self.__simple_list_content = None
        self.__complex_list_content = None
        self.__with_empty_list_item_content = None
        self.__list_with_sub_sup_content = None
        self.__list_with_sub_sup_simple_content = None
        self.__list_with_br_and_cctags_content = None
        self.__list_with_sub_sup_tail_content = None
        self.__list_with_ul_text_content = None
        self.__list_with_sub_no_prefix_content = None

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

        with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/recognizer/list_br_and_cctags.html', 'r') as file:
            self.__list_with_br_and_cctags_content = file.read()

        with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/recognizer/list_with_sub_sup_tail.html', 'r') as file:
            self.__list_with_sub_sup_tail_content = file.read()

        with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/recognizer/list_with_ul_text.html', 'r') as file:
            self.__list_with_ul_text_content = file.read()

        with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/recognizer/list_with_sub_no_prefix.html', 'r') as file:
            self.__list_with_sub_no_prefix_content = file.read()

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

    def test_list_with_sub_sup_tail(self):
        """测试列表中带尾部文本的下标和上标标签处理."""
        html_part = self.__list_recognize.recognize(
            'http://url.com',
            [(html_to_element(self.__list_with_sub_sup_tail_content), html_to_element(self.__list_with_sub_sup_tail_content))],
            self.__list_with_sub_sup_tail_content
        )

        # 验证能够正确识别列表
        assert len(html_part) > 0, '没有识别出任何HTML部分'

        # 查找包含转换后标记和尾部文本的内容
        # 这里覆盖了list.py中的第243-244行（sub/sup尾部文本处理）
        any_contains_text_after_marker = False
        for element, _ in html_part:
            element_text = element.text_content() if hasattr(element, 'text_content') else (element.text or '')
            # 检查是否包含格式化的下标/上标和它后面的尾部文本
            if ('~2~O' in element_text and '重要的物质' in element_text) or \
               ('^2^' in element_text and '爱因斯坦的公式' in element_text) or \
               ('~6~H~12~O~6~' in element_text and '一种糖' in element_text):
                any_contains_text_after_marker = True
                break

        # 验证尾部文本处理成功
        assert any_contains_text_after_marker, '未正确处理sub/sup元素的尾部文本'

    def test_list_with_br_and_cctags(self):
        """测试列表中包含<br/>标签和特殊CC标签的处理."""
        html_part = self.__list_recognize.recognize(
            'http://url.com',
            [(html_to_element(self.__list_with_br_and_cctags_content), html_to_element(self.__list_with_br_and_cctags_content))],
            self.__list_with_br_and_cctags_content
        )

        # 验证能够正确识别列表
        assert len(html_part) > 0, '没有识别出任何HTML部分'

        # 输出html_part内容的调试信息
        elements_info = []
        for i, (element, _) in enumerate(html_part):
            elements_info.append(f'Element {i}: Tag={element.tag}')
            if hasattr(element, 'text_content'):
                content = element.text_content()
                elements_info.append(f'  Content: {content[:50]}...')

        # 找到包含完整内容的元素
        content_found = False
        for element, _ in html_part:
            element_text = element.text_content() if hasattr(element, 'text_content') else (element.text or '')
            if 'First line' in element_text and 'Second line' in element_text and \
               'E=mc^2' in element_text and 'print' in element_text:
                content_found = True
                break

        # 验证所有内容均被正确处理
        assert content_found, '未找到正确处理的<br/>标签或CC标签内容'

    def test_to_content_list_node(self):
        """测试to_content_list_node方法."""
        # 直接创建一个cclist元素
        items_json = '[[{"c": "测试项", "t": "text"}]]'
        cclist_element = build_cc_element(
            CCTag.CC_LIST,
            items_json,
            '',
            ordered='False',
            html='<ul><li>测试项</li></ul>',
            list_nest_level='1'
        )
        raw_html_segment = '<ul><li>测试项</li></ul>'

        # 测试to_content_list_node方法
        content_node = self.__list_recognize.to_content_list_node('http://url.com', cclist_element, raw_html_segment)

        # 验证返回的内容结构正确
        assert 'type' in content_node, '返回的content_node缺少type字段'
        assert 'content' in content_node, '返回的content_node缺少content字段'
        assert 'raw_content' in content_node, '返回的content_node缺少raw_content字段'

        # 验证content字段包含必要的内容
        assert 'items' in content_node['content'], 'content字段缺少items'
        assert 'ordered' in content_node['content'], 'content字段缺少ordered'
        assert 'list_nest_level' in content_node['content'], 'content字段缺少list_nest_level'

        # 验证内容正确性
        assert content_node['content']['items'] is not None, 'items不应为None'
        assert isinstance(content_node['content']['ordered'], bool), 'ordered应为布尔值'
        # 由于list_nest_level可能是字符串或整数，所以验证其可以转换为整数
        assert str(content_node['content']['list_nest_level']).isdigit(), 'list_nest_level应为整数或字符串形式的整数'

    def test_to_content_list_node_invalid_type(self):
        """测试to_content_list_node方法处理非HtmlElement类型的输入."""
        # 使用一个非HtmlElement的输入
        with self.assertRaises(HtmlListRecognizerException):
            self.__list_recognize.to_content_list_node('http://url.com', '这不是HtmlElement', '<ul>测试</ul>')

    def test_get_attribute_exception(self):
        """测试__get_attribute方法的异常处理."""
        # 创建一个非cclist元素
        non_cclist_element = html_to_element('<div>这不是一个cclist元素</div>')

        # 使用pytest的断言异常机制验证异常抛出
        with self.assertRaises(HtmlListRecognizerException):
            # 注意这里直接访问私有方法需要使用_ListRecognizer__get_attribute的形式
            # 但由于是私有方法，无法直接访问，我们可以通过测试公开接口间接验证
            self.__list_recognize.to_content_list_node('http://url.com', non_cclist_element, '<div>这不是一个cclist元素</div>')

    def test_recognize_with_cc_html(self):
        """测试recognize方法中对cc_html的处理."""
        # 创建一个cclist元素
        cclist_element = build_cc_element(
            CCTag.CC_LIST,
            '[[{"c": "测试项", "t": "text"}]]',
            '',
            ordered='False',
            html='<ul><li>测试项</li></ul>',
            list_nest_level=1
        )

        # 使用recognize方法处理cclist元素
        html_part = self.__list_recognize.recognize(
            'http://url.com',
            [(cclist_element, cclist_element)],
            '<ul><li>测试项</li></ul>'
        )

        # 验证cclist元素被原样返回
        assert len(html_part) == 1, 'recognize应返回原始的cclist元素'
        assert html_part[0][0].tag == CCTag.CC_LIST, '返回的元素应该是cclist'

    def test_list_with_ul_text(self):
        """测试ul标签直接包含文本的处理."""
        html_part = self.__list_recognize.recognize(
            'http://url.com',
            [(html_to_element(self.__list_with_ul_text_content), html_to_element(self.__list_with_ul_text_content))],
            self.__list_with_ul_text_content
        )

        # 验证能够正确识别列表
        assert len(html_part) > 0, '没有识别出任何HTML部分'

        # 查找包含ul直接文本的内容
        ul_text_found = False
        for element, _ in html_part:
            element_text = element.text_content() if hasattr(element, 'text_content') else (element.text or '')
            if '前言' in element_text:
                ul_text_found = True
                break

        # 验证ul直接文本被正确处理
        assert ul_text_found, '未正确处理ul标签直接包含的文本'

    def test_list_with_sub_no_prefix(self):
        """测试sub/sup标签没有前缀文本时的处理."""
        html_part = self.__list_recognize.recognize(
            'http://url.com',
            [(html_to_element(self.__list_with_sub_no_prefix_content), html_to_element(self.__list_with_sub_no_prefix_content))],
            self.__list_with_sub_no_prefix_content
        )

        # 验证能够正确识别列表
        assert len(html_part) > 0, '没有识别出任何HTML部分'

        # 查找包含没有前缀的sub/sup标签的内容
        marker_found = False
        for element, _ in html_part:
            element_text = element.text_content() if hasattr(element, 'text_content') else (element.text or '')
            if ('~下标~' in element_text) or ('^上标^' in element_text):
                marker_found = True
                break

        # 验证没有前缀的sub/sup标签被正确处理
        assert marker_found, '未正确处理没有前缀的sub/sup标签'
