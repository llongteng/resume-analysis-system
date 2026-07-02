import json
import uuid

from app.models.database import get_db_connection
from app.core.logging import logger


def create_resume(
    file_name: str,
    file_path: str,
    file_size: int,
    file_hash: str,
) -> dict:
    """创建简历记录"""
    resume_id = f"res_{uuid.uuid4().hex[:12]}"
    with get_db_connection() as conn:
        conn.execute(
            """
            INSERT INTO resumes (id, file_name, file_path, file_size, file_hash, parse_status)
            VALUES (?, ?, ?, ?, ?, 'pending')
            """,
            (resume_id, file_name, file_path, file_size, file_hash),
        )
    logger.info(f"简历记录已创建: {resume_id}")
    return {
        "resume_id": resume_id,
        "file_name": file_name,
        "file_size": file_size,
        "file_hash": file_hash,
    }


def get_resume_by_id(resume_id: str) -> dict | None:
    """根据 ID 查询简历记录"""
    with get_db_connection() as conn:
        row = conn.execute(
            "SELECT * FROM resumes WHERE id = ?", (resume_id,)
        ).fetchone()
        if row:
            return dict(row)
    return None


def get_resume_by_hash(file_hash: str) -> dict | None:
    """根据文件哈希查询简历记录"""
    with get_db_connection() as conn:
        row = conn.execute(
            "SELECT * FROM resumes WHERE file_hash = ?", (file_hash,)
        ).fetchone()
        if row:
            return dict(row)
    return None


def update_resume_parse_result(
    resume_id: str,
    raw_text: str,
    cleaned_text: str,
    parsed_data: dict,
    parse_status: str = "success",
):
    """更新简历解析结果"""
    with get_db_connection() as conn:
        conn.execute(
            """
            UPDATE resumes
            SET raw_text = ?, cleaned_text = ?, parsed_data = ?, parse_status = ?,
                updated_at = datetime('now', 'localtime')
            WHERE id = ?
            """,
            (raw_text, cleaned_text, json.dumps(parsed_data, ensure_ascii=False), parse_status, resume_id),
        )
    logger.info(f"简历解析结果已更新: {resume_id}, status={parse_status}")


def update_resume_parse_status(resume_id: str, status: str):
    """更新简历解析状态"""
    with get_db_connection() as conn:
        conn.execute(
            "UPDATE resumes SET parse_status = ?, updated_at = datetime('now', 'localtime') WHERE id = ?",
            (status, resume_id),
        )
