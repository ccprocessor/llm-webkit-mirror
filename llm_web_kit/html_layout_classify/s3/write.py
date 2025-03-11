import bz2
import gzip
import io
import os
import uuid

from .cmd import json_encode
from .const import FIELD_ID
from .retry import upload_s3_object_with_retry

_compressions = {
    'gz': 'gz',
    'gzip': 'gz',
    'bz2': 'bz2',
    'bzip': 'bz2',
    'bzip2': 'bz2',
    'raw': 'raw',
    'none': 'raw',
}


def s3_upload_tmp_dir():
    tmp_dir = '/tmp/s3_upload'
    try:
        os.makedirs(tmp_dir, exist_ok=True)
        test_file = os.path.join(tmp_dir, '__test_file')
        try:
            open(test_file, 'a').close()
        finally:
            try:
                os.remove(test_file)
            except Exception:
                pass
    except Exception:
        tmp_dir = os.path.join('/tmp', 's3_upload')
        os.makedirs(tmp_dir, exist_ok=True)
    return tmp_dir


class S3DocWriter:
    def __init__(
        self,
        path: str,
        client=None,
        tmp_dir=None,
        skip_loc=False,
        compression='',
    ) -> None:
        if not path.startswith('s3://'):
            raise Exception(f'invalid s3 path [{path}].')

        compression = _compressions.get(compression)
        if compression and not path.endswith(f'.{compression}'):
            raise Exception(f'path must endswith [.{compression}]')
        if not compression and path.endswith('.gz'):
            compression = 'gz'
        if not compression and path.endswith('.bz2'):
            compression = 'bz2'

        self.path = path
        self.client = client
        self.skip_loc = skip_loc
        self.compression = compression

        if not tmp_dir:
            tmp_dir = s3_upload_tmp_dir()
        os.makedirs(tmp_dir, exist_ok=True)

        ext = self.__get_ext(path)
        self.tmp_file = os.path.join(tmp_dir, f'{str(uuid.uuid4())}.{ext}')
        self.tmp_fh = open(self.tmp_file, 'ab')
        self.offset = 0

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.flush()

    @staticmethod
    def __get_ext(path: str):
        filename = os.path.basename(path)
        parts = filename.split('.')
        if len(parts) > 1 and parts[0]:
            return parts[-1]
        return 'txt'

    def write(self, d: dict):
        d = d.copy()

        if not self.skip_loc and 'doc_loc' in d:
            track_loc = d.get('track_loc') or []
            track_loc.append(d['doc_loc'])
            d['track_loc'] = track_loc

        if self.compression == 'gz':
            if not self.skip_loc and FIELD_ID in d:
                d['doc_loc'] = f'{self.path}?bytes={self.offset},0'
            buf = io.BytesIO()
            with gzip.GzipFile(fileobj=buf, mode='wb') as f:
                f.write(json_encode(d))
            doc_bytes = buf.getvalue()

        elif self.compression == 'bz2':
            if not self.skip_loc and FIELD_ID in d:
                d['doc_loc'] = f'{self.path}?bytes={self.offset},0'
            buf = io.BytesIO()
            with bz2.BZ2File(buf, mode='wb') as f:
                f.write(json_encode(d))
            doc_bytes = buf.getvalue()

        else:
            doc_bytes = json_encode(d)

            # add doc_loc if doc has id
            if not self.skip_loc and FIELD_ID in d:
                doc_len, last_len = len(doc_bytes), 0
                while doc_len != last_len:
                    d['doc_loc'] = f'{self.path}?bytes={self.offset},{doc_len}'
                    doc_bytes = json_encode(d)
                    doc_len, last_len = len(doc_bytes), doc_len

        self.tmp_fh.write(doc_bytes)
        self.offset += len(doc_bytes)

        return len(doc_bytes)

    def flush(self):
        try:
            self.tmp_fh.close()
            upload_s3_object_with_retry(self.path, self.tmp_file, self.client)
        finally:
            try:
                os.remove(self.tmp_file)
            except Exception:
                pass
