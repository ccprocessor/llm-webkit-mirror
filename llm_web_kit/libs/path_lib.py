import os


def get_proj_root_dir():
    """获取项目的根目录.也就是含有.github, docs, llm_web_kit目录的那个目录."""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_py_pkg_root_dir():
    """获取python包的根目录.也就是含有__init__.py的那个目录.

    Args:
        None
    Returns:
        str: 项目的根目录
    """
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
