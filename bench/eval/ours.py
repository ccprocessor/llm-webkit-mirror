import json

from llm_web_kit.input.datajson import DataJson
from llm_web_kit.pipeline.pipeline_suit import PipelineSuit


def eval_ours_extract_html(pipeline_config, html_data_path, filePath) -> str:
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
    return result.to_html()
