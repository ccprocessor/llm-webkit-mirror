import os
import unittest

from llm_web_kit.simple import (extract_html_to_md, extract_html_to_mm_md,
                                extract_main_html_by_maigic_html)


class TestSimple(unittest.TestCase):
    def setUp(self):
        self.url = 'https://example.com'
        self.html_content = '<html><body><h1>Test Content</h1><p>This is a test paragraph.</p><img src="https://example.com/image.jpg" alt="Test Image" /></body></html>'
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
        self.base_path = os.path.dirname(os.path.abspath(__file__))

    def test_extractor_factory(self):
        # Setup mocks
        md = extract_html_to_md(self.url, self.html_content)
        self.assertEqual(md, '# Test Content\n\nThis is a test paragraph.\n')

    def test_extract_html_to_mm_md(self):
        # Setup mock
        mm_md = extract_html_to_mm_md(self.url, self.html_content)
        self.assertEqual(mm_md, '# Test Content\n\nThis is a test paragraph.\n\n![Test Image](e5db82b5bf63d49d80c5533616892d3386f43955369520986d67653c700fc53c)\n')

    def test_extract_pure_html_to_md(self):
        md = extract_html_to_md(self.url, self.html_content, clip_html=True)
        self.assertEqual(md, '# Test Content\n\nThis is a test paragraph.\n')

    def test_extract_pure_html_to_mm_md(self):
        mm_md = extract_html_to_mm_md(self.url, self.html_content, clip_html=True)
        self.assertEqual(mm_md, '# Test Content\n\nThis is a test paragraph.\n\n![Test Image](e5db82b5bf63d49d80c5533616892d3386f43955369520986d67653c700fc53c)\n')

    def test_extract_magic_html(self):
        magic_html, title = extract_main_html_by_maigic_html(self.url, self.html_content)
        self.assertEqual(magic_html, '<div><body><h1>Test Content</h1><p>This is a test paragraph.</p><img src="https://example.com/image.jpg" alt="Test Image"></body></div>')

    def test_extract_real_html_to_md(self):
        md = extract_html_to_md(self.url, self.real_html_content, clip_html=False)
        assert 'DOMContentLoaded' not in md

    def test_extract_lack_item(self):
        html_content = open(os.path.join(self.base_path, 'assets', 'lack_item.html'), 'r').read()
        md = extract_html_to_md(self.url, html_content, clip_html=False)
        assert len(md) > 0

    def test_extract_lack_item_2(self):
        html_content = open(os.path.join(self.base_path, 'assets', 'lack_item_2.html'), 'r').read()
        md = extract_html_to_md(self.url, html_content, clip_html=False)
        assert '2001-2015 Physics Forums' in md
