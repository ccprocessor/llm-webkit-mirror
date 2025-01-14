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
        input_data = DataJson({'dataset_name': 'news', 'data_source_category': 'html', 'html': '<html><body><h1>hello</h1></body></html>', 'url': 'http://www.baidu.com'})
        data: DataJson = pipesuit.format(input_data)
        assert data.get_content_list().length() == 0
        assert data.get_dataset_name() == 'news'
        assert data.get_file_format() == 'html'
        data_e: DataJson = pipesuit.extract(input_data)
        assert data_e.get_content_list().length() == 0
        assert data_e.get_dataset_name() == 'news'
        assert data_e.get_file_format() == 'html'

    def test_pipeline_pdf(self):
        """Test pipeline with PDF input."""
        pipesuit = PipelineSuit(f'{os.path.dirname(os.path.abspath(__file__))}/assets/pdf_pipe_normal.jsonc')
        self.assertIsNotNone(pipesuit)
        input_data = DataJson({'dataset_name': 'news', 'data_source_category': 'pdf'})

        # Test format
        data: DataJson = pipesuit.format(input_data)
        assert data.get_content_list().length() == 0
        assert data.get_dataset_name() == 'news'
        assert data.get_file_format() == 'pdf'

        # Test extract
        data_e: DataJson = pipesuit.extract(data)
        assert data_e.get_content_list().length() == 0
        assert data_e.get_dataset_name() == 'news'
        assert data_e.get_file_format() == 'pdf'

    def test_pipeline_ebook(self):
        """Test pipeline with ebook input."""
        pipesuit = PipelineSuit(f'{os.path.dirname(os.path.abspath(__file__))}/assets/ebook_pipe_normal.jsonc')
        self.assertIsNotNone(pipesuit)
        input_data = DataJson({'dataset_name': 'news', 'data_source_category': 'ebook', 'content_list': [[],[]]})

        # Test format
        data: DataJson = pipesuit.format(input_data)
        assert data.get_content_list().length() == 2
        assert data.get_dataset_name() == 'news'
        assert data.get_file_format() == 'ebook'

        # Test extract
        data_e: DataJson = pipesuit.extract(input_data)
        assert data_e.get_content_list().length() == 2
        assert data_e.get_dataset_name() == 'news'
        assert data_e.get_file_format() == 'ebook'
