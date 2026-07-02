# AI 智能简历分析与岗位匹配系统 PRD

## 1. 文档信息

| 项目 | 内容 |
|---|---|
| 文档名称 | AI 智能简历分析与岗位匹配系统 PRD |
| 文档版本 | v1.0 |
| 产品阶段 | MVP + 可扩展版本规划 |
| 目标交付 | 面试作业 / 技术评审演示系统 |
| 后端语言 | Python |
| 后端框架 | FastAPI |
| 前端技术 | React + Vite |
| 部署方式 | 阿里云 Serverless 函数计算 FC + GitHub Pages / 其他公网前端托管 |
| 缓存设计 | Redis 增强项，MVP 可用内存缓存替代 |
| 数据存储 | SQLite / 本地 JSON，后续可扩展 MySQL / PostgreSQL |

---

## 2. 项目背景

在招聘流程中，HR、招聘专员或技术面试官需要快速阅读大量候选人简历，并根据岗位要求判断候选人是否匹配。传统人工筛选方式存在以下问题：

1. 简历数量多，人工阅读耗时；
2. 候选人信息分散在 PDF 文档中，难以结构化管理；
3. 岗位 JD 与简历之间的匹配判断依赖人工经验，效率低且标准不统一；
4. 缺少可解释的匹配结果，例如候选人哪些技能匹配、哪些技能缺失；
5. 简历重复解析和重复评分会造成计算资源浪费。

因此，本项目希望构建一个 AI 赋能的智能简历分析系统，支持上传 PDF 简历，自动解析简历内容，提取候选人关键信息，并结合岗位需求描述进行匹配评分，帮助招聘者快速完成候选人初筛。

---

## 3. 产品定位

### 3.1 产品名称

AI 智能简历分析与岗位匹配系统

### 3.2 产品一句话描述

面向招聘场景的轻量级 AI 简历分析工具，支持 PDF 简历解析、候选人信息提取、岗位 JD 分析与匹配度评分，帮助招聘者快速完成候选人初筛。

### 3.3 产品目标

MVP 阶段目标：

1. 支持单个 PDF 简历上传；
2. 支持多页 PDF 文本解析；
3. 支持简历文本清洗和结构化处理；
4. 支持 AI 提取候选人基本信息、教育背景、工作经历、项目经历和技能信息；
5. 支持输入岗位 JD，并自动分析岗位要求；
6. 支持简历与岗位 JD 的匹配评分；
7. 支持返回结构化 JSON；
8. 支持前端页面在线演示；
9. 支持历史记录展示；
10. 支持缓存设计，避免重复解析和重复评分。

非目标：

1. 不做完整招聘 SaaS；
2. 不做企业组织架构管理；
3. 不做候选人投递流程；
4. 不做面试安排、Offer 审批等招聘流程；
5. MVP 阶段不实现登录注册和复杂权限控制。

---

## 4. 用户角色

### 4.1 招聘者 / HR

主要使用者，负责上传简历、输入岗位需求、查看候选人匹配结果。

### 4.2 技术面试官

辅助使用者，关注候选人的技能栈、项目经历、岗位匹配度、风险点和面试追问建议。

### 4.3 系统评审人员

面试作业或项目验收人员，关注系统功能完整性、接口规范、工程结构、AI 调用能力、部署可用性和 README 文档完整性。

---

## 5. 使用场景

### 5.1 简历快速解析

招聘者上传候选人的 PDF 简历，系统自动提取候选人的姓名、电话、邮箱、地址、学历、工作经历、项目经历和技能信息。

### 5.2 岗位匹配评分

招聘者输入岗位 JD，系统自动提取岗位名称、必备技能、加分技能和经验要求，并将候选人简历与岗位要求进行匹配，输出综合评分和解释。

### 5.3 候选人初筛

招聘者通过匹配分数、技能标签、缺失关键词和 AI 评价报告，快速判断候选人是否值得进入下一轮面试。

### 5.4 面试准备

技术面试官根据系统输出的风险点和追问建议，准备针对性的面试问题。

---

## 6. MVP 范围

### 6.1 必须实现

1. PDF 简历上传；
2. PDF 文本提取；
3. 简历文本清洗；
4. AI 关键信息提取；
5. 岗位 JD 输入；
6. 岗位关键词和要求提取；
7. 简历与岗位 JD 匹配评分；
8. 结构化 JSON 返回；
9. 前端页面在线演示；
10. 最近分析历史记录；
11. 基础异常处理；
12. README 文档。

### 6.2 增强项

1. Redis 缓存；
2. AI 综合评价报告；
3. 风险点识别；
4. 面试追问建议；
5. 评分权重展示；
6. JSON 原始结果展示；
7. AI 调用失败时正则兜底；
8. 文本型 PDF 优先解析，扫描版 PDF 预留 OCR 扩展。

### 6.3 后续扩展

1. 批量上传多份简历；
2. 候选人库；
3. 岗位管理；
4. HR 登录注册；
5. 多用户权限；
6. 面试流程管理；
7. 数据统计看板；
8. 接入企业招聘系统；
9. 支持 DOCX、图片简历、扫描版 PDF；
10. 支持更多模型供应商切换。

---

## 7. 核心业务流程

### 7.1 主流程

```text
用户进入前端页面
    ↓
上传单个 PDF 简历
    ↓
输入岗位 JD 文本
    ↓
点击“开始分析”
    ↓
后端接收 PDF 和 JD
    ↓
校验文件格式、大小和页数
    ↓
解析 PDF 文本
    ↓
清洗简历文本
    ↓
调用 AI 模型提取简历结构化信息
    ↓
调用 AI 模型分析岗位 JD
    ↓
执行规则评分 + AI 综合评分
    ↓
生成匹配结果、风险点、追问建议
    ↓
保存分析记录
    ↓
返回结构化 JSON
    ↓
前端展示候选人信息、技能标签、评分卡片、AI 报告和 JSON 结果
```

### 7.2 支持只解析简历

系统允许用户只上传 PDF 简历，不输入 JD。此时系统仅返回简历解析结果，不执行岗位匹配。

流程：

```text
上传 PDF 简历 → PDF 解析 → AI 提取候选人信息 → 返回结构化简历结果
```

### 7.3 后续输入 JD 后再匹配

当用户已经上传并解析过简历后，可以继续输入岗位 JD，基于已解析结果进行岗位匹配。

流程：

```text
选择已解析简历 → 输入岗位 JD → 执行匹配评分 → 返回匹配结果
```

---

## 8. 功能需求

## 8.1 简历上传

### 功能说明

用户可以通过前端页面上传单个 PDF 简历文件，系统校验文件合法性后保存文件并生成 resume_id。

### 上传限制

| 限制项 | 要求 |
|---|---|
| 文件格式 | PDF |
| 文件数量 | 单次上传 1 个文件 |
| 文件大小 | 最大 10MB |
| 页数限制 | 最多 5 页 |
| 文件类型校验 | 根据 MIME Type 和文件扩展名双重校验 |

### 功能规则

1. 仅允许上传 `.pdf` 文件；
2. 上传前端需要显示文件名称和大小；
3. 后端必须再次校验文件类型，不能只依赖前端限制；
4. 文件上传成功后返回 resume_id；
5. 文件上传失败时返回明确错误码。

---

## 8.2 PDF 文本解析

### 功能说明

系统解析上传的 PDF 文件，提取其中的文本内容，并兼容多页简历。

### 解析方案

MVP 阶段：

1. 优先使用 PyMuPDF 或 pdfplumber 提取文本；
2. 支持多页 PDF 内容合并；
3. 对每页文本进行分段处理；
4. 输出 raw_text 和 cleaned_text。

后续扩展：

1. 对扫描版 PDF 增加 OCR 识别；
2. 对图片型简历增加图像预处理；
3. 对复杂排版简历增加布局识别。

### 文本清洗规则

1. 去除多余空格；
2. 去除重复换行；
3. 合并无意义断行；
4. 保留邮箱、手机号、项目符号等关键信息；
5. 尽量保留简历原始段落结构。

---

## 8.3 AI 关键信息提取

### 功能说明

系统将清洗后的简历文本发送给 AI 模型，提取候选人的结构化信息。

### 字段结构

#### 8.3.1 基本信息 basic_info

| 字段 | 类型 | 是否必须 | 说明 |
|---|---|---|---|
| name | string | 是 | 姓名 |
| phone | string | 是 | 手机号 |
| email | string | 是 | 邮箱 |
| address | string | 是 | 地址 / 所在城市 |

#### 8.3.2 求职信息 job_intention

| 字段 | 类型 | 是否必须 | 说明 |
|---|---|---|---|
| target_position | string | 否 | 求职意向 |
| expected_salary | string | 否 | 期望薪资 |
| target_city | string | 否 | 目标城市 |

#### 8.3.3 教育背景 education

| 字段 | 类型 | 是否必须 | 说明 |
|---|---|---|---|
| school | string | 否 | 学校 |
| degree | string | 否 | 学历 |
| major | string | 否 | 专业 |
| start_date | string | 否 | 开始时间 |
| end_date | string | 否 | 结束时间 |

#### 8.3.4 工作经历 work_experience

| 字段 | 类型 | 是否必须 | 说明 |
|---|---|---|---|
| company | string | 否 | 公司名称 |
| position | string | 否 | 岗位名称 |
| start_date | string | 否 | 开始时间 |
| end_date | string | 否 | 结束时间 |
| responsibilities | array | 否 | 职责描述 |

#### 8.3.5 项目经历 projects

| 字段 | 类型 | 是否必须 | 说明 |
|---|---|---|---|
| project_name | string | 否 | 项目名称 |
| project_time | string | 否 | 项目时间 |
| description | string | 否 | 项目描述 |
| tech_stack | array | 否 | 技术栈 |
| role | string | 否 | 个人职责 |
| achievements | array | 否 | 项目成果 |

#### 8.3.6 技能信息 skills

后端按分类返回，前端以标签形式展示。

```json
{
  "programming_languages": ["Python", "JavaScript"],
  "frameworks": ["FastAPI", "React"],
  "databases": ["MySQL", "Redis"],
  "cloud_services": ["阿里云", "函数计算 FC"],
  "ai_tools": ["大语言模型", "OCR", "Prompt Engineering"],
  "others": ["Git", "Docker"]
}
```

#### 8.3.7 综合摘要 summary

| 字段 | 类型 | 是否必须 | 说明 |
|---|---|---|---|
| candidate_summary | string | 否 | 候选人简介 |
| strengths | array | 否 | 优势 |
| weaknesses | array | 否 | 不足 |
| suitable_positions | array | 否 | 适合岗位 |

---

## 8.4 AI 调用失败兜底

当 AI 模型不可用、超时或返回格式错误时，系统不能直接中断整个流程，应返回基础可用结果。

### 兜底策略

1. 返回 PDF 原始解析文本 raw_text；
2. 返回清洗后的文本 cleaned_text；
3. 使用正则提取基础字段；
4. 标记 ai_extract_status 为 failed；
5. 返回错误提示，但接口整体可正常响应。

### 正则兜底字段

| 字段 | 处理方式 |
|---|---|
| 手机号 | 正则匹配中国大陆手机号 |
| 邮箱 | 正则匹配邮箱格式 |
| 姓名疑似字段 | 从简历开头若干行推断 |
| 学历关键词 | 匹配本科、硕士、博士、大专等 |
| 技能关键词 | 匹配常见技术关键词，如 Python、Java、React、MySQL、Redis 等 |

---

## 8.5 岗位 JD 分析

### 功能说明

用户输入一段岗位需求描述，系统自动提取岗位相关信息，为后续匹配评分提供依据。

### 输入内容

用户可以粘贴任意文本格式的岗位 JD，例如：

```text
招聘 Python 后端开发工程师，要求熟悉 FastAPI、MySQL、Redis，了解 Serverless 架构，有 AI 应用开发经验优先。
```

### 输出结构

```json
{
  "job_title": "Python 后端开发工程师",
  "required_skills": ["Python", "FastAPI", "MySQL", "Redis"],
  "bonus_skills": ["Serverless", "AI 应用开发"],
  "experience_requirements": "1-3 年后端开发经验",
  "education_requirements": "本科及以上",
  "responsibilities": ["后端接口开发", "系统部署", "AI 能力集成"],
  "keywords": ["Python", "FastAPI", "Redis", "Serverless", "AI"]
}
```

---

## 8.6 简历匹配评分

### 功能说明

系统将结构化简历信息与岗位 JD 分析结果进行匹配，输出综合评分、分项评分、匹配关键词、缺失关键词、风险点和面试追问建议。

### 评分方式

采用“规则评分 + AI 综合评分”的混合方案。

1. 规则评分：根据技能关键词覆盖率、项目经验、工作经历和学历背景计算基础分；
2. AI 综合评分：由 AI 模型结合岗位 JD 和简历内容进行语义判断；
3. 最终评分：综合规则评分和 AI 评分后输出。

### 评分权重

| 评分项 | 权重 | 说明 |
|---|---:|---|
| 技能匹配度 | 40% | 候选人技能与岗位必备技能、加分技能的匹配情况 |
| 项目经验匹配度 | 25% | 项目经历与岗位职责、技术场景的相关性 |
| 工作经历 / 背景匹配度 | 20% | 工作年限、岗位经历、行业背景是否匹配 |
| 岗位关键词覆盖度 | 15% | 简历中覆盖 JD 关键词的比例 |

### 输出结果

```json
{
  "match_score": 86,
  "score_level": "high",
  "score_items": {
    "skill_match": {
      "score": 88,
      "weight": 0.4
    },
    "project_match": {
      "score": 82,
      "weight": 0.25
    },
    "experience_match": {
      "score": 80,
      "weight": 0.2
    },
    "keyword_coverage": {
      "score": 90,
      "weight": 0.15
    }
  },
  "matched_keywords": ["Python", "FastAPI", "AI", "Serverless"],
  "missing_keywords": ["Redis"],
  "risk_points": ["简历中未明确体现 Redis 项目经验"],
  "interview_questions": [
    "请介绍你在 FastAPI 项目中的接口设计经验。",
    "你是否在实际项目中使用过 Redis？主要解决什么问题？"
  ],
  "ai_summary": "候选人与岗位整体匹配度较高，具备 Python 后端和 AI 项目经验，但 Redis 经验需要进一步确认。"
}
```

---

## 8.7 历史记录

### 功能说明

系统展示最近分析过的简历记录，方便用户快速查看历史分析结果。

### 前端展示字段

| 字段 | 说明 |
|---|---|
| file_name | PDF 文件名 |
| candidate_name | 候选人姓名 |
| job_title | 岗位名称 |
| match_score | 匹配评分 |
| created_at | 分析时间 |

### 功能规则

1. 单页中展示最近分析记录；
2. MVP 阶段不做复杂搜索和筛选；
3. 点击历史记录可查看完整分析结果；
4. 后端可保存完整解析结果和评分结果；
5. 前端列表只展示核心摘要字段。

---

## 8.8 缓存机制

### 功能说明

为避免重复解析和重复调用 AI，系统设计缓存机制。

### 缓存策略

MVP 阶段：

1. 可以使用内存缓存作为替代；
2. 如果部署环境允许，可使用 Redis；
3. 缓存不可用时，不影响主流程，只降级为实时计算。

增强阶段：

1. 使用 Redis 缓存 PDF 解析结果；
2. 使用 Redis 缓存 AI 提取结果；
3. 使用 Redis 缓存岗位匹配结果。

### 缓存 Key 设计

```text
resume:parse:{file_hash}
resume:extract:{file_hash}
resume:match:{file_hash}:{jd_hash}
```

### 缓存内容

| 缓存内容 | Key | 说明 |
|---|---|---|
| PDF 解析文本 | resume:parse:{file_hash} | 避免重复解析 PDF |
| 简历结构化信息 | resume:extract:{file_hash} | 避免重复调用 AI 提取 |
| 匹配评分结果 | resume:match:{file_hash}:{jd_hash} | 避免同一简历和同一 JD 重复评分 |

---

## 9. 页面需求

## 9.1 前端整体设计

### 技术栈

React + Vite

### 页面形态

单页应用，包含上传区、JD 输入区、分析结果区、历史记录区。

### 页面风格

招聘后台风格 + AI 报告风格。

1. 简洁；
2. 清晰；
3. 信息层次明确；
4. 适合技术评审在线验收。

---

## 9.2 页面模块

### 9.2.1 顶部区域

展示系统名称和简短说明。

示例：

```text
AI 智能简历分析系统
上传 PDF 简历，输入岗位 JD，快速生成候选人匹配报告
```

### 9.2.2 简历上传区域

功能：

1. 选择 PDF 文件；
2. 显示文件名称；
3. 显示文件大小；
4. 校验文件格式；
5. 提示最大 10MB、最多 5 页。

### 9.2.3 岗位 JD 输入区域

功能：

1. 多行文本输入；
2. 支持粘贴岗位描述；
3. 支持为空；
4. 为空时仅解析简历，不做匹配。

### 9.2.4 分析按钮

按钮文案：

```text
开始分析
```

状态：

1. 默认状态；
2. 加载中；
3. 分析完成；
4. 分析失败。

### 9.2.5 候选人信息卡

展示：

1. 姓名；
2. 手机号；
3. 邮箱；
4. 地址；
5. 学历；
6. 工作年限；
7. 求职意向。

### 9.2.6 技能标签区

展示技能标签，例如：

```text
Python / FastAPI / React / MySQL / Redis / Serverless / AI
```

后端分类返回，前端可以按统一标签样式展示。

### 9.2.7 匹配评分区

展示：

1. 综合匹配分；
2. 技能匹配分；
3. 项目经验匹配分；
4. 工作背景匹配分；
5. 关键词覆盖分；
6. 评分权重说明。

### 9.2.8 AI 评价报告

展示：

1. 候选人综合评价；
2. 匹配优势；
3. 风险点；
4. 面试追问建议。

### 9.2.9 JSON 原始结果区

展示后端返回的完整 JSON，方便评审验证接口结构。

### 9.2.10 历史记录区

展示最近分析记录：

1. 文件名；
2. 候选人姓名；
3. 岗位名称；
4. 匹配分数；
5. 分析时间。

---

## 10. 接口需求

## 10.1 统一返回格式

所有接口统一返回：

```json
{
  "success": true,
  "code": "SUCCESS",
  "message": "操作成功",
  "data": {},
  "request_id": "req_xxx",
  "timestamp": 1780000000
}
```

失败示例：

```json
{
  "success": false,
  "code": "INVALID_FILE_TYPE",
  "message": "仅支持上传 PDF 文件",
  "data": null,
  "request_id": "req_xxx",
  "timestamp": 1780000000
}
```

---

## 10.2 上传简历接口

### 接口信息

```text
POST /api/resumes/upload
```

### 请求方式

`multipart/form-data`

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| file | file | 是 | PDF 简历文件 |

### 返回示例

```json
{
  "success": true,
  "code": "SUCCESS",
  "message": "上传成功",
  "data": {
    "resume_id": "res_001",
    "file_name": "zhangsan_resume.pdf",
    "file_size": 1024000,
    "file_hash": "abc123",
    "upload_time": "2026-07-02 10:00:00"
  },
  "request_id": "req_001",
  "timestamp": 1780000000
}
```

---

## 10.3 简历解析接口

### 接口信息

```text
POST /api/resumes/{resume_id}/parse
```

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| resume_id | string | 是 | 简历 ID |

### 返回示例

```json
{
  "success": true,
  "code": "SUCCESS",
  "message": "解析成功",
  "data": {
    "resume_id": "res_001",
    "parse_status": "success",
    "basic_info": {
      "name": "张三",
      "phone": "13800000000",
      "email": "zhangsan@example.com",
      "address": "杭州"
    },
    "job_intention": {
      "target_position": "Python 后端开发工程师",
      "expected_salary": "15k-20k",
      "target_city": "杭州"
    },
    "education": [],
    "work_experience": [],
    "projects": [],
    "skills": {
      "programming_languages": ["Python"],
      "frameworks": ["FastAPI"],
      "databases": ["MySQL", "Redis"],
      "cloud_services": ["阿里云"],
      "ai_tools": ["大语言模型"],
      "others": ["Git"]
    },
    "summary": {
      "candidate_summary": "候选人具备 Python 后端开发经验。",
      "strengths": ["后端开发基础较好"],
      "weaknesses": ["云服务经验描述较少"],
      "suitable_positions": ["Python 后端开发工程师"]
    },
    "raw_text": "...",
    "cleaned_text": "..."
  },
  "request_id": "req_002",
  "timestamp": 1780000000
}
```

---

## 10.4 岗位匹配接口

### 接口信息

```text
POST /api/match
```

### 请求参数

```json
{
  "resume_id": "res_001",
  "job_description": "招聘 Python 后端开发工程师，要求熟悉 FastAPI、MySQL、Redis..."
}
```

### 返回示例

```json
{
  "success": true,
  "code": "SUCCESS",
  "message": "匹配成功",
  "data": {
    "analysis_id": "ana_001",
    "resume_id": "res_001",
    "job_analysis": {
      "job_title": "Python 后端开发工程师",
      "required_skills": ["Python", "FastAPI", "MySQL", "Redis"],
      "bonus_skills": ["Serverless", "AI 应用开发"],
      "experience_requirements": "1-3 年后端开发经验",
      "education_requirements": "本科及以上",
      "keywords": ["Python", "FastAPI", "Redis", "Serverless", "AI"]
    },
    "match_result": {
      "match_score": 86,
      "score_level": "high",
      "score_items": {
        "skill_match": {"score": 88, "weight": 0.4},
        "project_match": {"score": 82, "weight": 0.25},
        "experience_match": {"score": 80, "weight": 0.2},
        "keyword_coverage": {"score": 90, "weight": 0.15}
      },
      "matched_keywords": ["Python", "FastAPI", "AI"],
      "missing_keywords": ["Redis"],
      "risk_points": ["简历中未明确体现 Redis 项目经验"],
      "interview_questions": ["请介绍你是否在项目中使用过 Redis？"],
      "ai_summary": "候选人与岗位整体匹配度较高，但 Redis 经验需要进一步确认。"
    }
  },
  "request_id": "req_003",
  "timestamp": 1780000000
}
```

---

## 10.5 查询分析结果接口

### 接口信息

```text
GET /api/analysis/{analysis_id}
```

### 返回内容

返回指定分析记录的完整简历解析结果和匹配结果。

---

## 10.6 查询历史记录接口

### 接口信息

```text
GET /api/analysis/history
```

### 返回示例

```json
{
  "success": true,
  "code": "SUCCESS",
  "message": "查询成功",
  "data": {
    "items": [
      {
        "analysis_id": "ana_001",
        "resume_id": "res_001",
        "file_name": "zhangsan_resume.pdf",
        "candidate_name": "张三",
        "job_title": "Python 后端开发工程师",
        "match_score": 86,
        "created_at": "2026-07-02 10:00:00"
      }
    ]
  },
  "request_id": "req_004",
  "timestamp": 1780000000
}
```

---

## 11. 数据结构设计

## 11.1 resumes 表

| 字段 | 类型 | 说明 |
|---|---|---|
| id | string | 简历 ID |
| file_name | string | 文件名 |
| file_path | string | 文件路径 |
| file_size | integer | 文件大小 |
| file_hash | string | 文件 Hash |
| raw_text | text | 原始文本 |
| cleaned_text | text | 清洗文本 |
| parsed_data | json | 结构化解析结果 |
| parse_status | string | 解析状态 |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

---

## 11.2 analysis_records 表

| 字段 | 类型 | 说明 |
|---|---|---|
| id | string | 分析记录 ID |
| resume_id | string | 简历 ID |
| job_description | text | 岗位 JD 原文 |
| job_analysis | json | 岗位分析结果 |
| match_result | json | 匹配评分结果 |
| match_score | integer | 综合评分 |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

---

## 12. AI 模型设计

## 12.1 模型接口可配置

系统不与单一模型强绑定，后端通过配置文件或环境变量配置模型供应商和 API Key。

示例配置：

```env
AI_PROVIDER=qwen
AI_API_KEY=your_api_key
AI_MODEL=qwen-plus
AI_TIMEOUT=30
```

后续可扩展：

1. 通义千问 / 百炼；
2. OpenAI；
3. DeepSeek；
4. 豆包；
5. 本地模型。

---

## 12.2 简历信息提取 Prompt 要求

要求 AI 必须输出严格 JSON，不得输出 Markdown。

核心要求：

1. 从简历文本中提取结构化字段；
2. 不确定字段返回空字符串或空数组；
3. 不得编造简历中不存在的信息；
4. 输出必须符合指定 JSON Schema；
5. 保留候选人的关键信息、技能、项目和工作经历。

---

## 12.3 岗位匹配 Prompt 要求

要求 AI 结合岗位 JD 和候选人简历信息，输出：

1. 综合评分；
2. 分项评分；
3. 匹配关键词；
4. 缺失关键词；
5. 风险点；
6. 面试追问建议；
7. 综合评价。

要求：

1. 不得只给主观评价；
2. 必须结合 JD 要求说明原因；
3. 必须返回 JSON；
4. 评分范围为 0-100；
5. 风险点必须具体，不能空泛。

---

## 13. 错误码设计

| 错误码 | 说明 | 处理方式 |
|---|---|---|
| SUCCESS | 操作成功 | 正常返回 |
| INVALID_FILE_TYPE | 文件类型错误 | 提示仅支持 PDF |
| FILE_TOO_LARGE | 文件过大 | 提示最大 10MB |
| PDF_PAGE_LIMIT_EXCEEDED | PDF 页数超限 | 提示最多 5 页 |
| PDF_PARSE_FAILED | PDF 解析失败 | 返回失败原因 |
| AI_EXTRACT_FAILED | AI 简历提取失败 | 返回正则兜底结果 |
| AI_RESPONSE_INVALID | AI 返回格式错误 | 尝试修复 JSON 或返回错误 |
| MATCH_FAILED | 匹配评分失败 | 返回错误提示 |
| CACHE_UNAVAILABLE | 缓存不可用 | 降级为实时计算 |
| RESOURCE_NOT_FOUND | 资源不存在 | 提示 resume_id 或 analysis_id 无效 |
| INTERNAL_ERROR | 系统内部错误 | 返回通用错误提示 |

---

## 14. 部署需求

## 14.1 后端部署

### 目标环境

阿里云 Serverless 函数计算 FC。

### 本地开发环境

支持本地运行和 Docker 调试。

### 部署要求

1. 后端服务提供公网可访问 API；
2. API 满足 RESTful 风格；
3. 支持跨域 CORS；
4. AI API Key 通过环境变量配置；
5. 不得将密钥提交到 GitHub；
6. 提供本地启动说明；
7. 提供部署说明。

---

## 14.2 前端部署

### 目标环境

GitHub Pages 或其他公网服务。

### 部署要求

1. 前端页面可公网访问；
2. 页面可上传 PDF；
3. 页面可输入 JD；
4. 页面可展示解析结果；
5. 页面可展示匹配评分；
6. 页面可展示 JSON 原始返回；
7. 页面可展示最近历史记录。

---

## 15. README 要求

GitHub 仓库必须包含 README.md。

建议目录：

```md
# AI 智能简历分析系统

## 1. 项目简介
## 2. 功能特性
## 3. 技术选型
## 4. 系统架构
## 5. 项目目录结构
## 6. 本地运行方式
## 7. 环境变量配置
## 8. API 接口说明
## 9. 前端部署说明
## 10. 后端部署说明
## 11. 示例请求与响应
## 12. 缓存设计
## 13. AI 模型设计
## 14. 已实现功能
## 15. 后续优化方向
```

README 中必须包含：

1. GitHub 仓库地址；
2. 在线演示地址；
3. 项目架构说明；
4. 技术选型说明；
5. 部署方式；
6. 使用说明；
7. API 示例；
8. 环境变量说明；
9. 运行截图或演示说明。

---

## 16. 验收标准

## 16.1 用户流程验收

| 验收项 | 标准 |
|---|---|
| 上传 PDF | 能成功上传单个 PDF 简历 |
| 解析简历 | 能提取 PDF 中的文本内容 |
| 清洗文本 | 能去除明显冗余字符和多余换行 |
| 信息提取 | 能返回姓名、电话、邮箱、地址等基础字段 |
| JD 输入 | 能输入岗位需求文本 |
| 岗位分析 | 能提取岗位关键词和技能要求 |
| 匹配评分 | 能返回综合分和分项评分 |
| 结果展示 | 前端能展示候选人信息、技能标签和评分 |
| JSON 展示 | 前端能展示后端原始 JSON |
| 历史记录 | 能展示最近分析记录 |

---

## 16.2 接口验收

| 验收项 | 标准 |
|---|---|
| RESTful 风格 | 接口路径和方法清晰 |
| 统一返回格式 | 所有接口包含 success、code、message、data、request_id、timestamp |
| 错误处理 | 文件错误、解析失败、AI 失败均有明确错误码 |
| 示例数据 | README 中提供请求和响应示例 |
| CORS | 前端可以正常调用后端接口 |

---

## 16.3 前端验收

| 验收项 | 标准 |
|---|---|
| 页面可访问 | 前端部署至公网，可在线打开 |
| 上传组件 | 支持选择 PDF 文件 |
| JD 输入框 | 支持输入多行岗位描述 |
| 加载状态 | 分析过程中有加载提示 |
| 结果卡片 | 清晰展示候选人信息和评分 |
| 历史记录 | 展示最近分析记录 |
| JSON 区域 | 可查看完整 JSON 结果 |

---

## 16.4 部署验收

| 验收项 | 标准 |
|---|---|
| 后端部署 | 后端部署至阿里云 Serverless 或提供可访问接口 |
| 前端部署 | 前端部署至 GitHub Pages 或其他公网服务 |
| 环境变量 | AI Key 不写死在代码中 |
| README | 包含部署和运行说明 |
| GitHub 仓库 | 代码提交到公开仓库 |

---

## 17. 项目优先级

## 17.1 P0 必须实现

1. PDF 上传；
2. PDF 文本解析；
3. 简历基础信息提取；
4. JD 输入；
5. 匹配评分；
6. JSON 返回；
7. 前端页面；
8. README；
9. 在线部署。

## 17.2 P1 优先实现

1. AI 评价报告；
2. 风险点；
3. 面试追问建议；
4. 历史记录；
5. 统一错误码；
6. 缓存设计。

## 17.3 P2 后续扩展

1. Redis 完整缓存；
2. 批量上传；
3. 登录注册；
4. 岗位管理；
5. 候选人库；
6. 扫描版 PDF OCR；
7. 多模型切换；
8. 企业招聘系统集成。

---

## 18. 非功能需求

## 18.1 性能要求

1. 单份 PDF 上传和解析应在可接受时间内完成；
2. AI 调用应设置超时时间；
3. 重复上传同一文件时优先命中缓存；
4. 前端分析过程中应展示加载状态。

## 18.2 安全要求

1. 限制上传文件类型；
2. 限制文件大小；
3. 不暴露 AI API Key；
4. 不将密钥提交至 GitHub；
5. 后端校验所有用户输入；
6. 防止异常文件导致服务崩溃。

## 18.3 可维护性要求

1. 后端模块清晰拆分；
2. AI 调用封装为独立模块；
3. PDF 解析封装为独立模块；
4. 评分逻辑封装为独立模块；
5. 错误码集中管理；
6. 配置通过环境变量管理。

## 18.4 可扩展性要求

1. 支持后续增加多模型；
2. 支持后续增加批量简历解析；
3. 支持后续接入数据库；
4. 支持后续增加登录注册；
5. 支持后续接入企业招聘系统。

---

## 19. 推荐项目目录结构

```text
resume-ai-analyzer/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── resumes.py
│   │   │   ├── match.py
│   │   │   └── analysis.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── response.py
│   │   │   └── errors.py
│   │   ├── services/
│   │   │   ├── pdf_parser.py
│   │   │   ├── ai_client.py
│   │   │   ├── resume_extractor.py
│   │   │   ├── jd_analyzer.py
│   │   │   ├── match_scorer.py
│   │   │   └── cache_service.py
│   │   ├── models/
│   │   │   └── schemas.py
│   │   ├── storage/
│   │   │   └── repository.py
│   │   └── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── docs/
│   └── PRD.md
├── README.md
└── .gitignore
```

---

## 20. 开发阶段建议

## 20.1 第一阶段：最小闭环

目标：完成可演示主流程。

1. 搭建 FastAPI 项目；
2. 实现 PDF 上传；
3. 实现 PDF 文本解析；
4. 实现 AI 简历提取；
5. 实现 JD 匹配评分；
6. 返回 JSON；
7. 搭建 React 页面；
8. 完成上传、输入 JD、展示结果。

## 20.2 第二阶段：工程增强

目标：提升评分维度和系统稳定性。

1. 增加统一返回格式；
2. 增加错误码；
3. 增加 AI 失败兜底；
4. 增加历史记录；
5. 增加缓存封装；
6. 增加 README 和部署说明。

## 20.3 第三阶段：部署验收

目标：满足在线验收。

1. 前端部署到 GitHub Pages；
2. 后端部署到阿里云 Serverless；
3. 配置 CORS；
4. 测试完整流程；
5. 补充 README；
6. 提供 GitHub 仓库地址和线上演示地址。

---

## 21. 后续扩展规划

### 21.1 批量简历分析

支持一次上传多份简历，并按匹配分排序。

### 21.2 候选人库

保存候选人完整信息，支持搜索、筛选和查看详情。

### 21.3 岗位管理

支持创建岗位、保存 JD、复用岗位需求。

### 21.4 多模型切换

支持不同模型供应商配置，便于根据成本、速度和效果切换。

### 21.5 OCR 扫描版简历识别

针对扫描版 PDF 或图片简历，增加 OCR 识别能力。

### 21.6 招聘系统集成

后续可通过 API 或 Webhook 接入企业招聘系统，实现候选人信息同步。

---

## 22. 最终交付物

1. GitHub 公开仓库；
2. 后端 FastAPI 项目；
3. 前端 React + Vite 项目；
4. README.md；
5. PRD.md；
6. API 示例；
7. 前端线上演示地址；
8. 后端接口地址；
9. 测试用 PDF 简历样例；
10. 提交给面试官的信息：
    - GitHub 仓库地址；
    - 线上演示地址；
    - 姓名；
    - 联系方式。

---

## 23. 总结

本系统以“简历上传解析 + AI 信息提取 + 岗位匹配评分 + 前端在线演示”为核心闭环，重点满足面试作业中的功能完整性、代码质量、工程化实践、技术深度和加分项要求。

MVP 阶段不追求完整招聘系统，而是聚焦于一个可以快速交付、可在线演示、接口清晰、AI 能力明确、工程结构合理的智能简历分析工具。后续可继续扩展为批量简历筛选、候选人库、岗位管理和企业招聘系统集成平台。
