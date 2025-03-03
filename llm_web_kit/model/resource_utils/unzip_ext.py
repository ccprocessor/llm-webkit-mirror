import os
import shutil
import tempfile
import zipfile
from typing import Optional

from llm_web_kit.model.resource_utils.download_assets import FileLock


def get_unzip_dir(zip_path: str) -> str:
    """Get the directory to unzip the zip file to. If the zip file is.

    /path/to/test.zip, the directory will be /path/to/test_unzip.

    Args:
        zip_path (str): The path to the zip file.

    Returns:
        str: The directory to unzip the zip file to.
    """
    zip_dir = os.path.dirname(zip_path)
    base_name = os.path.basename(zip_path).replace('.zip', '')
    return os.path.join(zip_dir, base_name + '_unzip')


def unzip_local_file(
    zip_path: str,
    target_dir: str,
    password: Optional[str] = None,
    exist_ok: bool = False,
    lock_timeout: float = 300,
) -> str:
    """Unzip a zip file to a target directory.

    Args:
        zip_path (str): The path to the zip file.
        target_dir (str): The directory to unzip the files to.
        password (Optional[str], optional): The password to the zip file. Defaults to None.
        exist_ok (bool, optional): If True, overwrite the files in the target directory if it already exists.
                                    If False, raise an exception if the target directory already exists. Defaults to False.

    Raises:
        Exception: If the target directory already exists and exist_ok is False.

    Returns:
        str: The path to the target directory.
    """
    lock_path = f'{zip_path}.lock'
    with FileLock(lock_path, timeout=lock_timeout):

        # ensure target directory not exists
        if os.path.exists(target_dir):
            if exist_ok:
                shutil.rmtree(target_dir)
            else:
                raise Exception(f'Target directory {target_dir} already exists')

        # 创建临时解压目录
        with tempfile.TemporaryDirectory() as temp_dir:
            extract_dir = os.path.join(temp_dir, 'temp')
            os.makedirs(extract_dir, exist_ok=True)

            # 解压到临时目录
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                if password:
                    zip_ref.setpassword(password.encode())
                zip_ref.extractall(extract_dir)

            # 原子性复制到目标目录
            shutil.copytree(extract_dir, target_dir)

    return target_dir
