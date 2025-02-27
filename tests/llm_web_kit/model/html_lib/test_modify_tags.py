import unittest

from lxml import html

from llm_web_kit.model.html_lib.modify_tags import (unwrap_single_child_tag,
                                                    wrap_bare_text)


class TestWrapBareText(unittest.TestCase):

    def test_text_with_child_element(self):
        # 测试父元素有文本和子元素时，文本被包裹
        root = html.fromstring('<div>Text<span>Child</span></div>')
        wrapped = wrap_bare_text(root)
        self.assertEqual(wrapped.text, '')  # 原文本应被清空
        self.assertEqual(len(wrapped), 2)  # 新span + 原span
        self.assertEqual(wrapped[0].tag, 'span')
        self.assertEqual(wrapped[0].text, 'Text')
        self.assertEqual(wrapped[1].text, 'Child')

    def test_tail_after_child_element(self):
        # 测试子元素尾部文本被包裹
        root = html.fromstring('<div><span>Child</span>Tail</div>')
        wrapped = wrap_bare_text(root)
        span = wrapped.find('.//span')
        self.assertEqual(span.tail, '')  # 原尾部文本应被清空
        next_span = span.getnext()
        self.assertEqual(next_span.tag, 'span')
        self.assertEqual(next_span.text, 'Tail')

    def test_multiple_children_with_text(self):
        # 测试多个子元素和文本混合的情况
        root = html.fromstring('<div>Start<span>A</span>Middle<b>B</b>End</div>')
        wrapped = wrap_bare_text(root)
        # 预期结构：3个文本span + 原span + 原b
        self.assertEqual(len(wrapped), 5)
        self.assertEqual(wrapped[0].text, 'Start')
        self.assertEqual(wrapped[1].tag, 'span')  # 原span
        self.assertEqual(wrapped[2].text, 'Middle')
        self.assertEqual(wrapped[3].tag, 'b')  # 原b标签

    def test_nested_elements_text_wrapping(self):
        # 测试嵌套元素中的文本处理
        root = html.fromstring('<div>D1<span>S1<p>P1</p>S2</span>D2</div>')
        wrapped = wrap_bare_text(root)
        # 检查div层
        self.assertEqual(wrapped[0].text, 'D1')
        self.assertEqual(wrapped[1].tag, 'span')
        self.assertEqual(wrapped[2].text, 'D2')
        # 检查span层
        span = wrapped[1]
        self.assertEqual(span[0].text, 'S1')
        self.assertEqual(span[1].tag, 'p')
        self.assertEqual(span[2].text, 'S2')

    def test_no_wrapping_when_no_children(self):
        # 测试没有子元素时不进行包裹
        root = html.fromstring('<p>Simple text</p>')
        original_text = root.text
        wrapped = wrap_bare_text(root)
        self.assertEqual(len(wrapped), 0)  # 没有子元素，不处理
        self.assertEqual(wrapped.text, original_text)


class TestUnwrapSingleChildTag(unittest.TestCase):

    def test_single_child_unwrapping(self):
        # 测试单层解包和类合并
        root = html.fromstring(
            "<html><body><div class='parent'><p class='child'></p></div></body></html>"
        )
        unwrapped = unwrap_single_child_tag(root)
        p = unwrapped.find('.//p')
        self.assertEqual(p.get('class'), 'parent|child')
        # 检查div是否被移除
        self.assertIsNone(unwrapped.find('.//div'))

    def test_class_merging_edge_cases(self):
        # 测试类合并的边界情况
        cases = [
            ('<div><p></p></div>', ''),  # 都没有class
            ('<div class=' '><p></p></div>', ''),  # 空class
            ("<div><p class='child'></p></div>", 'child'),
            ("<div class='parent'><p></p></div>", 'parent'),
        ]
        for html_str, expected in cases:
            root = html.fromstring(f'<html><body>{html_str}</body></html>')
            unwrapped = unwrap_single_child_tag(root)
            p = unwrapped.find('.//p')
            self.assertEqual(p.get('class'), expected)

    def test_multilevel_unwrapping(self):
        # 测试多层嵌套解包
        root = html.fromstring(
            """
        <html>
            <body>
                <div class='l1'>
                    <section class='l2'>
                        <p class='l3'></p>
                    </section>
                </div>
            </body>
        </html>
        """
        )
        unwrapped = unwrap_single_child_tag(root)
        p = unwrapped.find('.//p')
        self.assertEqual(p.get('class'), 'l1|l2|l3')
        # 检查祖先元素是否都被移除
        self.assertIsNone(unwrapped.find('.//div'))
        self.assertIsNone(unwrapped.find('.//section'))

    def test_no_unwrap_with_multiple_children(self):
        # 测试多个子元素时不解包
        root = html.fromstring('<html<div><p>A</p><p>B</p></div></html>')
        original_structure = html.tostring(root)
        unwrapped = unwrap_single_child_tag(root)
        # 结构应保持不变
        self.assertEqual(html.tostring(unwrapped), original_structure)

    def test_root_element_not_unwrapped(self):
        # 测试根元素不解包
        root = html.fromstring('<html><body><div><p>Content</p></div></body></html>')
        original_tag = root.tag
        unwrapped = unwrap_single_child_tag(root)
        self.assertEqual(unwrapped.tag, original_tag)
        self.assertEqual(len(unwrapped), 1)  # 仍然只有一个p子元素


if __name__ == '__main__':
    unittest.main()
