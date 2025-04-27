
"""单线程守护进程，需要从slurm上提交获得多进程处理能力。
进程启动之后进入一个无限循环，从server上获取待处理的文件，处理完成之后，更新server上的待处理文件的状态。
如果连续1个小时没有获取到待处理的文件，则退出进程。

程序首先从配置文件里读取结果要写入的目录和模型的server地址。对于多个server地址，程序每次随机选择一个进行请求。
"""
import json
import os
import random
import socket
import time
from io import BytesIO
from pathlib import Path

import click
import requests
from loguru import logger
from retry import retry

MODEL_VERESION = 'qwen2.5-72b-instruct'
GET_FILE_URL = None
UPDATE_STATUS_URL = None


def __get_runtime_id():
    # 获取 hostname
    hostname = socket.gethostname()
    job_id = os.environ.get('SLURM_JOB_ID', 'unknown')
    return f'{hostname}_{job_id}'


@retry(tries=5, delay=10, max_delay=5)
def __report_status(server_url, file_path, status, msg=''):
    """更新server上的状态."""
    requests.post(server_url, json={'file_path': file_path, 'status': status, 'msg': msg})
    logger.info(f'report status {status} for file {file_path}')


def __call_model_server(model_server_url, model_server_sk, model_name, simplified_html: str) -> tuple[str, bool]:
    """调用模型server，返回处理结果。

    Return:
        rtn: 处理结果
        succ: 是否成功, 如果失败，返回模型返回的全部信息。如果成功则只保留节点选择信息。
    """
    pass


def __process_one_input_file(result_save_dir, to_process_file_path, model_servers):
    """处理一个输入文件，返回处理结果。"""
    model_server = random.choice(model_servers)
    model_server_url = model_server['base_url']
    model_server_sk = model_server['sk']
    model_name = model_server['model_name']

    result_file_path = os.path.join(result_save_dir , Path(to_process_file_path).name)
    # 检查如果result_file_path存在，则不进行处理
    if Path(result_file_path).exists():
        logger.info(f'result_file_path {result_file_path} exists, skip')
        __report_status(UPDATE_STATUS_URL, to_process_file_path, 'SUCC')
        return

    file_buffer = BytesIO()
    with open(to_process_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line and line.strip():
                obj = json.loads(line.strip())
                simplified_html = obj['simplified_html']
                rtn, succ = __call_model_server(model_server_url, model_server_sk, model_name, simplified_html)
                if succ:
                    obj['model_name'] = model_name
                    obj['llm_node_select'] = rtn
                    to_save_str = json.dumps(obj, ensure_ascii=False)
                    file_buffer.write(to_save_str.encode('utf-8') + b'\n')
                else:
                    obj['model_name'] = model_name
                    obj['__error'] = rtn
                    to_save_str = json.dumps(obj, ensure_ascii=False)
                    file_buffer.write(to_save_str.encode('utf-8') + b'\n')

    file_buffer.seek(0)
    # 一次性写入到磁盘,降低磁盘IO
    with open(result_file_path, 'wb') as f:
        f.write(file_buffer.getvalue())
    logger.info(f'finished process {to_process_file_path}, write result to {result_file_path}')
    file_buffer.close()


@click.command()
@click.option('--config', type=click.Path(exists=True), help='配置文件路径')
def main(config: str):
    with open(config, 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    global GET_FILE_URL, UPDATE_STATUS_URL
    GET_FILE_URL = f'{cfg["task_server_addr"]}/get_file'
    UPDATE_STATUS_URL = f'{cfg["task_server_addr"]}/update_status'
    result_save_dir = cfg['result_save_dir']
    model_servers = cfg['model_servers']

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
            __process_one_input_file(result_save_dir, to_process_file_path, model_servers)
            # 更新状态
            __report_status(UPDATE_STATUS_URL, to_process_file_path, 'SUCC')
        except Exception as e:
            logger.error(f'get layout classify fail: {e}')
            logger.exception(e)
            time.sleep(1)


if __name__ == '__main__':
    main()
