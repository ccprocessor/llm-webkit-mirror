"""请求数据模型.

定义 API 请求的数据结构和验证规则。
"""

from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class HTMLParseRequest(BaseModel):
    """HTML 解析请求模型."""

    html_content: Optional[str] = Field(
        None,
        description="HTML 内容字符串",
        max_length=10485760  # 10MB
    )

    url: Optional[str] = Field(
        None,
        description="url 地址",
        max_length=10485760  # 10MB
    )

    options: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="解析选项配置"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "html_content": "<html><body><h1>Hello World</h1></body></html>",
                "url": "https://helloworld.com/hello",
                "options": {
                    "clean_html": True
                }
            }
        }
    )
