import re

from app.core.logging import logger
from app.services.ai_client import call_ai_json

JD_ANALYZE_SYSTEM_PROMPT = """你是一个专业的岗位需求分析助手。请从岗位描述中提取结构化信息，严格输出 JSON，不得输出任何其他内容。

要求：
1. 必须输出严格 JSON，不得输出 Markdown
2. 不确定的字段返回空字符串或空数组
3. 不得编造 JD 中不存在的信息

JSON 结构如下：
{
  "job_title": "岗位名称",
  "required_skills": ["必备技能1", "必备技能2"],
  "bonus_skills": ["加分技能1", "加分技能2"],
  "experience_requirements": "工作年限要求",
  "education_requirements": "学历要求",
  "responsibilities": ["职责1", "职责2"],
  "keywords": ["关键词1", "关键词2"]
}"""

# 常见技能关键词（与 resume_extractor 共用）
SKILL_KEYWORDS = [
    "Python", "Java", "JavaScript", "TypeScript", "Go", "Golang", "C++", "C#", "Rust", "PHP",
    "React", "Vue", "Angular", "Next.js", "Nuxt", "FastAPI", "Flask", "Django", "Spring",
    "Express", "Node.js", "NestJS", "Gin", "Fiber",
    "MySQL", "PostgreSQL", "MongoDB", "Redis", "Elasticsearch", "SQLite", "Oracle", "SQL Server",
    "Docker", "Kubernetes", "K8s", "Jenkins", "CI/CD", "GitHub Actions",
    "AWS", "Azure", "GCP", "阿里云", "腾讯云", "华为云", "Serverless", "函数计算",
    "Linux", "Nginx", "Git", "GraphQL", "REST", "gRPC", "Kafka", "RabbitMQ",
    "TensorFlow", "PyTorch", "大语言模型", "LLM", "NLP", "机器学习", "深度学习", "AI",
    "HTML", "CSS", "Tailwind", "Webpack", "Vite",
]


def analyze_job_description(job_description: str) -> dict:
    """
    分析岗位 JD，提取结构化信息。

    Args:
        job_description: 岗位描述文本

    Returns:
        结构化岗位信息 dict
    """
    try:
        result = call_ai_json(
            JD_ANALYZE_SYSTEM_PROMPT,
            f"请从以下岗位描述中提取结构化信息：\n\n{job_description}",
        )
        logger.info(f"JD 分析成功: {result.get('job_title', '未知')}")
        return result
    except Exception as e:
        logger.warning(f"JD AI 分析失败，使用基础提取: {e}")
        return fallback_analyze_jd(job_description)


def fallback_analyze_jd(job_description: str) -> dict:
    """JD 分析失败时的基础兜底：提取技能关键词和岗位名称"""
    # 提取技能关键词
    found_skills = []
    text_lower = job_description.lower()
    for skill in SKILL_KEYWORDS:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    # 尝试提取岗位名称（常见模式：招聘 XXX 工程师/开发/设计师）
    job_title = ""
    title_match = re.search(r'(?:招聘|诚聘|招)[\s]*([一-龥a-zA-Z]+(?:工程师|开发|设计师|架构师|运维|测试|产品|运营))', job_description)
    if title_match:
        job_title = title_match.group(1)

    # 尝试提取经验要求
    exp_match = re.search(r'(\d+[-~]\d+\s*年|[\d]+\s*年以上)', job_description)
    experience = exp_match.group(1) if exp_match else ""

    # 尝试提取学历要求
    edu_match = re.search(r'(本科|硕士|博士|大专|专科)及以上', job_description)
    education = edu_match.group(0) if edu_match else ""

    return {
        "job_title": job_title,
        "required_skills": found_skills,
        "bonus_skills": [],
        "experience_requirements": experience,
        "education_requirements": education,
        "responsibilities": [],
        "keywords": found_skills,
    }
