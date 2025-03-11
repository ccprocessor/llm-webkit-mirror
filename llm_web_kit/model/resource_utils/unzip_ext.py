import os
import tempfile
import zipfile
from functools import partial
from typing import Optional

from llm_web_kit.exception.exception import ModelResourceException
from llm_web_kit.libs.logger import mylogger as logger
from llm_web_kit.model.resource_utils.download_assets import CACHE_TMP_DIR
from llm_web_kit.model.resource_utils.process_with_lock import \
    process_and_verify_file_with_lock


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


def check_zip_path(
    zip_path: str, target_dir: str, password: Optional[str] = None
) -> bool:
    """Check if the zip file is correctly unzipped to the target directory.

    Args:
        zip_path (str): The path to the zip file.
        target_dir (str): The target directory.
        password (Optional[str], optional): The password to the zip file. Defaults to None.

    Returns:
        bool: True if the zip file is correctly unzipped to the target directory, False otherwise.
    """
    if not os.path.exists(zip_path):
        logger.error(f'zip file {zip_path} does not exist')
        return False
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        if password:
            zip_ref.setpassword(password.encode())

        zip_info_list = [info for info in zip_ref.infolist() if not info.is_dir()]
        for info in zip_info_list:
            file_path = os.path.join(target_dir, info.filename)
            if not os.path.exists(file_path):
                return False
            if os.path.getsize(file_path) != info.file_size:
                return False
        return True


def unzip_local_file_core(
    zip_path: str,
    target_dir: str,
    password: Optional[str] = None,
) -> str:
    """Unzip a zip file to a target directory.

    Args:
        zip_path (str): The path to the zip file.
        target_dir (str): The directory to unzip the files to.
        password (Optional[str], optional): The password to the zip file. Defaults to None.

    Raises:
        ModelResourceException: If the zip file does not exist.
        ModelResourceException: If the target directory already exists.

    Returns:
        str: The path to the target directory.
    """
    if not os.path.exists(zip_path):
        logger.error(f'zip file {zip_path} does not exist')
        raise ModelResourceException(f'zip file {zip_path} does not exist')

    if os.path.exists(target_dir):
        raise ModelResourceException(f'Target directory {target_dir} already exists')

    # make sure the parent directory exists
    os.makedirs(os.path.dirname(target_dir), exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        if password:
            zip_ref.setpassword(password.encode())
        with tempfile.TemporaryDirectory(dir=CACHE_TMP_DIR) as temp_dir:
            extract_dir = os.path.join(temp_dir, 'temp')
            os.makedirs(extract_dir, exist_ok=True)
            zip_ref.extractall(extract_dir)
            os.rename(extract_dir, target_dir)
    return target_dir


def unzip_local_file(
    zip_path: str,
    target_dir: str,
    password: Optional[str] = None,
    lock_suffix: str = '.unzip.lock',
    timeout: float = 60,
) -> str:
    """Unzip a zip file to a target directory with a lock.

    Args:
        zip_path (str): The path to the zip file.
        target_dir (str): The directory to unzip the files to.
        password (Optional[str], optional): The password to the zip file. Defaults to None.
        timeout (float, optional): The timeout for the lock. Defaults to 60.

    Returns:
        str: The path to the target directory.
    """
    process_func = partial(unzip_local_file_core, zip_path, target_dir, password)
    verify_func = partial(check_zip_path, zip_path, target_dir, password)
    return process_and_verify_file_with_lock(
        process_func, verify_func, target_dir, lock_suffix, timeout
    )
