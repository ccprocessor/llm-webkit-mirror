import io
import time

from botocore.exceptions import (IncompleteReadError, ReadTimeoutError,
                                 ResponseStreamingError)
from botocore.response import StreamingBody

from .retry import get_s3_object_with_retry, head_s3_object_with_retry


class _EmptyStream:
    def read(self, n):
        return b''

    def close(self):
        pass


class ResumableS3Stream(io.IOBase):
    def __init__(self, path: str, size_limit=0, client=None):
        self.path = path
        self.size_limit = size_limit
        self.client = client
        self.pos = 0
        self.size = -1
        self.stream = self.new_stream()

    def new_stream(self) -> StreamingBody:
        if self.size < 0 and self.size_limit > 0:
            head = head_s3_object_with_retry(self.path, True, self.client)
            assert head is not None
            if int(head['ContentLength']) <= self.size_limit:
                self.size_limit = 0
                self.size = int(head['ContentLength'])
            else:
                self.size = self.size_limit

        if self.size_limit > 0:
            kwargs = {'Range': f'bytes={self.pos}-{self.size_limit - 1}'}
        else:
            kwargs = {'Range': f'bytes={self.pos}-'} if self.pos > 0 else {}

        obj = get_s3_object_with_retry(self.path, client=self.client, **kwargs)

        if self.size < 0:
            self.size = int(obj['ContentLength'])

        return obj['Body']

    def readable(self):
        return True

    def read(self, n=None):
        if self.pos >= self.size:
            return b''

        retries = 0
        last_e = None
        while True:
            if retries > 5:
                msg = f'Retry exhausted for reading [{self.path}]'
                raise Exception(msg) from last_e
            try:
                data = self.stream.read(n)
                self.pos += len(data)
                return data
            except (ReadTimeoutError, ResponseStreamingError, IncompleteReadError) as e:
                try:
                    self.stream.close()
                except Exception:
                    pass
                last_e = e
                retries += 1
                time.sleep(3)
                self.stream = self.new_stream()

    def seekable(self):
        return True

    def seek(self, offset, whence=io.SEEK_SET):
        if whence == io.SEEK_SET:
            pos = offset
        elif whence == io.SEEK_CUR:
            pos = self.pos + offset
        elif whence == io.SEEK_END:
            pos = self.size + offset
        else:
            raise ValueError('Invalid argument: whence')
        if pos != self.pos:
            self.pos = pos
            try:
                self.stream.close()
            except Exception:
                pass
            if self.pos < self.size:
                self.stream = self.new_stream()
            else:
                self.stream = _EmptyStream()
        return pos

    def tell(self):
        return self.pos

    def close(self):
        self.stream.close()
