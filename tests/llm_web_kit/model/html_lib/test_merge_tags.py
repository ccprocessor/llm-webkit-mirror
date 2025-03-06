import unittest

from llm_web_kit.model.html_lib.base_func import document_fromstring
from llm_web_kit.model.html_lib.merge_tags import merge_list


class TestMergeList(unittest.TestCase):
    def assertMergedList(
        self, input_html, expected_text, expected_children_count=0, tag='ul'
    ):
        element = document_fromstring(input_html)
        processed = merge_list(element)

        # 查找目标列表元素
        target = processed.find(f'.//{tag}')
        self.assertIsNotNone(target, f'{tag}元素不存在')

        # 验证文本内容
        actual_text = target.text.strip() if target.text else ''
        self.assertEqual(actual_text, expected_text, '合并文本不一致')

        # 验证子元素数量
        self.assertEqual(len(target), expected_children_count, '子元素未正确删除')

        return target

    def test_merge_ul_with_li(self):
        html_str = """
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
        </ul>
        """
        # Some problem here. But now the web classification model is trained with this behavior.
        # TODO Fix this bug and retrain the model
        # expected = "Item 1 Item 2"
        expected = 'Item 1\nItem 2'
        self.assertMergedList(html_str, expected)

    def test_merge_ol_with_nested_elements(self):
        html_str = """
        <ol>
            <li><p>Text <b>bold</b></p></li>
            <li>Another</li>
        </ol>
        """
        # Some problem here. But now the web classification model is trained with this behavior.
        # TODO Fix this bug and retrain the model
        # expected = "Text bold Another"
        expected = 'Text bold\nAnother'
        self.assertMergedList(html_str, expected, tag='ol')

    def test_merge_dl_with_mixed_content(self):
        html_str = """
        <dl>Direct text
            <dt>Term</dt>
            <dd>Definition</dd>
        </dl>
        """
        # Some problem here. But now the web classification model is trained with this behavior.
        # TODO Fix this bug and retrain the model
        # expected = "Direct text Term Definition"
        expected = 'Direct text\n            TermDefinition'
        self.assertMergedList(html_str, expected, tag='dl')

    def test_preserve_attributes(self):
        html_str = """
        <ul class="list" id="main-list">
            <li>Item</li>
        </ul>
        """
        target = self.assertMergedList(html_str, 'Item')
        self.assertEqual(target.get('class'), 'list', 'class属性未保留')
        self.assertEqual(target.get('id'), 'main-list', 'id属性未保留')

    def test_empty_list(self):
        html_str = '<ul></ul>'
        self.assertMergedList(html_str, '', tag='ul')

    def test_deeply_nested_list(self):
        html_str = """
        <ul>
            <li>
                Level 1
                <ul>
                    <li>Level 2</li>
                </ul>
            </li>
        </ul>
        """
        # 外层ul应该被处理，内层ul会被合并
        element = document_fromstring(html_str)
        processed = merge_list(element)

        outer_ul = processed.find('.//ul')

        # Some problem here. But now the web classification model is trained with this behavior.
        # TODO Fix this bug and retrain the model
        # expected = "Level 1 Level 2"
        expected = 'Level 1\n                Level 2'
        self.assertEqual(outer_ul.text.strip(), expected, '嵌套列表未正确合并')
        self.assertEqual(len(outer_ul), 0, '子元素未删除')

        # 验证内层ul是否已被删除
        inner_ul = outer_ul.find('.//ul')
        self.assertIsNone(inner_ul, '嵌套列表未被处理')

    def test_multiple_list_types(self):
        html_str = """
        <div>
            <ul><li>Unordered</li></ul>
            <ol><li>Ordered</li></ol>
            <dl><dt>Term</dt></dl>
        </div>
        """
        element = document_fromstring(html_str)
        processed = merge_list(element)

        for tag in ['ul', 'ol', 'dl']:
            list_elem = processed.find(f'.//{tag}')
            self.assertIsNotNone(list_elem, f'{tag}元素不存在')
            self.assertTrue(
                list_elem.text.strip() in ['Unordered', 'Ordered', 'Term'],
                '文本内容错误',
            )
            self.assertEqual(len(list_elem), 0, '子元素未删除')


if __name__ == '__main__':
    unittest.main()
