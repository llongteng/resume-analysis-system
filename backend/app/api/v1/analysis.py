from fastapi import APIRouter, Query

from app.core.errors import ResourceNotFoundError
from app.core.response import success_response
from app.repositories import analysis_repository

router = APIRouter()


@router.get("/history")
async def get_history(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
):
    """获取分析历史记录（分页）"""
    offset = (page - 1) * page_size
    items = analysis_repository.get_analysis_history(limit=page_size, offset=offset)
    return success_response(data=items, message="查询成功")


@router.get("/{analysis_id}")
async def get_analysis(analysis_id: str):
    """查询指定分析记录的完整结果"""
    # analysis_id 格式为 ana_xxx，不会与 "history" 冲突
    record = analysis_repository.get_analysis_by_id(analysis_id)
    if not record:
        raise ResourceNotFoundError(f"分析记录不存在: {analysis_id}")
    return success_response(data=record, message="查询成功")
