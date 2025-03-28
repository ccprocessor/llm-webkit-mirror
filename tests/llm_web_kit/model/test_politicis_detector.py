# flake8: noqa: E402
import json
import os
import sys
import unittest
from unittest import TestCase
from unittest.mock import MagicMock, mock_open, patch

import pytest

current_file_path = os.path.abspath(__file__)
parent_dir_path = os.path.join(current_file_path, *[os.pardir] * 4)
normalized_path = os.path.normpath(parent_dir_path)
sys.path.append(normalized_path)

from llm_web_kit.exception.exception import ModelInputException
from llm_web_kit.model.politics_detector import (GTEModel, PoliticalDetector,
                                                 decide_political_by_prob,
                                                 decide_political_by_str,
                                                 decide_political_func,
                                                 political_filter_cpu,
                                                 update_political_by_str)
from llm_web_kit.model.resource_utils import CACHE_DIR


class TestPoliticalDetector:

    @patch('transformers.AutoTokenizer.from_pretrained')
    @patch('llm_web_kit.model.politics_detector.fasttext.load_model')
    @patch('llm_web_kit.model.politics_detector.PoliticalDetector.auto_download')
    def test_init(self, mock_auto_download, mock_load_model, mock_auto_tokenizer):
        mock_auto_download.return_value = '/fake/model/path'
        # Test with default model path
        _ = PoliticalDetector()
        mock_load_model.assert_called_once_with('/fake/model/path/model.bin')
        mock_auto_tokenizer.assert_called_once_with(
            '/fake/model/path/internlm2-chat-20b',
            use_fast=False,
            trust_remote_code=True,
        )

        # Test with custom model path
        mock_load_model.reset_mock()
        mock_auto_tokenizer.reset_mock()
        _ = PoliticalDetector('custom_model_path')
        mock_load_model.assert_called_once_with(os.path.join('custom_model_path', 'model.bin'))
        mock_auto_tokenizer.assert_called_once_with(
            os.path.join('custom_model_path', 'internlm2-chat-20b'),
            use_fast=False,
            trust_remote_code=True,
        )

    @patch('transformers.AutoTokenizer.from_pretrained')
    @patch('llm_web_kit.model.politics_detector.fasttext.load_model')
    @patch('llm_web_kit.model.politics_detector.PoliticalDetector.auto_download')
    def test_predict(self, mock_auto_download, mock_load_model, mock_auto_tokenizer):
        political_detect = PoliticalDetector()
        political_detect.model.predict.return_value = (['label1', 'label2'], [0.9, 0.1])
        predictions, probabilities = political_detect.predict('test text')
        assert predictions == ['label1', 'label2']
        assert probabilities == [0.9, 0.1]

class TestGTEModel(TestCase):
    @patch('llm_web_kit.model.politics_detector.GTEModel.auto_download')
    @patch('llm_web_kit.model.politics_detector.import_transformer')
    @patch('llm_web_kit.model.politics_detector.open', new_callable=mock_open, read_data=json.dumps({
                        'max_tokens': 8192,
                        'device': 'cuda',
                        'cls_index': 1,
                        'using_xformers': True,
                        'output_prefix': 'political',
                        'output_postfix': '25m3',
                        'model_name': 'gte-model'
                    }))
    def setUp(self, mock_open, mock_import, mock_auto_download):
        mock_auto_download.return_value = '/fake/model/path'

        mock_module = MagicMock()
        mock_tokenizer = MagicMock()
        mock_config = MagicMock()
        mock_seqcls = MagicMock()

        mock_module.AutoTokenizer.from_pretrained.return_value = mock_tokenizer
        mock_module.AutoConfig.from_pretrained.return_value = mock_config
        mock_module.AutoModelForSequenceClassification.from_pretrained.return_value = mock_seqcls
        mock_import.return_value = mock_module

        self.model_obj = GTEModel()

        mock_auto_download.assert_called_once()
        mock_import.assert_called_once()
        mock_module.AutoTokenizer.from_pretrained.assert_called_once_with('/fake/model/path/politics_classifier/best_ckpt')
        mock_module.AutoConfig.from_pretrained.assert_called_once_with('/fake/model/path/politics_classifier/best_ckpt', trust_remote_code=True)
        mock_module.AutoModelForSequenceClassification.from_pretrained.assert_called_once_with(
            '/fake/model/path/politics_classifier/best_ckpt',
            trust_remote_code=True,
            config=mock_config
        )

        mock_open.assert_called_with('/fake/model/path/politics_classifier/extra_parameters.json')

    def test_init(self):
        self.assertEqual(self.model_obj.max_tokens, 8192)
        self.assertEqual(self.model_obj.device, 'cuda')
        self.assertEqual(self.model_obj.cls_index, 1)
        self.assertEqual(self.model_obj.output_prefix, 'political')
        self.assertEqual(self.model_obj.output_postfix, '25m3')
        self.assertEqual(self.model_obj.model_name, 'gte-model')

    @patch('llm_web_kit.model.politics_detector.load_config')
    @patch('llm_web_kit.model.politics_detector.get_unzip_dir')
    @patch('llm_web_kit.model.politics_detector.download_auto_file')
    @patch('llm_web_kit.model.politics_detector.unzip_local_file')
    @patch('llm_web_kit.model.politics_detector.os.path.join')
    def test_auto_download(
        self,
        mock_path_join,
        mock_unzip_local_file,
        mock_download_auto_file,
        mock_get_unzip_dir,
        mock_load_config,
    ):
        mock_load_config.return_value = {
            'resources': {
                'political-25m3': {
                    'download_path': '/fake/download/path',
                    'md5': 'fakemd5'
                }
            },
        }
        mock_get_unzip_dir.return_value = '/fake/unzip/path'
        mock_path_join.side_effect = lambda *args: '@'.join(args)
        zip_path = CACHE_DIR + '@political-25m3.zip'
        mock_download_auto_file.return_value = zip_path
        mock_unzip_local_file.return_value = '/fake/unzip/path'

        result = self.model_obj.auto_download()

        mock_load_config.assert_called_once()
        mock_get_unzip_dir.assert_called_once_with(zip_path)
        mock_download_auto_file.assert_called_once_with(
            '/fake/download/path',
            zip_path,
            'fakemd5',
        )
        mock_unzip_local_file.assert_called_once_with(zip_path, '/fake/unzip/path')

        self.assertEqual(result, '/fake/unzip/path')

    def test_pre_process(self):
        # Mock tokenizer output
        # mock_tokenizer_instance = MagicMock()
        input_ids = [[101, 7592, 1010, 2088, 999, 102]]
        attn_mask = [[1, 1, 1, 1, 1, 1]]
        mock_input_ids = MagicMock(to=MagicMock(return_value=input_ids))
        mock_attn_mask = MagicMock(to=MagicMock(return_value=attn_mask))

        self.model_obj.tokenizer.return_value = {
            'input_ids': mock_input_ids,
            'attention_mask': mock_attn_mask
        }

        # mock_tokenized_output = {'input_ids': MagicMock(), 'attention_mask': MagicMock()}
        # self.model_obj.tokenizer.return_value = mock_tokenized_output

        # Define the sample input
        sample_input = 'Hello, world!</s>'
        # expected_output = {'inputs': {'input_ids': mock_tokenized_output['input_ids'], 'attention_mask': mock_tokenized_output['attention_mask']}}

        # Execute the pre_process function
        result = self.model_obj.pre_process(sample_input)

        # Assertions
        self.model_obj.tokenizer.assert_called_once_with([sample_input.replace('</s>', '')], **self.model_obj.tokenizer_config)
        for name, tensor in self.model_obj.tokenizer.return_value.items():
            tensor.to.assert_called_once_with('cuda')
        # self.assertEqual(result, expected_output)
        self.assertEqual(
            result['inputs']['input_ids'],
            input_ids
        )
        self.assertEqual(
            result['inputs']['attention_mask'],
            attn_mask,
        )


    def test_get_output_key(self):
        result = self.model_obj.get_output_key('test')
        self.assertEqual(result, 'political_test_25m3')


    @patch('llm_web_kit.model.politics_detector.GTEModel.pre_process')
    @patch('llm_web_kit.model.politics_detector.torch')
    @patch('llm_web_kit.model.politics_detector.GTEModel.get_output_key')
    def test_predict(self, mock_get_key, mock_torch, mock_pre_process):
        # 模拟 no_grad 上下文管理器
        mock_no_grad_context_manager = MagicMock()
        mock_torch.no_grad.return_value = mock_no_grad_context_manager
        # 模拟 model 推理
        mock_pre_process.return_value = {
            'inputs': {
                'input_ids': [[101, 7592, 1010, 2088, 999, 102]],
                'attention_mask': [[1, 1, 1, 1, 1, 1]]
            }
        }
        mock_get_key.return_value = 'political_prob'

        # 配置模型的行为
        logit_tensor = MagicMock()
        self.model_obj.model.return_value = logit_tensor

        # 配置sigmoid和softmax的行为
        mock_softmax_output = MagicMock()
        mock_softmax_output[:, 1].cpu().detach().numpy.return_value = [0.2]
        mock_torch.softmax.return_value = mock_softmax_output

        result = self.model_obj.predict('Hello, world!')

        # 验证torch.no_grad()的调用
        mock_torch.no_grad.assert_called_once()

        # 验证torch.softmax函数的调用
        mock_torch.softmax.assert_called_once_with(logit_tensor['logits'], dim=-1)

        # 验证结果
        self.assertEqual(result, [{'political_prob': 0.2}])


def test_decide_political_by_prob():
    predictions = ['__label__normal', '__label__political']
    probabilities = [0.6, 0.4]
    assert decide_political_by_prob(predictions, probabilities) == 0.6

    predictions = ['__label__political', '__label__normal']
    probabilities = [0.7, 0.3]
    assert decide_political_by_prob(predictions, probabilities) == 0.3


def test_decide_political_func():
    political_detect = MagicMock()
    political_detect.predict.return_value = (
        ['__label__normal', '__label__political'],
        [0.6, 0.4],
    )
    test_str = 'test text'
    assert decide_political_func(test_str, political_detect) == 0.6
    political_detect.predict.assert_called_once_with(test_str)

    test_str = 'test text' * 1000000
    # reset the call count
    political_detect.predict.reset_mock()
    assert decide_political_func(test_str, political_detect) == 0.6
    political_detect.predict.assert_called_once_with(test_str[:2560000])


def test_decide_political_by_str():
    with patch('llm_web_kit.model.politics_detector.get_singleton_political_detect') as mock_get_singleton_political_detect, patch(
            'llm_web_kit.model.politics_detector.decide_political_func') as mock_decide_political_func:
        mock_get_singleton_political_detect.return_value = MagicMock()
        mock_decide_political_func.return_value = 0.6
        assert decide_political_by_str('test text') == 0.6
        mock_get_singleton_political_detect.assert_called_once()


def test_update_political_by_str():
    with patch('llm_web_kit.model.politics_detector.decide_political_by_str') as mock_decide_political_by_str:
        mock_decide_political_by_str.return_value = 0.6
        assert update_political_by_str('test text') == {'political_prob': 0.6}

def test_political_filter_cpu():
    with patch('llm_web_kit.model.politics_detector.decide_political_by_str') as mock_decide_political_by_str:
        with patch('llm_web_kit.model.politics_detector.DataJson') as mock_datajson:
            mock_datajson_instance = MagicMock()
            mock_datajson_instance.get_content_list.return_value.to_txt.return_value = 'This is a test content.'
            mock_datajson.return_value = mock_datajson_instance
            mock_decide_political_by_str.return_value = 0.6
            assert political_filter_cpu({'content': 'This is a test content.'}, 'en') == {'political_prob': 0.6}

    with pytest.raises(ModelInputException) as excinfo:
        political_filter_cpu({'content': 'This is a test content.'}, 'fr')
    assert "Unsupport language 'fr'" in str(excinfo.value)

if __name__ == '__main__':
    unittest.main()
