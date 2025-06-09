import os

import torch

from llm_web_kit.model.resource_utils import import_transformer


class Markuplm():
    def __init__(self, path, device):
        self.path = path
        self.model_path = os.path.join(self.path, 'markuplm-base')

        self.device = device
        self.num_labels = 4
        self.max_tokens = 512
        self.label2id = {0: 'Article', 1: 'Forum_or_Article_with_commentsection', 2: 'Content Listing', 3: 'Other'}

        self.model = self.load_model()
        self.tokenizer = self.load_tokenizer()

    def load_tokenizer(self):
        transformers = import_transformer()

        return transformers.MarkupLMProcessor.from_pretrained(self.model_path)

    def load_model(self):
        transformers = import_transformer()
        model = transformers.MarkupLMForSequenceClassification.from_pretrained(self.model_path, num_labels=self.num_labels)
        model.to(self.device)
        model.eval()

        return model

    def inference_batch(self, html_batch: list[str]):
        token_batch = self.tokenizer(
            html_batch,
            return_tensors='pt',
            padding='max_length',
            truncation=True,
            max_length=self.max_tokens
        )

        batch = {k: v.to(self.device) for k, v in token_batch.items()}

        outputs = self.model(**batch)
        logits = outputs.logits

        prob = torch.softmax(logits, dim=-1)
        label_index = torch.argmax(prob, axis=-1).cpu().numpy()
        pos_prob = prob.detach().cpu().numpy()

        outputs_result = []
        for i,prob in enumerate(pos_prob):
            max_prob = round(float(max(prob)), 6)
            max_label = self.label2id[label_index[i]]
            output = {'pred_prob': str(max_prob), 'pred_label': str(max_label)}
            outputs_result.append(output)
        return outputs_result
