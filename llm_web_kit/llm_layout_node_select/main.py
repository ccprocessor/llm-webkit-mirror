
"""单线程守护进程，需要从slurm上提交获得多进程处理能力。
进程启动之后进入一个无限循环，从server上获取待处理的文件，处理完成之后，更新server上的待处理文件的状态。
如果连续1个小时没有获取到待处理的文件，则退出进程。

程序首先从配置文件里读取结果要写入的目录和模型的server地址。对于多个server地址，程序每次随机选择一个进行请求。
"""
import os
import random
import re
import socket
import time
from io import BytesIO
from pathlib import Path
from typing import Dict, Tuple

import click
import commentjson as json
import requests
from func_timeout import FunctionTimedOut, func_timeout
from loguru import logger
from openai import APIConnectionError, BadRequestError, OpenAI
from retry import retry
from transformers import AutoTokenizer

logger.add('logs/llm_layout_node_select.log', rotation='120 minutes', retention='1 days', level='ERROR', format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}')

GET_FILE_URL = None
UPDATE_STATUS_URL = None
TOKENIZER = None


def __get_runtime_id():
    # 获取 hostname
    hostname = socket.gethostname()
    job_id = os.environ.get('SLURM_JOB_ID', 'unknown')
    return f'{hostname}_{job_id}'


@retry(tries=5, delay=10, max_delay=5)
def __report_status(server_url, file_path, status, msg=''):
    """更新server上的状态."""
    requests.post(server_url, json={'file_path': file_path, 'status': status, 'msg': msg}, timeout=20)
    logger.info(f'report status {status} for file {file_path}')


def __build_prompt_with_html(simplified_html: str) -> Tuple[str, str]:
    system_prompt = """
你是一位网页正文抽取专家，你能阅读HTML的每个带有item_id的节点，联系前后节点内容，判断每个节点里的文字是否围绕着某个正文主题，并进一步判断该节点是否是该页面的主要内容还是其他内容。
具有以下特征的元素通常是主要内容：
- 对于新闻，博客，文章，信息发布类网页，正文，正文中的配图，正文中需要被发布的信息属于主要内容，
- 对于论坛，论坛的每一层，以及每一层的回复属于主要内容，
- 对于问答类网站，问题和回答，以及针对问题的回复与每一个回答的回复等元素通常是主要内容。
- 对于列表页，列表的每一项及其描述为主要内容。
- 对于商品页，商品图片、描述、价格、库存等属于主要内容。
具有以下特征的元素通常是补充信息：
- 导航栏、侧边栏、页脚，相关文章，导航链接列表等元素通常属于其它信息。
- 文章标题、正文的编者信息，评论内容的用户信息，点赞数，发布时间等元素通常是补充信息。注意，评论内容本身属于主要内容。

请针对每一个具有"_item_id"属性的元素，判断该元素的功能，并给出该元素是否是该页面的主要内容，补充信息，其他内容。
如果是主要内容，你可以将元素记为1，如果是其他内容，你可以将元素记为0。

以下会提供一个经过简化的网页HTML代码，你需要判断出具有"_item_id"属性所在位置的元素的功能，并给出该元素是否是该页面的主要内容或是其他内容。
不要返回除json字符串外的任何其他内容，回答的格式例如：
{
    "item_id 1": 0,
    "item_id 2": 1,
    "item_id 3": 0
}"""
    user_prompt = f"""以下是HTML代码：
    ```html
    {simplified_html}
    ```
    注意不要输出解释性内容，json里也不要有注释"""
    return system_prompt, user_prompt


def __chat_with_model(api_key: str, api_url: str, system_prompt: str, user_prompt: str, model_name: str) -> str:
    client = OpenAI(
        api_key=api_key,
        base_url=api_url,
    )
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt},
        ],
    )

    response_str = completion.model_dump_json()
    return response_str


def __check_model_response(response_str: str, xpath_cnt: int) -> Dict[str, str]:
    try:
        response_json = json.loads(response_str)
        response_content = response_json['choices'][0]['message']['content']
    except Exception:
        return None, 'raw_model_response_dejson_fail'

    try:
        json_str = re.search(r'\{.*\}', response_content, re.DOTALL).group()
        response = json.loads(json_str)
    except Exception:
        logger.error(f'raw_model_content_response_dejson_fail: {response_content}')
        return None, 'raw_model_content_response_dejson_fail'

    if len(response) != xpath_cnt:
        return None, 'raw_model_response_length_not_equal_xpath_cnt'

    return response, None


def __call_model_server(model_server_url, model_server_sk, model_name, simplified_html: str, xpath_cnt: int) -> tuple[str, bool]:
    """调用模型server，返回处理结果。

    Return:
        rtn: 处理结果
        succ: 是否成功, 如果失败，返回模型返回的全部信息。如果成功则只保留节点选择信息。
    """
    sys_prompt, user_prompt = __build_prompt_with_html(simplified_html)
    response_str = None
    try:
        response_str = __chat_with_model(model_server_sk, model_server_url, sys_prompt, user_prompt, model_name)
        rtn, err_msg = __check_model_response(response_str, xpath_cnt)
        if err_msg is None:
            return rtn, True  # 返回模型打标的Json结果
        else:
            return err_msg, False
    except APIConnectionError as e1:
        logger.error(f'connect model server {model_server_url} fail: {e1}')
        return err_msg, False
    except BadRequestError as e2:
        logger.error(f'bad request to model server {model_server_url}: {e2}')
        return 'token_length_exceed', False
    except Exception as e:
        logger.exception(e)
        return err_msg, False


def __process_one_input_file(result_save_dir, to_process_file_path, model_servers):
    """处理一个输入文件，返回处理结果。"""
    model_server = random.choice(model_servers)
    model_server_url = model_server['base_url']
    model_server_sk = model_server['sk']
    model_name = model_server['model_name']
    has_call_model_succ = False  # 记录是否有1个成功的调用，如果都失败，就保存这个文件
    all_err_reason = []

    result_file_path = os.path.join(result_save_dir , Path(to_process_file_path).name)
    # 检查如果result_file_path存在，则不进行处理
    if Path(result_file_path).exists():
        logger.info(f'result_file_path {result_file_path} exists, skip')
        __report_status(UPDATE_STATUS_URL, to_process_file_path, 'SUCC')
        return True

    file_buffer = BytesIO()
    with open(to_process_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line and line.strip():
                try:
                    obj = json.loads(line.strip())
                except Exception as e:
                    logger.error(f'load json fail: {line}, {str(e)}')
                    continue

                try:
                    simplified_html = obj['simplified_html']
                    track_id = obj['track_id']
                    logger.warning(f'process {to_process_file_path}, track_id: {track_id}, simplified_html length: {len(simplified_html)}')
                    xpath_cnt = len(obj['xpath_mapping'])
                    chat_with_model_timeout = 60 * 5
                    rtn, succ = func_timeout(chat_with_model_timeout, __call_model_server, args=(model_server_url, model_server_sk, model_name, simplified_html, xpath_cnt))
                except FunctionTimedOut:
                    logger.error(f'call model server {model_server_url} timeout:{chat_with_model_timeout}s, skip')
                    succ = False
                    rtn = 'timeout_of_call_model_server'
                    all_err_reason.append(rtn)
                except Exception as e:
                    logger.exception(e)
                    succ = False
                    rtn = 'unkonwn_error_of_call_model_server'
                    all_err_reason.append(rtn)

                if succ:
                    has_call_model_succ = True
                    obj['model_name'] = model_name
                    obj['llm_node_select'] = rtn  # a dict
                    to_save_str = json.dumps(obj, ensure_ascii=False)
                    file_buffer.write(to_save_str.encode('utf-8') + b'\n')
                    # logger.success(f'process {to_process_file_path} succ, model_name: {model_name}, llm_node_select: {rtn}')
                else:
                    obj['model_name'] = model_name
                    obj['__error'] = rtn
                    to_save_str = json.dumps(obj, ensure_ascii=False)
                    file_buffer.write(to_save_str.encode('utf-8') + b'\n')
                    all_err_reason.append(rtn)
                    logger.error(f'process {to_process_file_path} fail, err_reason: {rtn}')

    if not has_call_model_succ:
        logger.error(f'all model call fail, **NOT** save {to_process_file_path}, err_reason: {all_err_reason}')

        return False

    file_buffer.seek(0)
    # 一次性写入到磁盘,降低磁盘IO
    logger.success(f'write result to {result_file_path}')
    with open(result_file_path, 'wb') as f:
        f.write(file_buffer.getvalue())
    logger.info(f'finished process {to_process_file_path}, write result to {result_file_path}')
    file_buffer.close()
    return True


@click.command()
@click.option('--config', type=click.Path(exists=True), help='配置文件路径')
def main(config: str):
    with open(config, 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    global GET_FILE_URL, UPDATE_STATUS_URL, TOKENIZER
    GET_FILE_URL = f'{cfg["task_server_addr"]}/get_file'
    UPDATE_STATUS_URL = f'{cfg["task_server_addr"]}/update_status'
    result_save_dir = cfg['result_save_dir']
    model_servers = cfg['model_servers']
    tokenizer_path = cfg['qwen2.5-72b-tokenizer-path']
    # 检查这个路径是否存在，如果不存在则不使用tokenizer检查长度
    if not os.path.exists(tokenizer_path):
        TOKENIZER = None
    else:
        TOKENIZER = AutoTokenizer.from_pretrained(tokenizer_path)

    while True:
        try:
            # 获取待处理的文件路径
            logger.info(f'get layout classify file from {GET_FILE_URL}')
            to_process_file_path = requests.get(GET_FILE_URL, timeout=20).json()['file_path']
            logger.info(f'get layout classify file: {to_process_file_path}')
            if not to_process_file_path:
                logger.info('no file to process, sleep 10s')
                continue
            # 处理文件
            succ = __process_one_input_file(result_save_dir, to_process_file_path, model_servers)
            if not succ:
                logger.error(f'process {to_process_file_path} fail, sleep 10s')
                __report_status(UPDATE_STATUS_URL, to_process_file_path, 'FAIL')
                continue
            # 更新状态
            __report_status(UPDATE_STATUS_URL, to_process_file_path, 'SUCC')
        except Exception as e:
            logger.error(f'get layout classify fail: {e}')
            __report_status(UPDATE_STATUS_URL, to_process_file_path, 'FAIL')
            logger.exception(e)
            time.sleep(10)


if __name__ == '__main__':
    main()
