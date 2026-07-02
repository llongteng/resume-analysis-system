import re

from app.core.logging import logger
from app.services.ai_client import call_ai_json

# 评分权重
WEIGHTS = {
    "skill_match": 0.40,
    "project_match": 0.25,
    "experience_match": 0.20,
    "keyword_coverage": 0.15,
}

MATCH_SYSTEM_PROMPT = """你是一个专业的简历与岗位匹配评估助手。请根据候选人简历信息和岗位 JD，进行综合匹配评估，严格输出 JSON。

要求：
1. 必须输出严格 JSON，不得输出 Markdown
2. 评分范围 0-100
3. 风险点必须具体，不能空泛
4. 面试追问建议必须针对候选人的具体经历
5. 不得只给主观评价，必须结合 JD 要求说明原因

JSON 结构如下：
{
  "match_score": 86,
  "score_level": "high",
  "score_items": {
    "skill_match": {"score": 88, "weight": 0.4, "reason": "评分理由"},
    "project_match": {"score": 82, "weight": 0.25, "reason": "评分理由"},
    "experience_match": {"score": 80, "weight": 0.2, "reason": "评分理由"},
    "keyword_coverage": {"score": 90, "weight": 0.15, "reason": "评分理由"}
  },
  "matched_keywords": ["关键词1", "关键词2"],
  "missing_keywords": ["缺失关键词1"],
  "risk_points": ["风险点1", "风险点2"],
  "interview_questions": ["追问建议1", "追问建议2"],
  "ai_summary": "综合评价"
}

评分等级：
- high: 总分 >= 75
- medium: 50 <= 总分 < 75
- low: 总分 < 50"""


def compute_match(resume_data: dict, jd_analysis: dict) -> dict:
    """
    计算简历与岗位的匹配度。

    采用「规则评分 + AI 综合评分」混合方案。

    Args:
        resume_data: 结构化简历信息
        jd_analysis: 结构化岗位 JD 信息

    Returns:
        匹配评分结果 dict
    """
    # Step 1: 规则评分
    rule_scores = compute_rule_scores(resume_data, jd_analysis)
    logger.info(f"规则评分完成: {rule_scores['total']}")

    # Step 2: AI 综合评分
    try:
        ai_result = compute_ai_score(resume_data, jd_analysis, rule_scores)
        logger.info(f"AI 评分完成: {ai_result.get('match_score', 'N/A')}")
        return ai_result
    except Exception as e:
        logger.warning(f"AI 评分失败，使用规则评分兜底: {e}")
        return build_rule_only_result(rule_scores, resume_data, jd_analysis)


def compute_rule_scores(resume_data: dict, jd_analysis: dict) -> dict:
    """规则评分：基于关键词匹配计算基础分"""
    # 提取简历中的所有技能
    resume_skills = extract_resume_skills(resume_data)
    resume_text = (resume_data.get("cleaned_text", "") or "").lower()

    # 提取 JD 要求
    required_skills = [s.lower() for s in jd_analysis.get("required_skills", [])]
    bonus_skills = [s.lower() for s in jd_analysis.get("bonus_skills", [])]
    keywords = [k.lower() for k in jd_analysis.get("keywords", [])]

    # 1. 技能匹配度 (40%)
    skill_score = compute_skill_score(resume_skills, required_skills, bonus_skills)

    # 2. 项目经验匹配度 (25%)
    project_score = compute_project_score(resume_data, jd_analysis)

    # 3. 工作背景匹配度 (20%)
    experience_score = compute_experience_score(resume_data, jd_analysis)

    # 4. 关键词覆盖度 (15%)
    keyword_score = compute_keyword_score(resume_text, keywords)

    total = round(
        skill_score * WEIGHTS["skill_match"]
        + project_score * WEIGHTS["project_match"]
        + experience_score * WEIGHTS["experience_match"]
        + keyword_score * WEIGHTS["keyword_coverage"]
    )

    return {
        "total": total,
        "skill_match": skill_score,
        "project_match": project_score,
        "experience_match": experience_score,
        "keyword_coverage": keyword_score,
        "resume_skills": list(resume_skills),
    }


def extract_resume_skills(resume_data: dict) -> set[str]:
    """从简历中提取所有技能关键词（不区分大小写）"""
    skills_data = resume_data.get("skills", {})
    all_skills = set()
    for category in skills_data.values():
        if isinstance(category, list):
            for s in category:
                all_skills.add(s.lower())
    return all_skills


def compute_skill_score(resume_skills: set[str], required: list[str], bonus: list[str]) -> int:
    """技能匹配度评分"""
    if not required and not bonus:
        return 50  # 无技能要求时给默认分

    total_weight = 0
    matched_weight = 0

    # 必备技能权重 2
    for skill in required:
        total_weight += 2
        if skill in resume_skills:
            matched_weight += 2

    # 加分技能权重 1
    for skill in bonus:
        total_weight += 1
        if skill in resume_skills:
            matched_weight += 1

    if total_weight == 0:
        return 50

    return round(matched_weight / total_weight * 100)


def compute_project_score(resume_data: dict, jd_analysis: dict) -> int:
    """项目经验匹配度评分"""
    projects = resume_data.get("projects", [])
    responsibilities = jd_analysis.get("responsibilities", [])
    keywords = [k.lower() for k in jd_analysis.get("keywords", [])]

    if not projects:
        return 30  # 无项目经历给低分

    # 检查项目中是否包含 JD 相关关键词
    project_text = ""
    for p in projects:
        project_text += " ".join([
            p.get("project_name", ""),
            p.get("description", ""),
            " ".join(p.get("tech_stack", [])),
            " ".join(p.get("achievements", [])),
        ]) + " "
    project_text = project_text.lower()

    if not keywords:
        return 60  # 无关键词要求时给默认分

    matched = sum(1 for kw in keywords if kw in project_text)
    return round(matched / len(keywords) * 100)


def compute_experience_score(resume_data: dict, jd_analysis: dict) -> int:
    """工作背景匹配度评分"""
    work_exp = resume_data.get("work_experience", [])
    exp_req = jd_analysis.get("experience_requirements", "")

    if not work_exp and not exp_req:
        return 50

    score = 50  # 基础分

    # 有工作经历加分
    if work_exp:
        score += 20
        # 多段经历加分
        if len(work_exp) > 1:
            score += 10

    # 检查工作年限
    if exp_req:
        years_match = re.search(r'(\d+)', exp_req)
        if years_match:
            required_years = int(years_match.group(1))
            # 估算候选人工作年限（简单累加）
            candidate_years = estimate_work_years(work_exp)
            if candidate_years >= required_years:
                score += 20
            elif candidate_years >= required_years * 0.5:
                score += 10

    return min(score, 100)


def estimate_work_years(work_exp: list[dict]) -> int:
    """估算工作年限"""
    total_months = 0
    for exp in work_exp:
        start = exp.get("start_date", "")
        end = exp.get("end_date", "")

        start_year = re.search(r'(\d{4})', start)
        end_year = re.search(r'(\d{4})', end or "2026")

        if start_year and end_year:
            years = int(end_year.group(1)) - int(start_year.group(1))
            total_months += max(years * 12, 0)

    return total_months // 12


def compute_keyword_score(resume_text: str, keywords: list[str]) -> int:
    """关键词覆盖度评分"""
    if not keywords:
        return 50

    matched = sum(1 for kw in keywords if kw in resume_text)
    return round(matched / len(keywords) * 100)


def compute_ai_score(resume_data: dict, jd_analysis: dict, rule_scores: dict) -> dict:
    """AI 综合评分"""
    # 构建简历摘要（避免发送过长文本）
    resume_summary = build_resume_summary(resume_data)
    jd_summary = build_jd_summary(jd_analysis)

    user_prompt = f"""候选人简历摘要：
{resume_summary}

岗位 JD 分析：
{jd_summary}

规则评分参考：
- 技能匹配度: {rule_scores['skill_match']}/100
- 项目经验匹配度: {rule_scores['project_match']}/100
- 工作背景匹配度: {rule_scores['experience_match']}/100
- 关键词覆盖度: {rule_scores['keyword_coverage']}/100
- 规则总分: {rule_scores['total']}/100

请进行综合匹配评估。"""

    result = call_ai_json(MATCH_SYSTEM_PROMPT, user_prompt)

    # 确保必要字段存在
    result.setdefault("match_score", rule_scores["total"])
    result.setdefault("score_level", get_score_level(result["match_score"]))
    result.setdefault("matched_keywords", [])
    result.setdefault("missing_keywords", [])
    result.setdefault("risk_points", [])
    result.setdefault("interview_questions", [])
    result.setdefault("ai_summary", "")

    return result


def build_resume_summary(resume_data: dict) -> str:
    """构建简历摘要文本"""
    parts = []

    basic = resume_data.get("basic_info", {})
    if basic.get("name"):
        parts.append(f"姓名: {basic['name']}")

    education = resume_data.get("education", [])
    if education:
        edu_strs = [f"{e.get('school', '')} {e.get('degree', '')} {e.get('major', '')}" for e in education]
        parts.append(f"教育: {', '.join(edu_strs)}")

    work = resume_data.get("work_experience", [])
    if work:
        work_strs = [f"{w.get('company', '')} {w.get('position', '')}" for w in work]
        parts.append(f"工作: {', '.join(work_strs)}")

    projects = resume_data.get("projects", [])
    if projects:
        proj_strs = [f"{p.get('project_name', '')} ({', '.join(p.get('tech_stack', []))})" for p in projects]
        parts.append(f"项目: {', '.join(proj_strs)}")

    skills = resume_data.get("skills", {})
    all_skills = []
    for category in skills.values():
        if isinstance(category, list):
            all_skills.extend(category)
    if all_skills:
        parts.append(f"技能: {', '.join(all_skills)}")

    return "\n".join(parts)


def build_jd_summary(jd_analysis: dict) -> str:
    """构建 JD 摘要文本"""
    parts = []
    if jd_analysis.get("job_title"):
        parts.append(f"岗位: {jd_analysis['job_title']}")
    if jd_analysis.get("required_skills"):
        parts.append(f"必备技能: {', '.join(jd_analysis['required_skills'])}")
    if jd_analysis.get("bonus_skills"):
        parts.append(f"加分技能: {', '.join(jd_analysis['bonus_skills'])}")
    if jd_analysis.get("experience_requirements"):
        parts.append(f"经验要求: {jd_analysis['experience_requirements']}")
    if jd_analysis.get("education_requirements"):
        parts.append(f"学历要求: {jd_analysis['education_requirements']}")
    return "\n".join(parts)


def build_rule_only_result(rule_scores: dict, resume_data: dict, jd_analysis: dict) -> dict:
    """AI 失败时，用规则评分构建结果"""
    resume_skills = extract_resume_skills(resume_data)
    required = [s.lower() for s in jd_analysis.get("required_skills", [])]
    bonus = [s.lower() for s in jd_analysis.get("bonus_skills", [])]
    keywords = [k.lower() for k in jd_analysis.get("keywords", [])]
    resume_text = (resume_data.get("cleaned_text", "") or "").lower()

    # 计算匹配/缺失关键词
    matched_kw = [k for k in jd_analysis.get("keywords", []) if k.lower() in resume_text]
    missing_kw = [k for k in jd_analysis.get("keywords", []) if k.lower() not in resume_text]

    return {
        "match_score": rule_scores["total"],
        "score_level": get_score_level(rule_scores["total"]),
        "score_items": {
            "skill_match": {"score": rule_scores["skill_match"], "weight": WEIGHTS["skill_match"], "reason": "基于关键词匹配"},
            "project_match": {"score": rule_scores["project_match"], "weight": WEIGHTS["project_match"], "reason": "基于关键词匹配"},
            "experience_match": {"score": rule_scores["experience_match"], "weight": WEIGHTS["experience_match"], "reason": "基于工作年限和经历"},
            "keyword_coverage": {"score": rule_scores["keyword_coverage"], "weight": WEIGHTS["keyword_coverage"], "reason": "基于 JD 关键词覆盖率"},
        },
        "matched_keywords": matched_kw,
        "missing_keywords": missing_kw,
        "risk_points": [],
        "interview_questions": [],
        "ai_summary": "（AI 评分不可用，以上为规则评分结果）",
    }


def get_score_level(score: int) -> str:
    """根据分数返回等级"""
    if score >= 75:
        return "high"
    elif score >= 50:
        return "medium"
    else:
        return "low"
