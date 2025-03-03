import unittest
from unittest import TestCase
from unittest.mock import patch

from llm_web_kit.model.domain_safety_detector import DomainFilter
# 需要根据实际模块路径调整
from llm_web_kit.model.rule_based_safety_module import (
    RuleBasedSafetyModule, RuleBasedSafetyModuleDataPack, check_type)
from llm_web_kit.model.source_safety_detector import SourceFilter
from llm_web_kit.model.unsafe_words_detector import UnsafeWordsFilter


class TestCheckType(TestCase):
    def test_type_checking(self):
        """测试类型检查工具函数."""
        # 测试类型匹配的情况
        try:
            check_type('test', 'string', str)
        except TypeError:
            self.fail('Valid type check failed')

        # 测试类型不匹配的情况
        with self.assertRaises(TypeError) as cm:
            check_type('test', 123, str)

        expected_error = (
            "The type of test should be <class 'str'>, but got <class 'int'>"
        )
        self.assertEqual(str(cm.exception), expected_error)


class TestRuleBasedSafetyModuleDataPack(TestCase):
    def test_init_type_checks(self):
        """测试初始化时的类型检查."""
        valid_args = {
            'content_str': 'test',
            'language': 'en',
            'language_details': 'details',
            'content_style': 'article',
            'url': 'http://test.com',
            'dataset_name': 'test_dataset',
        }

        # 测试所有参数的正确类型
        try:
            RuleBasedSafetyModuleDataPack(**valid_args)
        except TypeError:
            self.fail('Type check failed for valid types')

        # 逐个测试每个参数的类型错误
        for param in valid_args:
            invalid_args = valid_args.copy()
            invalid_args[param] = 123  # 故意设置错误类型
            with self.assertRaises(TypeError):
                RuleBasedSafetyModuleDataPack(**invalid_args)

    def test_set_process_result(self):
        """测试设置处理结果的功能."""
        data_pack = RuleBasedSafetyModuleDataPack('test', 'en', 'details', 'article','http://test.com', 'test_dataset')

        # 测试正确类型
        data_pack.set_process_result(False, {'key': 'value'})
        self.assertFalse(data_pack.safety_remained)
        self.assertEqual(data_pack.safety_infos, {'key': 'value'})

        # 测试错误类型
        with self.assertRaises(TypeError):
            data_pack.set_process_result('not_bool', {'key': 'value'})

        with self.assertRaises(TypeError):
            data_pack.set_process_result(False, 'not_dict')

    def test_get_output(self):
        """测试输出字典的生成."""
        data_pack = RuleBasedSafetyModuleDataPack('test', 'en', 'details', 'article','http://test.com', 'test_dataset')
        data_pack.set_process_result(False, {'info': 'test'})

        expected_output = {'safety_remained': False, 'safety_infos': {'info': 'test'}}
        self.assertDictEqual(data_pack.get_output(), expected_output)


class TestRuleBasedSafetyModule(TestCase):
    @patch.object(DomainFilter,'filter')
    @patch.object(SourceFilter,'filter')
    @patch.object(UnsafeWordsFilter,'filter')
    def test_process_core(self, mock_unsafe_words_filter, mock_source_filter, mock_domain_filter):
        """测试核心处理流程."""
        # 设置模拟返回值
        mock_source_filter.return_value = {'from_safe_source': False, 'from_domestic_source': False}
        mock_domain_filter.return_value = (True, {})
        mock_unsafe_words_filter.return_value = (False, {'reason': 'test'})

        # 初始化测试对象
        safety_module = RuleBasedSafetyModule(prod=True)
        data_pack = RuleBasedSafetyModuleDataPack('test', 'en', 'details', 'article','http://test.com', 'test_dataset')

        # 执行核心处理
        result = safety_module.process_core(data_pack)

        # 验证过滤方法被正确调用
        mock_unsafe_words_filter.assert_called_once_with('test', 'en', 'details', 'article', False, False)
        # 验证处理结果设置正确
        self.assertFalse(result.safety_remained)
        self.assertEqual(result.safety_infos, {'reason': 'test'})

    @patch.object(DomainFilter,'filter')
    @patch.object(SourceFilter,'filter')
    @patch.object(UnsafeWordsFilter,'filter')
    def test_process_flow(self, mock_unsafe_words_filter, mock_source_filter, mock_domain_filter):
        """测试完整处理流程."""
        mock_source_filter.return_value = {'from_safe_source': False, 'from_domestic_source': False}
        mock_domain_filter.return_value = (True, {})
        mock_unsafe_words_filter.return_value = (True, {})

        safety_module = RuleBasedSafetyModule(prod=False)
        result = safety_module.process(
            content_str='content',
            language='en',
            language_details='details',
            content_style='article',
            url='http://test.com',
            dataset_name='test_dataset',
        )

        expected_result = {'safety_remained': True, 'safety_infos': {}}
        self.assertDictEqual(result, expected_result)

    def test_production_mode_effect(self):
        """测试生产模式的影响."""
        # 根据实际业务逻辑补充测试
        # 当前代码中prod参数未实际使用，需要根据具体实现调整
        pass

    def test_get_version(self):
        """测试版本获取."""
        safety_module = RuleBasedSafetyModule(prod=True)
        self.assertEqual(safety_module.get_version(), '1.0.0')


if __name__ == '__main__':
    unittest.main()
