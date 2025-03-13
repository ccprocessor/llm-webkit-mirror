import argparse
import json

from loguru import logger

from llm_web_kit.html_layout_classify.s3.client import list_s3_objects
from llm_web_kit.html_layout_classify.s3.read import read_s3_rows
from llm_web_kit.html_layout_classify.s3.write import S3DocWriter
from llm_web_kit.model.html_layout_cls import HTMLLayoutClassifier

CLASSIFY_MAP = {'other': 0, 'article': 1, 'forum': 2}
INT_CLASSIFY_MAP = {0: 'other', 1: 'article', 2: 'forum'}
MODEL_VERESION = '0.0.2'


def __list_layout_sample_dir(s3_dir: str) -> list:
    """列出所有的layout sample json文件."""
    if s3_dir.endswith('/'):
        layout_sample_files = [f for f in list(list_s3_objects(s3_dir, recursive=True)) if f.endswith('.jsonl')]
        return layout_sample_files
    return [s3_dir]


def __parse_predict_res(predict_res: list, layout_samples: list) -> int:
    """解析模型分类结果."""
    # [{'pred_prob': '0.626298', 'pred_label': 'other'}]
    res = {
        'url_list': [i['url'] for i in layout_samples],
        'layout_id': layout_samples[0]['layout_id'],
        'page_type': INT_CLASSIFY_MAP.get(
            __most_frequent_or_zero([CLASSIFY_MAP.get(i['pred_label'], 0) for i in predict_res]), 'other'),
        'max_pred_prod': max([i['pred_prob'] for i in predict_res]),
        'version': MODEL_VERESION,
    }
    return res


def __most_frequent_or_zero(int_elements):
    """计算分类结果最多的类型，否则为0."""
    if not int_elements:
        return 0

    elif len(int_elements) == 1:
        return int_elements[0]

    elif len(int_elements) == 2:
        return int_elements[0] if int_elements[0] == int_elements[1] else 0

    elif len(int_elements) == 3:
        if int_elements[0] == int_elements[1] or int_elements[0] == int_elements[2]:
            return int_elements[0]
        elif int_elements[1] == int_elements[2]:
            return int_elements[1]
        else:
            return 0
    else:
        logger.error(f'most_frequent_or_zero error:{int_elements}')


def __process_one_layout_sample(layout_sample_file: str, layout_type_dir: str):
    """处理一个layout的代表群体."""
    output_file_path = f"{layout_type_dir}{layout_sample_file.split('/')[-1]}"
    writer = S3DocWriter(output_file_path)

    def __get_type_by_layoutid(layout_samples: list):
        # html_str_input = [general_simplify_html_str(html['html_source']) for html in layout_samples]
        html_str_input = [html['simp_html'] for html in layout_samples]
        layout_classify_lst = model.predict(html_str_input)
        layout_classify = __parse_predict_res(layout_classify_lst, layout_samples)
        return layout_classify

    current_layout_id, samples = None, []
    idx = 0
    for row in read_s3_rows(layout_sample_file):
        idx += 1
        detail_data = json.loads(row.value)
        if current_layout_id == detail_data['layout_id']:
            samples.append(detail_data)
        else:
            if samples:
                classify_res = __get_type_by_layoutid(samples)
                writer.write(classify_res)
            current_layout_id, samples = detail_data['layout_id'], [detail_data]
    if samples:
        classify_res = __get_type_by_layoutid(samples)
        writer.write(classify_res)
    writer.flush()
    logger.info(f'read {layout_sample_file} file {idx} rows')


def __set_config():
    global model
    model = HTMLLayoutClassifier()


def main():
    parser = argparse.ArgumentParser(description='Process files with specified function.')
    parser.add_argument('layout_sample_dir', help='待分类文件夹路径或文件路径')
    parser.add_argument('layout_classify_dir', help='已分类结果输出路径')

    args = parser.parse_args()

    try:
        # 加载模型
        __set_config()
        layout_sample_files = __list_layout_sample_dir(args.layout_sample_dir)
        # 读取每个json文件的数据，根据每个layout_id为一簇，计算每个layout_id 对应的 layout_classify，并将结果写入s3
        for layout_sample_file in layout_sample_files:
            __process_one_layout_sample(layout_sample_file, args.layout_classify_dir)
    except Exception as e:
        logger.error(f'get layout classify fail: {e}')


if __name__ == '__main__':
    main()
