import unittest

from lxml import html

from llm_web_kit.model.html_lib.remove_tags import (
    all_tag_list_to_remove, build_tags_to_remove_map, is_blank_tag,
    is_diplay_none, remove_all_tags, remove_blank_tags_recursive,
    remove_invisible_tags, remove_tags)


class TestBuildTagsToRemoveMap(unittest.TestCase):
    def test_map_structure(self):
        tags_map = build_tags_to_remove_map()
        # 验证基础分类键存在
        self.assertIn('document_metadata', tags_map)
        self.assertIn('script', tags_map)
        # 验证具体标签归属
        self.assertIn('iframe', tags_map['embed'])
        self.assertIn('form', tags_map['form'])
        self.assertIn('canvas', tags_map['script'])


class TestAllTagListToRemove(unittest.TestCase):
    def test_tag_aggregation(self):
        all_tags = all_tag_list_to_remove()
        tags_map = build_tags_to_remove_map()
        expected = []
        for v in tags_map.values():
            expected.extend(v)
        # 验证总数一致且包含关键标签
        self.assertEqual(len(all_tags), len(expected))
        self.assertIn('iframe', all_tags)
        self.assertIn('noscript', all_tags)


class TestRemoveTags(unittest.TestCase):
    def setUp(self):
        self.sample_html = """
        <html>
            <script>content</script>
            <style>style</style>
            <form><input></form>
            <iframe></iframe>
            <p>保留内容</p>
        </html>
        """
        self.root = html.fromstring(self.sample_html)

    def test_remove_single_category(self):
        # 测试移除script相关标签
        new_root = remove_tags(self.root, ['script'])
        self.assertEqual(len(new_root.findall('.//script')), 0)
        self.assertGreater(len(new_root.findall('.//form')), 0)

    def test_remove_multiple_categories(self):
        # 同时移除表单和嵌入式内容
        new_root = remove_tags(self.root, ['form', 'embed'])
        self.assertEqual(len(new_root.findall('.//form')), 0)
        self.assertEqual(len(new_root.findall('.//embed')), 0)
        self.assertGreater(len(new_root.findall('.//p')), 0)

    def test_remove_nested_tags(self):
        # 测试嵌套标签移除
        html_content = (
            '<html><body><div><form><button></button></form></div></body></html>'
        )
        root = html.fromstring(html_content)
        new_root = remove_tags(root, ['form'])
        self.assertEqual(len(new_root.findall('.//form')), 0)
        self.assertIsNotNone(new_root.find('.//div'))


class TestRemoveAllTags(unittest.TestCase):
    def test_full_removal(self):
        html_content = """
        <div>
            <script></script>
            <iframe></iframe>
            <form></form>
            <svg></svg>
            <p>保留内容</p>
        </div>
        """
        root = html.fromstring(html_content)
        new_root = remove_all_tags(root)
        # 验证黑名单标签已移除
        self.assertEqual(len(new_root.findall('.//script')), 0)
        self.assertEqual(len(new_root.findall('.//iframe')), 0)
        # 验证非黑名单标签保留
        self.assertGreater(len(new_root.findall('.//p')), 0)


class TestIsDisplayNone(unittest.TestCase):
    def test_display_detection(self):
        # 标准display:none检测
        element = html.fromstring('<div style="display: none"></div>')
        self.assertTrue(is_diplay_none(element))

    def test_case_insensitive(self):
        # 大小写不敏感检测
        element = html.fromstring('<div style="DISPLAY:NONE"></div>')
        self.assertTrue(is_diplay_none(element))

    def test_partial_match(self):
        # 不匹配部分匹配的情况
        element = html.fromstring('<div style="display: none_"></div>')
        self.assertTrue(is_diplay_none(element))


class TestRemoveInvisibleTags(unittest.TestCase):
    def test_invisible_removal(self):
        html_content = """
        <div>
            <p style="display:none">隐藏内容</p>
            <span style="display: none">隐藏span</span>
            <div>可见内容</div>
        </div>
        """
        root = html.fromstring(html_content)
        new_root = remove_invisible_tags(root)
        # 验证隐藏元素已移除
        self.assertEqual(len(new_root.findall('.//p')), 0)
        self.assertIsNotNone(new_root.find('.//div'))


class TestIsBlankTag(unittest.TestCase):
    def test_img_tag(self):
        # 图片标签永远不空白
        element = html.fromstring('<img src="test.jpg">')
        self.assertFalse(is_blank_tag(element))

    def test_plain_text(self):
        # 包含真实文本
        element = html.fromstring('<div>真实内容</div>')
        self.assertFalse(is_blank_tag(element))

    def test_nested_blank(self):
        # 多层空白结构
        element = html.fromstring('<div><span><em></em></span></div>')
        self.assertTrue(is_blank_tag(element))

    def test_tail_text(self):
        # 包含尾部文本的情况
        element = html.fromstring('<div><span></span>尾部文本</div>')
        self.assertFalse(is_blank_tag(element))


class TestRemoveBlankTagsRecursive(unittest.TestCase):
    def test_shallow_removal(self):
        # 简单空白标签移除
        html_content = '<div><p>   </p></div>'
        root = html.fromstring(html_content)
        new_root = remove_blank_tags_recursive(root)
        self.assertEqual(len(new_root.findall('.//p')), 0)

    def test_deep_removal(self):
        # 深层嵌套空白标签
        html_content = """
        <div>
            <section>
                <article>
                    <p>  </p>
                </article>
            </section>
            <div></div>
        </div>
        """
        root = html.fromstring(html_content)
        new_root = remove_blank_tags_recursive(root)
        # 验证所有空白标签已移除
        self.assertEqual(len(new_root.findall('.//section')), 0)
        self.assertEqual(len(new_root.findall('.//div')), 0)

    def test_mixed_content(self):
        # 混合空白和非空白内容
        html_content = """
        <div>
            <p></p>
            <div>真实内容</div>
            <span>   </span>
        </div>
        """
        root = html.fromstring(html_content)
        new_root = remove_blank_tags_recursive(root)
        # 验证空白标签移除，保留有效内容
        self.assertEqual(len(new_root.findall('.//p')), 0)
        self.assertIsNotNone(new_root.find('.//div'))


if __name__ == '__main__':
    unittest.main()
