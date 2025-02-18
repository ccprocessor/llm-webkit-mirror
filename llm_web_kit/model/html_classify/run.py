"""
1. simplify html -> classify forum/article/other
"""

import importlib
import json

import torch
from torch.utils.data import DataLoader


class Main():
    def __init__(self, model_config, data_path):
        self.model_config = model_config
        self.data_path = data_path
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f'Using device: {self.device}')

    def load_module(self, model_class='model.Markuplm'):
        module_name, class_name = model_class.rsplit('.', 1)
        module = importlib.import_module(module_name)
        return module, class_name

    def load_data(self, input_path, key):
        data = []
        with open(input_path, 'r') as f:
            for line in f:
                data.append(json.loads(line)[key])
        return data

    def write_data(self, output_path, data):
        with open(output_path, 'w') as f:
            for line in data:
                f.write(json.dumps(line) + '\n')
                f.flush()

    def run(self):
        # load model
        module, class_name = self.load_module(self.model_config.pop('model_class'))
        self.model = getattr(module, class_name)(self.model_config, self.device)

        # load dataset
        module_model, model_name = self.load_module(self.model_config.pop('model_dataset'))
        val_html = self.load_data(self.data_path['input'], self.data_path['input_key'])
        self.val_dataset = getattr(module_model, model_name)(val_html, self.model.tokenizer)

        val_dataloader = DataLoader(self.val_dataset, batch_size=128, num_workers=32, pin_memory=True, shuffle=False)

        # inference
        outputs = self.model.inference(val_dataloader)

        self.write_data(self.data_path['output'], outputs)

        return outputs


if __name__ == '__main__':
    model_config = {
        'model_class': 'model.Markuplm',
        'model_dataset': 'dataset.MarkupLMDataset',
        'model_path': '/mnt/hwfile/opendatalab/dataproc/pengjiahui/models/markuplm-base',
        'checkpoint_path': '/mnt/hwfile/opendatalab/dataproc/pengjiahui/models/markuplm_202501222031_epoch_2.pt',
        'num_labels': 3,
    }

    data_path = {
        'input': '/mnt/hwfile/opendatalab/dataproc/pengjiahui/data/html/base_simplify_v2.jsonl',
        'input_key': 'html_simplified',
        'output': '/mnt/hwfile/opendatalab/dataproc/pengjiahui/data/html/base_simplify_v2_model.jsonl'
    }
    a = Main(model_config, data_path)
    outputs = a.run()
