import hashlib
import os
import tempfile
from functools import partial
from typing import Iterable, Optional

import requests
from tqdm import tqdm

from llm_web_kit.exception.exception import ModelResourceException
from llm_web_kit.libs.logger import mylogger as logger
from llm_web_kit.model.resource_utils.boto3_ext import (get_s3_client,
                                                        is_s3_path,
                                                        split_s3_path)
from llm_web_kit.model.resource_utils.process_with_lock import \
    process_and_verify_file_with_lock
from llm_web_kit.model.resource_utils.utils import CACHE_TMP_DIR


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


def verify_file_checksum(
    file_path: str, md5_sum: Optional[str] = None, sha256_sum: Optional[str] = None
) -> bool:
    """校验文件哈希值."""
    if not sum([bool(md5_sum), bool(sha256_sum)]) == 1:
        raise ModelResourceException(
            'Exactly one of md5_sum or sha256_sum must be provided'
        )

    if md5_sum:
        actual = calc_file_md5(file_path)
        if actual != md5_sum:
            logger.warning(
                f'MD5 mismatch: expect {md5_sum[:8]}..., got {actual[:8]}...'
            )
            return False

    if sha256_sum:
        actual = calc_file_sha256(file_path)
        if actual != sha256_sum:
            logger.warning(
                f'SHA256 mismatch: expect {sha256_sum[:8]}..., got {actual[:8]}...'
            )
            return False

    return True


def download_to_temp(conn, progress_bar, download_path):
    """下载到临时文件."""

    with open(download_path, 'wb') as f:
        for chunk in conn.read_stream():
            if chunk:  # 防止空chunk导致进度条卡死
                f.write(chunk)
                progress_bar.update(len(chunk))


def download_auto_file_core(
    resource_path: str,
    target_path: str,
) -> str:
    # 创建连接
    conn_cls = S3Connection if is_s3_path(resource_path) else HttpConnection
    conn = conn_cls(resource_path)
    total_size = conn.get_size()

    # 下载流程
    logger.info(f'Downloading {resource_path} => {target_path}')
    progress = tqdm(total=total_size, unit='iB', unit_scale=True)

    with tempfile.TemporaryDirectory(dir=CACHE_TMP_DIR) as temp_dir:
        download_path = os.path.join(temp_dir, 'download_file')
        try:
            download_to_temp(conn, progress, download_path)
            if not total_size == os.path.getsize(download_path):
                raise ModelResourceException(
                    f'Downloaded {resource_path} to {download_path}, but size mismatch'
                )

            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            print(f'download_path: {download_path}')
            print(f'target_path: {target_path}')
            os.rename(download_path, target_path)

            return target_path

        finally:
            progress.close()


def download_auto_file(
    resource_path: str,
    target_path: str,
    md5_sum: str = '',
    sha256_sum: str = '',
    lock_suffix: str = '.lock',
    lock_timeout: float = 60,
) -> str:
    """Download a file from the web or S3, verify its checksum, and return the
    target path. Use SoftFileLock to prevent concurrent downloads.

    Args:
        resource_path (str): the source URL or S3 path to download from
        target_path (str): the target path to save the downloaded file
        md5_sum (str, optional): the expected MD5 checksum of the file. Defaults to ''.
        sha256_sum (str, optional): the expected SHA256 checksum of the file. Defaults to ''.
        lock_suffix (str, optional): the suffix of the lock file. Defaults to '.lock'.
        lock_timeout (float, optional): the timeout of the lock file. Defaults to 60.

    Returns:
        str: the target path of the downloaded file
    """
    process_func = partial(download_auto_file_core, resource_path, target_path)
    verify_func = partial(verify_file_checksum, target_path, md5_sum, sha256_sum)
    return process_and_verify_file_with_lock(
        process_func, verify_func, target_path, lock_suffix, lock_timeout
    )
