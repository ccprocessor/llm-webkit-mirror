import argparse
import os
from pathlib import Path

from eval.magic_html import eval_magic_html
from eval.ours import eval_ours_extract_html
from eval.unstructured_eval import eval_unstructured

from llm_web_kit.data.filebase import FileBasedDataReader, FileBasedDataWriter

# 选项参数
parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, help='html文件路径')
parser.add_argument('--output', type=str, help='输出文件路径')
parser.add_argument('--tool', type=str, help='抽取工具', default='magic_html')
args = parser.parse_args()


sourcePath = os.path.join(Path(__file__).parent, 'html')
outputPath = os.path.join(Path(__file__).parent, 'output')
pipelineConfigPath = os.path.join(Path(__file__).parent, 'ours_config.jsonc')
html_data_path = os.path.join(Path(__file__).parent, 'ours_data_config.jsonl')


reader = FileBasedDataReader('')
writer = FileBasedDataWriter('')


def main():
    # 读取html文件
    for root, dirs, files in os.walk(sourcePath):
        for file in files:
            fileName = file.split('.')[0]
            html = reader.read(f'{root}/{file}').decode('utf-8')

            # 评估
            if args.tool == 'magic_html':
                output = eval_magic_html(html, fileName)
            elif args.tool == 'unstructured':
                output = eval_unstructured(html, fileName)
            elif args.tool == 'ours':
                print(pipelineConfigPath)
                print(html_data_path)
                print(f'{root}/{file}')
                output = eval_ours_extract_html(pipelineConfigPath, html_data_path, f'{root}/{file}')
            else:
                raise ValueError(f'Invalid tool: {args.tool}')

            # 如果目录不存在就创建
            writer.write(f'{outputPath}/{args.tool}/{fileName}.html', output.encode('utf-8'))


if __name__ == '__main__':
    main()
