import unittest
from unittest.mock import MagicMock, patch

import torch

from llm_web_kit.model.html_classify.model import Markuplm


class TestMarkuplm(unittest.TestCase):
    @patch('transformers.MarkupLMProcessor.from_pretrained')
    @patch('transformers.MarkupLMForSequenceClassification.from_pretrained')
    def setUp(self, mock_model, mock_tokenizer):
        self.markuplm = Markuplm('/mnt/hwfile/opendatalab/dataproc/pengjiahui/models','cpu')

        mock_tokenizer.return_value = MagicMock()
        mock_model.return_value = MagicMock()

        self.assertIsNotNone(self.markuplm.tokenizer)
        self.assertIsNotNone(self.markuplm.model)

    @patch('transformers.MarkupLMProcessor.from_pretrained')
    def test_load_tokenizer(self, mock_from_pretrained):
        mock_tokenizer = MagicMock()
        mock_from_pretrained.return_value = mock_tokenizer
        tokenizer = self.markuplm.load_tokenizer()
        mock_from_pretrained.assert_called_once_with(self.markuplm.model_path)
        self.assertEqual(tokenizer, mock_tokenizer)

    @patch('transformers.MarkupLMForSequenceClassification.from_pretrained')
    @patch('torch.load')
    def test_load_model(self, mock_torch_load, mock_from_pretrained):
        # 配置mock返回值
        mock_model = MagicMock()
        mock_from_pretrained.return_value = mock_model
        # 模拟加载检查点
        mock_state_dict = {'layer1.weight': torch.ones(2,2)}
        mock_torch_load.return_value = mock_state_dict
        # 调用load_model方法
        model = self.markuplm.load_model()
        # 验证mock方法被调用
        mock_from_pretrained.assert_called_once_with(self.markuplm.model_path, num_labels=self.markuplm.num_labels)
        mock_torch_load.assert_called_once_with(self.markuplm.checkpoint_path, map_location=self.markuplm.device)
        self.assertEqual(model, mock_model)

    def test_inference_batch_normal_input(self):
        # 创建一个包含5个HTML字符串的批次
        html_batch = ['<div>Sample 1</div>', '<div>Sample 2</div>', '<div>Sample 3</div>', '<div>Sample 4</div>', '<div>Sample 5</div>']

        # 模拟分词器的返回值
        mock_tokenizer = self.markuplm.tokenizer
        mock_tokenizer.return_value = {
            'input_ids': torch.randint(0, 100, (5, 512)),
            'attention_mask': torch.ones(5, 512, dtype=torch.long),
            'token_type_ids': torch.zeros(5, 512, dtype=torch.long),
            'xpath_tags_seq': torch.zeros(5, 512, 50, dtype=torch.long),
            'xpath_subs_seq': torch.zeros(5, 512, 50, dtype=torch.long)
        }

        # 模拟模型的返回值
        mock_model = self.markuplm.model
        mock_model.return_value = MagicMock(
            logits=torch.randn(5, 3)
        )

        # 调用推理方法
        outputs = self.markuplm.inference_batch(html_batch)

        # 验证输出
        self.assertEqual(len(outputs), 5)
        for output in outputs:
            self.assertIn('pred_prob', output)
            self.assertIn('pred_label', output)
            self.assertTrue(0 <= float(output['pred_prob']) <= 1)
            self.assertIn(output['pred_label'], ['article', 'forum', 'other'])

    def test_inference_batch_empty_input(self):
        # 创建一个空批次
        html_batch = []

        # 模拟分词器和模型的返回值
        mock_tokenizer = self.markuplm.tokenizer
        mock_tokenizer.return_value = {}

        mock_model = self.markuplm.model
        mock_model.return_value = MagicMock(
            logits=torch.randn(0, 3)
        )

        # 调用推理方法
        outputs = self.markuplm.inference_batch(html_batch)

        # 验证输出
        self.assertEqual(len(outputs), 0)

    def test_inference_batch_variable_length_inputs(self):
        # 创建一个包含不同长度HTML字符串的批次
        html_batch = ['<div>Sample</div>', '<div>Longer Sample</div>', '<div>Very Long Sample</div>', '<div>Short</div>', '<div>Medium Length</div>']

        # 模拟分词器的返回值
        mock_tokenizer = self.markuplm.tokenizer
        mock_tokenizer.return_value = {
            'input_ids': torch.randint(0, 100, (5, 512)),
            'attention_mask': torch.ones(5, 512, dtype=torch.long),
            'token_type_ids': torch.zeros(5, 512, dtype=torch.long),
            'xpath_tags_seq': torch.zeros(5, 512, 50, dtype=torch.long),
            'xpath_subs_seq': torch.zeros(5, 512, 50, dtype=torch.long)
        }

        # 模拟模型的返回值
        mock_model = self.markuplm.model
        mock_model.return_value = MagicMock(
            logits=torch.randn(5, 3)
        )

        # 调用推理方法
        outputs = self.markuplm.inference_batch(html_batch)

        # 验证输出
        self.assertEqual(len(outputs), 5)
        for output in outputs:
            self.assertIn('pred_prob', output)
            self.assertIn('pred_label', output)
            self.assertTrue(0 <= float(output['pred_prob']) <= 1)
            self.assertIn(output['pred_label'], ['article', 'forum', 'other'])


if __name__ == '__main__':
    unittest.main()
