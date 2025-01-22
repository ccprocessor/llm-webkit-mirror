import json
from typing import Dict, List, Tuple

from llm_web_kit.input.datajson import DataJson
from llm_web_kit.pipeline.pipeline_suit import PipelineSuit


def eval_ours_extract_html(pipeline_config, html_data_path, filePath) -> Tuple[str, List[Dict], str]:
    pipeline = PipelineSuit(pipeline_config)
    assert pipeline is not None

    # Read test data
    with open(html_data_path, 'r') as f:
        test_data = json.loads(f.readline().strip())

        # Create DataJson from test data
        input_data = DataJson(test_data)
        input_data.__setitem__('path', filePath)

    # Test extraction
    result = pipeline.extract(input_data)
    content_list = result.get_content_list()
    main_html = content_list.to_main_html()
    content = content_list.to_nlp_md()
    return content, content_list._get_data(), main_html
