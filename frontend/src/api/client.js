const API_PREFIX = import.meta.env.VITE_API_BASE_URL || '/api/v1'
const IS_DEMO = import.meta.env.VITE_DEMO_MODE === 'true'

// Mock 数据
const MOCK_DATA = {
  health: { success: true, data: { status: 'healthy', version: '1.0.0' } },
  history: {
    success: true,
    data: [
      {
        id: 'demo-001',
        candidate_name: '张三',
        file_name: '张三_前端工程师.pdf',
        job_title: '高级前端工程师',
        match_score: 85,
        score_level: 'high',
        created_at: '2024-01-15 10:30:00'
      },
      {
        id: 'demo-002',
        candidate_name: '李四',
        file_name: '李四_后端工程师.pdf',
        job_title: 'Python 后端开发',
        match_score: 72,
        score_level: 'medium',
        created_at: '2024-01-14 15:20:00'
      },
      {
        id: 'demo-003',
        candidate_name: '王五',
        file_name: '王五_全栈工程师.pdf',
        job_title: '全栈开发工程师',
        match_score: 91,
        score_level: 'high',
        created_at: '2024-01-13 09:15:00'
      }
    ]
  },
  analysis: {
    success: true,
    data: {
      id: 'demo-001',
      resume_data: {
        basic_info: {
          name: '张三',
          phone: '13800138000',
          email: 'zhangsan@example.com',
          address: '北京市朝阳区'
        },
        job_intention: {
          target_position: '高级前端工程师',
          expected_salary: '25-35K',
          target_city: '北京'
        },
        education: [
          {
            school: '北京大学',
            degree: '本科',
            major: '计算机科学与技术',
            start_date: '2016-09',
            end_date: '2020-06'
          }
        ],
        work_experience: [
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
      job_analysis: {
        title: '高级前端工程师',
        requirements: ['5年以上前端开发经验', '精通 React/Vue', '熟悉 TypeScript', '有大型项目经验']
      },
      match_result: {
        match_score: 85,
        score_level: 'high',
        score_items: {
          skill_match: { score: 90, weight: 0.4 },
          project_match: { score: 75, weight: 0.25 },
          experience_match: { score: 80, weight: 0.2 },
          keyword_coverage: { score: 88, weight: 0.15 }
        },
        matched_keywords: ['React', 'TypeScript', 'JavaScript', 'Vue', 'Webpack', 'Node.js'],
        missing_keywords: ['Next.js', '微前端', 'SSR'],
        ai_summary: '张三是一位经验丰富的前端工程师，在字节跳动有 3 年以上的工作经验。技术栈全面，覆盖主流前端框架，有大型项目经验。整体匹配度较高，建议进入面试环节。',
        risk_points: ['缺少 Next.js 等 SSR 框架经验', '微前端架构经验不足'],
        interview_questions: ['请介绍一下你在字节跳动负责的最大的项目', '你如何处理大型项目的性能优化？', '对微前端架构有什么了解？']
      }
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
          resume_id: 'demo-' + Date.now(),
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
        data: MOCK_DATA.analysis.data.resume_data
      }
    }
    if (url.includes('/match')) {
      return {
        success: true,
        data: {
          match_result: MOCK_DATA.analysis.data.match_result
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
