import errno
import hashlib
import os
import shutil
import tempfile
import time
from typing import Iterable, Optional

import requests
from tqdm import tqdm

from llm_web_kit.config.cfg_reader import load_config
from llm_web_kit.exception.exception import ModelInputException
from llm_web_kit.libs.logger import mylogger as logger
from llm_web_kit.model.resource_utils.boto3_ext import (get_s3_client,
                                                        is_s3_path,
                                                        split_s3_path)


def try_remove(path: str):
    """Attempt to remove a file, but ignore any exceptions that occur."""
    try:
        os.remove(path)
    except Exception:
        pass


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


class FileLock:
    """基于文件锁的上下文管理器（跨平台兼容版）"""

    def __init__(self, lock_path: str, timeout: float = 300):
        self.lock_path = lock_path
        self.timeout = timeout
        self._fd = None

    def __enter__(self):
        start_time = time.time()
        while True:
            try:
                # 原子性创建锁文件（O_EXCL标志是关键）
                self._fd = os.open(
                    self.lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644
                )
                # 写入进程信息和时间戳
                with os.fdopen(self._fd, 'w') as f:
                    f.write(f'{os.getpid()}\n{time.time()}')
                return self
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

                # 检查锁是否过期
                try:
                    with open(self.lock_path, 'r') as f:
                        pid, timestamp = f.read().split('\n')[:2]
                        if time.time() - float(timestamp) > self.timeout:
                            os.remove(self.lock_path)
                except (FileNotFoundError, ValueError):
                    pass

                if time.time() - start_time > self.timeout:
                    raise TimeoutError(f'Could not acquire lock after {self.timeout}s')
                time.sleep(0.1)

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self._fd:
                os.close(self._fd)
        except OSError:
            pass
        finally:
            try_remove(self.lock_path)


def verify_file_checksum(
    file_path: str, md5_sum: Optional[str] = None, sha256_sum: Optional[str] = None
) -> bool:
    """校验文件哈希值."""
    if not sum([bool(md5_sum), bool(sha256_sum)]) == 1:
        raise ModelInputException(
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


def download_to_temp(conn, progress_bar) -> str:
    """下载到临时文件."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_path = tmp_file.name
        logger.info(f'Downloading to temporary file: {tmp_path}')

        try:
            with open(tmp_path, 'wb') as f:
                for chunk in conn.read_stream():
                    if chunk:  # 防止空chunk导致进度条卡死
                        f.write(chunk)
                        progress_bar.update(len(chunk))
            return tmp_path
        except Exception:
            try_remove(tmp_path)
            raise


def move_to_target(tmp_path: str, target_path: str, expected_size: int):
    """移动文件并验证."""
    if os.path.getsize(tmp_path) != expected_size:
        raise ValueError(
            f'File size mismatch: {os.path.getsize(tmp_path)} vs {expected_size}'
        )

    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    shutil.move(tmp_path, target_path)  # 原子操作替换

    if not os.path.exists(target_path):
        raise RuntimeError(f'Move failed: {tmp_path} -> {target_path}')


def download_auto_file(
    resource_path: str,
    target_path: str,
    md5_sum: str = '',
    sha256_sum: str = '',
    exist_ok=True,
    lock_timeout: int = 300,
) -> str:
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

    """线程安全的文件下载函数"""
    lock_path = f'{target_path}.lock'

    with FileLock(lock_path, timeout=lock_timeout):
        # 二次检查（其他进程可能已经完成下载）
        if os.path.exists(target_path):
            if verify_file_checksum(target_path, md5_sum, sha256_sum):
                logger.info(f'File already exists with valid checksum: {target_path}')
                return target_path

            if not exist_ok:
                raise FileExistsError(
                    f'File exists with invalid checksum: {target_path}'
                )
            logger.warning(f'Removing invalid file: {target_path}')
            try_remove(target_path)

        # 创建连接
        conn_cls = S3Connection if is_s3_path(resource_path) else HttpConnection
        conn = conn_cls(resource_path)
        total_size = conn.get_size()

        # 下载流程
        logger.info(f'Downloading {resource_path} => {target_path}')
        progress = tqdm(total=total_size, unit='iB', unit_scale=True)

        try:
            tmp_path = download_to_temp(conn, progress)
            move_to_target(tmp_path, target_path, total_size)

            return target_path
        finally:
            progress.close()
            try_remove(tmp_path)  # 确保清理临时文件
