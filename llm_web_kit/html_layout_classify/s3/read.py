import io
import re
from typing import Tuple, Union

from botocore.exceptions import ClientError
from botocore.response import StreamingBody

from .client import get_s3_object
from .read_resume import ResumableS3Stream

__re_bytes = re.compile('^([0-9]+)([,-])([0-9]+)$')
__re_bytes_1 = re.compile('^([0-9]+),([0-9]+)$')

SIZE_1M = 1 << 20


def read_s3_object_detailed(
    path: str,
    bytes: Union[str, None] = None,
    client=None,
) -> Tuple[StreamingBody, dict]:
    """
    ### Usage
    ```
    obj = read_object('s3://bkt/path/to/file.txt')
    for line in obj.iter_lines():
      handle(line)
    ```
    """
    kwargs = {}
    if bytes:
        m = __re_bytes.match(bytes)
        if m is not None:
            frm = int(m.group(1))
            to = int(m.group(3))
            sep = m.group(2)
            if sep == ',':
                to = frm + to - 1
            if to >= frm:
                kwargs['Range'] = f'bytes={frm}-{to}'
            elif frm > 0:
                kwargs['Range'] = f'bytes={frm}-'

    obj = get_s3_object(path, client=client, **kwargs)
    return obj.pop('Body'), obj


def read_s3_object_bytes_detailed(path: str, size_limit=0, client=None):
    """This method cache all content in memory, avoid large file."""
    import time

    retries = 0
    last_e = None
    while True:
        if retries > 5:
            msg = f'Retry exhausted for reading [{path}]'
            raise Exception(msg) from last_e
        try:
            stream, obj = read_s3_object_detailed(path, client=client)
            with stream:
                amt = size_limit if size_limit > 0 else None
                buf = stream.read(amt)
            break
        except ClientError:
            raise
        except Exception as e:
            last_e = e
            retries += 1
            time.sleep(3)

    assert isinstance(buf, bytes)
    return buf, obj


def read_s3_object_io_detailed(path: str, size_limit=0, client=None):
    """This method cache all content in memory, avoid large file."""
    import io

    buf, obj = read_s3_object_bytes_detailed(path, size_limit, client=client)
    return io.BytesIO(buf), obj


def read_s3_object_io(path: str, size_limit=0, client=None):
    """This method cache all content in memory, avoid large file."""
    return read_s3_object_io_detailed(path, size_limit, client=client)[0]


def buffered_stream(stream, buffer_size: int, **kwargs):
    from warcio.bufferedreaders import BufferedReader
    return BufferedReader(stream, buffer_size, **kwargs)


def read_records(path: str, stream: io.IOBase, buffer_size: int):
    """do not handle stream.close()"""
    offset = 0

    # if path.endswith('.warc') or path.endswith('.warc.gz'):
    #     from .read_warc import read_warc_records
    #
    #     yield from read_warc_records(path, stream)

    if path.endswith('.gz'):
        r = buffered_stream(stream, buffer_size, decomp_type='gzip')
        while True:
            line = r.readline()
            if not line:
                if r.read_next_member():
                    continue
                break
            tell = stream.tell() - r.rem_length()
            yield (line.decode('utf-8'), offset, tell - offset)
            offset = tell

    elif path.endswith('.bz2'):
        raise Exception('bz2 is not supported yet.')

    # elif path.endswith('.7z'):
    #     from .read_7z import SevenZipReadStream
    #
    #     stream1 = SevenZipReadStream(stream)
    #     stream2 = buffered_stream(stream1, buffer_size)
    #
    #     while True:
    #         line = stream2.readline()
    #         if not line:
    #             break
    #         yield (line.decode('utf-8'), int(-1), int(0))

    else:  # plaintext
        stream1 = stream
        if isinstance(stream, ResumableS3Stream):
            stream1 = buffered_stream(stream, buffer_size)

        while True:
            line = stream1.readline()
            if not line:
                break
            yield (line.decode('utf-8'), offset, len(line))
            offset += len(line)


def read_s3_rows(path: str, use_stream=False, limit=0, size_limit=0, client=None):
    from .row_fallback import Row

    if use_stream:
        stream = ResumableS3Stream(path, size_limit, client=client)
    else:
        stream = read_s3_object_io(path, size_limit, client=client)

    with stream:
        cnt = 0
        for record in read_records(path, stream, SIZE_1M):
            value, offset, length = record

            if offset >= 0:
                loc = f'{path}?bytes={offset},{length}'
            else:
                loc = path

            yield Row(value=value, loc=loc)

            cnt += 1
            if limit > 0 and cnt >= limit:
                break
