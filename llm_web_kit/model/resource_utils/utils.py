import os
import shutil

from llm_web_kit.config.cfg_reader import load_config


def decide_cache_dir():
    """Get the cache directory for the web kit. The.

    Returns:
        _type_: _description_
    """
    cache_dir = '~/.llm_web_kit_cache'

    if 'WEB_KIT_CACHE_DIR' in os.environ:
        cache_dir = os.environ['WEB_KIT_CACHE_DIR']

    try:
        config = load_config()
        cache_dir = config['resources']['common']['cache_path']
    except Exception:
        pass

    if cache_dir.startswith('~/'):
        cache_dir = os.path.expanduser(cache_dir)

    cache_tmp_dir = os.path.join(cache_dir, 'tmp')

    return cache_dir, cache_tmp_dir


CACHE_DIR, CACHE_TMP_DIR = decide_cache_dir()


if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR, exist_ok=True)

if not os.path.exists(CACHE_TMP_DIR):
    os.makedirs(CACHE_TMP_DIR, exist_ok=True)


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
