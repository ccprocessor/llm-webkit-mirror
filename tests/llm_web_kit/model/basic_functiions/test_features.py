# flake8: noqa: E402
import math
import os
import sys
import unittest
from unittest.mock import patch

import numpy as np

current_file_path = os.path.abspath(__file__)
parent_dir_path = os.path.join(current_file_path, *[os.pardir] * 5)
normalized_path = os.path.normpath(parent_dir_path)
sys.path.append(normalized_path)

import llm_web_kit.model.basic_functions as bfuncs
from llm_web_kit.model.basic_functions.features import (
    content2lines, content2words, extract_formulas,
    formula_complexity_features, formula_count_features,
    formula_distribution_var, formula_type_ratios, get_content_len,
    get_content_len_without_space, get_lines_num, stats_continue_space,
    stats_entropy, stats_html_entity, stats_ngram_mini,
    stats_punctuation_end_sentence, stats_stop_words, stats_unicode)


class TestFeatures(unittest.TestCase):
    def setUp(self):
        # 公共测试数据
        self.sample_text = '这是一个测试文本。\n包含两行内容！\n'
        self.long_text = '   Hello   世界！   \nThis is a test text.\n' * 3
        self.empty_text = ''
        self.punctuation_text = '你好！这是一个测试。请问今天天气怎么样？'
        self.formulas_text = r"""Consider $E=mc^2$ and Maxwell's equations:
        $$\nabla \cdot \mathbf{E} = \frac{\rho}{\epsilon_0}$$
        Also $\int x^2 dx$ and matrix $\mathbf{A}\mathbf{B}$
        """

    # 测试文本长度相关函数
    def test_get_content_len(self):
        self.assertEqual(get_content_len(self.sample_text), 18)
        self.assertEqual(get_content_len(self.long_text), 117)
        self.assertEqual(get_content_len(self.empty_text), 0)

    def test_get_content_len_without_space(self):
        self.assertEqual(get_content_len_without_space('a b c'), 3)
        self.assertEqual(get_content_len_without_space('   '), 0)
        self.assertEqual(get_content_len_without_space('\n\t\r'), 0)

    # 测试文本行数相关函数
    def test_content2lines(self):
        self.assertEqual(content2lines('line1\nline2\n\nline3'), ['line1', 'line2', 'line3'])
        self.assertEqual(content2lines(self.empty_text), [])

    def test_get_lines_num(self):
        self.assertEqual(get_lines_num('line1\nline2'), 2)
        self.assertEqual(get_lines_num(self.empty_text), 0)

    # 测试分词相关函数
    @patch('llm_web_kit.model.basic_functions.features.jieba_lcut')
    def test_content2words(self, mock_jieba):
        mock_jieba.return_value = ['分词1', '分词2']
        self.assertEqual(content2words('测试分词'), ['分词1', '分词2'])
        self.assertEqual(content2words('test 123', alpha=True), [])

    # 测试连续空格统计
    def test_stats_continue_space(self):
        result = stats_continue_space('a   b    c')
        self.assertEqual(result['max_continue_space_num'], 4)
        result = stats_continue_space('no_space')
        self.assertEqual(result['max_continue_space_num'], 0)

    # 测试信息熵
    def test_stats_entropy(self):
        # 测试全相同字符
        result = stats_entropy('aaaaa')
        self.assertAlmostEqual(result['entropy'], 0.0, places=4)

        # 测试均匀分布
        text = 'abcd'
        p = 1 / 4
        expected = -4 * (p * math.log2(p))
        result = stats_entropy(text)
        self.assertAlmostEqual(result['entropy'], expected, places=4)

    # 测试标点结尾统计
    def test_stats_punctuation_end_sentence(self):
        with patch.object(bfuncs.character, 'get_common_punc_end_list') as mock_punc:
            mock_punc.return_value = ['！', '。', '？']
            result = stats_punctuation_end_sentence('你好！这是一个测试。最后一句')
            self.assertEqual(result['punc_end_sentence_num'], 2)

    # 测试停用词统计
    def test_stats_stop_words(self):
        with patch.object(bfuncs.word, 'get_stop_word_en_zh_set') as mock_stop:
            mock_stop.return_value = {'的', '是', 'a'}
            text = '这是一个的测试文本的a'
            result = stats_stop_words(text)
            self.assertEqual(result['stop_word_num'], 4)
            self.assertAlmostEqual(result['stop_word_frac'], 4 / 7, places=4)

    # 测试HTML实体统计
    def test_stats_html_entity(self):
        text = '&nbsp &amp; invalid &123'
        result = stats_html_entity(text)
        self.assertEqual(result['html_semi_entity_count'], 3)

    # 测试Unicode统计
    def test_stats_unicode(self):
        text = 'abc'
        result = stats_unicode(text)
        unicode_values = [97, 98, 99]
        expected_std = np.std(unicode_values)
        self.assertAlmostEqual(result['std_dev_unicode_value'], expected_std, places=4)

    # 测试ngram重复度
    def test_stats_ngram_mini(self):
        text = '重复 重复 重复 重复'
        result = stats_ngram_mini(text)
        self.assertGreater(result['dup_top_2gram'], 0.5)

    # 测试边界情况
    def test_edge_cases(self):
        # 空文本测试
        self.assertEqual(stats_entropy('')['entropy'], 0)
        self.assertEqual(stats_punctuation_end_sentence('')['punc_end_sentence_num'], 0)

        # 单字符测试
        result = stats_unicode('a')
        self.assertTrue(math.isnan(result['mean_diff_unicode_value']))

    # 测试 extract_formulas
    def test_extract_formulas(self):
        # 正常情况
        inline, block = extract_formulas(self.formulas_text)
        self.assertEqual(inline, ['E=mc^2', r'\int x^2 dx', r'\mathbf{A}\mathbf{B}'])
        self.assertEqual(block, [r'\nabla \cdot \mathbf{E} = \frac{\rho}{\epsilon_0}'])

        # 没有公式的情况
        inline_empty, block_empty = extract_formulas('No formulas here')
        self.assertEqual(inline_empty, [])
        self.assertEqual(block_empty, [])

        # 转义字符测试
        # escaped_text = r"Escaped \$not formula$ and real $formula$"
        # inline_esc, block_esc = extract_formulas(escaped_text)
        # self.assertEqual(inline_esc, ['formula'])

    # 测试 formula_count_features
    def test_formula_count_features(self):
        # 正常情况
        inline = ['a', 'b']
        block = ['c']
        features = formula_count_features(inline, block)
        self.assertEqual(features['inline_formula_count'], 2)
        self.assertEqual(features['block_formula_count'], 1)
        self.assertEqual(features['total_formula_count'], 3)

        # 空测试
        empty_features = formula_count_features([], [])
        self.assertEqual(empty_features['total_formula_count'], 0)

    # 测试 formula_complexity_features
    def test_formula_complexity_features(self):
        # 正常情况
        inline = [r'x + y = z', r'\sqrt{a}']
        block = [r'\frac{\partial f}{\partial x}']
        features = formula_complexity_features(inline, block)

        # 验证长度计算
        lengths = [9, 8, 29]
        expected_avg_len = sum(lengths) / 3
        self.assertAlmostEqual(features['average_formula_length'], expected_avg_len)

        # 验证操作符计数
        # x + y = z (+, =)
        # \sqrt{a} (sqrt)
        # \frac{\partial f}{\partial x} (frac, partial, partial)
        operator_counts = [2, 1, 1]
        expected_avg_ops = sum(operator_counts) / 3
        self.assertAlmostEqual(features['average_operator_count'], expected_avg_ops)

        # 空测试
        empty_features = formula_complexity_features([], [])
        self.assertEqual(empty_features['average_formula_length'], 0)

    # 测试 formula_distribution_var
    def test_formula_distribution_var(self):
        # 正常情况
        lines = [
            'No formula',
            '$inline$',
            'text',
            '$$block$$',
            'both $inline$ and $$block$$'
        ]
        variance = formula_distribution_var(lines)
        expected_lines = [1, 3, 4]
        expected_var = np.var(expected_lines)
        self.assertAlmostEqual(variance, expected_var)

        # 没有公式的情况
        self.assertEqual(formula_distribution_var(['No formulas']), 0)

        # 单行公式
        self.assertEqual(formula_distribution_var(['$formula$']), 0)

    # 测试 formula_type_ratios
    def test_formula_type_ratios(self):
        inline = [
            r'\int_0^1 x dx',
            r'\dot{x} = v',
            r'\mathbf{v} = \dot{x}'
        ]
        block = [
            r'\frac{\partial f}{\partial t}',
            r'\det(\mathbf{A})'
        ]
        features = formula_type_ratios(inline, block)

        # 积分公式：1个（inline[0]）
        # 导数公式：2个（inline[1], block[0]）
        # 矩阵公式：2个（inline[2], block[1]）
        self.assertAlmostEqual(features['integral_formula_ratio'], 1 / 5)
        self.assertAlmostEqual(features['derivative_formula_ratio'], 3 / 5)
        self.assertAlmostEqual(features['matrix_formula_ratio'], 2 / 5)

        # 空测试
        empty_features = formula_type_ratios([], [])
        self.assertEqual(empty_features['integral_formula_ratio'], 0)


if __name__ == '__main__':
    unittest.main()
