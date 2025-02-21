# Copyright (c) Opendatalab. All rights reserved.
"""Common basic operations."""
import ast
import json
from typing import Union

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
