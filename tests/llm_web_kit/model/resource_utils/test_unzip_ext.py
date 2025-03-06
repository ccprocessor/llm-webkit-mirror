import os
import tempfile
import zipfile
from unittest import TestCase

from llm_web_kit.exception.exception import ModelResourceException
from llm_web_kit.model.resource_utils.unzip_ext import (check_zip_file,
                                                        get_unzip_dir,
                                                        unzip_local_file)


def get_assert_dir():
    file_path = os.path.abspath(__file__)
    assert_dir = os.path.join(os.path.dirname(os.path.dirname(file_path)), 'assets')
    return assert_dir


class TestGetUnzipDir(TestCase):

    def test_get_unzip_dir_case1(self):
        assert get_unzip_dir('/path/to/test.zip') == '/path/to/test_unzip'

    def test_get_unzip_dir_case2(self):
        assert get_unzip_dir('/path/to/test') == '/path/to/test_unzip'


class TestCheckZipFile(TestCase):
    # # test_zip/
    # # ├── test1.txt "test1\n"
    # # ├── folder1
    # # │   └── test2.txt "test2\n"
    # # └── folder2

    def get_zipfile(self):
        # 创建一个临时文件夹
        zip_path = os.path.join(get_assert_dir(), 'zip_demo.zip')
        zip_file = zipfile.ZipFile(zip_path, 'r')
        return zip_file

    def test_check_zip_file_cese1(self):
        zip_file = self.get_zipfile()
        # # test_zip/
        # # ├── test1.txt
        # # ├── folder1
        # # │   └── test2.txt
        # # └── folder2

        with tempfile.TemporaryDirectory() as temp_dir:
            root_dir = os.path.join(temp_dir, 'test_zip')
            os.makedirs(os.path.join(root_dir, 'test_zip'))
            os.makedirs(os.path.join(root_dir, 'folder1'))
            os.makedirs(os.path.join(root_dir, 'folder2'))
            with open(os.path.join(root_dir, 'test1.txt'), 'w') as f:
                f.write('test1\n')
            with open(os.path.join(root_dir, 'folder1', 'test2.txt'), 'w') as f:
                f.write('test2\n')

            assert check_zip_file(zip_file, temp_dir) is True

    def test_check_zip_file_cese2(self):
        zip_file = self.get_zipfile()
        with tempfile.TemporaryDirectory() as temp_dir:
            root_dir = os.path.join(temp_dir, 'test_zip')
            os.makedirs(os.path.join(root_dir, 'test_zip'))
            os.makedirs(os.path.join(root_dir, 'folder1'))
            with open(os.path.join(root_dir, 'test1.txt'), 'w') as f:
                f.write('test1\n')
            with open(os.path.join(root_dir, 'folder1', 'test2.txt'), 'w') as f:
                f.write('test2\n')

            assert check_zip_file(zip_file, temp_dir) is True

    def test_check_zip_file_cese3(self):
        zip_file = self.get_zipfile()
        with tempfile.TemporaryDirectory() as temp_dir:
            root_dir = os.path.join(temp_dir, 'test_zip')
            os.makedirs(os.path.join(root_dir, 'test_zip'))
            os.makedirs(os.path.join(root_dir, 'folder1'))
            with open(os.path.join(root_dir, 'folder1', 'test2.txt'), 'w') as f:
                f.write('test2\n')

            assert check_zip_file(zip_file, temp_dir) is False

    def test_check_zip_file_cese4(self):
        zip_file = self.get_zipfile()
        with tempfile.TemporaryDirectory() as temp_dir:
            root_dir = os.path.join(temp_dir, 'test_zip')
            os.makedirs(os.path.join(root_dir, 'test_zip'))
            os.makedirs(os.path.join(root_dir, 'folder1'))
            with open(os.path.join(root_dir, 'test1.txt'), 'w') as f:
                f.write('test1\n')
            with open(os.path.join(root_dir, 'folder1', 'test2.txt'), 'w') as f:
                f.write('test123\n')

            assert check_zip_file(zip_file, temp_dir) is False


def test_unzip_local_file():
    # creat a temp dir to test
    with tempfile.TemporaryDirectory() as temp_dir1, tempfile.TemporaryDirectory() as temp_dir2:
        # test unzip a zip file with 2 txt files
        zip_path = os.path.join(temp_dir1, 'test.zip')
        target_dir = os.path.join(temp_dir2, 'target')
        # zip 2 txt files
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.writestr('test1.txt', 'This is a test file')
            zipf.writestr('test2.txt', 'This is another test file')

        unzip_local_file(zip_path, target_dir)
        with open(os.path.join(target_dir, 'test1.txt')) as f:
            assert f.read() == 'This is a test file'
        with open(os.path.join(target_dir, 'test2.txt')) as f:
            assert f.read() == 'This is another test file'

        unzip_local_file(zip_path, target_dir, exist_ok=True)
        with open(os.path.join(target_dir, 'test1.txt')) as f:
            assert f.read() == 'This is a test file'
        with open(os.path.join(target_dir, 'test2.txt')) as f:
            assert f.read() == 'This is another test file'
        try:
            unzip_local_file(zip_path, target_dir, exist_ok=False)
        except ModelResourceException as e:
            assert e.custom_message == f'Target directory {target_dir} already exists'
