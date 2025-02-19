import os
import unittest
from unittest import TestCase
from unittest.mock import patch

from llm_web_kit.model.html_layout_cls import HTMLLayoutClassifier


class TestHTMLLayoutClassifier(TestCase):

    @patch('llm_web_kit.model.html_layout_cls.Markuplm')
    @patch('llm_web_kit.model.html_layout_cls.HTMLLayoutClassifier.auto_download')
    def test_init(self, mock_auto_download, mock_markuplm):
        # Test default initialization
        mock_auto_download.return_value = '/fake/model/path'
        _ = HTMLLayoutClassifier()
        mock_markuplm.assert_called_once_with('/fake/model/path', 'cuda')

        # Test with custom model path
        mock_markuplm.reset_mock()
        HTMLLayoutClassifier(model_path='custom/path')
        mock_markuplm.assert_called_once_with('custom/path', 'cuda')

    @patch('llm_web_kit.model.html_layout_cls.CACHE_DIR')
    @patch('llm_web_kit.model.html_layout_cls.Markuplm')
    @patch('llm_web_kit.model.html_layout_cls.os.path.exists')
    @patch('llm_web_kit.model.html_layout_cls.unzip_local_file')
    @patch('llm_web_kit.model.html_layout_cls.download_auto_file')
    @patch('llm_web_kit.model.html_layout_cls.load_config')
    def test_auto_download(
        self,
        mock_load_config,
        mock_download,
        mock_unzip,
        mock_exists,
        mock_markuplm,
        mock_CACHE_DIR,
    ):
        mock_CACHE_DIR.return_value = '/fake/cache'
        # Mock config data
        mock_load_config.return_value = {
            'resources': {
                'html_cls-25m2': {'download_path': 's3://fake/path', 'md5': 'fake_md5'}
            }
        }

        # Mock file system state
        mock_exists.side_effect = lambda x: False if 'html_cls-25m2' in x else True
        mock_unzip.return_value = '/fake/unzip/path'
        mock_download.return_value = '/fake/cache/html_cls-25m2.zip'

        _ = HTMLLayoutClassifier()
        # result = classifier.auto_download()

        # self.assertEqual(result, "/fake/unzip/path")
        mock_download.assert_called_once_with(
            's3://fake/path',
            os.path.join(mock_CACHE_DIR, 'html_cls-25m2.zip'),
            'fake_md5',
        )
        mock_unzip.assert_called_once()

    @patch('llm_web_kit.model.html_layout_cls.Markuplm')
    def test_predict_single(self, mock_model):
        # Mock model init
        mock_model.return_value.inference_batch.return_value = [
            {'pred_prob': 0.98, 'pred_label': 'article'}
        ]

        classifier = HTMLLayoutClassifier(model_path='dummy')
        result = classifier.predict('<html>test</html>')

        self.assertEqual(result, {'pred_prob': 0.98, 'pred_label': 'article'})
        mock_model.return_value.inference_batch.assert_called_once_with(
            ['<html>test</html>']
        )

    @patch('llm_web_kit.model.html_layout_cls.Markuplm')
    def test_predict_batch(self, mock_model):
        # Setup mock model response
        mock_model.return_value.inference_batch.return_value = [
            {'pred_prob': 0.98, 'pred_label': 'article'},
            {'pred_prob': 0.99, 'pred_label': 'forum'},
        ]

        classifier = HTMLLayoutClassifier(model_path='dummy')
        inputs = ['<html>test1</html>', '<html>test2</html>']
        results = classifier.predict(inputs)

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['pred_label'], 'article')
        mock_model.return_value.inference_batch.assert_called_once_with(inputs)


if __name__ == '__main__':
    unittest.main()
