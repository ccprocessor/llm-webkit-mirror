#!/usr/bin/env python3
"""API 服务器启动脚本.

用于启动 LLM Web Kit API 服务。
"""

import os
import sys

import uvicorn

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from llm_web_kit.api.dependencies import get_settings

if __name__ == "__main__":
    settings = get_settings()
    print("启动 LLM Web Kit API 服务器...")
    print(f"API 文档地址: http://{settings.host}:{settings.port}/docs")
    print(f"ReDoc 文档地址: http://{settings.host}:{settings.port}/redoc")

    uvicorn.run(
        "llm_web_kit.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level=(settings.log_level or "INFO").lower()
    )
