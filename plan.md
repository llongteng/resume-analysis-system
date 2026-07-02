阶段一：项目初始化与基础框架 (预计 1-2 小时)

1.1 项目目录结构搭建
- 创建 backend/ 和 frontend/ 目录
- 按 README 规范创建后端分层目录结构
- 初始化 Git 仓库、.gitignore

1.2 后端基础框架
- 创建 requirements.txt (FastAPI, uvicorn, pydantic, python-multipart 等)
- 搭建 FastAPI 应用入口 main.py
- 实现核心模块:
  - core/config.py — 环境变量配置读取
  - core/response.py — 统一响应格式封装
  - core/errors.py — 自定义异常与错误码枚举
  - core/middleware.py — Request ID、CORS、请求日志中间件
- 实现健康检查接口 GET /api/v1/health
- 创建 .env.example

1.3 前端基础框架
- 使用 Vite 初始化 React 项目
- 配置 vite.config.js (base 路径、代理)
- 搭建基础页面骨架

---
阶段二：简历上传与 PDF 解析 (预计 2-3 小时)

2.1 简历上传功能
- 实现 POST /api/v1/resumes/upload 接口
- 文件类型校验 (MIME + 扩展名双重校验)
- 文件大小校验 (≤10MB)
- PDF 页数校验 (≤5页)
- 文件存储到 storage/uploads/，生成 resume_id 和 file_hash
- SQLite resumes 表设计与 Repository 层实现

2.2 PDF 文本解析功能
- 集成 PyMuPDF 或 pdfplumber
- 实现多页 PDF 文本提取
- 文本清洗逻辑 (去冗余空格、合并断行、保留关键信息)
- 实现 POST /api/v1/resumes/{resume_id}/parse 接口
- 缓存解析结果 (resume:parse:{file_hash})

---
阶段三：AI 信息提取 (预计 2-3 小时)

3.1 AI 客户端封装
- 实现 services/ai_client.py — 可配置的 AI 模型调用封装
- 支持 OpenAI SDK 风格接口 (兼容通义千问/DeepSeek/豆包等)
- 超时控制、重试机制

3.2 简历信息提取
- 设计简历提取 Prompt (要求严格 JSON 输出)
- 实现 services/resume_extractor.py
- 提取字段: basic_info, job_intention, education, work_experience, projects, skills, summary
- 正则兜底逻辑 (AI 失败时提取手机号/邮箱/学历/技能关键词)
- 缓存提取结果 (resume:extract:{file_hash})

3.3 岗位 JD 分析
- 设计 JD 分析 Prompt
- 实现 services/jd_analyzer.py
- 提取: job_title, required_skills, bonus_skills, experience_requirements, keywords

---
阶段四：匹配评分引擎 (预计 2-3 小时)

4.1 规则评分模块
- 实现 services/match_scorer.py
- 技能匹配度评分 (40%) — 必备技能 + 加分技能覆盖率
- 项目经验匹配度评分 (25%) — 项目与 JD 场景相关性
- 工作背景匹配度评分 (20%) — 年限、岗位、行业匹配
- 关键词覆盖度评分 (15%) — 简历覆盖 JD 关键词比例

4.2 AI 综合评分
- 设计匹配评分 Prompt
- AI 输出: 综合分、分项分、匹配/缺失关键词、风险点、面试追问建议、综合评价
- 规则评分 + AI 评分加权融合

4.3 匹配接口实现
- 实现 POST /api/v1/match 接口
- SQLite analysis_records 表与 Repository 层
- 缓存匹配结果 (resume:match:{file_hash}:{jd_hash})

---
阶段五：历史记录与缓存 (预计 1 小时)

5.1 历史记录接口
- 实现 GET /api/v1/analysis/history 接口
- 实现 GET /api/v1/analysis/{analysis_id} 接口

5.2 Redis 缓存集成
- 实现 services/cache_service.py
- 支持缓存开关配置 (CACHE_ENABLED)
- Redis 不可用时自动降级为实时计算

---
阶段六：前端页面开发 (预计 3-4 小时)

6.1 页面模块
- 顶部标题区
- 简历上传组件 (拖拽/选择、文件信息展示、格式校验提示)
- JD 输入区 (多行文本、支持为空)
- 分析按钮 (加载状态管理)

6.2 结果展示模块
- 候选人信息卡片
- 技能标签区 (分类标签展示)
- 匹配评分区 (总分 + 分项评分 + 权重说明)
- AI 评价报告 (综合评价、风险点、面试追问)
- JSON 原始结果展示区
- 历史记录列表

6.3 前端 API 对接
- 封装 API 请求层
- 对接上传、解析、匹配、历史记录接口
- 错误处理与 loading 状态

---
阶段七：Docker 与部署 (预计 1-2 小时)

7.1 Docker 配置
- 编写 Dockerfile
- 编写 docker-compose.yml (后端 + Redis)
- 本地 Docker 启动测试

7.2 前端部署准备
- GitHub Actions 自动构建配置
- GitHub Pages 部署配置

7.3 后端部署准备
- 阿里云 FC 部署配置说明

---
阶段八：测试与文档 (预计 1-2 小时)

8.1 接口测试
- 健康检查测试
- 文件类型错误测试
- 参数校验失败测试
- 完整流程测试 (上传 → 解析 → 匹配)

8.2 文档完善
- 完善 README.md
- API 示例补充
- 部署说明补充

---
总结

┌──────┬──────────────────────┬──────────┐
│ 阶段 │         内容         │ 预计耗时 │
├──────┼──────────────────────┼──────────┤
│ 一   │ 项目初始化与基础框架 │ 1-2h     │
├──────┼──────────────────────┼──────────┤
│ 二   │ 简历上传与 PDF 解析  │ 2-3h     │
├──────┼──────────────────────┼──────────┤
│ 三   │ AI 信息提取          │ 2-3h     │
├──────┼──────────────────────┼──────────┤
│ 四   │ 匹配评分引擎         │ 2-3h     │
├──────┼──────────────────────┼──────────┤
│ 五   │ 历史记录与缓存       │ 1h       │
├──────┼──────────────────────┼──────────┤
│ 六   │ 前端页面开发         │ 3-4h     │
├──────┼──────────────────────┼──────────┤
│ 七   │ Docker 与部署        │ 1-2h     │
├──────┼──────────────────────┼──────────┤
│ 八   │ 测试与文档           │ 1-2h     │
├──────┼──────────────────────┼──────────┤
│ 合计 │                      │ 13-20h   │
└──────┴──────────────────────┴──────────┘

开发顺序: 后端先行 (阶段一→五)，确保核心 API 可用后再开发前端 (阶段六)，最后处理部署和文档 (阶段七→八)。