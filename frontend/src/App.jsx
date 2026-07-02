import { useState, useEffect, useCallback } from 'react'
import { apiClient } from './api/client'
import UploadArea from './components/UploadArea'
import JDInput from './components/JDInput'
import CandidateCard from './components/CandidateCard'
import SkillTags from './components/SkillTags'
import ScoreCard from './components/ScoreCard'
import AIReport from './components/AIReport'
import JSONViewer from './components/JSONViewer'
import HistoryList from './components/HistoryList'
import './styles/App.css'

function App() {
  const [file, setFile] = useState(null)
  const [jd, setJd] = useState('')
  const [loading, setLoading] = useState(false)
  const [loadingText, setLoadingText] = useState('')
  const [error, setError] = useState('')
  const [parseResult, setParseResult] = useState(null)
  const [matchResult, setMatchResult] = useState(null)
  const [history, setHistory] = useState([])

  const loadHistory = useCallback(async () => {
    try {
      const res = await apiClient.getHistory()
      setHistory(res.data || [])
    } catch {
      // 静默失败
    }
  }, [])

  useEffect(() => {
    loadHistory()
  }, [loadHistory])

  const handleAnalyze = async () => {
    if (!file) return

    setLoading(true)
    setError('')
    setParseResult(null)
    setMatchResult(null)

    try {
      // Step 1: 上传
      setLoadingText('正在上传简历...')
      const uploadRes = await apiClient.uploadResume(file)
      const resumeId = uploadRes.data.resume_id

      // Step 2: 解析
      setLoadingText('正在解析简历（AI 信息提取）...')
      const parseRes = await apiClient.parseResume(resumeId)
      setParseResult(parseRes.data)

      // Step 3: 匹配（如果有 JD）
      if (jd.trim()) {
        setLoadingText('正在匹配评分...')
        const matchRes = await apiClient.match(resumeId, jd)
        setMatchResult(matchRes.data.match_result)
      }

      // 刷新历史记录
      loadHistory()
    } catch (err) {
      setError(err.message || '分析失败，请重试')
    } finally {
      setLoading(false)
      setLoadingText('')
    }
  }

  const handleHistorySelect = async (analysisId) => {
    try {
      const res = await apiClient.getAnalysis(analysisId)
      const data = res.data
      // 恢复候选人信息
      if (data.resume_data) {
        setParseResult(data.resume_data)
      }
      // 恢复匹配结果
      if (data.job_analysis && data.match_result) {
        setMatchResult(data.match_result)
      }
    } catch {
      // 静默失败
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>AI 智能简历分析系统</h1>
        <p>上传 PDF 简历，输入岗位 JD，快速生成候选人匹配报告</p>
      </header>

      <main className="app-main">
        {/* 输入区 */}
        <section className="input-section">
          <UploadArea onUpload={setFile} disabled={loading} />
          <JDInput value={jd} onChange={setJd} disabled={loading} />
          <button
            className="analyze-btn"
            onClick={handleAnalyze}
            disabled={!file || loading}
          >
            {loading && <span className="spinner" />}
            {loading ? loadingText : '开始分析'}
          </button>
          {error && <p className="error-text global-error">{error}</p>}
        </section>

        {/* 结果区 */}
        {(parseResult || matchResult) && (
          <section className="result-section">
            <h2>分析结果</h2>

            <CandidateCard
              basicInfo={parseResult?.basic_info}
              jobIntention={parseResult?.job_intention}
              education={parseResult?.education}
            />

            <SkillTags skills={parseResult?.skills} />

            {matchResult && (
              <>
                <ScoreCard matchResult={matchResult} />
                <AIReport matchResult={matchResult} />
              </>
            )}

            <JSONViewer data={matchResult || parseResult} />
          </section>
        )}

        {/* 历史记录 */}
        <HistoryList items={history} onSelect={handleHistorySelect} />
      </main>
    </div>
  )
}

export default App
