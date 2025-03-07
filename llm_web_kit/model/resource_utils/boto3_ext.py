import re
from typing import Dict, List, Tuple, Union

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from llm_web_kit.config.cfg_reader import load_config
from llm_web_kit.exception.exception import ModelResourceException

__re_s3_path = re.compile('^s3://([^/]+)(?:/(.*))?$')


def is_s3_path(path: str) -> bool:
    """check a path is s3 path or not.

    Args:
        path (str): path

    Returns:
        bool: is s3 path or not
    """
    return path.startswith('s3://')


def is_s3_404_error(e: Exception) -> bool:
    """check if an exception is 404 error.

    Args:
        e (Exception): exception

    Returns:
        bool: is 404 error or not
    """
    if not isinstance(e, ClientError):
        return False
    flag_1 = e.response.get('Error', {}).get('Code') in ['404', 'NoSuchKey']
    flag_2 = e.response.get('Error', {}).get('Message') == 'Not Found'
    flag_3 = e.response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 404
    return any([flag_1, flag_2, flag_3])


def split_s3_path(path: str) -> Tuple[str, str]:
    """split bucket and key from path.

    Args:
        path (str): s3 path

    Returns:
        Tuple[str, str]: bucket and key

    Raises:
        ModelResourceException: if path is not s3 path
    """
    if not is_s3_path(path):
        raise ModelResourceException(f'{path} is not a s3 path')
    m = __re_s3_path.match(path)
    if m is None:
        return '', ''
    return m.group(1), (m.group(2) or '')


def get_s3_config(path: str) -> Dict:
    """Get s3 config for a given path by its bucket name from the config file.

    Args:
        path (str): s3 path

    Raises:
        ModelResourceException: if bucket not in config
        ModelResourceException: if path is not s3 path

    Returns:
        dict: s3 config
    """
    bucket, _ = split_s3_path(path)
    config_dict = load_config()
    if bucket in config_dict['s3']:
        return config_dict['s3'][bucket]
    else:
        raise ModelResourceException(f'bucket {bucket} not in config')


def get_s3_client(path: Union[str, List[str]]) -> boto3.client:
    """Get s3 client for a given path.

    Args:
        path (Union[str, List[str]]): s3 path

    Returns:
        boto3.client: s3 client

    Raises:
        ModelResourceException: if bucket not in config
        ModelResourceException: if path is not s3 path
    """

    s3_config = get_s3_config(path)
    try:
        return boto3.client(
            's3',
            aws_access_key_id=s3_config['ak'],
            aws_secret_access_key=s3_config['sk'],
            endpoint_url=s3_config['endpoint'],
            config=Config(
                s3={'addressing_style': s3_config.get('addressing_style', 'path')},
                retries={'max_attempts': 8, 'mode': 'standard'},
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
    """Get s3 object metadata.

    Args:
        client (boto3.client): the s3 client
        path (str): the s3 path
        raise_404 (bool, optional):  raise 404 error or not. Defaults to False.

    Returns:
        Union[Dict, None]: s3 object metadata or None if not found

    Raises:
        ClientError: if raise_404 is True and object not
        ModelResourceException: if path is not s3 path
        ModelResourceException: if bucket not in config
    """
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
