import os
import shutil


def try_remove(path: str):
    """Attempt to remove a file by os.remove or to remove a directory by
    shutil.rmtree and ignore exceptions."""
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    except Exception:
        pass
