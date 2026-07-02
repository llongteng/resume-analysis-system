import json

from fastapi import APIRouter

from app.core.errors import ResourceNotFoundError
from app.core.logging import logger
from app.core.response import success_response
from app.repositories import resume_repository, analysis_repository
from app.schemas.match import MatchRequest, MatchResponse
from app.services import cache_service
from app.services.jd_analyzer import analyze_job_description
from app.services.match_scorer import compute_match

router = APIRouter()


@router.post("")
async def match_resume_to_job(req: MatchRequest):
    """
    简历与岗位匹配评分。

    流程：查询简历 → 分析 JD → 匹配评分 → 保存记录
    """
    # 1. 查询简历
    resume = resume_repository.get_resume_by_id(req.resume_id)
    if not resume:
        raise ResourceNotFoundError(f"简历不存在: {req.resume_id}")

    # 2. 检查简历是否已解析
    if not resume.get("parsed_data"):
        raise ResourceNotFoundError(f"简历尚未解析，请先调用 parse 接口")

    # 3. 解析简历数据
    resume_data = json.loads(resume["parsed_data"]) if isinstance(resume["parsed_data"], str) else resume["parsed_data"]

    # 4. 检查缓存
    jd_hash = cache_service.compute_hash(req.job_description)
    cache_key = f"{cache_service.CACHE_PREFIX_MATCH}{resume['file_hash']}:{jd_hash}"
    cached = cache_service.get_cached(cache_key)
    if cached:
        return success_response(data=cached, message="匹配成功（缓存）")

    # 5. 分析 JD
    jd_analysis = analyze_job_description(req.job_description)
    logger.info(f"JD 分析完成: {jd_analysis.get('job_title', '未知')}")

    # 6. 匹配评分
    match_result = compute_match(resume_data, jd_analysis)

    # 7. 保存分析记录
    record = analysis_repository.create_analysis(
        resume_id=req.resume_id,
        job_description=req.job_description,
        job_analysis=jd_analysis,
        match_result=match_result,
    )

    # 8. 构建返回数据
    result = MatchResponse(
        analysis_id=record["analysis_id"],
        resume_id=req.resume_id,
        job_analysis=jd_analysis,
        match_result=match_result,
    ).model_dump()

    # 9. 写入缓存
    cache_service.set_cached(cache_key, result)

    return success_response(data=result, message="匹配成功")
