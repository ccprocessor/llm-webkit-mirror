import os
import tempfile
import zipfile

from llm_web_kit.model.resource_utils.unzip_ext import (get_unzip_dir,
                                                        unzip_local_file)


def test_get_unzip_dir():
    assert get_unzip_dir('/path/to/test.zip') == '/path/to/test_unzip'
    assert get_unzip_dir('/path/to/test') == '/path/to/test_unzip'


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
        except Exception as e:
            assert str(e) == f'Target directory {target_dir} already exists'
