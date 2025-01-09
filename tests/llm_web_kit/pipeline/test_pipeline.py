import os
import unittest

from llm_web_kit.input.datajson import DataJson
from llm_web_kit.pipeline.pipeline_suit import PipelineSuit


class TestPipelineSuite(unittest.TestCase):
    """Test pipeline."""

    def test_pipeline_init(self):
        """Test pipeline init."""
        # html
        pipesuit = PipelineSuit(f'{os.path.dirname(os.path.abspath(__file__))}/assets/html_pipe_normal.jsonc')
        self.assertIsNotNone(pipesuit)
        input_data = {'dataset_name': 'news', 'file_format': 'html', 'html': '<html><body><h1>hello</h1></body></html>', 'url': 'http://www.baidu.com'}
        data: DataJson = pipesuit.format(input_data)
        assert data.get_content_list().length() == 0
        assert data.get_dataset_name() == 'news'
        assert data.get_file_format() == 'html'
        data_e: DataJson = pipesuit.extract(input_data)
        assert data_e.get_content_list().length() == 0
        assert data_e.get_dataset_name() == 'news'
        assert data_e.get_file_format() == 'html'
        # pdf
        pipesuit = PipelineSuit(f'{os.path.dirname(os.path.abspath(__file__))}/assets/pdf_pipe_normal.jsonc')
        self.assertIsNotNone(pipesuit)
        input_data = {'dataset_name': 'news', 'file_format': 'pdf'}
        data: DataJson = pipesuit.format(input_data)
        assert data.get_content_list().length() == 0
        assert data.get_dataset_name() == 'news'
        assert data.get_file_format() == 'pdf'
        data_e: DataJson = pipesuit.extract(input_data)
        assert data_e.get_content_list().length() == 0
        assert data_e.get_dataset_name() == 'news'
        assert data_e.get_file_format() == 'pdf'
        # ebook
        pipesuit = PipelineSuit(f'{os.path.dirname(os.path.abspath(__file__))}/assets/ebook_pipe_normal.jsonc')
        self.assertIsNotNone(pipesuit)
        input_data = {'dataset_name': 'news', 'file_format': 'ebook', 'content_list': {'a': 1, 'b': 2}}
        data: DataJson = pipesuit.format(input_data)
        assert data.get_content_list().length() == 2
        assert data.get_dataset_name() == 'news'
        assert data.get_file_format() == 'ebook'
        data_e: DataJson = pipesuit.extract(input_data)
        assert data_e.get_content_list().length() == 2
        assert data_e.get_dataset_name() == 'news'
        assert data_e.get_file_format() == 'ebook'
