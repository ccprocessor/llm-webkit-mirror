import os

import commentjson as json


def load_config() -> dict:
    """_summary_

    Args:
        config_file (_type_): _description_

    Returns:
        _type_: _description_
    """
    # 首先从环境变量LLM_WEB_KIT_CFG_PATH 读取配置文件的位置
    # 如果没有配置，就使用默认的配置文件位置
    # 如果配置文件不存在，就抛出异常
    env_cfg_path = os.getenv('LLM_WEB_KIT_CFG_PATH')
    if env_cfg_path:
        cfg_path = env_cfg_path
        if not os.path.exists(cfg_path):
            raise FileNotFoundError(f'environment variable LLM_WEB_KIT_CFG_PATH points to a non-exist file: {cfg_path}')
    else:
        cfg_path = os.path.expanduser('~/.llm-web-kit.jsonc')
        if not os.path.exists(cfg_path):
            raise FileNotFoundError(
                f'{cfg_path} does not exist, please create one or set environment variable LLM_WEB_KIT_CFG_PATH to a valid file path')

    # 读取配置文件
    with open(cfg_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    return config
