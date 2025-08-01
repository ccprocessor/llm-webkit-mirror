# Copyright (c) Opendatalab. All rights reserved.
"""Common basic operations."""
import ast
import base64
import json
import zlib
from typing import Union

from llm_web_kit.exception.exception import LlmWebKitBaseException

try:
    import orjson
except ModuleNotFoundError:
    orjson = None


def json_loads(s: Union[str, bytes], **kwargs) -> dict:
    """
    The function is designed to deserialize a JSON-formatted string or bytes object into a Python dictionary.
    Args:
        s: The JSON-formatted string or bytes object to be deserialized.
        **kwargs: Additional keyword arguments that can be passed to the json.loads method.

    Returns: dict: A Python dictionary representing the deserialized JSON data.

    """
    if not kwargs and orjson:
        try:
            return orjson.loads(s)
        except AttributeError:
            pass
        except orjson.JSONDecodeError:
            pass
    try:
        return json.loads(s, **kwargs)
    except Exception as e:
        if 'enclosed in double quotes' not in str(e):
            raise e
        if isinstance(s, bytes):
            s = s.decode('utf-8')
        else:
            s = str(s)
        return ast.literal_eval(s)


def json_dumps(d: dict, **kwargs) -> str:
    """
    The json_dumps function is designed to serialize a Python dictionary into a JSON-formatted string.
    Args:
        d: The Python dictionary to be serialized into a JSON string.
        **kwargs: Additional keyword arguments that can be passed to the json.dumps method.

    Returns: str: A JSON string representing the serialized JSON data.

    """
    if not kwargs and orjson:
        try:
            return orjson.dumps(d).decode('utf-8')
        except AttributeError:
            pass
    return json.dumps(d, ensure_ascii=False, **kwargs)


def compress_and_decompress_str(input_data: Union[str, bytes], compress: bool = True, base: bool = False) -> Union[
    str, bytes]:
    """
    压缩解压缩
    Args:
        input_data: The input data to be compressed or compressed base64 str or decompressed.
        compress: default compress, Whether to compress or decompress the input data.
        base: default not base, whether to compress or decompress the input data as base64.
    Returns:
        The compressed and decompressed data.
    """
    try:
        if compress:
            # 确保输入是字节串
            if isinstance(input_data, str):
                input_bytes = input_data.encode('utf-8')
            elif isinstance(input_data, bytes):
                input_bytes = input_data
            else:
                raise LlmWebKitBaseException('Input must be a string or bytes object.')

            if base:
                # 压缩并转换为Base64字符串
                compressed_bytes = zlib.compress(input_bytes)
                return base64.b64encode(compressed_bytes).decode('utf-8')
            else:
                return zlib.compress(input_bytes)

        else:
            # 解码Base64字符串并解压缩
            if isinstance(input_data, str):
                compressed_bytes = base64.b64decode(input_data)
            elif isinstance(input_data, bytearray):
                compressed_bytes = bytes(input_data)
            elif isinstance(input_data, bytes):
                compressed_bytes = input_data
            else:
                raise LlmWebKitBaseException('Input must be a Base64 encoded string or bytes object.')

            decompressed_bytes = zlib.decompress(compressed_bytes)
            return decompressed_bytes.decode('utf-8')  # 假设原始数据是UTF-8编码的字符串

    except (zlib.error, base64.binascii.Error, UnicodeDecodeError) as e:
        raise LlmWebKitBaseException(f'Error during compression/decompression: {e}')
