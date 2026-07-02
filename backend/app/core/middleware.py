import time
import uuid

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import logger


def setup_middleware(app: FastAPI, cors_origins: list[str], cors_origin_regex: str | None = None):
    """注册所有中间件"""

    # CORS
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_origin_regex=cors_origin_regex,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Request ID + 请求日志
    app.add_middleware(RequestLogMiddleware)


class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 生成 request_id
        request_id = request.headers.get("X-Request-ID", f"req_{uuid.uuid4().hex[:12]}")
        request.state.request_id = request_id

        # 记录请求开始
        start_time = time.time()
        logger.info(
            f"[{request_id}] => {request.method} {request.url.path}"
        )

        # 执行请求
        response = await call_next(request)

        # 记录请求结束
        duration = round((time.time() - start_time) * 1000, 2)
        logger.info(
            f"[{request_id}] <= {response.status_code} ({duration}ms)"
        )

        response.headers["X-Request-ID"] = request_id
        return response
