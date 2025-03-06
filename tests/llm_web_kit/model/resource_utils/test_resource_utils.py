import errno
import os
import unittest
from unittest.mock import MagicMock, mock_open, patch

from llm_web_kit.model.resource_utils.utils import FileLockContext, try_remove


class Test_try_remove:

    @patch('os.remove')
    def test_remove(self, removeMock):
        try_remove('path')
        removeMock.assert_called_once_with('path')

    @patch('os.remove')
    def test_remove_exception(self, removeMock):
        removeMock.side_effect = Exception
        try_remove('path')
        removeMock.assert_called_once_with('path')


class TestFileLock(unittest.TestCase):

    def setUp(self):
        self.lock_path = 'test.lock'

    @patch('os.fdopen')
    @patch('os.open')
    @patch('os.close')
    @patch('os.remove')
    def test_acquire_and_release_lock(
        self, mock_remove, mock_close, mock_open, mock_os_fdopen
    ):
        # 模拟成功获取锁
        mock_open.return_value = 123  # 假设文件描述符为123
        # 模拟文件描述符
        mock_fd = MagicMock()
        mock_fd.__enter__.return_value = mock_fd
        mock_fd.write.return_value = None
        mock_os_fdopen.return_value = mock_fd

        with FileLockContext(self.lock_path):
            mock_open.assert_called_once_with(
                self.lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644
            )
        mock_close.assert_called_once_with(123)
        mock_remove.assert_called_once_with(self.lock_path)

    @patch('os.fdopen')
    @patch('os.open')
    @patch('builtins.open', new_callable=mock_open, read_data='1234\n100')
    @patch('time.time')
    @patch('os.remove')
    def test_remove_stale_lock(
        self, mock_remove, mock_time, mock_file_open, mock_os_open, mock_os_fdopen
    ):
        # 第一次尝试创建锁文件失败（锁已存在）
        mock_os_open.side_effect = [
            OSError(errno.EEXIST, 'File exists'),
            123,  # 第二次成功
        ]

        # 模拟文件描述符
        mock_fd = MagicMock()
        mock_fd.__enter__.return_value = mock_fd
        mock_fd.write.return_value = None
        mock_os_fdopen.return_value = mock_fd

        # 当前时间设置为超过超时时间（timeout=300）
        mock_time.return_value = 401  # 100 + 300 + 1

        with FileLockContext(self.lock_path, timeout=300):
            mock_remove.assert_called_once_with(self.lock_path)
            mock_os_open.assert_any_call(
                self.lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644
            )

    @patch('os.open')
    @patch('time.time')
    def test_timeout_acquiring_lock(self, mock_time, mock_os_open):
        # 总是返回EEXIST错误
        mock_os_open.side_effect = OSError(errno.EEXIST, 'File exists')
        # 时间累计超过超时时间
        start_time = 1000
        mock_time.side_effect = [
            start_time,
            start_time + 301,
            start_time + 302,
            start_time + 303,
        ]

        with self.assertRaises(TimeoutError):
            with FileLockContext(self.lock_path, timeout=300):
                pass

    @patch('os.open')
    def test_other_os_error(self, mock_os_open):
        # 模拟其他OS错误（如权限不足）
        mock_os_open.side_effect = OSError(errno.EACCES, 'Permission denied')
        with self.assertRaises(OSError):
            with FileLockContext(self.lock_path):
                pass

    @patch('os.close')
    @patch('os.remove')
    def test_cleanup_on_exit(self, mock_remove, mock_close):

        mock_close.side_effect = None
        # 确保退出上下文时执行清理
        lock_path = 'test.lock'
        lock = FileLockContext(lock_path)
        lock._fd = 123  # 模拟已打开的文件描述符
        lock.__exit__('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', None, None)
        mock_remove.assert_called_once_with(self.lock_path)

    @patch('os.remove')
    def test_cleanup_failure_handled(self, mock_remove):
        # 模拟删除锁文件时失败
        mock_remove.side_effect = OSError
        lock = FileLockContext(self.lock_path)
        lock._fd = 123
        # 不应抛出异常
        lock.__exit__(None, None, None)

    @patch('os.getpid')
    @patch('time.time')
    def test_lock_file_content(self, mock_time, mock_pid):
        # 验证锁文件内容格式
        mock_pid.return_value = 9999
        mock_time.return_value = 123456.789

        with patch('os.open') as mock_os_open:
            mock_os_open.return_value = 123
            with patch('os.fdopen') as mock_fdopen:
                # 模拟写入文件描述符
                mock_file = MagicMock()
                mock_fdopen.return_value.__enter__.return_value = mock_file

                with FileLockContext(self.lock_path):
                    mock_fdopen.assert_called_once_with(123, 'w')
                    mock_file.write.assert_called_once_with('9999\n123456.789')
