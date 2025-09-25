#!/usr/bin/env python3
"""API 服务器启动脚本.

用于启动 LLM Web Kit API 服务。 支持通过命令行参数 `--port` 指定端口号。
"""

import argparse
import os
import sys

import uvicorn

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from llm_web_kit.api.dependencies import get_settings

if __name__ == "__main__":
    settings = get_settings()

    # 创建参数解析器
    parser = argparse.ArgumentParser(description="启动 LLM Web Kit API 服务器。")
    parser.add_argument(
        "--port",
        type=int,
        default=settings.port,
        help=f"指定服务器运行的端口号 (默认: {settings.port}，从配置中读取)。"
    )
    args = parser.parse_args()

    # 使用命令行参数指定的端口或配置中的默认端口
    port_to_use = args.port

    print("启动 LLM Web Kit API 服务器...")
    print(f"服务将运行在: http://{settings.host}:{port_to_use}")
    print(f"API 文档地址: http://{settings.host}:{port_to_use}/docs")
    print(f"ReDoc 文档地址: http://{settings.host}:{port_to_use}/redoc")

    uvicorn.run(
        "llm_web_kit.api.main:app",
        host=settings.host,
        port=port_to_use,
        reload=True,
        log_level=(settings.log_level or "INFO").lower()
    )
