from typing import Dict, List, Tuple

from llm_web_kit.extractor.extractor_chain import ExtractSimpleFactory
from llm_web_kit.input.datajson import DataJson, DataJsonKey


def eval_ours_extract_html(chain_config: dict, test_data: dict) -> Tuple[str, List[Dict], str, dict]:
    chain = ExtractSimpleFactory.create(chain_config)
    assert chain is not None

    # Create DataJson from test data
    input_data = DataJson(test_data)

    # Test extraction
    result = chain.extract(input_data)
    content_list = result.get_content_list()
    statics = result.get(DataJsonKey.METAINFO, {}).get(DataJsonKey.STATICS, {})
    content = content_list.to_nlp_md()
    return content, content_list._get_data(), statics


# if __name__ == '__main__':
#     root = Path(__file__).parent.parent.parent
#     from llm_web_kit.dataio.filebase import (FileBasedDataReader,
#                                              FileBasedDataWriter)
#     reader = FileBasedDataReader('')
#     writer = FileBasedDataWriter('')

#     # 确保输出目录存在
#     output_dir = f'{root}/bench/output/ours'
#     os.makedirs(output_dir, exist_ok=True)

#     with open(f'{root}/bench/config/ours_config.jsonc', 'r') as f:
#         chain_config = json.load(f)

#     # 循环处理每一行数据
#     with open(f'{root}/bench/config/data_math_config.jsonl', 'r') as f:
#         for line in f:
#             test_data = json.loads(line.strip())
#             content, content_list, statics = eval_ours_extract_html(
#                 chain_config,
#                 test_data
#             )
#             print('处理数据:', test_data.get('track_id'))
#             print('URL:', test_data.get('url'))
#             print('统计信息:', statics)

#             # 读取html
#             html_content = reader.read(
#                 f'{root}/bench/{test_data.get('path')}'
#             ).decode('utf-8')

#             # 提取main_html
#             from llm_web_kit.extractor.html.extractor import \
#                 MagicHTMLFIleFormatorExtractor
#             htmlExtractor = MagicHTMLFIleFormatorExtractor(chain_config)
#             main_html, method, title = htmlExtractor._extract_main_html(
#                 html_content, test_data.get('url', ''), test_data.get('page_layout_type', 'article')
#             )

#             out = {
#                 'url': test_data.get('url'),
#                 'content': content,
#                 'main_html': main_html,
#                 'content_list': content_list,
#                 'html': html_content,
#                 'statics': statics
#             }

#             # 获取path的前两级目录
#             path = test_data.get('path', '')
#             path_parts = path.split('/')
#             if len(path_parts) >= 2:
#                 output_subdir = '/'.join(path_parts[:2])
#             else:
#                 output_subdir = 'unknown'

#             # 创建对应的输出目录
#             output_dir = f'{root}/bench/output/ours/{output_subdir}'

#             # 追加写入结果
#             output_file = f'{output_dir}.jsonl'
#             writer.append_write(
#                 output_file,
#                 json.dumps(out).encode('utf-8') + b'\n'
#             )
#             print(f'结果已追加到: {output_file}')
