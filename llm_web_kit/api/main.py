"""FastAPI 应用主入口.

提供 LLM Web Kit 的 Web API 服务，包括 HTML 解析、内容提取等功能。
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .dependencies import get_inference_service, get_logger, get_settings
from .routers import htmls

settings = get_settings()
logger = get_logger(__name__)


# 创建 FastAPI 应用实例（元数据读取自 Settings）
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(htmls.router, prefix="/api/v1", tags=["HTML 处理"])


@app.get("/")
async def root():
    """根路径，返回服务状态信息."""
    return {
        "message": "LLM Web Kit API 服务运行中",
        "version": settings.api_version,
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """健康检查端点."""
    return {"status": "healthy", "service": "llm-web-kit-api"}


@app.on_event("startup")
async def app_startup():
    """应用启动时预热模型，避免首个请求冷启动延迟."""
    try:
        service = get_inference_service()
        await service.warmup()
        logger.info("InferenceService 模型预热完成")
    except Exception as e:
        logger.warning(f"InferenceService 预热失败（服务仍可运行，将在首次请求时再初始化）: {e}")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局异常处理器."""
    logger.error(f"未处理的异常: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "服务器内部错误", "error": str(exc)}
    )


if __name__ == "__main__":
    # 开发环境运行
    uvicorn.run(
        "llm_web_kit.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level=(settings.log_level or "INFO").lower()
    )
