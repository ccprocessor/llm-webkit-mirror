import os
import tempfile
import unittest

from llm_web_kit.dataio.filebase import (FileBasedDataReader,
                                         FileBasedDataWriter)


class TestFileBasedDataReader(unittest.TestCase):
    def setUp(self):
        """设置测试环境."""
        # 创建临时目录作为测试目录
        self.test_dir = tempfile.mkdtemp()
        self.reader = FileBasedDataReader(parent_dir=self.test_dir)

        # 创建测试文件
        self.test_data = b'Hello, World! This is a test file.'
        self.test_file = 'test.txt'
        with open(os.path.join(self.test_dir, self.test_file), 'wb') as f:
            f.write(self.test_data)

    def tearDown(self):
        """清理测试环境."""
        # 删除临时目录及其内容
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_dir)

    def test_read_basic(self):
        """测试基本的读取功能."""
        content = self.reader.read_at(self.test_file)
        self.assertEqual(content, self.test_data)

    def test_read_with_offset(self):
        """测试使用偏移量读取."""
        offset = 7  # 从"World"开始读取
        content = self.reader.read_at(self.test_file, offset=offset)
        self.assertEqual(content, self.test_data[offset:])

    def test_read_with_limit(self):
        """测试使用限制长度读取."""
        limit = 5  # 只读取"Hello"
        content = self.reader.read_at(self.test_file, limit=limit)
        self.assertEqual(content, self.test_data[:limit])

    def test_read_with_offset_and_limit(self):
        """测试同时使用偏移量和限制长度."""
        offset = 7  # 从"World"开始
        limit = 5   # 只读取"World"
        content = self.reader.read_at(self.test_file, offset=offset, limit=limit)
        self.assertEqual(content, self.test_data[offset:offset + limit])

    def test_read_absolute_path(self):
        """测试使用绝对路径读取."""
        abs_path = os.path.join(self.test_dir, self.test_file)
        content = self.reader.read_at(abs_path)
        self.assertEqual(content, self.test_data)

    def test_read_empty_parent_dir(self):
        """测试空父目录的情况."""
        reader = FileBasedDataReader()
        abs_path = os.path.join(self.test_dir, self.test_file)
        content = reader.read_at(abs_path)
        self.assertEqual(content, self.test_data)

    def test_read_with_subdir(self):
        """测试从子目录读取."""
        # 在子目录中创建测试文件
        subdir = 'subdir'
        os.makedirs(os.path.join(self.test_dir, subdir))
        subdir_file = os.path.join(subdir, 'test.txt')
        with open(os.path.join(self.test_dir, subdir_file), 'wb') as f:
            f.write(self.test_data)

        # 读取子目录中的文件
        content = self.reader.read_at(subdir_file)
        self.assertEqual(content, self.test_data)

    def test_read_large_file(self):
        """测试读取大文件."""
        # 创建一个较大的文件（1MB）
        large_data = b'0123456789' * 102400  # 1MB的数据
        large_file = 'large.txt'
        with open(os.path.join(self.test_dir, large_file), 'wb') as f:
            f.write(large_data)

        # 测试不同的读取方式
        # 1. 读取全部内容
        content = self.reader.read_at(large_file)
        self.assertEqual(content, large_data)

        # 2. 读取部分内容
        content = self.reader.read_at(large_file, offset=1024, limit=1024)
        self.assertEqual(content, large_data[1024:2048])


class TestFileBasedDataWriter(unittest.TestCase):
    def setUp(self):
        """设置测试环境."""
        # 创建临时目录作为测试目录
        self.test_dir = tempfile.mkdtemp()
        self.writer = FileBasedDataWriter(parent_dir=self.test_dir)

    def tearDown(self):
        """清理测试环境."""
        # 删除临时目录及其内容
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_dir)

    def test_write_basic(self):
        """测试基本的写入功能."""
        test_data = b'Hello, World!'
        test_file = 'test.txt'

        # 写入数据
        self.writer.write(test_file, test_data)

        # 验证文件内容
        with open(os.path.join(self.test_dir, test_file), 'rb') as f:
            content = f.read()
        self.assertEqual(content, test_data)

    def test_write_with_subdir(self):
        """测试写入到子目录."""
        test_data = b'Test data in subdirectory'
        test_file = 'subdir/test.txt'

        # 写入数据
        self.writer.write(test_file, test_data)

        # 验证文件内容
        with open(os.path.join(self.test_dir, test_file), 'rb') as f:
            content = f.read()
        self.assertEqual(content, test_data)

    def test_append_write(self):
        """测试追加写入功能."""
        initial_data = b'Initial content'
        append_data = b'Appended content'
        test_file = 'append_test.txt'

        # 先写入初始数据
        self.writer.write(test_file, initial_data)

        # 追加数据
        self.writer.append_write(test_file, append_data)

        # 验证文件内容
        with open(os.path.join(self.test_dir, test_file), 'rb') as f:
            content = f.read()
        self.assertEqual(content, initial_data + append_data)

    def test_append_write_new_file(self):
        """测试追加写入到新文件."""
        test_data = b'Append to new file'
        test_file = 'new_append.txt'

        # 追加写入到新文件
        self.writer.append_write(test_file, test_data)

        # 验证文件内容
        with open(os.path.join(self.test_dir, test_file), 'rb') as f:
            content = f.read()
        self.assertEqual(content, test_data)

    def test_absolute_path(self):
        """测试使用绝对路径."""
        test_data = b'Absolute path test'
        test_file = os.path.join(self.test_dir, 'absolute.txt')

        # 使用绝对路径写入
        self.writer.write(test_file, test_data)

        # 验证文件内容
        with open(test_file, 'rb') as f:
            content = f.read()
        self.assertEqual(content, test_data)

    def test_empty_parent_dir(self):
        """测试空父目录的情况."""
        writer = FileBasedDataWriter()
        test_data = b'Empty parent dir test'
        test_file = os.path.join(self.test_dir, 'empty_parent.txt')

        # 写入数据
        writer.write(test_file, test_data)

        # 验证文件内容
        with open(test_file, 'rb') as f:
            content = f.read()
        self.assertEqual(content, test_data)

    def test_multiple_append(self):
        """测试多次追加写入."""
        test_file = 'multiple_append.txt'
        data_parts = [b'Part 1', b'Part 2', b'Part 3']

        # 多次追加写入
        for part in data_parts:
            self.writer.append_write(test_file, part)

        # 验证文件内容
        with open(os.path.join(self.test_dir, test_file), 'rb') as f:
            content = f.read()
        self.assertEqual(content, b''.join(data_parts))


if __name__ == '__main__':
    unittest.main()
