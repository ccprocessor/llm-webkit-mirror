import unittest
from pathlib import Path

from llm_web_kit.extractor.html.pre_extractor import \
    HTMLFileFormatFilterTablePreExtractor
from llm_web_kit.input.datajson import DataJson

TEST_CASES = [
    {
        'input': [
            'assets/format_table.html'
        ]
    }
]
base_dir = Path(__file__).parent


class TestHtmlPreExtractorRemoveFormatTable(unittest.TestCase):
    def setUp(self):
        self.pre_extract = HTMLFileFormatFilterTablePreExtractor({})

    def test_RemoveFormatTable(self):
        """remove format table."""
        for test_case in TEST_CASES:
            raw_html_path = base_dir.joinpath(test_case['input'][0])
            print(raw_html_path)
            raw_html = raw_html_path.read_text(encoding='utf-8')
            data_json = {  # 构造一个测试数据，检测是否把文本中的连续空格字符转换为1个空格字符
                'html': raw_html,
                'content_list': [],
                'url': 'http://anomaly.pp.ua/ucp.php?mode=terms&sid=5fe672c6792edb29e8319b6fef6a19a1',
                'dataset_name': 'CC',
                'data_source_category': 'html',
                'path': ''
            }
            input_data = DataJson(data_json)
            results = self.pre_extract._filter_by_rule(input_data)
            assert results is False
