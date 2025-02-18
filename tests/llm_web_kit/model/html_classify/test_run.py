
import json
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

from torch.utils.data import DataLoader

sys.path.append('../../../../llm_web_kit/model/html_classify')
from run import Main


class TestMain(unittest.TestCase):
    def setUp(self):
        self.model_config = {
            'model_class': 'model.Markuplm',
            'model_dataset': 'dataset.MarkupLMDataset',
            'model_path': '/mnt/hwfile/opendatalab/dataproc/pengjiahui/models/markuplm-base',
            'checkpoint_path': '/mnt/hwfile/opendatalab/dataproc/pengjiahui/models/markuplm_202501222031_epoch_2.pt',
            'num_labels': 3
        }
        self.data_path = {
            'input': 'test_input.jsonl',
            'input_key': 'html',
            'output': 'test_output.jsonl'
        }
        with open(self.data_path['input'], 'w') as f:
            f.write(json.dumps({'html': '<div>Test</div>', 'human':'article'}) + '\n')
        self.main = Main(self.model_config, self.data_path)

    def test_init(self):
        self.assertEqual(self.main.model_config, self.model_config)
        self.assertEqual(self.main.data_path, self.data_path)
        self.assertIn(str(self.main.device), ['cpu', 'cuda'])

    def test_load_module(self):
        module, class_name = self.main.load_module('model.Markuplm')
        self.assertEqual(module.__name__, 'model')
        self.assertEqual(class_name, 'Markuplm')

    def test_load_data(self):
        data = self.main.load_data(self.data_path['input'], 'html')
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], '<div>Test</div>')

    def test_write_data(self):
        test_output = [{'result': 'success'}]
        self.main.write_data(self.data_path['output'], test_output)
        with open(self.data_path['output'], 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 1)
            self.assertEqual(json.loads(lines[0]), {'result': 'success'})

    def test_run(self):
        with patch('model.Markuplm') as mock_model:
            main = Main(self.model_config, self.data_path)
            mock_model_instance = mock_model.return_value
            mock_model_instance.inference.return_value = [{'pred_label': 'article'}]

            main.val_dataset = MagicMock()
            main.val_dataloader = DataLoader(main.val_dataset, batch_size=1)

            outputs = main.run()
            self.assertEqual(len(outputs), 1)
            self.assertEqual(outputs[0]['pred_label'], 'article')

    def tearDown(self):
        # clean data files
        if os.path.exists(self.data_path['input']):
            os.remove(self.data_path['input'])
        if os.path.exists(self.data_path['output']):
            os.remove(self.data_path['output'])


if __name__ == '__main__':
    unittest.main()
