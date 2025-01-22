import argparse
import json
import os
from pathlib import Path

from eval.magic_html import eval_magic_html
from eval.ours import eval_ours_extract_html
from eval.unstructured_eval import eval_unstructured

from llm_web_kit.dataio.filebase import (FileBasedDataReader,
                                         FileBasedDataWriter)

# 选项参数
parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, help='html文件路径')
parser.add_argument('--output', type=str, help='输出文件路径')
parser.add_argument('--tool', type=str, help='抽取工具', default='ours')
args = parser.parse_args()


root = Path(__file__).parent
sourcePath = os.path.join(root, 'html/all.json')
outputPath = os.path.join(root, 'output')
pipelineConfigPath = os.path.join(root, 'config/ours_config.jsonc')
pipeline_data_path = os.path.join(root, 'config/ours_data_config.jsonl')


reader = FileBasedDataReader('')
writer = FileBasedDataWriter('')


def main():
    out = {}
    # 读取html文件
    with open(sourcePath, 'r') as f:
        files = json.load(f)
        # files结构是{"filename":{"url":"","filepath":""}}，获取filepath
        for fileName in files:
            url = files[fileName]['url']
            filepath = files[fileName]['filepath']
            html = reader.read(f'{root}/html/{filepath}').decode('utf-8')

            # 评估
            if args.tool == 'magic_html':
                output = eval_magic_html(html, fileName)
            elif args.tool == 'unstructured':
                output = eval_unstructured(html, fileName)
            elif args.tool == 'ours':
                print(pipelineConfigPath)
                print(pipeline_data_path)
                print(f'{root}/html/{filepath}')
                output, content_list, main_html = eval_ours_extract_html(pipelineConfigPath, pipeline_data_path, f'{root}/html/{filepath}')
                out['content_list'] = content_list
                out['main_html'] = main_html
            else:
                raise ValueError(f'Invalid tool: {args.tool}')

            out['url'] = url
            out['content'] = output
            out['html'] = html
            writer.write(f'{outputPath}/{args.tool}/{fileName}.jsonl', json.dumps(out).encode('utf-8') + b'\n')


if __name__ == '__main__':
    main()
