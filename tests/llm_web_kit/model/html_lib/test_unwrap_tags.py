import unittest

from lxml import html

from llm_web_kit.model.html_lib.unwrap_tags import (  # 替换为实际模块路径
    build_tags_to_unwrap_map, get_all_tags_to_unwrap, unwrap_all_tags)


class TestBuildTagsToUnwrapMap(unittest.TestCase):
    def test_map_structure(self):
        """测试标签分类映射结构是否正确."""
        tag_map = build_tags_to_unwrap_map()
        # 验证存在预期的分类键
        self.assertIn('inline_text_semantics', tag_map)
        self.assertIn('demarcating_edits:', tag_map)  # 注意原代码中的冒号可能是个笔误
        # 验证分类数量是否正确
        self.assertEqual(len(tag_map), 2)

    def test_tag_inclusion(self):
        """测试关键标签是否包含在对应分类中."""
        tag_map = build_tags_to_unwrap_map()
        inline_tags = tag_map['inline_text_semantics']
        # 验证常见内联标签存在
        self.assertIn('a', inline_tags)
        self.assertIn('br', inline_tags)
        self.assertIn('span', inline_tags)
        # 验证特殊分类标签存在
        self.assertIn('ins', tag_map['demarcating_edits:'])


class TestGetAllTagsToUnwrap(unittest.TestCase):
    def test_tag_collection(self):
        """测试是否合并所有分类标签."""
        all_tags = get_all_tags_to_unwrap()
        tag_map = build_tags_to_unwrap_map()
        expected_length = sum(len(v) for v in tag_map.values())
        # 验证总标签数量正确
        self.assertEqual(len(all_tags), expected_length)
        # 验证分类标签都包含在内
        self.assertIn('a', all_tags)
        self.assertIn('ins', all_tags)
        # 验证没有重复标签（假设原始数据无重复）
        self.assertEqual(len(all_tags), len(set(all_tags)))


class TestUnwrapAllTags(unittest.TestCase):
    def test_single_tag_unwrapping(self):
        """测试单个标签解包."""
        original = '<div><b>bold text</b></div>'
        expected = '<div>bold text</div>'
        self._test_unwrap(original, expected)

    def test_nested_tags_unwrapping(self):
        """测试嵌套标签解包."""
        original = '<p><a><span>nested</span></a></p>'
        expected = '<p>nested</p>'
        self._test_unwrap(original, expected)

    def test_mixed_content_unwrapping(self):
        """测试混合内容解包."""
        original = '<div>Text <i>italic</i> and <b>bold</b></div>'
        expected = '<div>Text italic and bold</div>'
        self._test_unwrap(original, expected)

    def test_self_closing_tag_unwrapping(self):
        """测试自闭合标签解包."""
        original = '<div>Line<br/>break</div>'
        expected = '<div>Linebreak</div>'
        self._test_unwrap(original, expected)

    def test_tail_preservation(self):
        """测试标签后文本保留."""
        original = '<div>Hello<sup>1</sup>World</div>'
        expected = '<div>Hello1World</div>'
        self._test_unwrap(original, expected)

    def test_special_category_tag(self):
        """测试特殊分类标签解包."""
        original = '<div><ins>inserted text</ins></div>'
        expected = '<div>inserted text</div>'
        self._test_unwrap(original, expected)

    def test_attribute_removal(self):
        """测试标签属性移除."""
        original = '<div><a href="/link">link</a></div>'
        expected = '<div>link</div>'
        self._test_unwrap(original, expected)

    def _test_unwrap(self, original, expected, check_strict=True):
        """解包测试辅助函数."""
        root = html.fromstring(original)
        processed = unwrap_all_tags(root)
        result = html.tostring(processed, encoding='unicode').replace('\n', '')

        # 宽松模式：仅检查是否包含预期文本
        if not check_strict:
            self.assertIn(expected, result)
        else:
            # 严格模式：检查完整结构
            self.assertEqual(result.strip(), expected)


if __name__ == '__main__':
    unittest.main(verbosity=1)
