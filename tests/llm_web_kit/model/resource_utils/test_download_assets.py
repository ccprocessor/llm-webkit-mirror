import hashlib
import os
import tempfile
import time
import unittest
from unittest.mock import MagicMock, call, patch

from llm_web_kit.exception.exception import ModelResourceException
from llm_web_kit.model.resource_utils.download_assets import (
    HttpConnection, S3Connection, calc_file_md5, calc_file_sha256,
    download_auto_file, download_auto_file_core, download_to_temp,
    verify_file_checksum)


class TestChecksumCalculations:

    def test_calc_file_md5(self):
        with tempfile.NamedTemporaryFile() as f:
            test_data = b'hello world' * 100
            f.write(test_data)
            f.flush()
            expected = hashlib.md5(test_data).hexdigest()
            assert calc_file_md5(f.name) == expected

    def test_calc_file_sha256(self):
        with tempfile.NamedTemporaryFile() as f:
            test_data = b'hello world' * 100
            f.write(test_data)
            f.flush()
            expected = hashlib.sha256(test_data).hexdigest()
            assert calc_file_sha256(f.name) == expected


class TestConnections:

    @patch('requests.get')
    def test_http_connection(self, mock_get):
        test_data = b'test data'
        mock_response = MagicMock()
        mock_response.headers = {'content-length': str(len(test_data))}
        mock_response.iter_content.return_value = [test_data]
        mock_get.return_value = mock_response

        conn = HttpConnection('http://example.com')
        assert conn.get_size() == len(test_data)
        assert next(conn.read_stream()) == test_data
        del conn
        mock_response.close.assert_called()

    @patch('llm_web_kit.model.resource_utils.download_assets.get_s3_client')
    def test_s3_connection(self, mock_client):
        mock_body = MagicMock()
        mock_body.read.side_effect = [b'chunk1', b'chunk2', b'']
        mock_client.return_value.get_object.return_value = {
            'ContentLength': 100,
            'Body': mock_body,
        }

        conn = S3Connection('s3://bucket/key')
        assert conn.get_size() == 100
        assert list(conn.read_stream()) == [b'chunk1', b'chunk2']
        del conn
        mock_body.close.assert_called()


class TestDownloadCoreFunctionality(unittest.TestCase):

    @patch('llm_web_kit.model.resource_utils.download_assets.S3Connection')
    def test_successful_download(self, mock_conn):
        # Mock connection
        download_data = b'data'
        mock_instance = MagicMock()
        mock_instance.read_stream.return_value = [download_data]
        mock_instance.get_size.return_value = len(download_data)
        mock_conn.return_value = mock_instance

        with tempfile.TemporaryDirectory() as tmpdir:
            target = os.path.join(tmpdir, 'target.file')
            result = download_auto_file_core('s3://bucket/key', target)

            assert result == target
            assert os.path.exists(target)

    @patch('llm_web_kit.model.resource_utils.download_assets.HttpConnection')
    def test_size_mismatch(self, mock_conn):
        download_data = b'data'
        mock_instance = MagicMock()
        mock_instance.read_stream.return_value = [download_data]
        mock_instance.get_size.return_value = len(download_data) + 1

        mock_conn.return_value = mock_instance

        with tempfile.TemporaryDirectory() as tmpdir:
            target = os.path.join(tmpdir, 'target.file')
            with self.assertRaises(ModelResourceException):
                download_auto_file_core('http://example.com', target)


class TestDownloadToTemp:

    def test_normal_download(self):
        mock_conn = MagicMock()
        mock_conn.read_stream.return_value = [b'chunk1', b'chunk2']
        mock_progress = MagicMock()

        with tempfile.TemporaryDirectory() as tmpdir:
            temp_path = os.path.join(tmpdir, 'temp.file')
            download_to_temp(mock_conn, mock_progress, temp_path)

            with open(temp_path, 'rb') as f:
                assert f.read() == b'chunk1chunk2'
            mock_progress.update.assert_has_calls([call(6), call(6)])

    def test_empty_chunk_handling(self):
        mock_conn = MagicMock()
        mock_conn.read_stream.return_value = [b'', b'data', b'']
        mock_progress = MagicMock()

        with tempfile.TemporaryDirectory() as tmpdir:
            temp_path = os.path.join(tmpdir, 'temp.file')
            download_to_temp(mock_conn, mock_progress, temp_path)

            with open(temp_path, 'rb') as f:
                assert f.read() == b'data'


class TestVerifyChecksum(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile()
        self.temp_file.write(b'test data')
        self.temp_file.flush()

    def tearDown(self):
        self.temp_file.close()

    @patch('llm_web_kit.model.resource_utils.download_assets.calc_file_md5')
    def test_valid_md5(self, mock_md5):
        mock_md5.return_value = 'correct_md5'
        assert verify_file_checksum(self.temp_file.name, md5_sum='correct_md5') is True

    @patch('llm_web_kit.model.resource_utils.download_assets.calc_file_sha256')
    def test_invalid_sha256(self, mock_sha):
        mock_sha.return_value = 'wrong_sha'
        assert verify_file_checksum(self.temp_file.name, sha256_sum='correct_sha') is False

    def test_no_such_file(self):
        assert verify_file_checksum('dummy', md5_sum='a') is False

    def test_invalid_arguments(self):
        with self.assertRaises(ModelResourceException):
            verify_file_checksum('dummy', md5_sum='a', sha256_sum='b')


class TestDownloadAutoFile(unittest.TestCase):
    @patch(
        'llm_web_kit.model.resource_utils.download_assets.process_and_verify_file_with_lock'
    )
    @patch('llm_web_kit.model.resource_utils.download_assets.verify_file_checksum')
    @patch('llm_web_kit.model.resource_utils.download_assets.download_auto_file_core')
    def test_download(self, mock_download, mock_verify, mock_process):
        def download_func(resource_path, target_path):
            dir = os.path.dirname(target_path)
            os.makedirs(dir, exist_ok=True)
            with open(target_path, 'w') as f:
                time.sleep(1)
                f.write(resource_path)

        mock_download.side_effect = download_func

        def verify_func(target_path, md5 ,sha):
            with open(target_path, 'r') as f:
                return f.read() == md5

        mock_verify.side_effect = verify_func

        def process_and_verify(
            process_func, verify_func, target_path, lock_suffix, timeout
        ):
            process_func()
            if verify_func():
                return target_path

        mock_process.side_effect = process_and_verify
        with tempfile.TemporaryDirectory() as tmpdir:
            resource_url = 'http://example.com/resource'
            target_dir = os.path.join(tmpdir, 'target')
            result = download_auto_file(resource_url, target_dir, md5_sum=resource_url)
            assert result == os.path.join(tmpdir, 'target')


if __name__ == '__main__':
    unittest.main()
