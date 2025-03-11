import os
import tempfile
import zipfile
from unittest import TestCase
from unittest.mock import patch

from llm_web_kit.exception.exception import ModelResourceException
from llm_web_kit.model.resource_utils.unzip_ext import (check_zip_path,
                                                        get_unzip_dir,
                                                        unzip_local_file,
                                                        unzip_local_file_core)


class TestGetUnzipDir(TestCase):
    def test_get_unzip_dir_with_zip_extension(self):
        self.assertEqual(
            get_unzip_dir('/path/to/test.zip'),
            '/path/to/test_unzip',
        )

    def test_get_unzip_dir_without_zip_extension(self):
        self.assertEqual(
            get_unzip_dir('/path/to/test'),
            '/path/to/test_unzip',
        )


class TestCheckZipPath(TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.zip_path = os.path.join(self.temp_dir.name, 'test.zip')
        self.target_dir = os.path.join(self.temp_dir.name, 'target')
        os.makedirs(self.target_dir, exist_ok=True)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_check_valid_zip(self):
        # Create valid zip with test file
        with zipfile.ZipFile(self.zip_path, 'w') as zipf:
            zipf.writestr('file.txt', 'content')
        # Properly extract files
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.target_dir)

        self.assertTrue(check_zip_path(self.zip_path, self.target_dir))

    def test_check_missing_file(self):
        with zipfile.ZipFile(self.zip_path, 'w') as zipf:
            zipf.writestr('file.txt', 'content')
        # Extract and then delete file
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.target_dir)
        os.remove(os.path.join(self.target_dir, 'file.txt'))

        self.assertFalse(check_zip_path(self.zip_path, self.target_dir))

    def test_check_corrupted_file_size(self):
        with zipfile.ZipFile(self.zip_path, 'w') as zipf:
            zipf.writestr('file.txt', 'original content')
        # Modify extracted file
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.target_dir)
        with open(os.path.join(self.target_dir, 'file.txt'), 'w') as f:
            f.write('modified')

        self.assertFalse(check_zip_path(self.zip_path, self.target_dir))

    def test_password_protected_zip(self):
        password = 'secret'
        # Create encrypted zip
        with zipfile.ZipFile(self.zip_path, 'w') as zipf:
            zipf.writestr('file.txt', 'content')
            zipf.setpassword(password.encode())
        # Extract with correct password
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            zip_ref.setpassword(password.encode())
            zip_ref.extractall(self.target_dir)

        self.assertTrue(
            check_zip_path(self.zip_path, self.target_dir, password=password)
        )


class TestUnzipLocalFileCore(TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.zip_path = os.path.join(self.temp_dir.name, 'test.zip')
        self.target_dir = os.path.join(self.temp_dir.name, 'target')

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_nonexistent_zip_file(self):
        with self.assertRaises(ModelResourceException) as cm:
            unzip_local_file_core('invalid.zip', self.target_dir)
        self.assertIn('does not exist', str(cm.exception))

    def test_target_directory_conflict(self):
        # Create target directory first
        os.makedirs(self.target_dir)
        with zipfile.ZipFile(self.zip_path, 'w') as zipf:
            zipf.writestr('file.txt', 'content')

        with self.assertRaises(ModelResourceException) as cm:
            unzip_local_file_core(self.zip_path, self.target_dir)
        self.assertIn('already exists', str(cm.exception))

    def test_successful_extraction(self):
        with zipfile.ZipFile(self.zip_path, 'w') as zipf:
            zipf.writestr('file.txt', 'content')

        result = unzip_local_file_core(self.zip_path, self.target_dir)
        self.assertEqual(result, self.target_dir)
        self.assertTrue(os.path.exists(os.path.join(self.target_dir, 'file.txt')))

    def test_password_protected_extraction(self):
        password = 'secret'
        with zipfile.ZipFile(self.zip_path, 'w') as zipf:
            zipf.writestr('file.txt', 'content')
            zipf.setpassword(password.encode())

        unzip_local_file_core(self.zip_path, self.target_dir, password=password)
        self.assertTrue(os.path.exists(os.path.join(self.target_dir, 'file.txt')))


class TestUnzipLocalFile(TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.zip_path = os.path.join(self.temp_dir.name, 'test.zip')
        self.target_dir = os.path.join(self.temp_dir.name, 'target')
        with zipfile.ZipFile(self.zip_path, 'w') as zipf:
            zipf.writestr('file.txt', 'content')

    def tearDown(self):
        self.temp_dir.cleanup()

    @patch(
        'llm_web_kit.model.resource_utils.unzip_ext.process_and_verify_file_with_lock'
    )
    def test_unzip(self, mock_process):

        def process_and_verify(
            process_func, verify_func, target_path, lock_suffix, timeout
        ):
            process_func()
            if verify_func():
                return target_path

        mock_process.side_effect = process_and_verify
        result = unzip_local_file(self.zip_path, self.target_dir)
        self.assertEqual(result, self.target_dir)
        self.assertTrue(os.path.exists(os.path.join(self.target_dir, 'file.txt')))
