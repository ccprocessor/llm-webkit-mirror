
from abc import ABC

import torch


class Markuplm(ABC):
    # pad_token_id = 0
    def __init__(self, config: dict, device):
        self.checkpoint_path = config.get('checkpoint_path')
        self.num_labels = config.get('num_labels',3)
        self.model_path = config.get('model_path')

        self.device = device

        self.model = self.load_model()
        self.tokenizer = self.load_tokenizer()
        self.max_tokens = int(config.get('max_tokens', 512))
        self.label2id = {0:'article', 1:'forum', 2:'other'}

    def load_tokenizer(self):
        # 导入MarkupLMProcessor类
        from transformers import MarkupLMProcessor

        # 从self.model_path路径加载MarkupLMProcessor类
        return MarkupLMProcessor.from_pretrained(self.model_path)

    def load_model(self):
        from transformers import MarkupLMForSequenceClassification
        model = MarkupLMForSequenceClassification.from_pretrained(self.model_path, num_labels=self.num_labels)
        # load checkpoint
        model.load_state_dict(torch.load(self.checkpoint_path, map_location=self.device))
        model.to(self.device)
        model.eval()

        return model

    def inference(self, dataloader):
        outputs_result = []

        with torch.no_grad():
            for batch in dataloader:
                batch = {k: v.to(self.device) for k, v in batch.items()}

                outputs = self.model(**batch)
                logits = outputs.logits

                prob = torch.softmax(logits, dim=-1)
                label_index = torch.argmax(prob, axis=-1).cpu().numpy()
                pos_prob = prob.detach().cpu().numpy()

                for i,prob in enumerate(pos_prob):
                    max_prob = round(float(max(prob)), 6)
                    max_label = self.label2id[label_index[i]]
                    output = {'pred_prob': str(max_prob), 'pred_label': str(max_label)}
                    outputs_result.append(output)
        return outputs_result
