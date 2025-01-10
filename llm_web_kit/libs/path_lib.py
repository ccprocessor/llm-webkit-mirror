import os


def get_proj_root_dir():
    """获取项目的根目录."""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
