import os
import shutil
import tempfile
import zipfile
from typing import Optional

from llm_web_kit.exception.exception import ModelResourceException
from llm_web_kit.libs.logger import mylogger as logger
from llm_web_kit.model.resource_utils.utils import FileLockContext, try_remove


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


def check_zip_file(zip_ref: zipfile.ZipFile, target_dir: str) -> bool:
    """Check if the zip file is correctly unzipped to the target directory.

    Args:
        zip_ref (zipfile.ZipFile): The zip file object.
        target_dir (str): The target directory.

    Returns:
        bool: True if the zip file is correctly unzipped to the target directory, False otherwise.
    """

    zip_info_list = [info for info in zip_ref.infolist() if not info.is_dir()]
    for info in zip_info_list:
        file_path = os.path.join(target_dir, info.filename)
        if not os.path.exists(file_path):
            return False
        if os.path.getsize(file_path) != info.file_size:
            return False
    return True


def unzip_local_file(
    zip_path: str,
    target_dir: str,
    password: Optional[str] = None,
    exist_ok: bool = True,
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
        ModelResourceException: If the zip file does not exist.
        ModelResourceException: If the target directory already exists and exist_ok is False

    Returns:
        str: The path to the target directory.
    """
    lock_path = f'{zip_path}.lock'

    if not os.path.exists(zip_path):
        logger.error(f'zip file {zip_path} does not exist')
        raise ModelResourceException(f'zip file {zip_path} does not exist')

    def check_zip():
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            if password:
                zip_ref.setpassword(password.encode())
            return check_zip_file(zip_ref, target_dir)

    if os.path.exists(target_dir):
        if not exist_ok:
            raise ModelResourceException(
                f'Target directory {target_dir} already exists'
            )

        if check_zip():
            logger.info(f'zip file {zip_path} is already unzipped to {target_dir}')
            return target_dir
        else:
            logger.warning(
                f'zip file {zip_path} is not correctly unzipped to {target_dir}, retry to unzip'
            )
            try_remove(target_dir)

    with FileLockContext(lock_path, check_zip, timeout=lock_timeout) as lock:
        if lock is True:
            logger.info(
                f'zip file {zip_path} is already unzipped to {target_dir} while waiting'
            )
            return target_dir

        # ensure target directory not exists

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
