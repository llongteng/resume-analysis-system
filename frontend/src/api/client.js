const API_PREFIX = import.meta.env.VITE_API_BASE_URL || '/api/v1'

class ApiClient {
  async request(url, options = {}) {
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
