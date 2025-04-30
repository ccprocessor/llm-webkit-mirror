import json
import os
import unittest

from llm_web_kit.input.pre_data_json import PreDataJson
from llm_web_kit.main_html_parser.processor import (AbstractProcessor,
                                                    NoOpProcessor)


class MockProcessor(AbstractProcessor):
    """测试用的主处理器."""

    def __init__(self, config=None, **kwargs):
        super().__init__(config=config)
        self.process_called = False

    def _filter_by_rule(self, pre_data: PreDataJson) -> bool:
        """始终返回True表示需要处理."""
        return True

    def _do_process(self, pre_data: PreDataJson) -> PreDataJson:
        """实现主处理逻辑."""
        self.process_called = True
        pre_data['processor_executed'] = True
        return pre_data

    def get_name(self) -> str:
        return 'TestProcessor'


# 简单的处理器链实现，用于测试
class MockProcessorChain:
    """简单的处理器链实现，用于测试."""

    def __init__(self, config=None):
        self.config = config or {}
        self.pre_processors = []
        self.processors = []
        self.post_processors = []

        if config:
            processor_pipe = config.get('processor_pipe', {})
            for proc_config in processor_pipe.get('processor', []):
                if proc_config.get('enable', False):
                    python_class = proc_config.get('python_class')
                    if python_class == 'tests.llm_web_kit.main_html_parser.processor.test_processor_chain_normal.TestProcessor':
                        self.processors.append(MockProcessor(config=proc_config))

    def process(self, pre_data: PreDataJson) -> PreDataJson:
        """执行整个处理链."""
        for processor in self.processors:
            pre_data = processor.process(pre_data)

        return pre_data


# 测试工厂类
class TestProcessorSimpleFactory:
    """测试用的处理器链工厂类."""

    @staticmethod
    def create(config):
        """创建处理器链实例."""
        # 如果传入的是文件路径，读取配置
        if isinstance(config, str):
            with open(config, 'r') as f:
                config = json.load(f)

        return MockProcessorChain(config)


class TestProcessorChainNormal(unittest.TestCase):
    """测试处理器链的正常流程."""

    def setUp(self):
        """准备测试环境."""
        # 创建测试配置
        self.config = {
            'processor_pipe': {
                'processor': [
                    {
                        'enable': True,
                        'python_class': 'tests.llm_web_kit.main_html_parser.processor.test_processor_chain_normal.TestProcessor',
                        'class_init_kwargs': {}
                    }
                ]
            }
        }

        # 创建测试预处理数据
        self.pre_data = PreDataJson()
        self.pre_data['typical_raw_html'] = '<html><body>Test HTML</body></html>'

        # 使用我们自己的工厂和处理器链实现
        self.factory = TestProcessorSimpleFactory

    def test_processor_chain_creation(self):
        """测试处理器链的创建."""
        processor_chain = self.factory.create(self.config)
        self.assertIsInstance(processor_chain, MockProcessorChain)

    def test_processor_chain_process(self):
        """测试处理器链的处理过程."""
        processor_chain = self.factory.create(self.config)
        result_data = processor_chain.process(self.pre_data)

        # 验证所有处理器都被执行
        self.assertTrue(result_data.get('processor_executed', False), '主处理器未被执行')

    def test_processor_chain_with_disable_processor(self):
        """测试禁用某些处理器."""
        # 禁用预处理器
        self.config['processor_pipe']['processor'][0]['enable'] = False
        processor_chain = self.factory.create(self.config)
        result_data = processor_chain.process(self.pre_data)

        self.assertFalse(result_data.get('processor_executed', False), '主处理器未被执行')

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
        original_process = MockProcessor._do_process

        MockProcessor._do_process = record_execution('main')(original_process)

        processor_chain = self.factory.create(self.config)
        result_data = processor_chain.process(self.pre_data)

        # 恢复原始方法
        MockProcessor._do_process = original_process

        self.assertEqual(result_data.get('execution_order', []), ['main'],
                        '处理器执行顺序不正确')

    def test_processor_chain_from_file(self):
        """测试从配置文件创建处理器链."""
        # 将配置写入临时文件
        temp_config_file = 'temp_config.json'
        try:
            with open(temp_config_file, 'w') as f:
                json.dump(self.config, f)

            # 从文件创建处理器链
            processor_chain = self.factory.create(temp_config_file)
            result_data = processor_chain.process(self.pre_data)

            # 验证所有处理器都被执行
            self.assertTrue(result_data.get('processor_executed', False), '主处理器未被执行')
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

        processor_chain = self.factory.create(self.config)
        result_data = processor_chain.process(self.pre_data)

        # 验证所有处理器都被执行
        self.assertTrue(result_data.get('processor_executed', False), '主处理器未被执行')

    def test_filter_by_rule(self):
        """测试过滤规则功能."""
        # 创建一个总是返回False的过滤规则
        class FilteringProcessor(AbstractProcessor):
            def _filter_by_rule(self, pre_data: PreDataJson) -> bool:
                return False

            def _do_process(self, pre_data: PreDataJson) -> PreDataJson:
                pre_data['filtering_processor_executed'] = True
                return pre_data

        processor = FilteringProcessor()
        test_data = PreDataJson()
        test_data['typical_raw_html'] = self.pre_data['typical_raw_html']
        result = processor.process(test_data)

        # 验证处理方法没有被执行
        self.assertFalse(result.get('filtering_processor_executed', False), '过滤后的处理器被执行了')

    def test_noop_processor(self):
        """测试NoOp处理器."""
        processor = NoOpProcessor()
        original_data = PreDataJson()
        original_data['test_key'] = 'test_value'
        original_data_dict = {key: original_data[key] for key in original_data.keys()}

        result = processor.process(original_data)

        # 验证数据没有变化
        for key in original_data_dict:
            self.assertEqual(original_data_dict[key], result[key], 'NoOp处理器改变了数据')

    def test_processor_chain_with_error(self):
        """测试处理过程中发生错误."""
        # 添加一个会抛出异常的预处理器
        class ErrorProcessor(AbstractProcessor):
            def _filter_by_rule(self, pre_data: PreDataJson) -> bool:
                return True

            def _do_process(self, pre_data: PreDataJson) -> PreDataJson:
                raise ValueError('测试错误：处理失败')

        # 创建一个包含错误处理器的配置
        config = {
            'processor_pipe': {
                'processor': [
                    {
                        'enable': True,
                        'python_class': 'tests.llm_web_kit.main_html_parser.processor.test_processor_chain_normal.ErrorProcessor'
                    }
                ]
            }
        }

        # 自定义一个会抛出异常的处理器链
        class ErrorProcessorChain(MockProcessorChain):
            def __init__(self, config):
                super().__init__(config)
                self.processors = [ErrorProcessor()]

        # 自定义一个返回错误处理器链的工厂
        class ErrorFactory:
            @staticmethod
            def create(config):
                return ErrorProcessorChain(config)

        with self.assertRaises(ValueError) as context:
            processor_chain = ErrorFactory.create(config)
            processor_chain.process(self.pre_data)

        self.assertIn('测试错误', str(context.exception), '错误消息不包含预期内容')
