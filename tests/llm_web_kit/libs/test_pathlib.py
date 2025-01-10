
import os
import unittest

from llm_web_kit.libs.path_lib import get_proj_root_dir


class TestPathLib(unittest.TestCase):
    def test_get_proj_root_dir(self):
        """Test get_proj_root_dir function."""
        root_proj = get_proj_root_dir()
        # 检查一下这个路径下是否包含如下几个目录或者文件
        expected_dirs = ['tests', 'llm_web_kit', 'docs']
        expected_files = ['.gitignore', 'requirements.txt', 'setup.py']
        for dir in expected_dirs:
            self.assertTrue(os.path.exists(os.path.join(root_proj, dir)))
        for file in expected_files:
            self.assertTrue(os.path.exists(os.path.join(root_proj, file)))
