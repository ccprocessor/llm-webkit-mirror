#!/usr/bin/env python3
"""全面测试新的simple.py API，整合原有测试场景."""

import os
import unittest

from llm_web_kit.exception.exception import (InvalidExtractorTypeException,
                                             InvalidOutputFormatException)
from llm_web_kit.simple import (ExtractorFactory, ExtractorType, PipeType,
                                extract_content_from_html_with_layout_batch,
                                extract_content_from_html_with_llm,
                                extract_content_from_html_with_magic_html,
                                extract_content_from_main_html, extract_html,
                                extract_main_html_only)


class TestSimple(unittest.TestCase):
    """Simple API的全面测试用例."""

    def setUp(self):
        """设置测试数据."""
        self.url = 'https://example.com'
        self.html_content = '<html><body><h1>Test Content</h1><p>This is a test paragraph.</p><img src="https://example.com/image.jpg" alt="Test Image" /></body></html>'

        # 原有测试中的复杂HTML内容
        self.real_html_content = """
        <!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTML标签综合示例</title>

    <!-- 内嵌CSS样式 -->
    <style>
        /* 基础样式设置 */
        body {
            font-family: 'Microsoft YaHei', sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }

        /* 页眉样式 */
        header {
            background-color: #2c3e50;
            color: white;
            padding: 1rem;
            text-align: center;
        }

        /* 主体内容样式 */
        main {
            max-width: 800px;
            margin: 2rem auto;
            padding: 1rem;
            background: white;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        /* 交互按钮样式 */
        .action-btn {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 0.8rem 1.5rem;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        .action-btn:hover {
            background-color: #2980b9;
        }
    </style>
</head>
<body>
    <!-- 语义化页眉 -->
    <header>
        <h1>网页标题</h1>
        <nav>
            <ul style="list-style-type: none; display: flex; justify-content: center; gap: 1rem;">
                <li><a href="#" style="color: white; text-decoration: none;">首页</a></li>
                <li><a href="#" style="color: white; text-decoration: none;">关于</a></li>
            </ul>
        </nav>
    </header>

    <!-- 主体内容区域 -->
    <main>
        <article>
            <h2>文章标题</h2>
            <p>这是有效的文本内容，展示了如何在HTML文档中组织实际内容。</p>

            <!-- 带交互的元素 -->
            <button id="demoBtn" class="action-btn">点击演示</button>
            <div id="dynamicContent" style="margin-top: 1rem; display: none;">
                <p>这是通过JavaScript动态显示的内容！</p>
            </div>
        </article>
    </main>

    <!-- 页脚区域 -->
    <footer style="text-align: center; padding: 1rem; background-color: #34495e; color: white;">
        <p>© 2025 版权所有</p>
    </footer>

    <!-- 内嵌JavaScript -->
    <script>
        // 等待DOM加载完成
        document.addEventListener('DOMContentLoaded', function() {
            const demoBtn = document.getElementById('demoBtn');
            const dynamicContent = document.getElementById('dynamicContent');

            // 按钮点击事件处理
            demoBtn.addEventListener('click', function() {
                dynamicContent.style.display = 'block';
                this.textContent = '已显示内容';

                // 创建动态元素
                const newElement = document.createElement('p');
                newElement.textContent = '这是动态创建的元素！';
                newElement.style.color = '#e74c3c';
                dynamicContent.appendChild(newElement);
            });

            console.log('页面初始化完成');
        });
    </script>
</body>
</html>
        """

        self.main_html = '<div><body><h1>Test Content</h1><p>This is a test paragraph.</p><img src="https://example.com/image.jpg" alt="Test Image"></body></div>'
        self.expected_md = '# Test Content\n\nThis is a test paragraph.\n'
        self.expected_mm_md = '# Test Content\n\nThis is a test paragraph.\n\n![Test Image](e5db82b5bf63d49d80c5533616892d3386f43955369520986d67653c700fc53c)\n'
        self.base_path = os.path.dirname(os.path.abspath(__file__))

    # ========================================
    # 基础功能测试
    # ========================================

    def test_extract_html_to_md(self):
        """测试提取HTML到MD."""
        md = extract_content_from_html_with_magic_html(self.url, self.html_content)
        self.assertEqual(md, self.expected_md)

    def test_extract_html_to_mm_md(self):
        """测试提取HTML到MM_MD."""
        mm_md = extract_content_from_html_with_magic_html(self.url, self.html_content, 'mm_md')
        self.assertEqual(mm_md, self.expected_mm_md)

    def test_extract_magic_main_html(self):
        """测试提取main_html."""
        main_html = extract_main_html_only(self.url, self.html_content, PipeType.MAGIC_HTML)
        self.assertEqual(main_html, self.main_html)

    def test_extract_noclip(self):
        """测试从原始HTML直接提取内容."""
        # 对应原来的clip_html=False
        md = extract_content_from_main_html(self.url, self.html_content)
        self.assertEqual(md, self.expected_md)

    # ========================================
    # 测试核心方法 extract_html 的7种场景
    # ========================================

    def test_extract_html_stage1_magic_html(self):
        """测试第一阶段：MAGIC_HTML提取main_html."""
        result = extract_html(self.url, self.html_content, PipeType.MAGIC_HTML)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
        self.assertIn('<', result)
        self.assertIn('>', result)

    def test_extract_html_stage1_llm(self):
        """测试第一阶段：LLM提取main_html."""
        try:
            result = extract_html(self.url, self.html_content, PipeType.LLM)
            self.assertIsInstance(result, str)
        except Exception as e:
            # LLM解析器可能未实现，这是预期的
            self.assertTrue('待实现' in str(e) or 'not found' in str(e).lower() or 'ImportError' in str(e))

    def test_extract_html_stage1_layout_batch(self):
        """测试第一阶段：LAYOUT_BATCH提取main_html."""
        try:
            result = extract_html(self.url, self.html_content, PipeType.LAYOUT_BATCH)
            self.assertIsInstance(result, str)
        except Exception as e:
            # LAYOUT_BATCH解析器可能未实现，这是预期的
            self.assertTrue('待实现' in str(e) or 'not found' in str(e).lower() or 'ImportError' in str(e))

    def test_extract_html_stage2_noclip(self):
        """测试第二阶段：NOCLIP从main_html转换为markdown."""
        result = extract_html(self.url, self.main_html, PipeType.NOCLIP, 'md')
        self.assertEqual(result, self.expected_md)

    def test_extract_html_stage2_noclip_mm_md(self):
        """测试第二阶段：NOCLIP转换为mm_md格式."""
        result = extract_html(self.url, self.main_html, PipeType.NOCLIP, 'mm_md')
        self.assertEqual(result, self.expected_mm_md)

    def test_extract_html_both_stages_magic_html_noclip(self):
        """测试两阶段：MAGIC_HTML_NOCLIP."""
        result = extract_html(self.url, self.html_content, PipeType.MAGIC_HTML_NOCLIP, 'md')
        self.assertEqual(result, self.expected_md)

    def test_extract_html_both_stages_magic_html_noclip_mm_md(self):
        """测试两阶段：MAGIC_HTML_NOCLIP输出mm_md格式."""
        result = extract_html(self.url, self.html_content, PipeType.MAGIC_HTML_NOCLIP, 'mm_md')
        self.assertEqual(result, self.expected_mm_md)

    # ========================================
    # 测试对外方法
    # ========================================

    def test_extract_main_html_only_default(self):
        """测试对外方法：extract_main_html_only默认使用MAGIC_HTML."""
        result = extract_main_html_only(self.url, self.html_content)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
        self.assertIn('<', result)

    def test_extract_content_from_main_html_default(self):
        """测试对外方法：extract_content_from_main_html默认md格式."""
        result = extract_content_from_main_html(self.url, self.main_html)
        self.assertEqual(result, self.expected_md)

    def test_extract_content_from_main_html_mm_md(self):
        """测试对外方法：extract_content_from_main_html输出mm_md格式."""
        result = extract_content_from_main_html(self.url, self.main_html, 'mm_md')
        self.assertEqual(result, self.expected_mm_md)

    def test_extract_content_from_html_with_magic_html(self):
        """测试对外方法：extract_content_from_html_with_magic_html."""
        result = extract_content_from_html_with_magic_html(self.url, self.html_content)
        self.assertEqual(result, self.expected_md)

        result_mm = extract_content_from_html_with_magic_html(self.url, self.html_content, 'mm_md')
        self.assertEqual(result_mm, self.expected_mm_md)

    def test_extract_content_from_html_with_llm(self):
        """测试对外方法：extract_content_from_html_with_llm."""
        try:
            result = extract_content_from_html_with_llm(self.url, self.html_content)
            self.assertIsInstance(result, str)
        except Exception as e:
            # LLM解析器可能未实现，这是预期的
            self.assertTrue('待实现' in str(e) or 'not found' in str(e).lower() or 'ImportError' in str(e))

    def test_extract_content_from_html_with_layout_batch(self):
        """测试对外方法：extract_content_from_html_with_layout_batch."""
        try:
            result = extract_content_from_html_with_layout_batch(self.url, self.html_content)
            self.assertIsInstance(result, str)
        except Exception as e:
            # LAYOUT_BATCH解析器可能未实现，这是预期的
            self.assertTrue('待实现' in str(e) or 'not found' in str(e).lower() or 'ImportError' in str(e))

    # ========================================
    # 测试异常处理
    # ========================================

    def test_invalid_extractor_type_exception(self):
        """测试无效的extractor类型异常."""
        with self.assertRaises(InvalidExtractorTypeException) as context:
            ExtractorFactory.get_extractor('INVALID_TYPE', PipeType.MAGIC_HTML)

        self.assertIn('Invalid extractor type', str(context.exception.custom_message))
        self.assertEqual(context.exception.error_code, 81000000)

    def test_invalid_output_format_exception(self):
        """测试无效的输出格式异常."""
        with self.assertRaises(InvalidOutputFormatException) as context:
            extract_html(self.url, self.main_html, PipeType.NOCLIP, 'INVALID_FORMAT')

        self.assertIn('Invalid output format', str(context.exception.custom_message))
        self.assertEqual(context.exception.error_code, 82000000)

    # ========================================
    # 测试不同输出格式
    # ========================================

    def test_output_format_md(self):
        """测试md输出格式."""
        result = extract_html(self.url, self.main_html, PipeType.NOCLIP, 'md')
        self.assertEqual(result, self.expected_md)

    def test_output_format_mm_md(self):
        """测试mm_md输出格式."""
        result = extract_html(self.url, self.main_html, PipeType.NOCLIP, 'mm_md')
        self.assertEqual(result, self.expected_mm_md)

    def test_output_format_json(self):
        """测试json输出格式."""
        result = extract_html(self.url, self.main_html, PipeType.NOCLIP, 'json')
        self.assertIsInstance(result, str)
        # JSON输出应该包含JSON结构
        self.assertTrue(result.startswith('{') or result.startswith('['))

    # ========================================
    # 测试ExtractorFactory缓存机制
    # ========================================

    def test_extractor_factory_caching(self):
        """测试ExtractorFactory的缓存机制."""
        # 第一次获取
        extractor1 = ExtractorFactory.get_extractor(ExtractorType.HTML, PipeType.MAGIC_HTML)

        # 第二次获取应该返回同一个实例（从缓存）
        extractor2 = ExtractorFactory.get_extractor(ExtractorType.HTML, PipeType.MAGIC_HTML)

        self.assertIs(extractor1, extractor2, '应该返回同一个缓存的实例')

    def test_extractor_factory_different_pipe_types(self):
        """测试不同pipe_type会创建不同的extractor实例."""
        extractor1 = ExtractorFactory.get_extractor(ExtractorType.HTML, PipeType.MAGIC_HTML)
        extractor2 = ExtractorFactory.get_extractor(ExtractorType.HTML, PipeType.NOCLIP)

        self.assertIsNot(extractor1, extractor2, '不同pipe_type应该返回不同的实例')

    # ========================================
    # 测试边缘情况
    # ========================================

    def test_empty_html_content(self):
        """测试空HTML内容."""
        # 空HTML会导致解析异常，这是预期的行为
        with self.assertRaises(Exception):
            extract_html(self.url, '', PipeType.MAGIC_HTML)

    def test_empty_main_html_for_stage2(self):
        """测试空main_html用于第二阶段."""
        # 空main_html会导致解析异常，这是预期的行为
        with self.assertRaises(Exception):
            extract_html(self.url, '', PipeType.NOCLIP)

    def test_malformed_html(self):
        """测试格式错误的HTML."""
        malformed_html = '<html><body><h1>Test<p>No closing tags'
        result = extract_html(self.url, malformed_html, PipeType.MAGIC_HTML)
        self.assertIsInstance(result, str)

    # ========================================
    # 测试不同场景抽取内容符合预期
    # ========================================

    def test_extract_real_html_to_md(self):
        """测试真实HTML内容，验证JavaScript被过滤."""
        md = extract_content_from_main_html(self.url, self.real_html_content)
        self.assertNotIn('DOMContentLoaded', md)

    def test_extract_lack_item(self):
        """测试lack_item.html文件."""
        html_content = open(os.path.join(self.base_path, 'assets', 'lack_item.html'), 'r').read()
        md = extract_content_from_main_html(self.url, html_content)
        self.assertGreater(len(md), 0)

    def test_extract_lack_item_2(self):
        """测试lack_item_2.html文件."""
        html_content = open(os.path.join(self.base_path, 'assets', 'lack_item_2.html'), 'r').read()
        md = extract_content_from_main_html(self.url, html_content)
        # 验证提取到了主要内容
        self.assertIn('2001-2015 Physics Forums', md)

    def test_extract_word_press(self):
        """测试word_press.html文件."""
        html_content = open(os.path.join(self.base_path, 'assets', 'word_press.html'), 'r').read()
        md = extract_content_from_main_html(self.url, html_content)
        self.assertIn('For descriptions of the methods (AM1, HF, MP2, ...) a', md)

    def test_filter_display_none_content(self):
        """测试display:none的内容是否被正确过滤."""
        html_content = '''<html><body>
        <div class="options-div-0-0 option-box__items" style="display: none;">
            <span class="bedroom-rate__title">Room Only Rate</span>
            <span class="bedroom-rate__price">£1,230.00</span>
        </div>
        <p>正常内容</p>
        </body></html>'''

        # 使用MAGIC_HTML_NOCLIP模拟原来的clip_html=False
        md = extract_content_from_main_html(self.url, html_content)

        # 验证隐藏内容被过滤掉了
        self.assertNotIn('Room Only Rate', md)
        self.assertNotIn('£1,230.00', md)

        # 验证正常内容被保留
        self.assertIn('正常内容', md)

    # ========================================
    # 集成测试
    # ========================================

    def test_full_pipeline_integration(self):
        """测试完整的两阶段流水线."""
        # 第一阶段：提取main_html
        main_html = extract_main_html_only(self.url, self.real_html_content)
        self.assertIsInstance(main_html, str)
        self.assertTrue(len(main_html) > 0)

        # 第二阶段：从main_html提取内容
        markdown = extract_content_from_main_html(self.url, main_html)
        self.assertIsInstance(markdown, str)
        self.assertTrue(len(markdown) > 0)

        # 对比直接两阶段调用的结果
        direct_result = extract_content_from_html_with_magic_html(self.url, self.real_html_content)
        self.assertEqual(markdown, direct_result, "分步骤处理和直接处理的结果应该一致")

    def test_multiple_calls_consistency(self):
        """测试多次调用的一致性."""
        results = []
        for _ in range(3):
            result = extract_html(self.url, self.html_content, PipeType.MAGIC_HTML_NOCLIP)
            results.append(result)

        # 所有结果应该相同
        self.assertTrue(all(r == results[0] for r in results))


if __name__ == '__main__':
    unittest.main(verbosity=2)
