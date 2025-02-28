import errno
import io
import os
import tempfile
import unittest
from typing import Tuple
from unittest.mock import MagicMock, call, mock_open, patch

from llm_web_kit.exception.exception import ModelInputException
from llm_web_kit.model.resource_utils.download_assets import (
    FileLock, HttpConnection, S3Connection, calc_file_md5, calc_file_sha256,
    decide_cache_dir, download_auto_file, download_to_temp, move_to_target,
    try_remove, verify_file_checksum)


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


class Test_decide_cache_dir:

    @patch('os.environ', {'WEB_KIT_CACHE_DIR': '/env/cache_dir'})
    @patch('llm_web_kit.model.resource_utils.download_assets.load_config')
    def test_only_env(self, get_configMock):
        get_configMock.side_effect = Exception
        assert decide_cache_dir() == '/env/cache_dir'

    @patch('os.environ', {})
    @patch('llm_web_kit.model.resource_utils.download_assets.load_config')
    def test_only_config(self, get_configMock):
        get_configMock.return_value = {
            'resources': {'common': {'cache_path': '/config/cache_dir'}}
        }
        assert decide_cache_dir() == '/config/cache_dir'

    @patch('os.environ', {})
    @patch('llm_web_kit.model.resource_utils.download_assets.load_config')
    def test_default(self, get_configMock):
        get_configMock.side_effect = Exception
        # if no env or config, use default
        assert decide_cache_dir() == os.path.expanduser('~/.llm_web_kit_cache')

    @patch('os.environ', {'WEB_KIT_CACHE_DIR': '/env/cache_dir'})
    @patch('llm_web_kit.model.resource_utils.download_assets.load_config')
    def test_both(self, get_configMock):
        get_configMock.return_value = {
            'resources': {'common': {'cache_path': '/config/cache_dir'}}
        }
        # config is preferred
        assert decide_cache_dir() == '/config/cache_dir'


class Test_calc_file_md5:

    def test_calc_file_md5(self):
        import hashlib

        with tempfile.NamedTemporaryFile() as f:
            test_bytes = b'hello world' * 10000
            f.write(test_bytes)
            f.flush()
            assert calc_file_md5(f.name) == hashlib.md5(test_bytes).hexdigest()


class Test_calc_file_sha256:

    def test_calc_file_sha256(self):
        import hashlib

        with tempfile.NamedTemporaryFile() as f:
            test_bytes = b'hello world' * 10000
            f.write(test_bytes)
            f.flush()
            assert calc_file_sha256(f.name) == hashlib.sha256(test_bytes).hexdigest()


def read_mockio_size(mock_io: io.BytesIO, size: int):
    while True:
        data = mock_io.read(size)
        if not data:
            break
        yield data


def get_mock_http_response(test_data: bytes) -> Tuple[MagicMock, int]:
    mock_io = io.BytesIO(test_data)
    content_length = len(test_data)
    response_mock = MagicMock()
    response_mock.headers = {'content-length': str(content_length)}
    response_mock.iter_content.return_value = read_mockio_size(mock_io, 1024)
    return response_mock, content_length


def get_mock_s3_response(test_data: bytes) -> Tuple[MagicMock, int]:
    mock_io = io.BytesIO(test_data)
    content_length = len(test_data)
    clientMock = MagicMock()
    body = MagicMock()
    body.read.side_effect = read_mockio_size(mock_io, 1024)
    clientMock.get_object.return_value = {'ContentLength': content_length, 'Body': body}
    return clientMock, content_length


@patch('llm_web_kit.model.resource_utils.download_assets.get_s3_client')
@patch('llm_web_kit.model.resource_utils.download_assets.split_s3_path')
def test_S3Connection(split_s3_pathMock, get_s3_clientMock):
    test_data = b'hello world' * 100

    # Mock the split_s3_path function
    split_s3_pathMock.return_value = ('bucket', 'key')

    # Mock the S3 client
    clientMock, content_length = get_mock_s3_response(test_data)
    get_s3_clientMock.return_value = clientMock

    # Test the S3Connection class
    conn = S3Connection('s3://bucket/key')
    assert conn.get_size() == content_length
    assert b''.join(conn.read_stream()) == test_data


@patch('requests.get')
def test_HttpConnection(requests_get_mock):
    test_data = b'hello world' * 100
    response_mock, content_length = get_mock_http_response(test_data)
    requests_get_mock.return_value = response_mock

    # Test the HttpConnection class
    conn = HttpConnection('http://example.com/file')
    assert conn.get_size() == content_length
    assert b''.join(conn.read_stream()) == test_data


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

        with FileLock(self.lock_path):
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

        with FileLock(self.lock_path, timeout=300):
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
            with FileLock(self.lock_path, timeout=300):
                pass

    @patch('os.open')
    def test_other_os_error(self, mock_os_open):
        # 模拟其他OS错误（如权限不足）
        mock_os_open.side_effect = OSError(errno.EACCES, 'Permission denied')
        with self.assertRaises(OSError):
            with FileLock(self.lock_path):
                pass

    @patch('os.close')
    @patch('os.remove')
    def test_cleanup_on_exit(self, mock_remove, mock_close):

        mock_close.side_effect = None
        # 确保退出上下文时执行清理
        lock_path = 'test.lock'
        lock = FileLock(lock_path)
        lock._fd = 123  # 模拟已打开的文件描述符
        lock.__exit__('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', None, None)
        mock_remove.assert_called_once_with(self.lock_path)

    @patch('os.remove')
    def test_cleanup_failure_handled(self, mock_remove):
        # 模拟删除锁文件时失败
        mock_remove.side_effect = OSError
        lock = FileLock(self.lock_path)
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

                with FileLock(self.lock_path):
                    mock_fdopen.assert_called_once_with(123, 'w')
                    mock_file.write.assert_called_once_with('9999\n123456.789')


class TestDownloadAutoFile(unittest.TestCase):

    @patch('llm_web_kit.model.resource_utils.download_assets.os.path.exists')
    @patch('llm_web_kit.model.resource_utils.download_assets.calc_file_md5')
    @patch('llm_web_kit.model.resource_utils.download_assets.is_s3_path')
    @patch('llm_web_kit.model.resource_utils.download_assets.S3Connection')
    @patch('llm_web_kit.model.resource_utils.download_assets.HttpConnection')
    def test_file_exists_correct_md5(
        self,
        mock_http_conn,
        mock_s3_conn,
        mock_is_s3_path,
        mock_calc_file_md5,
        mock_os_path_exists,
    ):
        # Arrange
        mock_os_path_exists.return_value = True
        mock_calc_file_md5.return_value = 'correct_md5'
        mock_is_s3_path.return_value = False
        mock_http_conn.return_value = MagicMock(get_size=MagicMock(return_value=100))

        # Act
        result = download_auto_file(
            'http://example.com', 'target_path', md5_sum='correct_md5'
        )

        # Assert
        assert result == 'target_path'

        mock_os_path_exists.assert_called_once_with('target_path')
        mock_calc_file_md5.assert_called_once_with('target_path')
        mock_http_conn.assert_not_called()
        mock_s3_conn.assert_not_called()
        try:
            os.remove('target_path.lock')
        except FileNotFoundError:
            pass

    @patch('llm_web_kit.model.resource_utils.download_assets.os.path.exists')
    @patch('llm_web_kit.model.resource_utils.download_assets.calc_file_sha256')
    @patch('llm_web_kit.model.resource_utils.download_assets.is_s3_path')
    @patch('llm_web_kit.model.resource_utils.download_assets.S3Connection')
    @patch('llm_web_kit.model.resource_utils.download_assets.HttpConnection')
    def test_file_exists_correct_sha256(
        self,
        mock_http_conn,
        mock_s3_conn,
        mock_is_s3_path,
        mock_calc_file_sha256,
        mock_os_path_exists,
    ):
        # Arrange
        mock_os_path_exists.return_value = True
        mock_calc_file_sha256.return_value = 'correct_sha256'
        mock_is_s3_path.return_value = False
        mock_http_conn.return_value = MagicMock(get_size=MagicMock(return_value=100))

        # Act
        result = download_auto_file(
            'http://example.com', 'sha256_target_path', sha256_sum='correct_sha256'
        )

        # Assert
        assert result == 'sha256_target_path'

        mock_os_path_exists.assert_called_once_with('sha256_target_path')
        mock_calc_file_sha256.assert_called_once_with('sha256_target_path')
        mock_http_conn.assert_not_called()
        mock_s3_conn.assert_not_called()
        try:
            os.remove('sha256_target_path.lock')
        except FileNotFoundError:
            pass

    @patch('llm_web_kit.model.resource_utils.download_assets.calc_file_md5')
    @patch('llm_web_kit.model.resource_utils.download_assets.os.remove')
    @patch('llm_web_kit.model.resource_utils.download_assets.is_s3_path')
    @patch('llm_web_kit.model.resource_utils.download_assets.S3Connection')
    @patch('llm_web_kit.model.resource_utils.download_assets.HttpConnection')
    def test_file_exists_wrong_md5_download_http(
        self,
        mock_http_conn,
        mock_s3_conn,
        mock_is_s3_path,
        mock_os_remove,
        mock_calc_file_md5,
    ):
        # Arrange
        mock_calc_file_md5.return_value = 'wrong_md5'
        mock_is_s3_path.return_value = False

        with tempfile.TemporaryDirectory() as tmp_dir:
            with open(os.path.join(tmp_dir, 'target_path'), 'wb') as f:
                f.write(b'hello world')
            response_mock, content_length = get_mock_http_response(b'hello world')
            mock_http_conn.return_value = MagicMock(
                get_size=MagicMock(return_value=content_length),
                read_stream=MagicMock(return_value=response_mock.iter_content()),
            )

            target_path = os.path.join(tmp_dir, 'target_path')
            # Act
            result = download_auto_file(
                'http://example.com', target_path, md5_sum='correct_md5'
            )

            assert result == target_path
            with open(target_path, 'rb') as f:
                assert f.read() == b'hello world'

    @patch('llm_web_kit.model.resource_utils.download_assets.calc_file_sha256')
    @patch('llm_web_kit.model.resource_utils.download_assets.os.remove')
    @patch('llm_web_kit.model.resource_utils.download_assets.is_s3_path')
    @patch('llm_web_kit.model.resource_utils.download_assets.S3Connection')
    @patch('llm_web_kit.model.resource_utils.download_assets.HttpConnection')
    def test_file_exists_wrong_sha256_download_http(
        self,
        mock_http_conn,
        mock_s3_conn,
        mock_is_s3_path,
        mock_os_remove,
        mock_calc_file_sha256,
    ):
        # Arrange
        mock_calc_file_sha256.return_value = 'wrong_sha256'
        mock_is_s3_path.return_value = False

        with tempfile.TemporaryDirectory() as tmp_dir:
            with open(os.path.join(tmp_dir, 'target_path'), 'wb') as f:
                f.write(b'hello world')
            response_mock, content_length = get_mock_http_response(b'hello world')
            mock_http_conn.return_value = MagicMock(
                get_size=MagicMock(return_value=content_length),
                read_stream=MagicMock(return_value=response_mock.iter_content()),
            )

            target_path = os.path.join(tmp_dir, 'target_path')
            # Act
            result = download_auto_file(
                'http://example.com', target_path, sha256_sum='correct_sha256'
            )

            assert result == target_path
            with open(target_path, 'rb') as f:
                assert f.read() == b'hello world'

    @patch('llm_web_kit.model.resource_utils.download_assets.calc_file_md5')
    @patch('llm_web_kit.model.resource_utils.download_assets.os.remove')
    @patch('llm_web_kit.model.resource_utils.download_assets.is_s3_path')
    @patch('llm_web_kit.model.resource_utils.download_assets.S3Connection')
    @patch('llm_web_kit.model.resource_utils.download_assets.HttpConnection')
    def test_file_not_exists_download_http(
        self,
        mock_http_conn,
        mock_s3_conn,
        mock_is_s3_path,
        mock_os_remove,
        mock_calc_file_md5,
    ):
        # Arrange
        mock_is_s3_path.return_value = False

        with tempfile.TemporaryDirectory() as tmp_dir:
            response_mock, content_length = get_mock_http_response(b'hello world')
            mock_http_conn.return_value = MagicMock(
                get_size=MagicMock(return_value=content_length),
                read_stream=MagicMock(return_value=response_mock.iter_content()),
            )

            target_path = os.path.join(tmp_dir, 'target_path')
            # Act
            result = download_auto_file(
                'http://example.com', target_path, md5_sum='correct_md5'
            )

            assert result == target_path
            with open(target_path, 'rb') as f:
                assert f.read() == b'hello world'


# def verify_file_checksum(
#     file_path: str, md5_sum: Optional[str] = None, sha256_sum: Optional[str] = None
# ) -> bool:
#     """校验文件哈希值."""
# if not sum([bool(md5_sum), bool(sha256_sum)]) == 1:
#     raise ModelInputException('Exactly one of md5_sum or sha256_sum must be provided')

#     if md5_sum:
#         actual = calc_file_md5(file_path)
#         if actual != md5_sum:
#             logger.warning(
#                 f'MD5 mismatch: expect {md5_sum[:8]}..., got {actual[:8]}...'
#             )
#             return False

#     if sha256_sum:
#         actual = calc_file_sha256(file_path)
#         if actual != sha256_sum:
#             logger.warning(
#                 f'SHA256 mismatch: expect {sha256_sum[:8]}..., got {actual[:8]}...'
#             )
#             return False


#     return True
class Test_verify_file_checksum(unittest.TestCase):
    # test pass two value
    # test pass two None
    # test pass one value correct
    # test pass one value incorrect

    @patch('llm_web_kit.model.resource_utils.download_assets.calc_file_md5')
    @patch('llm_web_kit.model.resource_utils.download_assets.calc_file_sha256')
    def test_pass_two_value(self, mock_calc_file_sha256, mock_calc_file_md5):
        file_path = 'file_path'
        md5_sum = 'md5_sum'
        sha256_sum = 'sha256_sum'
        mock_calc_file_md5.return_value = md5_sum
        mock_calc_file_sha256.return_value = sha256_sum
        # will raise ModelInputException
        with self.assertRaises(ModelInputException):
            verify_file_checksum(file_path, md5_sum, sha256_sum)

    @patch('llm_web_kit.model.resource_utils.download_assets.calc_file_md5')
    @patch('llm_web_kit.model.resource_utils.download_assets.calc_file_sha256')
    def test_pass_two_None(self, mock_calc_file_sha256, mock_calc_file_md5):
        file_path = 'file_path'
        md5_sum = None
        sha256_sum = None
        # will raise ModelInputException
        with self.assertRaises(ModelInputException):
            verify_file_checksum(file_path, md5_sum, sha256_sum)

    @patch('llm_web_kit.model.resource_utils.download_assets.calc_file_md5')
    @patch('llm_web_kit.model.resource_utils.download_assets.calc_file_sha256')
    def test_pass_one_value_correct(self, mock_calc_file_sha256, mock_calc_file_md5):
        file_path = 'file_path'
        md5_sum = 'md5_sum'
        sha256_sum = None
        mock_calc_file_md5.return_value = md5_sum
        mock_calc_file_sha256.return_value = None
        assert verify_file_checksum(file_path, md5_sum, sha256_sum) is True

    @patch('llm_web_kit.model.resource_utils.download_assets.calc_file_md5')
    @patch('llm_web_kit.model.resource_utils.download_assets.calc_file_sha256')
    def test_pass_one_value_incorrect(self, mock_calc_file_sha256, mock_calc_file_md5):
        file_path = 'file_path'
        md5_sum = 'md5_sum'
        sha256_sum = None
        mock_calc_file_md5.return_value = 'wrong_md5'
        mock_calc_file_sha256.return_value = None
        assert verify_file_checksum(file_path, md5_sum, sha256_sum) is False


class TestDownloadToTemp(unittest.TestCase):

    def setUp(self):
        self.mock_conn = MagicMock()
        self.mock_progress = MagicMock()

    # mock_open
    @patch('builtins.open', new_callable=mock_open)
    @patch('tempfile.NamedTemporaryFile')
    def test_normal_download(self, mock_temp, mock_open_func):
        # 模拟下载流数据
        test_data = [b'chunk1', b'chunk2', b'chunk3']
        self.mock_conn.read_stream.return_value = iter(test_data)

        # 配置临时文件mock
        mock_temp.return_value.__enter__.return_value.name = '/tmp/fake.tmp'

        result = download_to_temp(self.mock_conn, self.mock_progress)

        mock_open_func.return_value.write.assert_has_calls(
            [call(b'chunk1'), call(b'chunk2'), call(b'chunk3')]
        )
        # 验证进度条更新
        self.mock_progress.update.assert_has_calls(
            [call(6), call(6), call(6)]  # 每个chunk的长度是6
        )
        self.assertEqual(result, '/tmp/fake.tmp')

    @patch('builtins.open', new_callable=mock_open)
    @patch('tempfile.NamedTemporaryFile')
    def test_exception_handling(self, mock_temp, mock_open_func):
        # 模拟写入时发生异常
        self.mock_conn.read_stream.return_value = iter([b'data'])
        mock_temp.return_value.__enter__.return_value.name = '/tmp/fail.tmp'

        # file_mock = mock_temp.return_value.__enter__.return_value.__enter__.return_value
        # file_mock.write.side_effect = IOError("Disk failure")

        mock_open_func.return_value.write.side_effect = IOError('Disk failure')
        with self.assertRaises(IOError):
            download_to_temp(self.mock_conn, self.mock_progress)

    def test_empty_chunk_handling(self):
        # 测试包含空chunk的情况
        self.mock_conn.read_stream.return_value = iter([b'', b'valid', b''])

        with tempfile.NamedTemporaryFile(delete=False) as real_temp:
            with patch('tempfile.NamedTemporaryFile') as mock_temp:
                mock_temp.return_value.__enter__.return_value.name = real_temp.name
                download_to_temp(self.mock_conn, self.mock_progress)

        # 验证只有有效chunk被写入
        with open(real_temp.name, 'rb') as f:
            self.assertEqual(f.read(), b'valid')
        os.unlink(real_temp.name)


class TestMoveToTarget(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.target_path = os.path.join(self.tmp_dir.name, 'subdir/target.file')

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_normal_move(self):
        # 创建测试文件
        tmp_path = os.path.join(self.tmp_dir.name, 'test.tmp')
        with open(tmp_path, 'wb') as f:
            f.write(b'test content')

        move_to_target(tmp_path, self.target_path, 12)

        # 验证结果
        self.assertTrue(os.path.exists(self.target_path))
        self.assertFalse(os.path.exists(tmp_path))
        self.assertEqual(os.path.getsize(self.target_path), 12)

    def test_size_mismatch(self):
        tmp_path = os.path.join(self.tmp_dir.name, 'bad.tmp')
        with open(tmp_path, 'wb') as f:
            f.write(b'short')

        with self.assertRaisesRegex(ValueError, 'size mismatch'):
            move_to_target(tmp_path, self.target_path, 100)

    def test_directory_creation(self):
        tmp_path = os.path.join(self.tmp_dir.name, 'test.tmp')
        with open(tmp_path, 'wb') as f:
            f.write(b'content')

        # 目标目录不存在
        deep_path = os.path.join(self.tmp_dir.name, 'a/b/c/target.file')
        move_to_target(tmp_path, deep_path, 7)

        self.assertTrue(os.path.exists(deep_path))


if __name__ == '__main__':
    unittest.main()
