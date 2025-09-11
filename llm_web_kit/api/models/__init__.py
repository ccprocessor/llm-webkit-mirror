"""Pydantic 模型模块.

包含所有 API 请求和响应的数据模型定义。
"""

from .request import HTMLParseRequest
from .response import ErrorResponse, HTMLParseResponse

__all__ = [
    "HTMLParseRequest",
    "HTMLParseResponse",
    "ErrorResponse"
]
