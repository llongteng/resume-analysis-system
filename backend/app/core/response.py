import time
import uuid

from fastapi.responses import JSONResponse

from app.core.errors import ErrorCode


def success_response(data=None, message: str = "操作成功", code: str = "SUCCESS") -> dict:
    """构建成功响应字典"""
    return {
        "success": True,
        "code": code,
        "message": message,
        "data": data,
        "request_id": f"req_{uuid.uuid4().hex[:12]}",
        "timestamp": int(time.time()),
    }


def error_response(
    code: ErrorCode,
    message: str | None = None,
    data=None,
    status_code: int = 400,
) -> JSONResponse:
    """构建错误 JSONResponse"""
    from app.core.errors import ERROR_MESSAGES

    content = {
        "success": False,
        "code": code.value,
        "message": message or ERROR_MESSAGES.get(code, "未知错误"),
        "data": data,
        "request_id": f"req_{uuid.uuid4().hex[:12]}",
        "timestamp": int(time.time()),
    }
    return JSONResponse(content=content, status_code=status_code)
