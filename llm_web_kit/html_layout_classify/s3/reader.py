"""read config from:

- user config  [specific s3 configs]
- user ~/.aws/ [for ak/sk of s3 clusters]
- default config [same for all users]
"""

import configparser
import json
import os
import re
from pathlib import Path

import yaml

_USER_CONFIG_FILES = [
    '.xinghe.yaml',
    '.xinghe.yml',
    '.code-clean.yaml',
    '.code-clean.yml',
]


def _get_home_dir():
    spark_user = os.environ.get('SPARK_USER')
    if spark_user:
        return os.path.join('/share', spark_user)  # hard code
    return Path.home()


def _read_ini_s3_section(s: str):
    config = {}
    for line in s.split('\n'):
        ml = re.match(r'^\s*([^=\s]+)\s*=\s*(.+?)\s*$', line)
        if ml:
            config[ml.group(1)] = ml.group(2)
    return config


def _read_ini_file(file: str):
    parser = configparser.ConfigParser()
    parser.read(file)
    config = {}
    for name, section in parser.items():
        name = re.sub(r'^\s*profile\s+', '', name)
        name = name.strip().strip('"')
        for key, val in section.items():
            if key == 's3':
                val = _read_ini_s3_section(val)
                config.setdefault(name, {}).update(val)
            else:
                config.setdefault(name, {})[key] = val
    return config


def _merge_config(old: dict, new: dict):
    ret = {}
    for key, old_val in old.items():
        if key not in new:
            ret[key] = old_val
            continue
        new_val = new.pop(key)
        if isinstance(old_val, dict) and isinstance(new_val, dict):
            ret[key] = _merge_config(old_val, new_val)
        else:
            ret[key] = new_val
    for key, new_val in new.items():
        ret[key] = new_val
    return ret


def _read_s3_config():
    home = _get_home_dir()
    conf_file = os.path.join(home, '.aws', 'config')
    cred_file = os.path.join(home, '.aws', 'credentials')
    config = {}
    if os.path.isfile(conf_file):
        config = _read_ini_file(conf_file)
    if os.path.isfile(cred_file):
        config = _merge_config(config, _read_ini_file(cred_file))
    return {'s3': {'profiles': config}}


def _read_user_config():
    home = _get_home_dir()
    for filename in _USER_CONFIG_FILES:
        conf_file = os.path.join(home, filename)
        if os.path.isfile(conf_file):
            break
    else:
        return {}
    with open(conf_file, 'r') as f:
        config = yaml.safe_load(f)
    assert isinstance(config, dict)
    return config


def get_conf_dir():
    conf_dir = os.getenv('XINGHE_CONF_DIR')
    if not conf_dir and os.getenv('BASE_DIR'):
        conf_dir = os.path.join(os.environ['BASE_DIR'], 'conf')
    if not conf_dir:
        raise Exception('XINGHE_CONF_DIR not set.')
    return conf_dir


def _read_default_config():
    conf_file = os.path.join(get_conf_dir(), 'config.yaml')
    if not os.path.isfile(conf_file):
        raise Exception(f'config file [{conf_file}] not found.')
    with open(conf_file, 'r') as f:
        config = yaml.safe_load(f)
    assert isinstance(config, dict)
    return config


def read_config():
    # config = _read_default_config()
    config = {}
    config = _merge_config(config, _read_s3_config())
    config = _merge_config(config, _read_user_config())
    return config


if __name__ == '__main__':
    c = read_config()
    print(json.dumps(c, indent=2))
