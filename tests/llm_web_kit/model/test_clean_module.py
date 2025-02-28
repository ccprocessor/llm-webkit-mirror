import unittest
from unittest import TestCase
from unittest.mock import patch

# 需要根据实际模块路径调整
from llm_web_kit.model.clean_module import (CleanModule, CleanModuleDataPack,
                                            check_type)
from llm_web_kit.model.quality_model import QualityFilter


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


class TestCleanModuleDataPack(TestCase):
    def test_init_type_checks(self):
        """测试初始化时的类型检查."""
        valid_args = {
            'content_str': 'test',
            'language': 'en',
            'language_details': 'details',
            'content_style': 'article',
        }

        # 测试所有参数的正确类型
        try:
            CleanModuleDataPack(**valid_args)
        except TypeError:
            self.fail('Type check failed for valid types')

        # 逐个测试每个参数的类型错误
        for param in valid_args:
            invalid_args = valid_args.copy()
            invalid_args[param] = 123  # 故意设置错误类型
            with self.assertRaises(TypeError):
                CleanModuleDataPack(**invalid_args)

    def test_set_process_result(self):
        """测试设置处理结果的功能."""
        data_pack = CleanModuleDataPack('test', 'en', 'details', 'article')

        # 测试正确类型
        data_pack.set_process_result(False, {'key': 'value'})
        self.assertFalse(data_pack.clean_remained)
        self.assertEqual(data_pack.clean_infos, {'key': 'value'})

        # 测试错误类型
        with self.assertRaises(TypeError):
            data_pack.set_process_result('not_bool', {'key': 'value'})

        with self.assertRaises(TypeError):
            data_pack.set_process_result(False, 'not_dict')

    def test_get_output(self):
        """测试输出字典的生成."""
        data_pack = CleanModuleDataPack('test', 'en', 'details', 'article')
        data_pack.set_process_result(False, {'info': 'test'})

        expected_output = {'clean_remained': False, 'clean_infos': {'info': 'test'}}
        self.assertDictEqual(data_pack.get_output(), expected_output)


class TestCleanModule(TestCase):
    @patch.object(QualityFilter, 'filter')
    def test_process_core(self, mock_filter):
        """测试核心处理流程."""
        # 设置模拟返回值
        mock_filter.return_value = (False, {'reason': 'test'})

        # 初始化测试对象
        clean_module = CleanModule(prod=True)
        data_pack = CleanModuleDataPack('test', 'en', 'details', 'article')

        # 执行核心处理
        result = clean_module.process_core(data_pack)

        # 验证过滤方法被正确调用
        mock_filter.assert_called_once_with('test', 'en', 'details', 'article')
        # 验证处理结果设置正确
        self.assertFalse(result.clean_remained)
        self.assertEqual(result.clean_infos, {'reason': 'test'})

    @patch.object(QualityFilter, 'filter')
    def test_process_flow(self, mock_filter):
        """测试完整处理流程."""
        mock_filter.return_value = (True, {'quality': 0.95})

        clean_module = CleanModule(prod=False)
        result = clean_module.process(
            content_str='content',
            language='en',
            language_details='details',
            content_style='article',
        )

        expected_result = {'clean_remained': True, 'clean_infos': {'quality': 0.95}}
        self.assertDictEqual(result, expected_result)

    def test_production_mode_effect(self):
        """测试生产模式的影响."""
        # 根据实际业务逻辑补充测试
        # 当前代码中prod参数未实际使用，需要根据具体实现调整
        pass

    def test_get_version(self):
        """测试版本获取."""
        clean_module = CleanModule(prod=True)
        self.assertEqual(clean_module.get_version(), '1.0.0')


if __name__ == '__main__':
    unittest.main()
