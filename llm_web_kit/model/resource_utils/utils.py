import errno
import os
import time


def try_remove(path: str):
    """Attempt to remove a file, but ignore any exceptions that occur."""
    try:
        os.remove(path)
    except Exception:
        pass


class FileLockContext:
    """基于文件锁的上下文管理器（跨平台兼容版）"""

    def __init__(self, lock_path: str, check_callback=None, timeout: float = 300):
        self.lock_path = lock_path
        self.check_callback = check_callback
        self.timeout = timeout
        self._fd = None

    def __enter__(self):
        start_time = time.time()
        while True:
            if self.check_callback:
                if self.check_callback():
                    return True
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
