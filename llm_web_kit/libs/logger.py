import sys
import tempfile

from loguru import logger

from llm_web_kit.config.cfg_reader import load_config


def init_logger(config: dict = None):
    """按照配置初始化日志系统."""
    tempfile.gettempdir()
    default_log_format = '{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}'

    logger_cfg = []
    if config:
        logger_cfg = config.get('logger', [])

    if not logger_cfg:
        logger_cfg = load_config(suppress_error=True).get('logger', [])

    if not logger_cfg:
        return logger

    # 如果有关于日志的配置，则按照配置初始化日志系统
    logger.remove()  # 移除默认的日志处理器
    for logger_configs in logger_cfg:
        to = logger_configs.get('to', None)
        if not to:
            continue
        # 检查 to 是否指向控制台
        level = logger_configs.get('log-level', 'INFO')
        log_format = logger_configs.get('log-format', default_log_format)
        enable = logger_configs.get('enable', True)
        if enable:
            if to == 'sys.stdout':
                to = sys.stdout  # 使用 sys.stdout 对象而不是字符串
                logger.add(to, level=level, format=log_format)
                continue
            else:
                rotation = logger_configs.get('rotation', '1 days')
                retention = logger_configs.get('retention', '1 days')

                logger.add(to, rotation=rotation, retention=retention, level=level, format=log_format, enqueue=True)

    return logger


init_logger()

mylogger = logger
