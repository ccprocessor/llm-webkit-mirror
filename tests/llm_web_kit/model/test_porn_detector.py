import json
import logging
import os
import sys
import unittest
from unittest import TestCase
from unittest.mock import MagicMock, mock_open, patch

from transformers import logging as transformers_logging

from llm_web_kit.model.porn_detector import BertModel, XlmrModel  # noqa: E402
from llm_web_kit.model.resource_utils import CACHE_DIR

current_file_path = os.path.abspath(__file__)
parent_dir_path = os.path.join(current_file_path, *[os.pardir] * 4)
normalized_path = os.path.normpath(parent_dir_path)
sys.path.append(normalized_path)


transformers_logging.set_verbosity_error()

logging.disable(logging.CRITICAL)


class TestBertModel(TestCase):
    @patch('transformers.AutoModelForSequenceClassification.from_pretrained')
    @patch('transformers.AutoTokenizer.from_pretrained')
    @patch('llm_web_kit.model.porn_detector.os.path.join')
    @patch('llm_web_kit.model.porn_detector.open', new_callable=mock_open, read_data='{"cls_index": 0, "use_sigmoid": true, "max_tokens": 512, "device": "cuda"}')
    @patch('llm_web_kit.model.porn_detector.BertModel.auto_download')
    def test_init(self, mock_auto_download, mock_open, mock_os_path_join, mock_from_pretrained_tokenizer, mock_from_pretrained_model):
        # 模拟auto_download和os.path.join
        mock_auto_download.return_value = '/fake/model/path'
        mock_os_path_join.side_effect = lambda *args: '/'.join(args)

        # 实例化 BertModel
        model = BertModel()

        # 验证是否调用了预期的函数
        mock_auto_download.assert_called_once()
        mock_from_pretrained_model.assert_called_once_with('/fake/model/path/porn_classifier/classifier_hf')
        mock_from_pretrained_tokenizer.assert_called_once_with('/fake/model/path/porn_classifier/classifier_hf')
        mock_open.assert_called_once_with('/fake/model/path/porn_classifier/extra_parameters.json')

        # 检查模型初始化的参数
        self.assertEqual(model.cls_index, 0)
        self.assertTrue(model.use_sigmoid)
        self.assertEqual(model.max_tokens, 512)
        self.assertEqual(model.remain_tail, -1)
        self.assertEqual(model.device, 'cuda')
        self.assertEqual(model.output_prefix, '')
        self.assertEqual(model.output_postfix, '')
        self.assertEqual(model.model_name, 'porn-23w44')
        # 检查tokenizer的参数
        self.assertEqual(
            model.tokenizer_config,
            {
                'padding': True,
                'truncation': True,
                'max_length': 512,
                'return_tensors': 'pt',
            }
        )

    @patch('transformers.AutoModelForSequenceClassification.from_pretrained')
    @patch('transformers.AutoTokenizer.from_pretrained')
    @patch('llm_web_kit.model.porn_detector.os.path.join')
    @patch('llm_web_kit.model.porn_detector.open', new_callable=mock_open, read_data='{"cls_index": 0, "use_sigmoid": true, "max_tokens": 512, "device": "cuda"}')
    @patch('llm_web_kit.model.porn_detector.BertModel.auto_download')
    @patch('llm_web_kit.model.porn_detector.torch')
    def test_pre_process(self, mock_torch, mock_auto_download, mock_open, mock_os_path_join, mock_from_pretrained_tokenizer, mock_from_pretrained_model):
        mock_auto_download.return_value = '/fake/model/path'
        mock_os_path_join.side_effect = lambda *args: '/'.join(args)
        # 模拟torch.tensor和torch.cat的行为
        mock_torch.tensor.side_effect = lambda x: MagicMock(unsqueeze=MagicMock(return_value=x))
        mock_torch.cat.side_effect = lambda x: MagicMock(to=MagicMock(return_value=x))
        # 模拟tokenizer的行为
        mock_tokenizer_instance = MagicMock(sep_token_id=102, pad_token_id=0)
        input_ids = [[101, 7592, 1010, 2088, 999, 102]]
        attn_mask = [[1, 1, 1, 1, 1, 1]]
        mock_input_ids = MagicMock(to=MagicMock(return_value=input_ids))
        mock_attn_mask = MagicMock(to=MagicMock(return_value=attn_mask))
        mock_input_ids.__iter__.return_value = iter(input_ids)
        mock_attn_mask.__iter__.return_value = iter(attn_mask)
        mock_tokenizer_instance.return_value = {
            'input_ids': mock_input_ids,
            'attention_mask': mock_attn_mask
        }

        mock_from_pretrained_tokenizer.return_value = mock_tokenizer_instance

        # 实例化 BertModel 并调用 pre_process
        model = BertModel()
        result = model.pre_process('Hello, world!')

        # 测试默认情况
        self.assertEqual(
            result['inputs']['input_ids'],
            input_ids
        )
        self.assertEqual(
            result['inputs']['attention_mask'],
            attn_mask,
        )

        # 测试remain_tail>0, input_length > self.max_tokens的情况
        mock_input_ids.reset_mock()
        mock_attn_mask.reset_mock()
        mock_tokenizer_instance.reset_mock()
        model.remain_tail = 1
        model.max_tokens = 4
        result = model.pre_process('Hello, world!')
        expected_input_ids = [
            input_ids[0][:(model.max_tokens - model.remain_tail)] + input_ids[0][-model.remain_tail:]
        ]
        expected_attn_mask = [attn_mask[0][:model.max_tokens]]
        self.assertEqual(result['inputs']['input_ids'], expected_input_ids)
        self.assertEqual(result['inputs']['attention_mask'], expected_attn_mask)

    @patch('transformers.AutoModelForSequenceClassification.from_pretrained')
    @patch('transformers.AutoTokenizer.from_pretrained')
    @patch('llm_web_kit.model.porn_detector.os.path.join')
    @patch('llm_web_kit.model.porn_detector.open', new_callable=mock_open, read_data='{"cls_index": 0, "use_sigmoid": true, "max_tokens": 512, "device": "cuda"}')
    @patch('llm_web_kit.model.porn_detector.BertModel.auto_download')
    @patch('llm_web_kit.model.porn_detector.BertModel.pre_process')
    @patch('llm_web_kit.model.porn_detector.torch')
    def test_predict(self, mock_torch, mock_pre_process, mock_auto_download, mock_open, mock_os_path_join, mock_from_pretrained_tokenizer, mock_from_pretrained_model):
        mock_auto_download.return_value = '/fake/model/path'
        mock_os_path_join.side_effect = lambda *args: '/'.join(args)
        # 模拟 no_grad 上下文管理器
        mock_no_grad_context_manager = MagicMock()
        mock_torch.no_grad.return_value = mock_no_grad_context_manager
        # 模拟 model 推理
        mock_model_instance = MagicMock()
        mock_from_pretrained_model.return_value = mock_model_instance
        # 模拟 tokenizer
        mock_tokenizer_instance = MagicMock()
        mock_from_pretrained_tokenizer.return_value = mock_tokenizer_instance
        mock_tokenizer_instance.return_value = {
            'input_ids': [[101, 7592, 1010, 2088, 999, 102]],
            'attention_mask': [[1, 1, 1, 1, 1, 1]]
        }

        # 配置模型的行为
        logit_tensor = MagicMock()
        mock_model_instance.return_value = MagicMock(logits=logit_tensor)

        mock_model_instance.eval.return_value = mock_model_instance
        mock_model_instance.to.return_value = mock_model_instance
        mock_model_instance.to_bettertransformer.return_value = mock_model_instance

        # 配置sigmoid和softmax的行为
        mock_sigmoid_output = MagicMock()
        mock_torch.sigmoid.return_value = mock_sigmoid_output
        mock_sigmoid_output[:, 0].cpu().numpy.return_value = [0.2]

        mock_softmax_output = MagicMock()
        mock_torch.softmax.return_value = mock_softmax_output
        mock_softmax_output[:, 0].cpu().numpy.return_value = [0.2]

        # 实例化 BertModel 并调用 predict
        model = BertModel()
        result = model.predict('Hello, world!')

        # 验证 eval 和 to 方法是否被正确调用
        mock_model_instance.eval.assert_called_once()
        mock_model_instance.to.assert_called_once_with('cuda', dtype=mock_torch.float16)

        # 如果存在 to_bettertransformer 方法，验证它也被调用了
        if hasattr(mock_model_instance, 'to_bettertransformer'):
            mock_model_instance.to_bettertransformer.assert_called_once()

        # 验证torch.no_grad()的调用
        mock_torch.no_grad.assert_called_once()

        # 验证torch.sigmoid或torch.softmax函数的调用
        if model.use_sigmoid:
            mock_torch.sigmoid.assert_called_once_with(logit_tensor)
        else:
            mock_torch.softmax.assert_called_once_with(logit_tensor)

        # 验证结果
        self.assertEqual(result, [{'porn-23w44_prob': 0.2}])


class TestXlmrModel(TestCase):
    @patch('llm_web_kit.model.porn_detector.XlmrModel.auto_download')
    @patch('llm_web_kit.model.porn_detector.import_transformer')
    @patch('llm_web_kit.model.porn_detector.open', new_callable=mock_open, read_data=json.dumps({
        'max_tokens': 512,
        'batch_size':300,
        'device': 'cuda'
    }))
    def setUp(self, mock_open, mock_import, mock_auto_download):
        mock_auto_download.return_value = '/fake/model/path'

        mock_module = MagicMock()
        mock_tokenizer = MagicMock()
        mock_seqcls = MagicMock()

        mock_module.AutoTokenizer.from_pretrained.return_value = mock_tokenizer
        mock_module.AutoModelForSequenceClassification.from_pretrained.return_value = mock_seqcls
        mock_import.return_value = mock_module

        self.model_obj = XlmrModel()

        mock_auto_download.assert_called_once()
        mock_import.assert_called_once()
        mock_module.AutoTokenizer.from_pretrained.assert_called_once_with('/fake/model/path/porn_classifier/classifier_hf')
        mock_module.AutoModelForSequenceClassification.from_pretrained.assert_called_once_with(
            '/fake/model/path/porn_classifier/classifier_hf',
        )

        mock_open.assert_called_with('/fake/model/path/porn_classifier/extra_parameters.json')

    @patch('llm_web_kit.model.porn_detector.load_config')
    @patch('llm_web_kit.model.porn_detector.get_unzip_dir')
    @patch('llm_web_kit.model.porn_detector.download_auto_file')
    @patch('llm_web_kit.model.porn_detector.unzip_local_file')
    def test_auto_download(
        self,
        mock_unzip_local_file,
        mock_download_auto_file,
        mock_get_unzip_dir,
        mock_load_config,
    ):
        mock_load_config.return_value = {
            'resources': {
                'porn-24m5': {
                    'download_path': '/fake/download/path',
                    'md5': 'fakemd5'
                }
            },
        }
        mock_get_unzip_dir.return_value = '/fake/unzip/path'
        zip_path = os.path.join(CACHE_DIR, 'porn-24m5.zip')
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

    def test_get_output_key(self):
        result = self.model_obj.get_output_key('test')
        self.assertEqual(result, 'porn-24m5_test')


if __name__ == '__main__':
    unittest.main()
