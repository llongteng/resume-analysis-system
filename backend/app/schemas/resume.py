"""
简历相关 Pydantic 模型。

- ResumeUploadResponse: 阶段二上传接口返回值
- BasicInfo ~ ResumeParseData: 阶段三 AI 信息提取结果的结构化模型
"""

from pydantic import BaseModel


class ResumeUploadResponse(BaseModel):
    resume_id: str
    file_name: str
    file_size: int
    file_hash: str


class BasicInfo(BaseModel):
    name: str = ""
    phone: str = ""
    email: str = ""
    address: str = ""


class JobIntention(BaseModel):
    target_position: str = ""
    expected_salary: str = ""
    target_city: str = ""


class Education(BaseModel):
    school: str = ""
    degree: str = ""
    major: str = ""
    start_date: str = ""
    end_date: str = ""


class WorkExperience(BaseModel):
    company: str = ""
    position: str = ""
    start_date: str = ""
    end_date: str = ""
    responsibilities: list[str] = []


class Project(BaseModel):
    project_name: str = ""
    project_time: str = ""
    description: str = ""
    tech_stack: list[str] = []
    role: str = ""
    achievements: list[str] = []


class Skills(BaseModel):
    programming_languages: list[str] = []
    frameworks: list[str] = []
    databases: list[str] = []
    cloud_services: list[str] = []
    ai_tools: list[str] = []
    others: list[str] = []


class Summary(BaseModel):
    candidate_summary: str = ""
    strengths: list[str] = []
    weaknesses: list[str] = []
    suitable_positions: list[str] = []


class ResumeParseData(BaseModel):
    resume_id: str
    parse_status: str
    basic_info: BasicInfo = BasicInfo()
    job_intention: JobIntention = JobIntention()
    education: list[Education] = []
    work_experience: list[WorkExperience] = []
    projects: list[Project] = []
    skills: Skills = Skills()
    summary: Summary = Summary()
    raw_text: str = ""
    cleaned_text: str = ""
