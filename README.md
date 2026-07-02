# ai-resume-analyzer

AI 智能简历分析与岗位匹配系统。

本项目面向招聘初筛场景，支持上传 PDF 简历，自动解析简历文本并提取候选人关键信息；同时支持输入岗位 JD，系统会提取岗位需求关键词，并计算候选人与岗位的匹配度评分，最终返回结构化 JSON 与前端可视化分析结果。

本项目采用 **Python + FastAPI + SQLite + Redis + React + Vite** 技术栈。后端支持本地 Docker 运行，并预留部署至 **阿里云函数计算 FC**；前端部署至 **GitHub Pages**，用于线上演示与评审验收。

---

## 1. 项目目标

本系统的目标不是构建完整招聘 SaaS，而是在限定时间内完成一个工程结构清晰、功能闭环完整、可线上演示的 AI 简历分析 MVP。

核心目标：

- 支持单个 PDF 简历上传
- 支持多页 PDF 文本解析
- 支持 AI 提取结构化简历信息
- 支持岗位 JD 输入与关键词提取
- 支持简历与岗位需求匹配评分
- 支持 JSON 结构化结果返回
- 支持前端页面展示分析结果
- 支持 SQLite 保存分析记录
- 支持 Redis 缓存解析与评分结果
- 支持 Docker 本地运行
- 支持前端部署到 GitHub Pages
- 后端预留阿里云函数计算 FC 部署能力

---

## 2. 核心功能

### 2.1 简历上传与解析

- 支持上传单个 PDF 格式简历
- 支持多页 PDF 文本解析
- 对解析文本进行清洗、去重和合理分段
- 默认限制文件大小不超过 10MB
- 对扫描版 PDF 预留 OCR 兜底扩展能力

### 2.2 AI 关键信息提取

系统从简历文本中提取以下信息：

| 信息类别 | 字段 |
|---|---|
| 基本信息 | 姓名、手机号、邮箱、地址 |
| 求职信息 | 求职意向、期望薪资、目标城市 |
| 教育背景 | 学校、学历、专业、毕业时间 |
| 工作经历 | 公司、岗位、时间段、职责描述 |
| 项目经历 | 项目名称、项目时间、技术栈、个人职责、项目成果 |
| 技能信息 | 编程语言、后端框架、数据库、云服务、AI 工具 |
| 综合评价 | 候选人优势、潜在风险点、适配岗位方向 |

当 AI 模型不可用或调用失败时，系统会降级使用基础规则提取：

- 手机号
- 邮箱
- 疑似姓名
- 学历关键词
- 技能关键词

### 2.3 岗位 JD 分析

系统支持输入招聘岗位描述，并自动提取：

- 岗位名称
- 必备技能
- 加分技能
- 工作年限要求
- 学历要求
- 项目经验要求
- 岗位关键词

### 2.4 简历匹配评分

系统将候选人简历信息与岗位 JD 进行匹配，输出总分和分项评分。

默认评分权重：

| 评分项 | 权重 |
|---|---:|
| 技能匹配度 | 40% |
| 项目经验匹配度 | 25% |
| 工作年限 / 背景匹配度 | 20% |
| 岗位关键词覆盖度 | 15% |

评分结果包括：

- 总匹配分
- 分项评分
- 匹配关键词
- 缺失关键词
- 推荐理由
- 风险点
- 面试追问建议

### 2.5 缓存机制

系统使用 Redis 作为增强缓存层，避免重复解析和重复评分。

缓存 Key 示例：

```text
resume:parse:{file_hash}
resume:extract:{file_hash}
resume:match:{file_hash}:{jd_hash}
```

如本地未启动 Redis，系统应允许通过配置关闭缓存，保证核心流程仍可运行。

### 2.6 前端页面

前端采用 React + Vite 构建单页应用，包含：

- PDF 简历上传区
- 岗位 JD 输入区
- 一键分析按钮
- 候选人信息卡片
- 技能标签展示
- 匹配评分展示
- AI 候选人评价报告
- 风险点与面试追问建议
- 原始 JSON 返回结果展示
- 最近分析记录展示

---

## 3. 技术选型

### 3.1 后端技术栈

| 技术 | 用途 | 选择原因 |
|---|---|---|
| Python | 后端开发语言 | 符合题目要求，生态成熟，适合 AI 服务集成 |
| FastAPI | RESTful API 框架 | 支持类型校验、自动文档、异步能力，工程结构清晰 |
| Pydantic | 参数校验与数据模型 | 与 FastAPI 原生集成，减少重复造轮子 |
| PyMuPDF / pdfplumber | PDF 文本解析 | 适合文本型 PDF 简历解析 |
| SQLite | MVP 数据存储 | 轻量、易部署，适合面试作业与本地演示 |
| Redis | 缓存解析和评分结果 | 避免重复调用 AI，提高性能并体现工程深度 |
| Docker | 本地运行环境 | 降低环境差异，便于评审快速启动 |
| 阿里云函数计算 FC | 后端部署目标 | 符合题目指定 Serverless 运行环境 |

### 3.2 前端技术栈

| 技术 | 用途 | 选择原因 |
|---|---|---|
| React | 前端页面开发 | 生态成熟，适合构建交互页面 |
| Vite | 前端构建工具 | 启动快、配置简单、适合 MVP |
| GitHub Pages | 前端部署 | 免费、公开访问、适合评审验收 |

### 3.3 AI 模型接入方式

AI 模型采用可配置方式接入，不在代码中强绑定具体供应商。

通过环境变量配置：

```env
AI_PROVIDER=your_ai_provider
AI_API_KEY=your_ai_api_key
AI_BASE_URL=https://api.example.com/v1
AI_MODEL_NAME=your_model_name
```

可接入模型服务包括但不限于：

- 阿里云百炼 / 通义千问
- DeepSeek
- 豆包
- OpenAI
- 其他兼容 OpenAI SDK 风格的模型服务

---

## 4. 项目目录结构

```text
ai-resume-analyzer/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI 应用入口
│   │   ├── core/                    # 核心配置与基础能力
│   │   │   ├── config.py            # 环境变量与配置读取
│   │   │   ├── response.py          # 统一响应结构
│   │   │   ├── errors.py            # 自定义异常与错误码
│   │   │   ├── logging.py           # 日志配置
│   │   │   └── middleware.py        # 请求日志、CORS 中间件
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── routes.py        # v1 路由聚合
│   │   │       ├── health.py        # 健康检查接口
│   │   │       ├── resumes.py       # 简历上传与解析接口
│   │   │       ├── match.py         # 岗位匹配接口
│   │   │       └── analysis.py      # 分析记录查询接口
│   │   ├── schemas/                 # Pydantic 请求与响应模型
│   │   │   ├── resume.py            # 简历相关 Schema
│   │   │   └── match.py             # 匹配相关 Schema
│   │   ├── services/                # 业务服务层
│   │   │   ├── ai_client.py         # AI 模型调用封装（含重试）
│   │   │   ├── pdf_parser.py        # PDF 文本提取与清洗
│   │   │   ├── resume_extractor.py  # 简历信息提取（AI + 正则兜底）
│   │   │   ├── jd_analyzer.py       # 岗位 JD 分析
│   │   │   ├── match_scorer.py      # 匹配评分引擎
│   │   │   └── cache_service.py     # Redis 缓存服务
│   │   ├── models/
│   │   │   └── database.py          # SQLite 数据库初始化
│   │   ├── repositories/            # 数据访问层
│   │   │   ├── resume_repository.py
│   │   │   └── analysis_repository.py
│   │   └── utils/
│   │       └── file_validator.py    # 文件校验工具
│   ├── storage/
│   │   ├── uploads/                 # 本地上传文件目录
│   │   └── app.db                   # SQLite 数据库文件
│   ├── tests/                       # 测试用例
│   │   ├── conftest.py
│   │   └── test_api.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                  # 主应用组件
│   │   ├── main.jsx                 # 入口文件
│   │   ├── api/
│   │   │   └── client.js            # API 请求封装
│   │   ├── components/
│   │   │   ├── UploadArea.jsx       # 简历上传组件
│   │   │   ├── JDInput.jsx          # JD 输入组件
│   │   │   ├── CandidateCard.jsx    # 候选人信息卡片
│   │   │   ├── SkillTags.jsx        # 技能标签展示
│   │   │   ├── ScoreCard.jsx        # 匹配评分展示
│   │   │   ├── AIReport.jsx         # AI 评价报告
│   │   │   ├── JSONViewer.jsx       # JSON 原始结果
│   │   │   └── HistoryList.jsx      # 历史记录列表
│   │   └── styles/
│   │       └── App.css              # 全局样式
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
│
├── .github/
│   └── workflows/
│       └── deploy-frontend.yml      # GitHub Pages 自动部署
│
├── .gitignore
├── README.md
├── PRD.md
└── plan.md
│
└── README.md
```

---

## 5. 环境要求

### 5.1 后端环境

- Python >= 3.10
- pip >= 23.x
- Docker >= 24.x，推荐
- Docker Compose >= 2.x，推荐
- Redis >= 6.x，使用 Docker Compose 启动即可

### 5.2 前端环境

- Node.js >= 18
- npm >= 9

---

## 6. 环境变量配置

后端目录下需要提供 `.env.example` 文件。

示例：

```env
APP_NAME=ai-resume-analyzer
APP_ENV=development
APP_DEBUG=true

API_PREFIX=/api/v1

AI_PROVIDER=your_ai_provider
AI_API_KEY=your_ai_api_key
AI_BASE_URL=https://api.example.com/v1
AI_MODEL_NAME=your_model_name

CACHE_ENABLED=true
REDIS_URL=redis://redis:6379/0

STORAGE_DRIVER=local
UPLOAD_DIR=./storage/uploads

DATABASE_URL=sqlite:///./storage/app.db

CORS_ALLOW_ORIGINS=http://localhost:5173
```

本地开发时复制一份：

```bash
cp .env.example .env
```

注意：

- `.env` 不允许提交到 Git 仓库
- 不允许在代码中硬编码 API Key
- README 中不展示真实 API Key
- 日志中不输出 API Key、完整简历文本、手机号、邮箱等敏感信息

---

## 7. 后端启动方式

### 7.1 推荐方式：Docker Compose 启动

进入后端目录：

```bash
cd backend
```

复制环境变量文件：

```bash
cp .env.example .env
```

启动后端与 Redis：

```bash
docker compose up --build
```

服务启动后访问：

```text
http://localhost:8000
```

API 文档地址：

```text
http://localhost:8000/docs
```

健康检查：

```text
http://localhost:8000/api/v1/health
```

### 7.2 本地 Python 启动

进入后端目录：

```bash
cd backend
```

创建虚拟环境：

```bash
python -m venv .venv
```

激活虚拟环境：

macOS / Linux：

```bash
source .venv/bin/activate
```

Windows：

```bash
.venv\Scripts\activate
```

安装依赖：

```bash
pip install -r requirements.txt
```

启动服务：

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 8. 前端启动方式

进入前端目录：

```bash
cd frontend
```

安装依赖：

```bash
npm install
```

启动开发服务：

```bash
npm run dev
```

默认访问地址：

```text
http://localhost:5173
```

---

## 9. 前端部署到 GitHub Pages

构建前端：

```bash
cd frontend
npm run build
```

部署方式建议：

- 使用 `gh-pages` 分支部署
- 或使用 GitHub Actions 自动构建并发布
- Vite 项目需要根据仓库名配置 `base`

如果仓库名为 `ai-resume-analyzer`，`vite.config.js` 中建议配置：

```js
export default {
  base: '/ai-resume-analyzer/'
}
```

前端线上演示地址：

```text
待补充：FRONTEND_DEMO_URL
```

---

## 10. 后端部署到阿里云函数计算 FC

后端目标部署平台为阿里云函数计算 FC。

部署前需要确认：

- 已开通阿里云函数计算 FC
- 已配置 Python 运行环境
- 已配置 HTTP 触发器
- 已设置环境变量
- 已确认依赖安装方式
- 已确认上传文件临时目录策略
- 已确认 Redis 是否使用云 Redis 或关闭缓存
- 已确认后端 API 可公网访问

后端公网地址：

```text
待补充：BACKEND_API_URL
```

MVP 阶段允许先使用 Docker 本地运行完成评审演示；正式提交时，如果已部署阿里云 FC，需要在提交说明中补充公网 API 地址。

---

## 11. API 接口说明

### 11.1 健康检查

```http
GET /api/v1/health
```

成功响应：

```json
{
  "success": true,
  "code": "SUCCESS",
  "message": "ok",
  "data": {
    "status": "healthy"
  },
  "request_id": "req_xxx",
  "timestamp": 1780000000
}
```

---

### 11.2 上传简历

```http
POST /api/v1/resumes/upload
Content-Type: multipart/form-data
```

请求参数：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| file | File | 是 | PDF 简历文件 |

成功响应：

```json
{
  "success": true,
  "code": "SUCCESS",
  "message": "resume uploaded",
  "data": {
    "resume_id": "res_xxx",
    "file_name": "resume.pdf",
    "file_hash": "sha256_xxx"
  },
  "request_id": "req_xxx",
  "timestamp": 1780000000
}
```

---

### 11.3 解析简历

```http
POST /api/v1/resumes/{resume_id}/parse
```

成功响应：

```json
{
  "success": true,
  "code": "SUCCESS",
  "message": "resume parsed",
  "data": {
    "resume_id": "res_xxx",
    "basic_info": {
      "name": "张三",
      "phone": "13800000000",
      "email": "zhangsan@example.com",
      "address": "杭州"
    },
    "job_intention": {
      "position": "Python 后端工程师",
      "expected_salary": "面议",
      "target_city": "杭州"
    },
    "education": [],
    "work_experience": [],
    "projects": [],
    "skills": {
      "languages": ["Python"],
      "frameworks": ["FastAPI"],
      "databases": ["Redis"],
      "cloud": ["Aliyun FC"],
      "ai_tools": ["LLM"]
    },
    "raw_text": "..."
  },
  "request_id": "req_xxx",
  "timestamp": 1780000000
}
```

---

### 11.4 岗位匹配评分

```http
POST /api/v1/match
Content-Type: application/json
```

请求示例：

```json
{
  "resume_id": "res_xxx",
  "job_description": "我们正在招聘 Python 后端工程师，需要熟悉 FastAPI、Redis、Serverless 和 AI 模型调用。"
}
```

成功响应：

```json
{
  "success": true,
  "code": "SUCCESS",
  "message": "匹配成功",
  "data": {
    "analysis_id": "ana_xxx",
    "resume_id": "res_xxx",
    "job_analysis": {
      "job_title": "Python 后端工程师",
      "required_skills": ["Python", "FastAPI", "Redis"],
      "bonus_skills": ["Serverless", "AI 模型调用"],
      "experience_requirements": "1-3 年",
      "education_requirements": "本科及以上",
      "keywords": ["Python", "FastAPI", "Redis", "Serverless", "AI"]
    },
    "match_result": {
      "match_score": 86,
      "score_level": "high",
      "score_items": {
        "skill_match": {"score": 88, "weight": 0.4, "reason": "评分理由"},
        "project_match": {"score": 82, "weight": 0.25, "reason": "评分理由"},
        "experience_match": {"score": 80, "weight": 0.2, "reason": "评分理由"},
        "keyword_coverage": {"score": 90, "weight": 0.15, "reason": "评分理由"}
      },
      "matched_keywords": ["Python", "FastAPI", "AI"],
      "missing_keywords": ["Redis"],
      "risk_points": ["简历中未明确体现 Redis 使用经验"],
      "interview_questions": [
        "请介绍一次你在 FastAPI 项目中的接口设计经验。",
        "你是否在生产环境中使用过 Redis？主要解决什么问题？"
      ],
      "ai_summary": "候选人与岗位整体匹配度较高，具备 Python 后端和 AI 项目经验，但 Redis 经验需要进一步确认。"
    }
  },
  "request_id": "req_xxx",
  "timestamp": 1780000000
}
```

---

### 11.5 查询分析记录

```http
GET /api/v1/analysis/history
```

成功响应：

```json
{
  "success": true,
  "code": "SUCCESS",
  "message": "查询成功",
  "data": [
    {
      "id": "ana_xxx",
      "resume_id": "res_xxx",
      "file_name": "resume.pdf",
      "candidate_name": "张三",
      "job_title": "Python 后端工程师",
      "match_score": 86,
      "score_level": "high",
      "created_at": "2026-07-02 10:00:00"
    }
  ],
  "request_id": "req_xxx",
  "timestamp": 1780000000
}
```

---

## 12. 统一响应格式

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

字段说明：

| 字段 | 说明 |
|---|---|
| success | 是否成功 |
| code | 业务状态码 |
| message | 响应说明 |
| data | 业务数据 |
| request_id | 请求唯一 ID |
| timestamp | 响应时间戳 |

---

## 13. 错误码说明

| 错误码 | 说明 |
|---|---|
| INVALID_FILE_TYPE | 文件类型不合法，仅支持 PDF |
| FILE_TOO_LARGE | 文件超过大小限制 |
| PDF_PARSE_FAILED | PDF 文本解析失败 |
| AI_EXTRACT_FAILED | AI 简历信息提取失败 |
| AI_MATCH_FAILED | AI 岗位匹配失败 |
| MATCH_FAILED | 匹配评分失败 |
| CACHE_UNAVAILABLE | 缓存服务不可用 |
| RESOURCE_NOT_FOUND | 资源不存在 |
| VALIDATION_ERROR | 请求参数校验失败 |
| INTERNAL_ERROR | 服务内部错误 |

错误响应示例：

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

## 14. 工程规范

### 14.1 路由规范

- 所有接口统一使用 `/api/v1` 前缀
- 按模块划分路由文件
- 不允许在 `main.py` 中直接堆叠业务接口
- 新增模块时，必须在 `api/v1/routes.py` 中统一注册

### 14.2 分层规范

后端采用以下分层：

```text
Router / Controller -> Service -> Repository / Model
```

要求：

- Router 只负责请求接收、参数校验、响应返回
- Service 负责业务流程编排
- Repository 负责数据读写
- Model / Schema 负责数据结构定义
- Utils 只存放无业务状态的通用工具函数

### 14.3 错误处理规范

- 所有业务异常必须抛出自定义业务异常
- 所有未捕获异常由全局异常处理器统一处理
- 不允许直接返回框架默认错误结构
- 错误响应必须符合统一响应格式
- 参数校验失败统一返回 `VALIDATION_ERROR`

### 14.4 中间件规范

中间件加载顺序建议：

```text
Request ID Middleware
-> CORS Middleware
-> Request Log Middleware
-> Auth Placeholder Middleware
-> Router
```

MVP 阶段不实现真实登录鉴权，但需要在中间件层保留 Auth 占位，便于后续扩展 HR 登录和权限系统。

### 14.5 日志规范

- 请求进入和响应返回需要记录日志
- 解析失败、AI 调用失败、匹配失败需要记录错误日志
- 日志中不得输出 API Key、完整简历文本、手机号、邮箱等敏感信息
- 每条请求日志应包含 `request_id`
- 日志级别至少包含 `INFO`、`WARNING`、`ERROR`

### 14.6 配置规范

- 所有环境差异配置通过环境变量管理
- 不允许在代码中硬编码 API Key
- `.env` 不允许提交到 Git 仓库
- `.env.example` 必须保留在仓库中

### 14.7 模块扩容规范

新增业务模块时，应遵守以下结构：

```text
api/v1/{module}.py
schemas/{module}.py
services/{module}_service.py
repositories/{module}_repository.py
models/{module}.py
```

命名要求：

- 路由文件使用复数或业务名，例如 `resumes.py`
- Service 文件使用 `{module}_service.py`
- Repository 文件使用 `{module}_repository.py`
- Schema 文件按模块拆分，避免所有模型堆在一个文件中

---

## 15. 测试方式

### 15.1 测试健康检查

```bash
curl http://localhost:8000/api/v1/health
```

### 15.2 测试文件类型错误

```bash
curl -X POST http://localhost:8000/api/v1/resumes/upload \
  -F "file=@test.txt"
```

预期返回：

```json
{
  "success": false,
  "code": "INVALID_FILE_TYPE",
  "message": "仅支持上传 PDF 文件",
  "data": null
}
```

### 15.3 测试参数校验失败

```bash
curl -X POST http://localhost:8000/api/v1/match \
  -H "Content-Type: application/json" \
  -d "{}"
```

预期返回：

```json
{
  "success": false,
  "code": "VALIDATION_ERROR",
  "message": "请求参数校验失败",
  "data": null
}
```

---

## 16. 自动化测试

项目包含 15 个接口测试用例，覆盖全部 API 端点。

运行测试：

```bash
cd backend
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
python -m pytest tests/ -v
```

测试覆盖：

| 测试项 | 说明 |
|---|---|
| 健康检查 | GET /api/v1/health |
| 文件类型错误 | 上传非 PDF 文件 |
| 上传成功 | 上传 PDF 并返回 resume_id |
| 重复上传 | 相同文件返回同一 resume_id |
| 解析不存在 | 404 RESOURCE_NOT_FOUND |
| 解析成功 | PDF 文本提取 + AI 信息提取 |
| 匹配不存在 | 404 RESOURCE_NOT_FOUND |
| 匹配未解析 | 简历未 parse 时报错 |
| 匹配成功 | 规则评分 + AI 评分 |
| 参数校验 | 缺少必填参数返回 422 |
| 历史记录 | 分页查询 |
| 分析详情 | 含 resume_data 关联 |
| 页数超限 | 超过 5 页 PDF 拦截 |

---

## 17. 当前版本范围

### 16.1 MVP 必须完成

- PDF 简历上传
- PDF 文本解析
- AI 信息提取
- 岗位 JD 输入
- 岗位关键词提取
- 简历匹配评分
- SQLite 保存分析记录
- Redis 缓存解析与评分结果
- 结构化 JSON 返回
- 统一响应格式
- 基础错误处理
- 前端分析页面
- 前端 GitHub Pages 部署
- README 使用说明

### 16.2 增强项

- 风险点提示
- 面试追问建议
- AI 综合评价报告
- 前端 JSON 原始结果展示
- 最近分析记录展示
- Docker Compose 一键启动后端与 Redis

### 16.3 暂不实现

- 登录注册
- HR 权限系统
- 企业多租户
- 批量简历上传
- 候选人长期管理
- 面试流程管理
- Offer 管理

---

## 17. 给面试官的提交说明模板

```text
您好，我已完成 AI 智能简历分析与岗位匹配系统的开发与部署，相关信息如下：

GitHub 仓库地址：
https://github.com/你的用户名/ai-resume-analyzer

前端线上演示地址：
待补充

后端 API 地址：
待补充

项目说明：
本项目支持 PDF 简历上传、简历文本解析、AI 结构化信息提取、岗位 JD 关键词分析、简历匹配评分、JSON 结果返回和前端可视化展示。后端采用 Python + FastAPI，支持 Docker 本地运行，并预留阿里云函数计算 FC 部署；前端采用 React + Vite，并部署到 GitHub Pages。

姓名：
待补充

联系方式：
待补充
```

---

## 18. 变动留痕

| 日期 | 变动内容 | 原因 |
|---|---|---|
| 2026-07-02 | 初始化 README | 明确项目启动、接口、部署和验收方式 |
| 2026-07-02 | 固化项目名为 ai-resume-analyzer | 与用户确认后的仓库命名一致 |
| 2026-07-02 | AI 模型改为可配置供应商 | 避免绑定单一模型，提升可扩展性 |
| 2026-07-02 | 存储方案确定为 SQLite + Redis | 兼顾 MVP 交付效率与缓存加分项 |
| 2026-07-02 | 前端部署确定为 GitHub Pages | 满足公网演示与评审验收 |
| 2026-07-02 | 后端运行方式确定为 Docker 本地运行 + 阿里云 FC 预留 | 降低本地环境差异，并符合 Serverless 部署目标 |

---

## 19. 后续规划

后续可扩展能力包括：

- 支持批量上传多份简历
- 支持岗位模板管理
- 支持候选人历史库
- 支持 HR 登录与权限控制
- 支持多企业 / 多租户隔离
- 支持扫描版 PDF OCR 识别
- 支持更多 AI 模型供应商切换
- 支持更细粒度的评分解释和面试题生成
