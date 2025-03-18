import json
import os
import socket
import time
from io import BytesIO
from pathlib import Path

import click
import requests
from loguru import logger
from retry import retry

from llm_web_kit.model.html_layout_cls import HTMLLayoutClassifier

CLASSIFY_MAP = {'other': 0, 'article': 1, 'forum': 2}
INT_CLASSIFY_MAP = {0: 'other', 1: 'article', 2: 'forum'}
MODEL_VERESION = '0.0.2'
MODEL = None
GET_FILE_URL = None
UPDATE_STATUS_URL = None


def __get_runtime_id():
    # 获取 hostname
    hostname = socket.gethostname()
    job_id = os.environ.get('SLURM_JOB_ID', 'unknown')
    return f'{hostname}_{job_id}'


def __read_sample_of_layout_id(to_process_file_path):
    """读取to_process_file_path路径的文件，并根据layout_id进行读取，每个layout_id为一组.

    每次yield一个list, 列表中是layout_id对应的layout_samples. 读取直到layout_id发生变化.
    """
    cur_layout_id = None
    cur_layout_samples = []
    with open(to_process_file_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            if data['layout_id'] == cur_layout_id or cur_layout_id is None:
                cur_layout_samples.append(data)
                cur_layout_id = data['layout_id']
            else:
                yield cur_layout_samples
                cur_layout_id = data['layout_id']
                cur_layout_samples = [data]
    yield cur_layout_samples


def __do_page_classify(samples:list) -> tuple[str, float]:
    """对samples进行分类，返回分类结果标签和最大概率."""
    if len(samples) <= 1:
        logger.error(f"samples of layout_id {samples[0]['layout_id']} is less than 1 or empty")
        return 'other', 0.0

    # 进行2次分类
    html_str_inputs = [html['simp_html'] for html in samples]
    classify_res_top_2 = MODEL.predict(html_str_inputs[0:2])
    # 如果分类结果一致，则直接写入结果
    if classify_res_top_2[0]['pred_label'] == classify_res_top_2[1]['pred_label']:  # 如果1和2的分类结果一致，则直接返回1的分类结果
        return classify_res_top_2[0]['pred_label'], max(classify_res_top_2[0]['pred_prob'], classify_res_top_2[1]['pred_prob'])
    else:  # 如果分类结果不一致，则进行第三次分类
        if len(samples) > 2:
            classify_3 = MODEL.predict([html_str_inputs[2]])
            if classify_3[0]['pred_label'] == classify_res_top_2[0]['pred_label']:
                return classify_3[0]['pred_label'], max(classify_3[0]['pred_prob'], classify_res_top_2[0]['pred_prob'])
            elif classify_3[0]['pred_label'] == classify_res_top_2[1]['pred_label']:
                return classify_3[0]['pred_label'], max(classify_3[0]['pred_prob'], classify_res_top_2[1]['pred_prob'])
            else:  # 第三个和前两个任何一个分类结果都不一致，则把类别分到other里
                return 'other', 0.0
        else:
            return 'other', 0.0


def __process_one_layout_file(result_save_dir, to_process_file_path):
    """读取to_process_file_path路径的文件，并进行分类，将结果写入result_save_dir路径
    读取的时候，需要根据layout_id进行读取，每个layout_id为一组，每组内部进行分类。 分类的时候，先进行2次分类，如果分类结果一致，则直接
    写入结果，如果分类结果不一致，则进行第三次分类，第三次分类的时候，需要根据前两次分类结果，进行分类。"""
    result_file_path = os.path.join(result_save_dir , Path(to_process_file_path).name)
    # 检查如果result_file_path存在，则不进行处理
    if Path(result_file_path).exists():
        logger.info(f'result_file_path {result_file_path} exists, skip')
        __report_status(UPDATE_STATUS_URL, to_process_file_path, 'SUCC')
        return

    file_buffer = BytesIO()
    for samples_of_layout_id in __read_sample_of_layout_id(to_process_file_path):
        label, max_score = __do_page_classify(samples_of_layout_id)
        classify_res = {
            'url_list': [i['url'] for i in samples_of_layout_id],
            'layout_id': samples_of_layout_id[0]['layout_id'],
            'page_type': label,
            'max_pred_prod': max_score,
            'version': MODEL_VERESION,
        }
        logger.info(f"{samples_of_layout_id[0]['layout_id']}, {label}, {max_score}, {samples_of_layout_id[0]['url']}")
        file_buffer.write(json.dumps(classify_res, ensure_ascii=False).encode('utf-8') + b'\n')

    file_buffer.seek(0)
    # 一次性写入到磁盘,降低磁盘IO
    with open(result_file_path, 'wb') as f:
        f.write(file_buffer.getvalue())
    logger.info(f'finished process {to_process_file_path}, write result to {result_file_path}')
    file_buffer.close()


@retry(tries=5, delay=10, max_delay=5)
def __report_status(server_url, file_path, status, msg=''):
    """更新server上的状态."""
    requests.post(server_url, json={'file_path': file_path, 'status': status, 'msg': msg})
    logger.info(f'report status {status} for file {file_path}')


@click.command()
@click.option('--result-save-dir', type=click.Path(exists=True), help='分类结果文件输出路径')
@click.option('--server-addr', type=str, help='server的地址，例如http://127.0.0.1:5000')
def main(result_save_dir: str, server_addr: str):
    global GET_FILE_URL, UPDATE_STATUS_URL, MODEL
    GET_FILE_URL = f'{server_addr}/get_file'
    UPDATE_STATUS_URL = f'{server_addr}/update_status'
    logger.info('init model')
    MODEL = HTMLLayoutClassifier()
    logger.info('init model done')
    while True:
        try:
            # 获取待处理的文件路径
            logger.info(f'get layout classify file from {GET_FILE_URL}')
            to_process_file_path = requests.get(GET_FILE_URL).json()['file_path']
            logger.info(f'get layout classify file: {to_process_file_path}')
            if not to_process_file_path:
                logger.info('no file to process, sleep 10s')
                time.sleep(10)
                continue
            # 处理文件
            __process_one_layout_file(result_save_dir, to_process_file_path)
            # 更新状态
            __report_status(UPDATE_STATUS_URL, to_process_file_path, 'SUCC')
        except Exception as e:
            logger.error(f'get layout classify fail: {e}')
            logger.exception(e)
            time.sleep(1)


if __name__ == '__main__':
    main()
