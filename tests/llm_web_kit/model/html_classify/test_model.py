import sys
import unittest
from unittest.mock import MagicMock, patch

import torch

sys.path.append('../../../../llm_web_kit/model/html_classify')
from model import Markuplm


class TestMarkuplm(unittest.TestCase):
    def setUp(self):
        self.config = {
            'model_class': 'model.Markuplm',
            'model_dataset': 'dataset.MarkupLMDataset',
            'model_path': '/mnt/hwfile/opendatalab/dataproc/pengjiahui/models/markuplm-base',
            'checkpoint_path': '/mnt/hwfile/opendatalab/dataproc/pengjiahui/models/markuplm_202501222031_epoch_2.pt',
            'num_labels': 3
        }
        self.device = 'cpu'
        self.markuplm = Markuplm(self.config, self.device)

    def test_init(self):
        # 检查基本配置是否正确初始化
        self.assertEqual(self.markuplm.checkpoint_path, '/mnt/hwfile/opendatalab/dataproc/pengjiahui/models/markuplm_202501222031_epoch_2.pt')
        self.assertEqual(self.markuplm.num_labels, 3)
        self.assertEqual(self.markuplm.model_path, '/mnt/hwfile/opendatalab/dataproc/pengjiahui/models/markuplm-base')
        self.assertEqual(self.markuplm.device, 'cpu')
        self.assertEqual(self.markuplm.max_tokens, 512)
        self.assertEqual(self.markuplm.label2id, {0:'article', 1:'forum', 2:'other'})

    @patch('transformers.MarkupLMProcessor.from_pretrained')
    def test_load_tokenizer(self, mock_from_pretrained):
        # 配置mock返回值
        mock_tokenizer = MagicMock()
        mock_from_pretrained.return_value = mock_tokenizer

        # 调用load_tokenizer方法
        tokenizer = self.markuplm.load_tokenizer()

        # 验证mock方法被调用
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

    def test_inference(self):
        # 创建模拟的dataloader
        class MockDataloader:
            def __iter__(self):
                return iter([{'input_ids': torch.randint(0, 100, (2, 512))}])

        dataloader = MockDataloader()

        # 调用inference方法
        outputs_result = self.markuplm.inference(dataloader)

        # 验证输出格式
        self.assertEqual(len(outputs_result), 2)
        for output in outputs_result:
            self.assertIn('pred_prob', output)
            self.assertIn('pred_label', output)
            self.assertRegex(output['pred_prob'], r'^\d+\.\d+$')
            self.assertIn(output['pred_label'], ['article', 'forum', 'other'])


if __name__ == '__main__':
    unittest.main()
