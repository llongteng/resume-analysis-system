import os
import uuid

from fastapi import APIRouter, UploadFile, File

from app.core.config import get_settings
from app.core.errors import ResourceNotFoundError
from app.core.logging import logger
from app.core.response import success_response
from app.repositories import resume_repository
from app.schemas.resume import ResumeUploadResponse
from app.services import cache_service
from app.services.pdf_parser import extract_text_from_pdf, clean_resume_text
from app.services.resume_extractor import extract_resume_info
from app.utils.file_validator import validate_pdf_file, compute_file_hash

router = APIRouter()


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    """上传 PDF 简历"""
    settings = get_settings()

    # 读取文件内容
    content = await file.read()
    file_size = len(content)
    file_name = file.filename or "unknown.pdf"

    # 校验文件（扩展名、MIME、大小、页数）
    validate_pdf_file(file_name, file_size, content, file.content_type)

    # 计算文件哈希
    file_hash = compute_file_hash(content)

    # 检查是否已存在相同文件
    existing = resume_repository.get_resume_by_hash(file_hash)
    if existing:
        logger.info(f"文件已存在，返回已有记录: {existing['id']}")
        return success_response(
            data=ResumeUploadResponse(
                resume_id=existing["id"],
                file_name=existing["file_name"],
                file_size=existing["file_size"],
                file_hash=existing["file_hash"],
            ).model_dump(),
            message="文件已存在",
        )

    # 保存文件
    upload_dir = os.path.abspath(settings.UPLOAD_DIR)
    os.makedirs(upload_dir, exist_ok=True)
    save_name = f"{uuid.uuid4().hex}_{file_name}"
    file_path = os.path.join(upload_dir, save_name)

    with open(file_path, "wb") as f:
        f.write(content)

    # 创建数据库记录
    result = resume_repository.create_resume(
        file_name=file_name,
        file_path=file_path,
        file_size=file_size,
        file_hash=file_hash,
    )

    return success_response(
        data=ResumeUploadResponse(**result).model_dump(),
        message="上传成功",
    )


@router.post("/{resume_id}/parse")
async def parse_resume(resume_id: str):
    """
    解析简历：PDF 文本提取 + 清洗 + AI 信息提取。

    返回结构化简历信息，包含 basic_info、education、skills 等字段。
    AI 失败时自动降级为正则兜底提取。
    """
    # 查询简历记录
    resume = resume_repository.get_resume_by_id(resume_id)
    if not resume:
        raise ResourceNotFoundError(f"简历不存在: {resume_id}")

    # 检查缓存
    cache_key = f"{cache_service.CACHE_PREFIX_EXTRACT}{resume['file_hash']}"
    cached = cache_service.get_cached(cache_key)
    if cached:
        return success_response(data=cached, message="解析成功（缓存）")

    # Step 1: 提取 PDF 文本
    raw_text, pages = extract_text_from_pdf(resume["file_path"])

    # Step 2: 清洗文本
    cleaned_text = clean_resume_text(raw_text)

    # Step 3: AI 信息提取（失败时自动降级为正则兜底）
    extract_result = extract_resume_info(cleaned_text)

    # 合并结果
    result = {
        "resume_id": resume_id,
        "parse_status": extract_result.get("ai_extract_status", "success"),
        "basic_info": extract_result.get("basic_info", {}),
        "job_intention": extract_result.get("job_intention", {}),
        "education": extract_result.get("education", []),
        "work_experience": extract_result.get("work_experience", []),
        "projects": extract_result.get("projects", []),
        "skills": extract_result.get("skills", {}),
        "summary": extract_result.get("summary", {}),
        "raw_text": raw_text,
        "cleaned_text": cleaned_text,
        "page_count": len(pages),
    }

    # 更新数据库
    resume_repository.update_resume_parse_result(
        resume_id=resume_id,
        raw_text=raw_text,
        cleaned_text=cleaned_text,
        parsed_data=result,
        parse_status=result["parse_status"],
    )

    # 写入缓存
    cache_service.set_cached(cache_key, result)

    return success_response(data=result, message="解析成功")
