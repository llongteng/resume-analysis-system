# 部署指南

## 架构说明

- **前端**: Vercel (免费静态站点)
- **后端**: Render (免费 Python 服务)
- **AI 模型**: 小米 MiMo

## 第一步：部署后端到 Render

### 1. 注册 Render 账号
访问 https://render.com 并使用 GitHub 账号注册

### 2. 创建 Web Service
1. 点击 "New +" → "Web Service"
2. 连接你的 GitHub 仓库: `llongteng/resume-analysis-system`
3. 配置如下:
   - **Name**: `resume-analyzer-api`
   - **Root Directory**: `backend`
   - **Region**: `Singapore` (亚洲区域)
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 3. 设置环境变量
在 Render 控制台的 "Environment" 选项卡中添加:

| 变量名 | 值 |
|--------|-----|
| `APP_ENV` | `production` |
| `APP_DEBUG` | `false` |
| `AI_PROVIDER` | `openai_compatible` |
| `AI_API_KEY` | `你的小米 MiMo API Key` |
| `AI_BASE_URL` | `https://token-plan-cn.xiaomimimo.com/v1` |
| `AI_MODEL_NAME` | `mimo-v2.5-pro` |
| `AI_TIMEOUT` | `60` |
| `CACHE_ENABLED` | `false` |
| `DATABASE_URL` | `sqlite:///./storage/app.db` |
| `CORS_ALLOW_ORIGINS` | `https://*.vercel.app` |

### 4. 部署
点击 "Create Web Service"，等待部署完成。部署后会得到一个 URL，类似:
```
https://resume-analyzer-api.onrender.com
```

## 第二步：部署前端到 Vercel

### 1. 安装 Vercel CLI
```bash
npm i -g vercel
```

### 2. 登录 Vercel
```bash
vercel login
```

### 3. 部署
在项目根目录运行:
```bash
vercel
```

按照提示操作:
- Set up and deploy? → Y
- Which scope? → 选择你的账号
- Link to existing project? → N
- Project name? → `resume-analysis-system`
- Directory with code? → `./frontend`
- Override settings? → N

### 4. 设置环境变量
```bash
vercel env add VITE_API_BASE_URL
```
输入你的 Render 后端 URL + `/api/v1`，例如:
```
https://resume-analyzer-api.onrender.com/api/v1
```

### 5. 重新部署
```bash
vercel --prod
```

## 第三步：更新 CORS 配置

部署前端后，获取 Vercel 的域名，然后更新 Render 后端的 `CORS_ALLOW_ORIGINS` 环境变量:

```
https://resume-analysis-system.vercel.app,https://resume-analysis-system-*.vercel.app
```

## 测试部署

1. 访问你的 Vercel 域名
2. 上传一份 PDF 简历
3. 输入岗位 JD
4. 点击 "开始分析"

## 常见问题

### Q: Render 免费版会休眠吗？
A: 是的，15 分钟无请求后会休眠，首次请求需要 30-60 秒冷启动。

### Q: 如何查看后端日志？
A: 在 Render 控制台的 "Logs" 选项卡中查看。

### Q: 如何更新部署？
A: 推送代码到 GitHub，Render 和 Vercel 会自动重新部署。

## 获取小米 MiMo API Key

1. 访问小米 MiMo 控制台
2. 开通 API 服务
3. 创建 API Key
4. 在 Render 环境变量中填写 `AI_API_KEY`
