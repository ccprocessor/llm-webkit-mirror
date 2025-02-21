import re
from typing import Dict, List, Union

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from llm_web_kit.config.cfg_reader import load_config

__re_s3_path = re.compile('^s3://([^/]+)(?:/(.*))?$')


def is_s3_path(path: str) -> bool:
    return path.startswith('s3://')


def is_s3_404_error(e: Exception):
    if not isinstance(e, ClientError):
        return False
    flag_1 = e.response.get('Error', {}).get('Code') in ['404', 'NoSuchKey']
    flag_2 = e.response.get('Error', {}).get('Message') == 'Not Found'
    flag_3 = e.response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 404
    return any([flag_1, flag_2, flag_3])


def split_s3_path(path: str):
    """split bucket and key from path."""
    m = __re_s3_path.match(path)
    if m is None:
        return '', ''
    return m.group(1), (m.group(2) or '')


def get_s3_config(path: str):
    """Get s3 config for a given path by its bucket name from the config file.

    Args:
        path (str): s3 path

    Raises:
        ValueError: if bucket not found in config

    Returns:
        dict: s3 config
    """
    bucket, _ = split_s3_path(path)
    config_dict = load_config()
    if bucket in config_dict['s3']:
        return config_dict['s3'][bucket]
    else:
        raise ValueError(f'bucket {bucket} not in config')


def get_s3_client(path: Union[str, List[str]]):
    s3_config = get_s3_config(path)
    try:
        return boto3.client(
            's3',
            aws_access_key_id=s3_config['ak'],
            aws_secret_access_key=s3_config['sk'],
            endpoint_url=s3_config['endpoint'],
            config=Config(
                s3={'addressing_style': s3_config.get('addressing_style', 'path')},
                retries={
                    'max_attempts': 8,
                    'mode': 'standard'
                },
                connect_timeout=600,
                read_timeout=600,
            ),
        )
    except Exception:
        # older boto3 do not support retries.mode param.
        return boto3.client(
            's3',
            aws_access_key_id=s3_config['ak'],
            aws_secret_access_key=s3_config['sk'],
            endpoint_url=s3_config['endpoint'],
            config=Config(
                s3={'addressing_style': s3_config.get('addressing_style', 'path')},
                retries={'max_attempts': 8},
            ),
        )


def head_s3_object(client, path: str, raise_404=False) -> Union[Dict, None]:
    bucket, key = split_s3_path(path)
    try:
        resp = client.head_object(Bucket=bucket, Key=key)
        return resp
    except ClientError as e:
        if not raise_404 and is_s3_404_error(e):
            return None
        raise


if __name__ == '__main__':
    print(get_s3_config('s3://web-parse-huawei'))
    print(get_s3_config('s3://llm-users-phdd2'))
    print(get_s3_client('s3://web-parse-huawei'))
    print(get_s3_client('s3://llm-users-phdd2'))
