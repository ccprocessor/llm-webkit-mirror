import argparse
import json
import os
import uuid
from pathlib import Path

from bench.common.metrics import Metrics
from bench.common.result import Result_Detail, Result_Summary
from bench.eval.ours import eval_ours_extract_html
from llm_web_kit.dataio.filebase import (FileBasedDataReader,
                                         FileBasedDataWriter)
from llm_web_kit.extractor.html.main_html_parser import MagicHTMLMainHtmlParser
from llm_web_kit.libs.statics import Statics


def parse_arguments():
    """解析命令行参数."""
    parser = argparse.ArgumentParser(description='HTML提取与评估工具')
    parser.add_argument('--input', type=str, help='HTML文件路径')
    parser.add_argument('--output', type=str, help='输出文件路径')
    parser.add_argument('--tool',
                        type=str,
                        choices=['ours', 'magic_html', 'unstructured'],
                        help='抽取工具',
                        default='ours')
    return parser.parse_args()


def setup_paths():
    """设置文件路径."""
    root = Path(__file__).parent
    paths = {
        'root': root,
        'source': root / 'data' / 'all.json',
        'output': root / 'output',
        'pipeline_config': root / 'config' / 'ours_config.jsonc',
        'pipeline_data': root / 'config' / 'data_config.jsonl'
    }
    return paths


def run_ours(config_path, data_path, output_path, statics_pre, reader, writer,
             summary, detail):
    """运行我们的提取模型.

    Args:
        config_path: 配置文件路径
        data_path: 数据文件路径
        output_path: 输出路径
        statics_pre: 统计对象
        reader: 文件读取器
        writer: 文件写入器
    """
    try:
        # 确保路径是字符串
        config_path_str = str(config_path)
        data_path_str = str(data_path)
        output_path_str = str(output_path)

        print(f'配置路径: {config_path_str}')
        print(f'数据路径: {data_path_str}')
        print(f'输出路径: {output_path_str}')

        # 加载配置文件
        import commentjson
        with open(config_path_str, 'r', encoding='utf-8') as f:
            chain_config = commentjson.load(f)

        with open(data_path_str, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    if not line.strip():
                        print(f'跳过空行 {line_num}')
                        continue

                    print(f'处理第 {line_num} 行: {line[:50]}...')
                    data_json = json.loads(line.strip())

                    # 执行评估
                    content, content_list, statics = eval_ours_extract_html(
                        chain_config, data_json)

                    # 获取路径并进行安全处理
                    path = data_json.get('path', '')

                    # 构建文件绝对路径 - 使用字符串操作而非Path对象
                    root_dir = os.path.dirname(os.path.dirname(data_path_str))
                    file_path = os.path.join(root_dir, path) if path else None

                    # HTML内容
                    html_content = ''
                    if file_path and os.path.exists(file_path):
                        try:
                            html_content = reader.read(file_path).decode(
                                'utf-8')
                            print(f'成功读取HTML，长度: {len(html_content)}')
                        except Exception as e:
                            print(f'读取HTML文件失败: {e}')
                    else:
                        print(f'文件不存在或路径为空: {file_path}')

                    # 提取main_html
                    htmlExtractor = MagicHTMLMainHtmlParser(
                        chain_config)
                    main_html, method, title = htmlExtractor._extract_main_html(
                        html_content, data_json.get('url', ''),
                        data_json.get('page_layout_type', 'article'))

                    # 准备输出内容
                    out = {
                        'url': data_json.get('url', ''),
                        'content': content,
                        'main_html': main_html,
                        'content_list': content_list,
                        'html': html_content,
                        'statics': statics
                    }

                    # 输出统计信息
                    Statics(statics).print()
                    statics_pre.merge_statics(statics)

                    # 确定输出路径
                    track_id = data_json.get('track_id', str(uuid.uuid4()))
                    output_dir = os.path.join(output_path_str, 'ours')
                    output_file = os.path.join(output_dir, f'{track_id}.jsonl')

                    # 确保目录存在
                    os.makedirs(output_dir, exist_ok=True)

                    # 写入结果 - 分步处理以便更好定位问题
                    json_str = json.dumps(out, ensure_ascii=False)
                    out_bytes = json_str.encode('utf-8') + b'\n'
                    writer.write(output_file, out_bytes)
                    print(f'成功写入结果到: {output_file}')
                    summary.total += 1
                except Exception as e:
                    summary.error_summary['count'] += 1
                    import traceback
                    print(f'处理单条数据时出错: {e}')
                    print(traceback.format_exc())
    except Exception as e:
        import traceback
        print(f'运行ours评估时出错: {e}')
        print(traceback.format_exc())
    return summary, detail, statics_pre


def run_magic_html(html, url, file_name, output_path, writer):
    """运行magic_html提取模型.

    Args:
        html: HTML内容
        url: 网页URL
        file_name: 文件名
        output_path: 输出路径
        writer: 文件写入器
    """
    try:
        from bench.eval.magic_html import eval_magic_html
        output = eval_magic_html(html, file_name)
        out = {
            'url': url,
            'content': output,
            'html': html,
        }

        # 确保目录存在
        os.makedirs(os.path.join(output_path, 'magic_html'), exist_ok=True)

        writer.write(
            os.path.join(output_path, 'magic_html', f'{file_name}.jsonl'),
            json.dumps(out, ensure_ascii=False).encode('utf-8') + b'\n')
    except Exception as e:
        print(f'运行magic_html评估时出错: {e}')


def run_unstructured(html, url, file_name, output_path, writer):
    """运行unstructured提取模型.

    Args:
        html: HTML内容
        url: 网页URL
        file_name: 文件名
        output_path: 输出路径
        writer: 文件写入器
    """
    try:
        from bench.eval.unstructured_eval import eval_unstructured
        output = eval_unstructured(html, file_name)
        out = {
            'url': url,
            'content': output,
            'html': html,
        }

        # 确保目录存在
        os.makedirs(os.path.join(output_path, 'unstructured'), exist_ok=True)

        writer.write(
            os.path.join(output_path, 'unstructured', f'{file_name}.jsonl'),
            json.dumps(out, ensure_ascii=False).encode('utf-8') + b'\n')
    except Exception as e:
        print(f'运行unstructured评估时出错: {e}')


def main():
    """主函数."""
    # 解析参数
    args = parse_arguments()

    # 设置路径
    paths = setup_paths()

    # 创建读写器
    reader = FileBasedDataReader('')
    writer = FileBasedDataWriter('')

    # 生成任务ID
    task_id = str(uuid.uuid1())
    output_path = os.path.join(paths['output'], task_id)

    # 创建评测结果概览
    summary = Result_Summary.create(task_id=task_id,
                                    output_path=output_path,
                                    total=0,
                                    result_summary={},
                                    error_count=0)

    # 创建评测结果详情
    detail = Result_Detail.create(
        task_id=summary.task_id,  # 使用相同的task_id
        output_path=output_path,
    )

    # 创建统计对象
    statics_gt = Statics()
    statics_pre = Statics()
    metrics = Metrics()

    # 如果是ours工具，直接运行ours评估
    if args.tool == 'ours':
        summary, detail, statics_pre = run_ours(paths['pipeline_config'],
                                                paths['pipeline_data'],
                                                paths['output'], statics_pre,
                                                reader, writer, summary,
                                                detail)
    else:
        # 读取HTML文件
        try:
            with open(paths['source'], 'r', encoding='utf-8') as f:
                files = json.load(f)
                # files结构是{"filename":{"url":"","filepath":""}}
                for file_name in files:
                    try:
                        file_data = files[file_name]
                        url = file_data.get('url', '')
                        origin_filepath = file_data.get('origin_filepath', '')
                        groundtruth_filepath = file_data.get(
                            'groundtruth_filepath', '')
                        layout_type = file_data.get('layout_type', '')

                        print(f'处理: {file_name}, 类型: {layout_type}')

                        # 读取HTML和标准答案
                        root_dir = paths['root'] / 'data'
                        html_path = root_dir / origin_filepath
                        groundtruth_path = root_dir / groundtruth_filepath

                        try:
                            html = reader.read(str(html_path)).decode('utf-8')
                            groundtruth_data = reader.read(
                                str(groundtruth_path)).decode('utf-8')
                            groundtruth = json.loads(groundtruth_data)
                            statics_gt.merge_statics(
                                groundtruth.get('statics', {}))
                        except Exception as e:
                            print(f'读取文件失败: {e}')
                            continue

                        # 根据工具类型运行不同的评估
                        if args.tool == 'magic_html':
                            run_magic_html(html, url, file_name,
                                           paths['output'], writer)
                        elif args.tool == 'unstructured':
                            run_unstructured(html, url, file_name,
                                             paths['output'], writer)
                    except Exception as e:
                        print(f'处理文件 {file_name} 时出错: {e}')
        except Exception as e:
            print(f'读取源文件时出错: {e}')

    # 完成评估并输出结果
    summary.finish()
    detail.finish()

    # 输出统计信息
    statics_gt.print()
    statics_pre.print()

    # 计算评估结果
    result = metrics.eval_type_acc(statics_gt, statics_pre)
    print(json.dumps(result, indent=4))

    # 更新摘要结果
    summary.result_summary = result

    # 输出摘要和详情
    print(json.dumps(summary.to_dict(), indent=4))
    print(json.dumps(detail.to_dict(), indent=4))

    return summary, detail


if __name__ == '__main__':
    main()
