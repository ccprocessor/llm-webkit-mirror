import argparse
import os
from pathlib import Path

from eval.magic_html import eval_magic_html
from eval.unstructured_eval import eval_unstructured

# 选项参数
parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, help='html文件路径')
parser.add_argument('--output', type=str, help='输出文件路径')
parser.add_argument('--tool', type=str, help='抽取工具', default='magic_html')
args = parser.parse_args()


sourcePath = os.path.join(Path(__file__).parent, './html')
outputPath = os.path.join(Path(__file__).parent, './output')


def main():
    htmls: list[tuple[str, str]] = []
    outputs: list[tuple[str, str]] = []
    # 读取html文件
    if args.input:
        with open(args.input, 'r') as f:
            html = f.read()
            htmls.append((args.input, html))
    else:
        # 流式读取bench/html目录以及下面所有目录
        for root, dirs, files in os.walk(sourcePath):
            for file in files:
                with open(f'{root}/{file}', 'r') as f:
                    # 获取文件名
                    fileName = file.split('.')[0]
                    html = f.read()
                    htmls.append((fileName, html))

    # 评估
    if args.tool == 'magic_html':
        for html in htmls:
            output = eval_magic_html(html[1], html[0])
            outputs.append((html[0], output))
    elif args.tool == 'unstructured':
        for html in htmls:
            output = eval_unstructured(html[1], html[0])
            outputs.append((html[0], output))
    else:
        raise ValueError(f'Invalid tool: {args.tool}')

    # 输出
    if args.output:
        with open(args.output, 'w') as f:
            for output in outputs:
                f.write(output[1])
    else:
        for output in outputs:
            # 如果目录不存在就创建
            if not os.path.exists(f'{outputPath}/{args.tool}'):
                os.makedirs(f'{outputPath}/{args.tool}')
            with open(f'{outputPath}/{args.tool}/{output[0]}.html', 'w') as f:
                f.write(output[1])


if __name__ == '__main__':
    main()
