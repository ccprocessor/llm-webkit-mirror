import hashlib
import os
import shutil
import tempfile
from typing import Iterable

import requests
from tqdm import tqdm

from llm_web_kit.config.cfg_reader import load_config
from llm_web_kit.libs.logger import mylogger as logger
from llm_web_kit.model.resource_utils.boto3_ext import (get_s3_client,
                                                        is_s3_path,
                                                        split_s3_path)


def decide_cache_dir():
    """Get the cache directory for the web kit. The.

    Returns:
        _type_: _description_
    """
    cache_dir = '~/.llm_web_kit_cache'

    if 'WEB_KIT_CACHE_DIR' in os.environ:
        cache_dir = os.environ['WEB_KIT_CACHE_DIR']

    try:
        config = load_config()
        cache_dir = config['resources']['common']['cache_path']
    except Exception:
        pass

    if cache_dir.startswith('~/'):
        cache_dir = os.path.expanduser(cache_dir)

    return cache_dir


CACHE_DIR = decide_cache_dir()


def calc_file_md5(file_path: str) -> str:
    """Calculate the MD5 checksum of a file."""
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def calc_file_sha256(file_path: str) -> str:
    """Calculate the sha256 checksum of a file."""
    with open(file_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


class Connection:

    def __init__(self, *args, **kwargs):
        pass

    def get_size(self) -> int:
        raise NotImplementedError

    def read_stream(self) -> Iterable[bytes]:
        raise NotImplementedError


class S3Connection(Connection):

    def __init__(self, resource_path: str):
        super().__init__(resource_path)
        self.client = get_s3_client(resource_path)
        self.bucket, self.key = split_s3_path(resource_path)
        self.obj = self.client.get_object(Bucket=self.bucket, Key=self.key)

    def get_size(self) -> int:
        return self.obj['ContentLength']

    def read_stream(self) -> Iterable[bytes]:
        block_size = 1024
        for chunk in iter(lambda: self.obj['Body'].read(block_size), b''):
            yield chunk

    def __del__(self):
        self.obj['Body'].close()


class HttpConnection(Connection):

    def __init__(self, resource_path: str):
        super().__init__(resource_path)
        self.response = requests.get(resource_path, stream=True)
        self.response.raise_for_status()

    def get_size(self) -> int:
        return int(self.response.headers.get('content-length', 0))

    def read_stream(self) -> Iterable[bytes]:
        block_size = 1024
        for chunk in self.response.iter_content(block_size):
            yield chunk

    def __del__(self):
        self.response.close()


def download_auto_file(resource_path: str, target_path: str, md5_sum: str = '', sha256_sum: str = '',exist_ok=True) -> str:
    """Download a file from a given resource path (either an S3 path or an HTTP
    URL) to a target path on the local file system.

    This function will first download the file to a temporary file, then move the temporary file to the target path after
    the download is complete. A progress bar will be displayed during the download.

    If the size of the downloaded file does not match the expected size, an exception will be raised.

    Args:
        resource_path (str): The path of the resource to download. This can be either an S3 path (e.g., "s3://bucket/key")
            or an HTTP URL (e.g., "http://example.com/file").
        target_path (str): The path on the local file system where the downloaded file should be saved.\
        exist_ok (bool, optional): If False, raise an exception if the target path already exists. Defaults to True.

    Returns:
        str: The path where the downloaded file was saved.

    Raises:
        Exception: If an error occurs during the download, or if the size of the downloaded file does not match the
            expected size, or if the temporary file cannot be moved to the target path.
    """
    if os.path.exists(target_path):
        # if the file already exists, check if it has the correct md5 sum
        if md5_sum:
            file_md5 = calc_file_md5(target_path)
            if file_md5 == md5_sum:
                logger.info(f'File {target_path} already exists and has the correct md5 sum')
                return target_path
            else:
                logger.info(f'File {target_path} already exists but has incorrect md5 sum.')
        # if the file already exists, and not passed md5_sum
        if sha256_sum:
            file_sha256 = calc_file_sha256(target_path)
            if file_sha256 == sha256_sum:
                logger.info(f'File {target_path} already exists and has the correct sha256 sum')
                return target_path
            else:
                logger.info(f'File {target_path} already exists but has incorrect sha256 sum.')
        if not exist_ok:
            # if not exist_ok, raise exception
            raise Exception(f'File {target_path} already exists and exist_ok is False')
        else:
            os.remove(target_path)

    if is_s3_path(resource_path):
        conn = S3Connection(resource_path)
    else:
        conn = HttpConnection(resource_path)

    total_size_in_bytes = conn.get_size()

    logger.info(f'Downloading {resource_path} to {target_path}, but first to a temporary file')
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with tempfile.NamedTemporaryFile() as tmp_file:
        tmp_file_path = tmp_file.name
        logger.info(f'Donwloading {resource_path} to {tmp_file_path}')
        try:

            with open(tmp_file_path, 'wb') as f:
                for chunk in conn.read_stream():
                    progress_bar.update(len(chunk))
                    f.write(chunk)

            local_asset_size = os.path.getsize(tmp_file_path)
            if local_asset_size != total_size_in_bytes:
                raise Exception(f'Downloaded asset size {local_asset_size} does not match expected size {total_size_in_bytes}')

            logger.info(f'Download complete. Copying {tmp_file_path} to {target_path}')
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            shutil.copy(tmp_file_path, target_path)

            if not os.path.exists(target_path):
                raise Exception(f'Failed to move {tmp_file_path} to {target_path}')
        except Exception as e:
            logger.error(f'Error downloading {resource_path}: {e}')
            raise e
        finally:
            progress_bar.close()

    return target_path
