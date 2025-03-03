import json

from llm_web_kit.html_layout_classify.s3.utils import (S3DocWriter,
                                                       list_s3_objects,
                                                       read_s3_rows)
from llm_web_kit.model.html_layout_cls import HTMLLayoutClassifier
from llm_web_kit.model.html_lib.simplify import general_simplify_html_str


def __list_layout_sample_dir(s3_dir: str) -> list:
    """列出所有的layout sample json文件."""
    if s3_dir.endswith('/'):
        layout_sample_files = [f for f in list(list_s3_objects(s3_dir, recursive=True)) if f.endswith('.jsonl.gz')]
        return layout_sample_files
    return [s3_dir]


def most_frequent_or_zero(int_elements):
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
        print(f"error data:{int_elements}")


def __process_one_layout_sample(layout_sample_file: str, layout_type_dir: str):
    """处理一个layout的代表群体."""
    output_file_path = f"{layout_type_dir}{layout_sample_file.split('/')[-1].replace('.gz', '').replace('.jsonl', '')}.json"
    s3_writer = S3DocWriter(output_file_path)

    def __get_type_by_layoutid(layout_samples: list):
        html_str_input = [general_simplify_html_str(html['html_source']) for html in layout_samples]
        # html_str_input = [html["simp_html"] for html in layout_samples]
        layout_classify_lst = model.predict(html_str_input)
        layout_classify = most_frequent_or_zero(layout_classify_lst)
        return {'layout_id': layout_samples[0]['layout_id'], 'layout_classify': layout_classify}

    current_layout_id, samples = None, []
    for row in read_s3_rows(layout_sample_file):
        detail_data = json.loads(row.value)
        if current_layout_id == detail_data['layout_id']:
            samples.append(detail_data)
        else:
            if samples:
                layoutid_classify = __get_type_by_layoutid(samples)
                s3_writer.write(layoutid_classify)
            current_layout_id, samples = detail_data['layout_id'], [detail_data]
    if samples:
        layoutid_classify = __get_type_by_layoutid(samples)
        s3_writer.write(layoutid_classify)
    s3_writer.flush()


def __set_config():
    global model
    model = HTMLLayoutClassifier()


def main(layout_sample_dir: str, layout_type_dir: str):
    try:
        __set_config()
        # 解析所有json文件
        layout_sample_files = __list_layout_sample_dir(layout_sample_dir)
        # 然后针对每个文件，每次读一个layout的代表，然后计算分类情况
        for layout_sample_file in layout_sample_files:
            __process_one_layout_sample(layout_sample_file, layout_type_dir)
    except Exception as e:
        msg = 'get layout classify fail'
        raise Exception(msg) from e


if __name__ == '__main__':
    # layout_sample_dir = "s3://web-parse-huawei/CC/contrast_test_data/txt/v002/"
    layout_sample_dir = 's3://web-parse-huawei/renpengli/sorted_demo/v001/part-67c576582e79-000000.jsonl'
    layout_type_dir = 's3://web-parse-huawei/renpengli/layoutid_sorted/'
    main(layout_sample_dir, layout_type_dir)
