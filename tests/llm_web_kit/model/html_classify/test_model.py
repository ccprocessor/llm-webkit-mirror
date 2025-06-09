import unittest
from unittest.mock import MagicMock, patch

import torch

from llm_web_kit.model.html_classify.model import Markuplm


class TestMarkuplm(unittest.TestCase):
    @patch('transformers.MarkupLMProcessor.from_pretrained')
    @patch('transformers.MarkupLMForSequenceClassification.from_pretrained')
    @patch('torch.load')
    def test_init(self, mock_load, mock_model_from_pretrained, mock_tokenizer_from_pretrained):
        # Mocking paths
        mock_load.return_value = MagicMock()  # Mock the model state dict
        mock_model_from_pretrained.return_value = MagicMock()  # Mock the model
        mock_tokenizer_from_pretrained.return_value = MagicMock()  # Mock the tokenizer

        # Initialize Markuplm
        model_path = '/fake/path'
        device = 'cpu'
        markuplm = Markuplm(model_path, device)

        # Assertions
        self.assertEqual(markuplm.path, model_path)
        self.assertEqual(markuplm.device, device)
        mock_model_from_pretrained.assert_called_once_with(markuplm.model_path, num_labels=markuplm.num_labels)
        mock_tokenizer_from_pretrained.assert_called_once_with(markuplm.model_path)

    @patch('transformers.MarkupLMProcessor.from_pretrained')
    @patch('transformers.MarkupLMForSequenceClassification.from_pretrained')
    @patch('torch.load')
    def test_inference_batch(self, mock_load, mock_model_from_pretrained, mock_tokenizer_from_pretrained):
        # Mocking model and tokenizer
        mock_model = MagicMock()
        mock_tokenizer = MagicMock()
        mock_model_from_pretrained.return_value = mock_model
        mock_tokenizer_from_pretrained.return_value = mock_tokenizer

        # Mocking model output
        logits_tensor = torch.tensor([[0.2, 0.5, 0.3]])
        mock_outputs = MagicMock()
        mock_outputs.logits = logits_tensor
        mock_model.return_value = mock_outputs

        # Initialize Markuplm
        model_path = '/fake/path'
        device = 'cpu'
        markuplm = Markuplm(model_path, device)

        # Mock input
        html_batch = ['<html>test</html>']
        result = markuplm.inference_batch(html_batch)

        # Assertions
        mock_tokenizer.assert_called_once_with(
            html_batch,
            return_tensors='pt',
            padding='max_length',
            truncation=True,
            max_length=markuplm.max_tokens
        )
        self.assertEqual(len(result), 1)
        self.assertIn('pred_prob', result[0])
        self.assertIn('pred_label', result[0])


if __name__ == '__main__':
    unittest.main()
