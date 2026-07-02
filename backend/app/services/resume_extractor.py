import re

from app.core.logging import logger
from app.services.ai_client import call_ai_json

# ============================================================
# AI 提取 Prompt
# ============================================================

RESUME_EXTRACT_SYSTEM_PROMPT = """你是一个专业的简历信息提取助手。请从简历文本中提取结构化信息，严格输出 JSON，不得输出任何其他内容。

要求：
1. 必须输出严格 JSON，不得输出 Markdown
2. 不确定的字段返回空字符串或空数组
3. 不得编造简历中不存在的信息
4. 保留候选人的关键信息

JSON 结构如下：
{
  "basic_info": {
    "name": "姓名",
    "phone": "手机号",
    "email": "邮箱",
    "address": "地址/所在城市"
  },
  "job_intention": {
    "target_position": "求职意向",
    "expected_salary": "期望薪资",
    "target_city": "目标城市"
  },
  "education": [
    {
      "school": "学校",
      "degree": "学历",
      "major": "专业",
      "start_date": "开始时间",
      "end_date": "结束时间"
    }
  ],
  "work_experience": [
    {
      "company": "公司名称",
      "position": "岗位名称",
      "start_date": "开始时间",
      "end_date": "结束时间",
      "responsibilities": ["职责1", "职责2"]
    }
  ],
  "projects": [
    {
      "project_name": "项目名称",
      "project_time": "项目时间",
      "description": "项目描述",
      "tech_stack": ["技术1", "技术2"],
      "role": "个人职责",
      "achievements": ["成果1", "成果2"]
    }
  ],
  "skills": {
    "programming_languages": ["Python", "JavaScript"],
    "frameworks": ["FastAPI", "React"],
    "databases": ["MySQL", "Redis"],
    "cloud_services": ["阿里云"],
    "ai_tools": ["大语言模型"],
    "others": ["Git", "Docker"]
  },
  "summary": {
    "candidate_summary": "候选人简介",
    "strengths": ["优势1", "优势2"],
    "weaknesses": ["不足1"],
    "suitable_positions": ["适合岗位1"]
  }
}"""


def extract_resume_info(cleaned_text: str) -> dict:
    """
    从简历文本中提取结构化信息。

    优先使用 AI 提取，失败时降级为正则兜底。

    Args:
        cleaned_text: 清洗后的简历文本

    Returns:
        结构化简历信息 dict
    """
    try:
        result = call_ai_json(
            RESUME_EXTRACT_SYSTEM_PROMPT,
            f"请从以下简历文本中提取结构化信息：\n\n{cleaned_text}",
        )
        result["ai_extract_status"] = "success"
        logger.info("AI 简历提取成功")
        return result
    except Exception as e:
        logger.warning(f"AI 简历提取失败，降级为正则兜底: {e}")
        return fallback_extract(cleaned_text)


# ============================================================
# 正则兜底提取
# ============================================================

# 中国大陆手机号
PHONE_PATTERN = re.compile(r'1[3-9]\d{9}')
# 邮箱
EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
# 学历关键词
DEGREE_KEYWORDS = ["博士", "硕士", "研究生", "本科", "学士", "大专", "专科", "高中", "MBA", "EMBA"]
# 常见技能关键词
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


def fallback_extract(cleaned_text: str) -> dict:
    """正则兜底提取基础字段"""
    # 手机号
    phone_match = PHONE_PATTERN.search(cleaned_text)
    phone = phone_match.group() if phone_match else ""

    # 邮箱
    email_match = EMAIL_PATTERN.search(cleaned_text)
    email = email_match.group() if email_match else ""

    # 姓名（从简历开头几行推断）
    name = _guess_name(cleaned_text)

    # 学历
    degrees = []
    for kw in DEGREE_KEYWORDS:
        if kw in cleaned_text:
            degrees.append(kw)

    # 技能关键词
    found_skills = []
    text_lower = cleaned_text.lower()
    for skill in SKILL_KEYWORDS:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    return {
        "basic_info": {
            "name": name,
            "phone": phone,
            "email": email,
            "address": "",
        },
        "job_intention": {
            "target_position": "",
            "expected_salary": "",
            "target_city": "",
        },
        "education": [],
        "work_experience": [],
        "projects": [],
        "skills": {
            "programming_languages": [],
            "frameworks": [],
            "databases": [],
            "cloud_services": [],
            "ai_tools": [],
            "others": found_skills,
        },
        "summary": {
            "candidate_summary": "",
            "strengths": [],
            "weaknesses": [],
            "suitable_positions": [],
        },
        "ai_extract_status": "fallback",
    }


def _guess_name(text: str) -> str:
    """从简历开头几行推断姓名"""
    # 常见非姓名短词（排除误判）
    EXCLUDE_WORDS = {
        "个人简介", "自我评价", "求职意向", "教育背景", "工作经历", "项目经历",
        "基本信息", "联系方式", "专业技能", "技术栈", "个人优势", "获奖情况",
        "实习经历", "培训经历", "证书资质", "兴趣爱好", "个人总结", "自我介绍",
        "个人信息", "候选人", "求职者", "简历", "详情", "简介",
    }

    lines = text.strip().split("\n")[:5]
    for line in lines:
        line = line.strip()
        # 跳过空行、过长行、包含数字/特殊字符的行
        if not line or len(line) > 10 or re.search(r'[\d@.:/]', line):
            continue
        # 去除常见前缀
        for prefix in ["姓名", "名字", "Name", "name"]:
            if line.startswith(prefix):
                line = line[len(prefix):].strip().lstrip("：:").strip()
        # 中文姓名通常 2-4 个字，排除常见非姓名词
        if re.match(r'^[一-龥]{2,4}$', line) and line not in EXCLUDE_WORDS:
            return line
    return ""
