from botocore.exceptions import ClientError

from .client import get_s3_object, head_s3_object, upload_s3_object
from .retry_utils import with_retry


@with_retry
def _get_s3_object_or_ex(path: str, client, **kwargs):
    try:
        return get_s3_object(path, client=client, **kwargs)
    except ClientError as e:
        return e


def get_s3_object_with_retry(path: str, client=None, **kwargs):
    ret = _get_s3_object_or_ex(path, client, **kwargs)
    if isinstance(ret, ClientError):
        raise ret
    return ret


@with_retry
def _head_s3_object_or_ex(path: str, raise_404: bool, client):
    try:
        return head_s3_object(path, raise_404, client=client)
    except ClientError as e:
        return e


def head_s3_object_with_retry(path: str, raise_404=False, client=None):
    ret = _head_s3_object_or_ex(path, raise_404, client)
    if isinstance(ret, ClientError):
        raise ret
    return ret


@with_retry(sleep_time=180)
def upload_s3_object_with_retry(path: str, local_file_path: str, client=None):
    upload_s3_object(path, local_file_path, client=client)
