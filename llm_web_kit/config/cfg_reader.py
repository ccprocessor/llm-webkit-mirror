import os

import commentjson as json
from loguru import logger

from llm_web_kit.exception.exception import ModelResourceException
from llm_web_kit.libs.path_lib import get_py_pkg_root_dir


def load_config(suppress_error: bool = False) -> dict:
    """Load the configuration file for the web kit. First try to read the
    configuration file from the environment variable LLM_WEB_KIT_CFG_PATH. If
    the environment variable is not set, use the default configuration file
    path ~/.llm-web-kit.jsonc. If the configuration file does not exist, raise
    an exception.

    Raises:
        ModelResourceException: LLM_WEB_KIT_CFG_PATH points to a non-exist file
        ModelResourceException: cfg_path does not exist

    Returns:
        config(dict): The configuration dictionary
    """
    # 首先从环境变量LLM_WEB_KIT_CFG_PATH 读取配置文件的位置
    # 如果没有配置，就使用默认的配置文件位置
    # 如果配置文件不存在，就抛出异常
    env_cfg_path = os.getenv('LLM_WEB_KIT_CFG_PATH')
    if env_cfg_path:
        cfg_path = env_cfg_path
        if not os.path.exists(cfg_path):
            if suppress_error:
                return {}

            logger.warning(
                f'environment variable LLM_WEB_KIT_CFG_PATH points to a non-exist file: {cfg_path}'
            )
            raise ModelResourceException(
                f'environment variable LLM_WEB_KIT_CFG_PATH points to a non-exist file: {cfg_path}'
            )
    else:
        cfg_path = os.path.expanduser('~/.llm-web-kit.jsonc')
        if not os.path.exists(cfg_path):
            if suppress_error:
                return {}

            logger.warning(
                f'{cfg_path} does not exist, please create one or set environment variable LLM_WEB_KIT_CFG_PATH to a valid file path'
            )
            raise ModelResourceException(
                f'{cfg_path} does not exist, please create one or set environment variable LLM_WEB_KIT_CFG_PATH to a valid file path'
            )

    # 读取配置文件
    with open(cfg_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    return config


def load_pipe_tpl(pipe_name: str) -> dict:
    """Load the pipe template for the web kit.

    Args:
        pipe_name(str): The name of the pipe to load

    Returns: pipe_tpl(dict): The pipe template dictionary
    """
    pipe_tpl_path = os.path.join(get_py_pkg_root_dir(), 'config', 'pipe_tpl', f'{pipe_name}.jsonc')
    with open(pipe_tpl_path, 'r', encoding='utf-8') as f:
        pipe_tpl = json.load(f)
    return pipe_tpl
