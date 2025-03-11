"""本模块提供从 S3 或 HTTP 下载文件的功能，支持校验和验证和并发下载锁机制。

主要功能：
1. 计算文件的 MD5 和 SHA256 校验和
2. 通过 S3 或 HTTP 连接下载文件
3. 使用文件锁防止并发下载冲突
4. 自动校验文件完整性

类说明：
- Connection: 抽象基类，定义下载连接接口
- S3Connection: 实现 S3 文件下载连接
- HttpConnection: 实现 HTTP 文件下载连接

函数说明：
- calc_file_md5/sha256: 计算文件哈希值
- verify_file_checksum: 校验文件哈希
- download_auto_file_core: 核心下载逻辑
- download_auto_file: 自动下载入口函数（含锁机制）
"""

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
    """计算文件的 MD5 校验和.

    Args:
        file_path: 文件路径

    Returns:
        MD5 哈希字符串（32位十六进制）
    """
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def calc_file_sha256(file_path: str) -> str:
    """计算文件的 SHA256 校验和.

    Args:
        file_path: 文件路径

    Returns:
        SHA256 哈希字符串（64位十六进制）
    """
    with open(file_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def verify_file_checksum(
    file_path: str, md5_sum: Optional[str] = None, sha256_sum: Optional[str] = None
) -> bool:
    """验证文件的 MD5 或 SHA256 校验和.

    Args:
        file_path: 待验证文件路径
        md5_sum: 预期 MD5 值（与 sha256_sum 二选一）
        sha256_sum: 预期 SHA256 值（与 md5_sum 二选一）

    Returns:
        bool: 校验是否通过

    Raises:
        ModelResourceException: 当未提供或同时提供两个校验和时
    """
    if not (bool(md5_sum) ^ bool(sha256_sum)):
        raise ModelResourceException(
            'Exactly one of md5_sum or sha256_sum must be provided'
        )
    if not os.path.exists(file_path):
        return False
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


class Connection:
    """下载连接的抽象基类."""

    def get_size(self) -> int:
        """获取文件大小（字节）"""
        raise NotImplementedError

    def read_stream(self) -> Iterable[bytes]:
        """返回数据流的迭代器."""
        raise NotImplementedError


class S3Connection(Connection):
    """S3 文件下载连接."""

    def __init__(self, resource_path: str):
        super().__init__()
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
        if hasattr(self, 'obj') and 'Body' in self.obj:
            self.obj['Body'].close()


class HttpConnection(Connection):
    """HTTP 文件下载连接."""

    def __init__(self, resource_path: str):
        super().__init__()
        self.response = requests.get(resource_path, stream=True)
        self.response.raise_for_status()

    def get_size(self) -> int:
        return int(self.response.headers.get('content-length', 0))

    def read_stream(self) -> Iterable[bytes]:
        block_size = 1024
        for chunk in self.response.iter_content(block_size):
            yield chunk

    def __del__(self):
        if hasattr(self, 'response'):
            self.response.close()


def download_to_temp(conn: Connection, progress_bar: tqdm, download_path: str):
    """下载文件到临时目录.

    Args:
        conn: 下载连接
        progress_bar: 进度条
        download_path: 临时文件路径
    """

    with open(download_path, 'wb') as f:
        for chunk in conn.read_stream():
            if chunk:  # 防止空chunk导致进度条卡死
                f.write(chunk)
                progress_bar.update(len(chunk))


def download_auto_file_core(
    resource_path: str,
    target_path: str,
) -> str:
    """下载文件的核心逻辑（无锁）

    Args:
        resource_path: 源文件路径（S3或HTTP URL）
        target_path: 目标保存路径

    Returns:
        下载后的文件路径

    Raises:
        ModelResourceException: 下载失败或文件大小不匹配时
    """
    # 初始化连接
    conn_cls = S3Connection if is_s3_path(resource_path) else HttpConnection
    conn = conn_cls(resource_path)
    total_size = conn.get_size()

    # 配置进度条
    logger.info(f'Downloading {resource_path} => {target_path}')
    progress = tqdm(total=total_size, unit='iB', unit_scale=True)

    # 使用临时目录确保原子性
    os.makedirs(CACHE_TMP_DIR, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=CACHE_TMP_DIR) as temp_dir:
        download_path = os.path.join(temp_dir, 'download_file')
        try:
            download_to_temp(conn, progress, download_path)

            # 验证文件大小
            actual_size = os.path.getsize(download_path)
            if total_size != actual_size:
                raise ModelResourceException(
                    f'Size mismatch: expected {total_size}, got {actual_size}'
                )

            # 移动到目标路径
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            os.rename(download_path, target_path)  # 替换 os.rename
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
    """自动下载文件（含锁机制和校验）

    Args:
        resource_path: 源文件路径
        target_path: 目标保存路径
        md5_sum: 预期 MD5 值（与 sha256_sum 二选一）
        sha256_sum: 预期 SHA256 值（与 md5_sum 二选一）
        lock_suffix: 锁文件后缀
        lock_timeout: 锁超时时间（秒）

    Returns:
        下载后的文件路径

    Raises:
        ModelResourceException: 校验失败或下载错误时
    """
    process_func = partial(download_auto_file_core, resource_path, target_path)
    verify_func = partial(verify_file_checksum, target_path, md5_sum, sha256_sum)
    return process_and_verify_file_with_lock(
        process_func, verify_func, target_path, lock_suffix, lock_timeout
    )
