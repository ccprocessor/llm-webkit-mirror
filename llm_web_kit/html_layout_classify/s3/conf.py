import fnmatch
import random
import socket
from typing import List, Union

from .config import s3_bucket_prefixes, s3_buckets, s3_profiles
from .path import split_s3_path


def _is_inside_cluster(cluster_config: dict):
    inside_hosts = cluster_config.get('inside_hosts')
    if not (isinstance(inside_hosts, list) and inside_hosts):
        return False
    inside_hosts = [str(pat).lower() for pat in inside_hosts]
    try:
        host = socket.gethostname().lower()
    except Exception:
        return False
    for host_pattern in inside_hosts:
        if fnmatch.fnmatch(host, host_pattern):
            return True
    return False


def _get_s3_bucket_config(path: str):
    bucket = split_s3_path(path)[0] if path else ''
    bucket_config = s3_buckets.get(bucket)
    if not bucket_config:
        for prefix, c in s3_bucket_prefixes.items():
            if bucket.startswith(prefix):
                bucket_config = c
                break
    if not bucket_config:
        bucket_config = s3_profiles.get(bucket)
    if not bucket_config:
        bucket_config = s3_buckets.get('[default]')
        assert bucket_config is not None
    return bucket_config


def _get_s3_config(
    bucket_config,
    outside: bool,
    prefer_ip=False,
    prefer_auto=False,
):
    cluster = bucket_config['cluster']
    assert isinstance(cluster, dict)

    if outside:
        endpoint_key = 'outside'
    elif prefer_auto:
        endpoint_key = 'auto'
    elif _is_inside_cluster(cluster):
        endpoint_key = 'inside'
    else:
        endpoint_key = 'outside'

    if endpoint_key not in cluster:
        endpoint_key = 'outside'

    if prefer_ip and f'{endpoint_key}_ips' in cluster:
        endpoint_key = f'{endpoint_key}_ips'

    endpoints = cluster[endpoint_key]

    if isinstance(endpoints, str):
        endpoint = endpoints
    elif isinstance(endpoints, list):
        endpoint = random.choice(endpoints)
    else:
        raise Exception(f'invalid endpoint for [{cluster}]')

    return {
        'endpoint': endpoint,
        'ak': bucket_config['ak'],
        'sk': bucket_config['sk'],
    }


def get_s3_config(path: Union[str, List[str]], outside=False):
    paths = [path] if type(path) == str else path
    bucket_config = None
    for p in paths:
        bc = _get_s3_bucket_config(p)
        if bucket_config in [bc, None]:
            bucket_config = bc
            continue
        raise Exception(f'{paths} have different s3 config, cannot read together.')
    if not bucket_config:
        raise Exception('path is empty.')
    return _get_s3_config(bucket_config, outside, prefer_ip=True)
