from pydantic import BaseModel, Field


class MatchRequest(BaseModel):
    resume_id: str = Field(..., description="简历 ID")
    job_description: str = Field(..., description="岗位 JD 文本", min_length=1)


class MatchResponse(BaseModel):
    analysis_id: str
    resume_id: str
    job_analysis: dict
    match_result: dict
