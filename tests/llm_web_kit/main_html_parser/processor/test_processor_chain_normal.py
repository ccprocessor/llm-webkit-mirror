#!/usr/bin/env python

"""处理器链正常流程的测试用例."""

import json
import os
import unittest
from unittest.mock import patch

from llm_web_kit.input.pre_data_json import PreDataJson
from llm_web_kit.main_html_parser.processor import (AbstractMainHtmlProcessor,
                                                    AbstractPostProcessor,
                                                    AbstractPreProcessor)
from llm_web_kit.main_html_parser.processor_chain import (
    HtmlProcessorSimpleFactory, MainHtmlProcessorChain)


class TestPreProcessor(AbstractPreProcessor):
    """测试用的预处理器."""

    def __init__(self, config=None, **kwargs):
        super().__init__(config=config)
        self.pre_process_called = False

    def pre_process(self, pre_data: PreDataJson) -> PreDataJson:
        self.pre_process_called = True
        pre_data['pre_processor_executed'] = True
        return pre_data

    def get_name(self) -> str:
        return 'TestPreProcessor'


class TestProcessor(AbstractMainHtmlProcessor):
    """测试用的主处理器."""

    def __init__(self, config=None, **kwargs):
        super().__init__(config=config)
        self.process_called = False

    def process(self, pre_data: PreDataJson) -> PreDataJson:
        self.process_called = True
        pre_data['processor_executed'] = True
        return pre_data

    def get_name(self) -> str:
        return 'TestProcessor'


class TestPostProcessor(AbstractPostProcessor):
    """测试用的后处理器."""

    def __init__(self, config=None, **kwargs):
        super().__init__(config=config)
        self.post_process_called = False

    def post_process(self, pre_data: PreDataJson) -> PreDataJson:
        self.post_process_called = True
        pre_data['post_processor_executed'] = True
        return pre_data

    def get_name(self) -> str:
        return 'TestPostProcessor'


class TestProcessorChainNormal(unittest.TestCase):
    """测试处理器链的正常流程."""

    def setUp(self):
        """准备测试环境."""
        # 创建测试配置
        self.config = {
            'global_config': {
                'logging_level': 'INFO',
                'timeout': 30
            },
            'processor_pipe': {
                'pre_processor': [
                    {
                        'enable': True,
                        'python_class': 'tests.llm_web_kit.main_html_parser.processor.test_processor_chain_normal.TestPreProcessor',
                        'class_init_kwargs': {}
                    }
                ],
                'processor': [
                    {
                        'enable': True,
                        'python_class': 'tests.llm_web_kit.main_html_parser.processor.test_processor_chain_normal.TestProcessor',
                        'class_init_kwargs': {}
                    }
                ],
                'post_processor': [
                    {
                        'enable': True,
                        'python_class': 'tests.llm_web_kit.main_html_parser.processor.test_processor_chain_normal.TestPostProcessor',
                        'class_init_kwargs': {}
                    }
                ]
            }
        }

        # 创建测试预处理数据
        self.pre_data = PreDataJson()
        self.pre_data['typical_raw_html'] = '<html><body>Test HTML</body></html>'

    def test_processor_chain_creation(self):
        """测试处理器链的创建."""
        processor_chain = HtmlProcessorSimpleFactory.create(self.config)
        self.assertIsInstance(processor_chain, MainHtmlProcessorChain)

    def test_processor_chain_process(self):
        """测试处理器链的处理过程."""
        processor_chain = HtmlProcessorSimpleFactory.create(self.config)
        result_data = processor_chain.process(self.pre_data)

        # 验证所有处理器都被执行
        self.assertTrue(result_data.get('pre_processor_executed', False), '预处理器未被执行')
        self.assertTrue(result_data.get('processor_executed', False), '主处理器未被执行')
        self.assertTrue(result_data.get('post_processor_executed', False), '后处理器未被执行')

    def test_processor_chain_with_disable_processor(self):
        """测试禁用某些处理器."""
        # 禁用预处理器
        self.config['processor_pipe']['pre_processor'][0]['enable'] = False
        processor_chain = HtmlProcessorSimpleFactory.create(self.config)
        result_data = processor_chain.process(self.pre_data)

        # 验证预处理器未被执行，其他处理器被执行
        self.assertFalse(result_data.get('pre_processor_executed', False), '禁用的预处理器被执行了')
        self.assertTrue(result_data.get('processor_executed', False), '主处理器未被执行')
        self.assertTrue(result_data.get('post_processor_executed', False), '后处理器未被执行')

    def test_processor_chain_execution_order(self):
        """测试处理器链的执行顺序."""
        # 创建带执行顺序记录的配置
        self.pre_data['execution_order'] = []

        # 使用装饰器记录执行顺序
        def record_execution(processor_type):
            def decorator(func):
                def wrapper(self, pre_data):
                    pre_data['execution_order'].append(processor_type)
                    return func(self, pre_data)
                return wrapper
            return decorator

        # 应用装饰器到测试处理器
        TestPreProcessor.pre_process = record_execution('pre')(TestPreProcessor.pre_process)
        TestProcessor.process = record_execution('main')(TestProcessor.process)
        TestPostProcessor.post_process = record_execution('post')(TestPostProcessor.post_process)

        processor_chain = HtmlProcessorSimpleFactory.create(self.config)
        result_data = processor_chain.process(self.pre_data)

        # 验证执行顺序：预处理器 -> 主处理器 -> 后处理器
        self.assertEqual(result_data.get('execution_order', []), ['pre', 'main', 'post'],
                        '处理器执行顺序不正确')

    def test_processor_chain_from_file(self):
        """测试从配置文件创建处理器链."""
        # 将配置写入临时文件
        temp_config_file = 'temp_config.json'
        try:
            with open(temp_config_file, 'w') as f:
                json.dump(self.config, f)

            # 从文件创建处理器链
            processor_chain = HtmlProcessorSimpleFactory.create(temp_config_file)
            result_data = processor_chain.process(self.pre_data)

            # 验证所有处理器都被执行
            self.assertTrue(result_data.get('pre_processor_executed', False), '预处理器未被执行')
            self.assertTrue(result_data.get('processor_executed', False), '主处理器未被执行')
            self.assertTrue(result_data.get('post_processor_executed', False), '后处理器未被执行')
        finally:
            # 清理临时文件
            if os.path.exists(temp_config_file):
                os.remove(temp_config_file)

    def test_processor_chain_with_multiple_processors(self):
        """测试多个处理器的执行."""
        # 添加多个处理器
        self.config['processor_pipe']['processor'].append({
            'enable': True,
            'python_class': 'tests.llm_web_kit.main_html_parser.processor.test_processor_chain_normal.TestProcessor',
            'class_init_kwargs': {}
        })

        processor_chain = HtmlProcessorSimpleFactory.create(self.config)
        result_data = processor_chain.process(self.pre_data)

        # 验证所有处理器都被执行
        self.assertTrue(result_data.get('pre_processor_executed', False), '预处理器未被执行')
        self.assertTrue(result_data.get('processor_executed', False), '主处理器未被执行')
        self.assertTrue(result_data.get('post_processor_executed', False), '后处理器未被执行')

    @patch('llm_web_kit.libs.class_loader.load_python_class_by_name')
    def test_processor_chain_with_error(self, mock_load_class):
        """测试处理过程中发生错误."""
        # 模拟加载类失败
        mock_load_class.side_effect = ImportError('测试错误：无法加载类')

        with self.assertRaises(Exception) as context:
            HtmlProcessorSimpleFactory.create(self.config)

        self.assertIn('测试错误', str(context.exception), '错误消息不包含预期内容')


if __name__ == '__main__':
    unittest.main()
