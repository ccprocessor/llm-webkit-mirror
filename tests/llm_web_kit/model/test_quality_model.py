import os
import sys
import unittest
from unittest import TestCase
from unittest.mock import MagicMock, mock_open, patch

from llm_web_kit.exception.exception import ModelInputException  # noqa: E402
from llm_web_kit.model.quality_model import QualityModel  # noqa: E402
from llm_web_kit.model.quality_model import get_quality_model  # noqa: E402
from llm_web_kit.model.quality_model import quality_prober  # noqa: E402
from llm_web_kit.model.quality_model import QualityFilter
from llm_web_kit.model.resource_utils.download_assets import \
    CACHE_DIR  # noqa: E402

current_file_path = os.path.abspath(__file__)
parent_dir_path = os.path.join(current_file_path, *[os.pardir] * 4)
normalized_path = os.path.normpath(parent_dir_path)
sys.path.append(normalized_path)


class TestQualityModel(TestCase):
    @patch('llm_web_kit.model.quality_model.QualityModel._load_model')
    @patch('llm_web_kit.model.quality_model.QualityModel.auto_download')
    def test_init(self, mock_auto_download, mock_load_model):
        # 模拟auto_download
        mock_auto_download.return_value = '/fake/model/path'

        # 实例化 QualityModel
        _ = QualityModel()
        # 验证是否调用了预期的函数
        mock_auto_download.assert_called_once()
        mock_load_model.assert_called_once_with('/fake/model/path')

        mock_auto_download.reset_mock()
        mock_load_model.reset_mock()
        # 实例化 QualityModel
        _ = QualityModel(model_path='/test/model/path')
        # 验证是否调用了预期的函数
        mock_load_model.assert_called_once_with('/test/model/path')

        mock_auto_download.reset_mock()
        mock_load_model.reset_mock()
        # 实例化 QualityModel
        _ = QualityModel(language='en', content_style='article')
        # 验证是否调用了预期的函数
        mock_auto_download.assert_called_once_with('en', 'article')
        mock_load_model.assert_called_once_with('/fake/model/path')

    @patch(
        'llm_web_kit.model.quality_model.load_config',
        return_value={
            'resources': {
                'zh_en_article': {
                    'download_path': 'mock_download_path',
                    'md5': 'mock_md5',
                }
            }
        },
    )
    @patch('llm_web_kit.model.quality_model.get_unzip_dir')
    @patch('llm_web_kit.model.quality_model.download_auto_file')
    @patch('llm_web_kit.model.quality_model.unzip_local_file')
    @patch('llm_web_kit.model.quality_model.QualityModel._load_model')
    @patch('llm_web_kit.model.quality_model.os.path.join')
    def test_auto_download(
        self,
        mock_path_join,
        mock_load_model,
        mock_unzip_local_file,
        mock_download_auto_file,
        mock_get_unzip_dir,
        mock_load_config,
    ):
        mock_get_unzip_dir.return_value = '/fake/unzip/path'
        mock_path_join.side_effect = lambda *args: '@'.join(args)
        zip_path = CACHE_DIR + '@zh_en_article.zip'
        mock_download_auto_file.return_value = zip_path
        mock_unzip_local_file.return_value = '/fake/unzip/path'

        _ = QualityModel('en', 'article')

        mock_get_unzip_dir.assert_called_once_with(zip_path)
        mock_download_auto_file.assert_called_once_with(
            'mock_download_path',
            zip_path,
            'mock_md5',
        )
        mock_unzip_local_file.assert_called_once_with(zip_path, '/fake/unzip/path')

    @patch('llm_web_kit.model.quality_model.ctypes.cdll.LoadLibrary')
    @patch('llm_web_kit.model.quality_model.pickle.load')
    @patch('llm_web_kit.model.quality_model.os.path.join')
    @patch('llm_web_kit.model.quality_model.open', new_callable=mock_open)
    def test_load_model(
        self, mock_open, mock_path_join, mock_pickle_load, mock_loadlib
    ):
        mock_path_join.side_effect = lambda *args: '/'.join(args)
        _ = QualityModel(model_path='/fake/model/path')

        mock_loadlib.assert_called_once_with('libgomp.so.1')

        mock_open.assert_called_once_with('/fake/model/path', 'rb')
        mock_pickle_load.assert_called_once_with(mock_open.return_value)

    @patch('llm_web_kit.model.quality_model.pd.json_normalize')
    @patch('llm_web_kit.model.quality_model.QualityModel._load_model')
    def test_predict_with_features(self, mock_load_model, mock_json_normalize):
        # 设置模拟的 DataFrame
        mock_df = MagicMock()
        mock_json_normalize.return_value = mock_df

        # 创建一个模拟的模型并设置预测方法的返回值
        mock_model = MagicMock()
        mock_model.predict.return_value = [0.9]  # 假设模型总是预测0.9

        # 实例化 QualityModel，并替换其 quality_model 属性为模拟的模型
        qm = QualityModel(model_path='/fake/model/path')
        qm.quality_model = mock_model

        # 定义要测试的特征字典
        test_features = {'key1': 'value1', 'key2': 'value2'}

        # 调用 predict_with_features 方法
        prediction = qm.predict_with_features(test_features)

        # 验证 json_normalize 是否被正确调用
        mock_json_normalize.assert_called_once_with(test_features)

        # 验证模型的 predict 方法是否被正确调用
        mock_model.predict.assert_called_once_with(mock_df)

        # 验证预测结果
        self.assertEqual(prediction, 0.9)

    @patch('llm_web_kit.model.quality_model.stats_stop_words')
    @patch('llm_web_kit.model.quality_model.stats_entropy')
    @patch('llm_web_kit.model.quality_model.get_content_len')
    @patch('llm_web_kit.model.quality_model.content2words')
    @patch('llm_web_kit.model.quality_model.div_zero')
    @patch('llm_web_kit.model.quality_model.stats_punctuation_end_sentence')
    @patch('llm_web_kit.model.quality_model.stats_continue_space')
    @patch('llm_web_kit.model.quality_model.content2lines')
    @patch('llm_web_kit.model.quality_model.get_content_len_without_space')
    @patch('llm_web_kit.model.quality_model.stats_html_entity')
    @patch('llm_web_kit.model.quality_model.stats_ngram_mini')
    @patch('llm_web_kit.model.quality_model.stats_unicode')
    @patch('llm_web_kit.model.quality_model.QualityModel.predict_with_features')
    @patch('llm_web_kit.model.quality_model.QualityModel._load_model')
    def test_predict_with_content(
        self,
        mock_load_model,
        mock_predict_with_features,
        mock_stats_unicode,
        mock_stats_ngram_mini,
        mock_stats_html_entity,
        mock_get_content_len_without_space,
        mock_content2lines,
        mock_stats_continue_space,
        mock_stats_punctuation_end_sentence,
        mock_div_zero,
        mock_content2words,
        mock_get_content_len,
        mock_stats_entropy,
        mock_stats_stop_words,
    ):
        # 定义要测试的内容
        test_content = """Objective: This study analyzed the cost-effectiveness of delivering alcohol screening, brief intervention, and referral to treatment (SBIRT) in emergency departments (ED) when compared to outpatient medical settings.
Methods: A probabilistic decision analytic tree categorized patients into health states. Utility weights and social costs were assigned to each health state. Health outcome measures were the proportion of patients not drinking above threshold levels at follow-up, the proportion of patients transitioning from above threshold levels at baseline to abstinent or below threshold levels at follow-up, and the quality-adjusted life years (QALYs) gained. Expected costs under a provider perspective were the marginal costs of SBIRT, and under a societal perspective were the sum of SBIRT cost per patient and the change in social costs. Incremental cost-effectiveness ratios were computed.
Results: When considering provider costs only, compared to outpatient, SBIRT in ED cost $8.63 less, generated 0.005 more QALYs per patient, and resulted in 13.8% more patients drinking below threshold levels. Sensitivity analyses in which patients were assumed to receive a fixed number of treatment sessions that met clinical sites' guidelines made SBIRT more expensive in ED than outpatient; the ED remained more effective. In this sensitivity analysis, the ED was the most cost-effective setting if decision makers were willing to pay more than $1500 per QALY gained.
Conclusions: Alcohol SBIRT generates costs savings and improves health in both ED and outpatient settings. EDs provide better effectiveness at a lower cost and greater social cost reductions than outpatient.
"""

        # 设置模拟函数的返回值
        mock_stats_stop_words.return_value = {
            'stop_word_num': 88,
            'stop_word_frac': 0.3577,
        }
        mock_stats_entropy.return_value = {'entropy': 4.5059}
        mock_get_content_len.return_value = 1681
        mock_content2words.return_value = test_content.split(' ')
        mock_div_zero.side_effect = lambda x, y: x / y if y != 0 else 0
        mock_stats_punctuation_end_sentence.return_value = {
            'punc_end_sentence_num': 43,
            'punc_end_sentence_mean_len': 33.4186,
            'longest_punc_sentence_len': 130,
        }
        mock_stats_continue_space.return_value = {'max_continue_space_num': 1}
        mock_content2lines.return_value = ['line1', 'line2', 'line3', 'line4']
        mock_get_content_len_without_space.return_value = 1437
        mock_stats_html_entity.return_value = {
            'html_semi_entity_count': 0,
            'html_semi_entity_frac': 0.0,
        }
        mock_stats_ngram_mini.return_value = {
            'dup_top_2gram': 0.0527,
            'dup_top_4gram': 0.0544,
            'dup_10gram': 0.0,
        }
        mock_stats_unicode.return_value = {
            'std_dev_unicode_value': 29.1184,
            'mean_diff_unicode_value': -0.0410,
        }
        mock_predict_with_features.return_value = 0.7

        # 创建 QualityModel 实例
        qm = QualityModel(model_path='/fake/model/path')

        # 调用 predict_with_content 方法
        result = qm.predict_with_content(test_content)

        # 验证 predict_with_features 是否被正确调用
        mock_predict_with_features.assert_called()

        # 验证预测结果
        self.assertEqual(result, 0.7)

    @patch('llm_web_kit.model.quality_model.QualityModel.auto_download')
    @patch('llm_web_kit.model.quality_model.QualityModel._load_model')
    def test_get_quality_model(self, mock_load_model, mock_auto_download):
        qm, threshold = get_quality_model('en', 'article')
        self.assertIsInstance(qm, QualityModel)
        self.assertIsInstance(threshold, float)
        qm, threshold = get_quality_model('xx', 'article')
        self.assertIsNone(qm)
        self.assertIsNone(threshold)

    @patch('llm_web_kit.model.quality_model.get_quality_model')
    @patch('llm_web_kit.model.quality_model.DataJson')
    def test_quality_prober(self, mock_DataJson, mock_get_quality_model):
        # 设置模拟对象
        mock_model = MagicMock()
        mock_model.predict_with_content.return_value = 0.85
        mock_threshold = 0.8
        mock_get_quality_model.return_value = (mock_model, mock_threshold)

        # 模拟 DataJson 类的行为
        mock_datajson_instance = MagicMock()
        mock_datajson_instance.get_content_list.return_value.to_txt.return_value = (
            'This is a test content.'
        )
        mock_DataJson.return_value = mock_datajson_instance

        # 测试数据
        test_data_dict = {'content': 'This is a test content.'}
        test_language = 'en'
        test_content_style = 'article'

        result = quality_prober(test_data_dict, test_language, test_content_style)

        # 断言预期结果
        self.assertDictEqual(result, {'quality_prob': 0.85})
        mock_get_quality_model.assert_called_once_with(
            test_language, test_content_style
        )
        mock_model.predict_with_content.assert_called_once_with(
            'This is a test content.', test_content_style
        )

        mock_get_quality_model.reset_mock()
        mock_get_quality_model.return_value = None, None
        test_language = 'xx'
        test_content_style = 'article'

        with self.assertRaises(ModelInputException):
            quality_prober(test_data_dict, test_language, test_content_style)

        # 确认是否正确调用了 get_quality_model
        mock_get_quality_model.assert_called_once_with(
            test_language, test_content_style
        )


class TestQualityFilter(unittest.TestCase):
    def setUp(self):
        self.filter = QualityFilter()

    @patch.dict(
        'llm_web_kit.model.quality_model._model_resource_map',
        {'en-article': 'mock_value'},
        clear=True,
    )
    def test_check_supported(self):
        # 测试支持的语言和内容风格
        self.assertTrue(self.filter.check_supported('en', 'article'))
        # 测试不支持的组合
        self.assertFalse(self.filter.check_supported('fr', 'blog'))

    @patch('llm_web_kit.model.quality_model.get_quality_model')
    def test_filter_supported_high_score(self, mock_get_model):
        """测试支持的语言风格且分数高于阈值的情况."""
        # 配置mock模型
        mock_model = MagicMock()
        mock_model.predict_with_content.return_value = 0.85
        mock_get_model.return_value = (mock_model, 0.7)

        # 执行过滤
        result, details = self.filter.filter('test content', 'en', 'details', 'article')

        # 验证结果
        self.assertTrue(result)
        self.assertEqual(details['quality_prob'], 0.85)
        mock_get_model.assert_called_once_with('en', 'article')
        mock_model.predict_with_content.assert_called_once_with(
            'test content', 'article'
        )

    @patch('llm_web_kit.model.quality_model.get_quality_model')
    def test_filter_supported_low_score(self, mock_get_model):
        """测试支持的语言风格但分数低于阈值的情况."""
        mock_model = MagicMock()
        mock_model.predict_with_content.return_value = 0.6
        mock_get_model.return_value = (mock_model, 0.7)

        result, details = self.filter.filter(
            'low quality content', 'en', 'details', 'article'
        )

        self.assertFalse(result)
        self.assertEqual(details['quality_prob'], 0.6)

    @patch.dict('llm_web_kit.model.quality_model._model_resource_map', {}, clear=True)
    def test_filter_unsupported_combination(self):
        """测试不支持的语言风格组合."""
        with self.assertRaises(ValueError) as context:
            self.filter.filter('content', 'jp', 'details', 'novel')

        self.assertIn(
            "Unsupport language 'jp' with content_style 'novel'", str(context.exception)
        )

    @patch('llm_web_kit.model.quality_model.get_quality_model')
    def test_edge_case_threshold(self, mock_get_model):
        """测试阈值边界情况."""
        mock_model = MagicMock()
        mock_model.predict_with_content.return_value = 0.7
        mock_get_model.return_value = (mock_model, 0.7)

        result, _ = self.filter.filter('boundary content', 'en', 'details', 'article')
        self.assertFalse(result)  # 0.7不大于0.7应返回False

    @patch('llm_web_kit.model.quality_model.get_quality_model')
    def test_error_handling_in_model(self, mock_get_model):
        """测试模型预测时的异常处理."""
        mock_model = MagicMock()
        mock_model.predict_with_content.side_effect = Exception('Model failure')
        mock_get_model.return_value = (mock_model, 0.7)

        with self.assertRaises(Exception) as context:
            self.filter.filter('error content', 'en', 'details', 'article')

        self.assertIn('Model failure', str(context.exception))


if __name__ == '__main__':
    unittest.main()
