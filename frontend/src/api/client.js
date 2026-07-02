const API_PREFIX = import.meta.env.VITE_API_BASE_URL || '/api/v1'
const IS_DEMO = import.meta.env.VITE_DEMO_MODE === 'true'

// Mock 数据
const MOCK_DATA = {
  health: { success: true, data: { status: 'healthy', version: '1.0.0' } },
  history: {
    success: true,
    data: {
      analyses: [
        {
          id: 'demo-001',
          resume_name: '张三_前端工程师.pdf',
          job_title: '高级前端工程师',
          match_score: 85,
          created_at: '2024-01-15T10:30:00Z',
          status: 'completed'
        },
        {
          id: 'demo-002',
          resume_name: '李四_后端工程师.pdf',
          job_title: 'Python 后端开发',
          match_score: 72,
          created_at: '2024-01-14T15:20:00Z',
          status: 'completed'
        },
        {
          id: 'demo-003',
          resume_name: '王五_全栈工程师.pdf',
          job_title: '全栈开发工程师',
          match_score: 91,
          created_at: '2024-01-13T09:15:00Z',
          status: 'completed'
        }
      ],
      total: 3,
      page: 1,
      page_size: 10
    }
  },
  analysis: {
    success: true,
    data: {
      id: 'demo-001',
      resume: {
        name: '张三',
        email: 'zhangsan@example.com',
        phone: '13800138000',
        education: [
          {
            school: '北京大学',
            degree: '本科',
            major: '计算机科学与技术',
            start_date: '2016-09',
            end_date: '2020-06'
          }
        ],
        experience: [
          {
            company: '字节跳动',
            position: '前端工程师',
            start_date: '2020-07',
            end_date: '2024-01',
            description: '负责抖音 Web 端开发，使用 React + TypeScript'
          }
        ],
        skills: ['React', 'TypeScript', 'JavaScript', 'Node.js', 'Vue', 'Webpack', 'Git']
      },
      job_description: '高级前端工程师\n\n要求：\n- 5年以上前端开发经验\n- 精通 React/Vue\n- 熟悉 TypeScript\n- 有大型项目经验',
      match_result: {
        overall_score: 85,
        dimension_scores: {
          skills_match: 90,
          experience_match: 80,
          education_match: 85,
          project_match: 75
        },
        matched_skills: ['React', 'TypeScript', 'JavaScript', 'Vue', 'Webpack'],
        missing_skills: ['Next.js', '微前端'],
        recommendations: [
          '候选人技术栈与岗位需求高度匹配',
          '建议关注候选人在大型项目中的架构设计能力',
          '可以进一步了解候选人的团队协作经验'
        ]
      },
      ai_report: '## 综合评估\n\n张三是一位经验丰富的前端工程师，在字节跳动有 3 年以上的工作经验。\n\n### 优势\n- 技术栈全面，覆盖主流前端框架\n- 大厂背景，有大型项目经验\n- 持续学习新技术\n\n### 待提升\n- 缺少 Next.js 等 SSR 框架经验\n- 微前端架构经验不足\n\n### 建议\n整体匹配度较高，建议进入面试环节。',
      created_at: '2024-01-15T10:30:00Z'
    }
  }
}

// 模拟延迟
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms))

class ApiClient {
  async request(url, options = {}) {
    // Demo 模式返回 mock 数据
    if (IS_DEMO) {
      await delay(500) // 模拟网络延迟
      return this.getMockData(url)
    }

    const response = await fetch(`${API_PREFIX}${url}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    })

    const data = await response.json()

    if (!data.success) {
      throw new ApiError(data.code, data.message)
    }

    return data
  }

  async upload(url, formData) {
    // Demo 模式返回 mock 数据
    if (IS_DEMO) {
      await delay(800)
      return {
        success: true,
        data: {
          id: 'demo-' + Date.now(),
          filename: 'demo-resume.pdf',
          status: 'uploaded'
        }
      }
    }

    const response = await fetch(`${API_PREFIX}${url}`, {
      method: 'POST',
      body: formData,
    })

    const data = await response.json()

    if (!data.success) {
      throw new ApiError(data.code, data.message)
    }

    return data
  }

  getMockData(url) {
    if (url.includes('/health')) {
      return MOCK_DATA.health
    }
    if (url.includes('/analysis/history')) {
      return MOCK_DATA.history
    }
    if (url.includes('/analysis/')) {
      return MOCK_DATA.analysis
    }
    if (url.includes('/resumes/') && url.includes('/parse')) {
      return {
        success: true,
        data: {
          id: 'demo-parsed',
          status: 'parsed',
          resume: MOCK_DATA.analysis.data.resume
        }
      }
    }
    if (url.includes('/match')) {
      return {
        success: true,
        data: {
          match_result: MOCK_DATA.analysis.data.match_result,
          ai_report: MOCK_DATA.analysis.data.ai_report
        }
      }
    }
    return { success: true, data: {} }
  }

  // 健康检查
  health() {
    return this.request('/health')
  }

  // 上传简历
  uploadResume(file) {
    const formData = new FormData()
    formData.append('file', file)
    return this.upload('/resumes/upload', formData)
  }

  // 解析简历
  parseResume(resumeId) {
    return this.request(`/resumes/${resumeId}/parse`, { method: 'POST' })
  }

  // 岗位匹配
  match(resumeId, jobDescription) {
    return this.request('/match', {
      method: 'POST',
      body: JSON.stringify({ resume_id: resumeId, job_description: jobDescription }),
    })
  }

  // 查询历史记录
  getHistory() {
    return this.request('/analysis/history')
  }

  // 查询分析详情
  getAnalysis(analysisId) {
    return this.request(`/analysis/${analysisId}`)
  }
}

class ApiError extends Error {
  constructor(code, message) {
    super(message)
    this.code = code
    this.name = 'ApiError'
  }
}

export const apiClient = new ApiClient()
export { ApiError }
