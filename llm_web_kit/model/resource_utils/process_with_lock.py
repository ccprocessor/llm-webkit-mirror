import os
import time
from typing import Callable

from filelock import SoftFileLock, Timeout

from llm_web_kit.model.resource_utils.utils import try_remove


def get_path_mtime(target_path: str) -> float:
    """获得文件或目录的最新修改时间. 如果是文件，则直接返回 mtime. 如果是目录，则遍历目录获取最新的 mtime.

    Args:
        target_path: 文件或目录路径

    Returns:
        float: 最新修改时间
    """
    if os.path.isdir(target_path):
        # walk through the directory and get the latest mtime
        latest_mtime = None
        for root, _, files in os.walk(target_path):
            for file in files:
                file_path = os.path.join(root, file)
                mtime = os.path.getmtime(file_path)
                if latest_mtime is None or mtime > latest_mtime:
                    latest_mtime = mtime
        return latest_mtime
    else:
        return os.path.getmtime(target_path)


def process_and_verify_file_with_lock(
    process_func: Callable[[], str],  # 无参数，返回目标路径
    verify_func: Callable[[], bool],  # 无参数，返回验证结果
    target_path: str,
    lock_suffix: str = '.lock',
    timeout: float = 60,
) -> str:
    # """通用处理验证框架.

    # :param process_func: 无参数的处理函数，返回最终目标路径
    # :param verify_func: 无参数的验证函数，返回布尔值
    # :param target_path: 目标路径（文件或目录）
    # :param lock_suffix: 锁文件后缀
    # :param timeout: 处理超时时间（秒）
    # """
    """
    通用使用文件锁进行资源处理与资源验证的框架.
    使用文件锁保证处理函数调用时是唯一的。
    资源校验不在锁保护范围内从而提高效率。
    当资源校验不通过时，会删除目标文件并重新处理。
    简易逻辑为：
    1. 检查目标是否存在且有效，如果是则直接返回目标路径
    2. 如果目标不存在或无效，则尝试获取锁
    3. 如果锁存在且陈旧，则删除锁和目标文件重新处理
    4. 如果锁存在且未陈旧，则等待锁释放
    5. 如果锁不存在，则执行处理函数
    6. 处理完成后返回目标路径

    Args:
        process_func: 无参数的处理函数，返回最终目标路径
        verify_func: 无参数的验证函数，返回布尔值
        target_path: 目标路径（文件或目录）
        lock_suffix: 锁文件后缀
        timeout: 处理超时时间（秒）
    Returns:
        str: 最终目标路径
    """
    lock_path = target_path + lock_suffix

    while True:
        # 检查目标是否存在且有效
        if os.path.exists(target_path):
            if verify_func():
                return target_path
            else:
                # 目标存在但验证失败
                if os.path.exists(lock_path):
                    now = time.time()
                    try:
                        mtime = get_path_mtime(target_path)
                        if now - mtime < timeout:
                            time.sleep(1)
                            continue
                        else:
                            try_remove(lock_path)
                            try_remove(target_path)
                    except FileNotFoundError:
                        pass
                else:
                    try_remove(target_path)
        else:

            # 尝试获取锁
            file_lock = SoftFileLock(lock_path)
            try:
                file_lock.acquire(timeout=1)
                # 二次验证（可能其他进程已处理完成）
                if os.path.exists(target_path) and verify_func():
                    return target_path
                # 执行处理
                return process_func()
            except Timeout:
                time.sleep(1)
                continue
            finally:
                if file_lock.is_locked:
                    file_lock.release()
