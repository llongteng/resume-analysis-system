from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.api.v1.routes import api_router
from app.core.config import get_settings
from app.core.errors import BusinessError, ErrorCode
from app.core.logging import logger
from app.core.middleware import setup_middleware
from app.core.response import error_response
from app.models.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化数据库
    init_db()
    logger.info("数据库初始化完成")
    yield
    # 关闭时清理资源
    logger.info("应用关闭")


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        description="AI 智能简历分析与岗位匹配系统",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # 注册中间件
    setup_middleware(app, settings.cors_origins_list, settings.cors_origin_regex)

    # 注册路由
    app.include_router(api_router, prefix=settings.API_PREFIX)

    # 全局业务异常处理
    @app.exception_handler(BusinessError)
    async def business_error_handler(request: Request, exc: BusinessError):
        logger.warning(f"BusinessError: {exc.code.value} - {exc.message}")
        return error_response(code=exc.code, message=exc.message)

    # 全局未知异常处理
    @app.exception_handler(Exception)
    async def global_error_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {type(exc).__name__}: {exc}", exc_info=True)
        return error_response(
            code=ErrorCode.INTERNAL_ERROR,
            status_code=500,
        )

    return app


app = create_app()
