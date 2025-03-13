import multiprocessing
import os
import shutil
import tempfile
import time
import unittest
from functools import partial
from unittest.mock import Mock, patch

from filelock import Timeout

from llm_web_kit.model.resource_utils.process_with_lock import (
    get_path_mtime, process_and_verify_file_with_lock)


class TestGetPathMtime(unittest.TestCase):
    """测试 get_path_mtime 函数."""

    def setUp(self):
        self.test_dir = 'test_dir'
        self.test_file = 'test_file.txt'
        os.makedirs(self.test_dir, exist_ok=True)
        with open(self.test_file, 'w') as f:
            f.write('test')

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_file_mtime(self):
        # 测试文件路径
        expected_mtime = os.path.getmtime(self.test_file)
        result = get_path_mtime(self.test_file)
        self.assertEqual(result, expected_mtime)

    def test_dir_with_files(self):
        # 测试包含文件的目录
        file1 = os.path.join(self.test_dir, 'file1.txt')
        file2 = os.path.join(self.test_dir, 'file2.txt')

        with open(file1, 'w') as f:
            f.write('test1')
        time.sleep(0.1)  # 确保mtime不同
        with open(file2, 'w') as f:
            f.write('test2')

        latest_mtime = max(os.path.getmtime(file1), os.path.getmtime(file2))
        result = get_path_mtime(self.test_dir)
        self.assertEqual(result, latest_mtime)

    def test_empty_dir(self):
        # 测试空目录（预期返回0）
        empty_dir = 'empty_dir'
        os.makedirs(empty_dir, exist_ok=True)
        try:
            result = get_path_mtime(empty_dir)
            self.assertEqual(result, None)  # 根据当前函数逻辑返回0
        finally:
            shutil.rmtree(empty_dir)


class TestProcessAndVerifyFileWithLock(unittest.TestCase):
    """测试 process_and_verify_file_with_lock 函数."""

    def setUp(self):
        self.target_path = 'target.txt'
        self.lock_path = self.target_path + '.lock'

    def tearDown(self):
        if os.path.exists(self.target_path):
            os.remove(self.target_path)
        if os.path.exists(self.lock_path):
            os.remove(self.lock_path)

    @patch('os.path.exists')
    @patch('llm_web_kit.model.resource_utils.process_with_lock.try_remove')
    def test_target_exists_and_valid(self, mock_remove, mock_exists):
        # 目标存在且验证成功
        mock_exists.side_effect = lambda path: path == self.target_path
        process_func = Mock()
        verify_func = Mock(return_value=True)

        result = process_and_verify_file_with_lock(
            process_func, verify_func, self.target_path
        )

        self.assertEqual(result, self.target_path)
        process_func.assert_not_called()
        verify_func.assert_called_once()

    @patch('os.path.exists')
    @patch('llm_web_kit.model.resource_utils.process_with_lock.try_remove')
    @patch('time.sleep')
    def test_target_not_exists_acquire_lock_success(
        self, mock_sleep, mock_remove, mock_exists
    ):
        # 目标不存在，成功获取锁
        mock_exists.side_effect = lambda path: False
        process_func = Mock(return_value=self.target_path)
        verify_func = Mock()

        result = process_and_verify_file_with_lock(
            process_func, verify_func, self.target_path
        )

        process_func.assert_called_once()
        self.assertEqual(result, self.target_path)

    @patch('os.path.exists')
    @patch('llm_web_kit.model.resource_utils.process_with_lock.try_remove')
    @patch('time.sleep')
    def test_second_validation_after_lock(self, mock_sleep, mock_remove, mock_exists):
        # 获取锁后二次验证成功（其他进程已完成）
        mock_exists.side_effect = lambda path: {
            self.lock_path: False,
            self.target_path: True,
        }
        verify_func = Mock(return_value=True)
        process_func = Mock()

        result = process_and_verify_file_with_lock(
            process_func, verify_func, self.target_path
        )

        process_func.assert_not_called()
        self.assertEqual(result, self.target_path)

    @patch('os.path.exists')
    @patch('llm_web_kit.model.resource_utils.process_with_lock.SoftFileLock')
    @patch('time.sleep')
    def test_lock_timeout_retry_success(self, mock_sleep, mock_lock, mock_exists):
        # 第一次获取锁超时，重试后成功
        lock_str = self.target_path + '.lock'
        mock_exists.return_value = False
        lock_instance = Mock()
        mock_lock.return_value = lock_instance

        # 第一次acquire抛出Timeout，第二次成功
        lock_instance.acquire.side_effect = [Timeout(lock_str), None]
        process_func = Mock(return_value=self.target_path)
        verify_func = Mock()

        process_and_verify_file_with_lock(process_func, verify_func, self.target_path)

        self.assertEqual(lock_instance.acquire.call_count, 2)
        process_func.assert_called_once()


class TestProcessWithLockRealFiles(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.target_name = 'test_target.dat'
        self.lock_suffix = '.lock'

        self.target_path = os.path.join(self.temp_dir.name, self.target_name)
        self.lock_path = self.target_path + self.lock_suffix

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_zombie_process_recovery(self):
        # 准备过期文件和僵尸锁文件
        with open(self.target_path, 'w') as f:
            f.write('old content')
        with open(self.lock_path, 'w') as f:
            f.write('lock')

        # 设置文件修改时间为超时前（60秒超时，设置为2分钟前）
        old_mtime = time.time() - 59
        os.utime(self.target_path, (old_mtime, old_mtime))

        # Mock验证函数和处理函数
        def verify_func():
            # 验证文件内容
            with open(self.target_path) as f:
                content = f.read()
            return content == 'new content'

        process_called = [False]  # 使用list实现nonlocal效果

        def real_process():
            # 真实写入文件
            with open(self.target_path, 'w') as f:
                f.write('new content')
            process_called[0] = True
            return self.target_path

        # 执行测试
        result = process_and_verify_file_with_lock(
            process_func=real_process,
            verify_func=verify_func,
            target_path=self.target_path,
            lock_suffix=self.lock_suffix,
            timeout=60,
        )

        # 验证结果
        self.assertTrue(os.path.exists(self.target_path))
        self.assertFalse(os.path.exists(self.lock_path))
        self.assertTrue(process_called[0])
        self.assertEqual(result, self.target_path)

        # 验证文件内容
        with open(self.target_path) as f:
            content = f.read()
        self.assertEqual(content, 'new content')


def dummy_process_func(target_path, data_content):
    # 写入文件
    with open(target_path, 'w') as f:
        time.sleep(1)
        f.write(data_content)
    return target_path


def dummy_verify_func(target_path, data_content):
    # 验证文件内容
    try:
        with open(target_path) as f:
            content = f.read()
    except FileNotFoundError:
        return False
    return content == data_content


class TestMultiProcessWithLock(unittest.TestCase):

    def setUp(self):
        # 临时文件夹
        self.temp_dir = tempfile.TemporaryDirectory()
        self.target_name = 'test_target.dat'
        self.lock_suffix = '.lock'
        self.data_content = 'test content'
        self.target_path = os.path.join(self.temp_dir.name, self.target_name)
        self.lock_path = self.target_path + self.lock_suffix

    def tearDown(self):
        self.temp_dir.cleanup()

    # 开始时什么都没有，多个进程尝试拿锁，一个进程拿到锁并用1s写入一个资源文件（指定内容，verify尝试检查）。然后所有的进程都发现这个文件被写入，成功返回。资源文件存在，并且锁文件被删掉
    def test_multi_process_with_lock(self):
        process_func = partial(dummy_process_func, self.target_path, self.data_content)
        verify_func = partial(dummy_verify_func, self.target_path, self.data_content)

        # 多进程同时执行
        # 构建多个进程 然后同时执行
        pool = multiprocessing.Pool(16)
        process = partial(
            process_and_verify_file_with_lock,
            process_func,
            verify_func,
            self.target_path,
            self.lock_suffix,
        )
        results = pool.map(process, [60] * 32)
        pool.close()
        # 检查文件是否存在
        self.assertTrue(os.path.exists(self.target_path))
        self.assertFalse(os.path.exists(self.lock_path))
        # 检查结果
        for result in results:
            self.assertEqual(result, self.target_path)
        # 检查文件内容
        with open(self.target_path) as f:
            content = f.read()
        self.assertEqual(content, self.data_content)

    # 开始时有个文件，这个文件mtime比较早，且有个锁文件（模拟之前下载失败了）。然后同样多进程尝试执行，有某个进程尝试删掉这个文件和锁文件，然后还原为场景1，最终大家成功返回。
    def test_multi_process_with_zombie_files(self):
        # 准备过期文件和僵尸锁文件
        with open(self.target_path, 'w') as f:
            f.write('old content')
        with open(self.lock_path, 'w') as f:
            f.write('lock')

        # 设置文件修改时间为超时前（60秒超时，设置为2分钟前）
        old_mtime = time.time() - 59
        os.utime(self.target_path, (old_mtime, old_mtime))

        process_func = partial(dummy_process_func, self.target_path, self.data_content)
        verify_func = partial(dummy_verify_func, self.target_path, self.data_content)

        # 多进程同时执行
        pool = multiprocessing.Pool(16)
        process = partial(
            process_and_verify_file_with_lock,
            process_func,
            verify_func,
            self.target_path,
            self.lock_suffix,
        )
        results = pool.map(process, [60] * 32)
        pool.close()
        # 检查文件是否存在
        self.assertTrue(os.path.exists(self.target_path))
        self.assertFalse(os.path.exists(self.lock_path))
        # 检查结果
        for result in results:
            self.assertEqual(result, self.target_path)
        # 检查文件内容
        with open(self.target_path) as f:
            content = f.read()
        self.assertEqual(content, self.data_content)


if __name__ == '__main__':
    unittest.main()
