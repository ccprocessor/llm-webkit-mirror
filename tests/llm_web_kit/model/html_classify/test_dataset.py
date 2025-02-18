import sys
import unittest
from unittest.mock import patch

import torch
from transformers import MarkupLMProcessor

sys.path.append('../../../../llm_web_kit/model/html_classify')
from dataset import MarkupLMDataset


class TestMarkupLMDataset(unittest.TestCase):
    def setUp(self):
        self.config = {
            'model_class': 'model.Markuplm',
            'model_dataset': 'dataset.MarkupLMDataset',
            'model_path': '/mnt/hwfile/opendatalab/dataproc/pengjiahui/models/markuplm-base',
            'checkpoint_path': '/mnt/hwfile/opendatalab/dataproc/pengjiahui/models/markuplm_202501222031_epoch_2.pt',
            'num_labels': 3
        }

        self.html_strings = [
            '<div>Example 1</div>',
            '<p>Example 2</p>',
            '<span>Example 3</span>'
        ]
        self.processor = MarkupLMProcessor.from_pretrained(self.config['model_path'])
        self.dataset = MarkupLMDataset(self.html_strings, self.processor)

    def test_len(self):
        self.assertEqual(len(self.dataset), len(self.html_strings))

    @patch('transformers.MarkupLMProcessor')
    def test_getitem(self, mock_processor):
        mock_processor_instance = mock_processor.return_value
        mock_processor_instance.return_value = {
            'input_ids': torch.tensor([1, 2, 3]),
            'attention_mask': torch.tensor([1, 1, 1])
        }

        dataset = MarkupLMDataset(self.html_strings, mock_processor_instance)

        sample = dataset[0]

        self.assertIn('input_ids', sample)
        self.assertIn('attention_mask', sample)
        self.assertEqual(sample['input_ids'].shape, torch.Size([3]))
        self.assertEqual(sample['attention_mask'].shape, torch.Size([3]))

        mock_processor_instance.assert_called_once_with(
            self.html_strings[0],
            return_tensors='pt',
            padding='max_length',
            truncation=True,
            max_length=512
        )

    def test_empty_dataset(self):
        empty_html_strings = []
        dataset = MarkupLMDataset(empty_html_strings, self.processor)
        self.assertEqual(len(dataset), 0)

        # 尝试访问不存在的索引，应抛出 IndexError
        with self.assertRaises(IndexError):
            dataset[0]


if __name__ == '__main__':
    unittest.main()
