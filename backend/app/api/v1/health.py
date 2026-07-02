from fastapi import APIRouter

from app.core.response import success_response

router = APIRouter()


@router.get("/health")
async def health_check():
    """健康检查接口"""
    return success_response(data={"status": "healthy"}, message="ok")
