import json
import uuid

from app.models.database import get_db_connection
from app.core.logging import logger


def create_analysis(
    resume_id: str,
    job_description: str,
    job_analysis: dict,
    match_result: dict,
) -> dict:
    """创建分析记录"""
    analysis_id = f"ana_{uuid.uuid4().hex[:12]}"
    match_score = match_result.get("match_score", 0)

    with get_db_connection() as conn:
        conn.execute(
            """
            INSERT INTO analysis_records (id, resume_id, job_description, job_analysis, match_result, match_score)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                analysis_id,
                resume_id,
                job_description,
                json.dumps(job_analysis, ensure_ascii=False),
                json.dumps(match_result, ensure_ascii=False),
                match_score,
            ),
        )
    logger.info(f"分析记录已创建: {analysis_id}, score={match_score}")
    return {
        "analysis_id": analysis_id,
        "resume_id": resume_id,
        "match_score": match_score,
    }


def get_analysis_by_id(analysis_id: str) -> dict | None:
    """根据 ID 查询分析记录（含简历解析数据）"""
    with get_db_connection() as conn:
        row = conn.execute(
            """
            SELECT ar.*, r.parsed_data as resume_parsed_data
            FROM analysis_records ar
            LEFT JOIN resumes r ON ar.resume_id = r.id
            WHERE ar.id = ?
            """,
            (analysis_id,),
        ).fetchone()
        if row:
            record = dict(row)
            # 解析 JSON 字段
            if record.get("job_analysis"):
                record["job_analysis"] = json.loads(record["job_analysis"])
            if record.get("match_result"):
                record["match_result"] = json.loads(record["match_result"])
            # 解析简历数据
            if record.get("resume_parsed_data"):
                record["resume_data"] = json.loads(record["resume_parsed_data"])
            record.pop("resume_parsed_data", None)
            return record
    return None


def get_analysis_history(limit: int = 20, offset: int = 0) -> list[dict]:
    """获取分析历史记录（含候选人姓名，支持分页）"""
    with get_db_connection() as conn:
        rows = conn.execute(
            """
            SELECT ar.id, ar.resume_id, r.file_name,
                   COALESCE(json_extract(r.parsed_data, '$.basic_info.name'), '') as candidate_name,
                   COALESCE(json_extract(ar.job_analysis, '$.job_title'), '') as job_title,
                   ar.match_score, ar.created_at,
                   COALESCE(json_extract(ar.match_result, '$.score_level'), '') as score_level
            FROM analysis_records ar
            LEFT JOIN resumes r ON ar.resume_id = r.id
            ORDER BY ar.created_at DESC
            LIMIT ? OFFSET ?
            """,
            (limit, offset),
        ).fetchall()
        return [dict(row) for row in rows]
