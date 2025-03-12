import json
from typing import Dict, List, Tuple

from llm_web_kit.extractor.extractor_chain import ExtractSimpleFactory
from llm_web_kit.input.datajson import DataJson, DataJsonKey


def eval_ours_extract_html(chain_config: dict, html_data_path: str, filePath: str, page_layout_type: str = '', url: str = '') -> Tuple[str, List[Dict], str, dict]:
    chain = ExtractSimpleFactory.create(chain_config)
    assert chain is not None

    # Read test data
    with open(html_data_path, 'r') as f:
        test_data = json.loads(f.readline().strip())

        # Create DataJson from test data
        input_data = DataJson(test_data)
        input_data.__setitem__('path', filePath)
        input_data.__setitem__('page_layout_type', page_layout_type)
        input_data.__setitem__('url', url)

    # Test extraction
    result = chain.extract(input_data)
    content_list = result.get_content_list()
    statics = result.get(DataJsonKey.METAINFO, {}).get(DataJsonKey.STATICS, {})
    main_html = content_list.to_main_html()
    content = content_list.to_nlp_md()
    return content, content_list._get_data(), main_html, statics
