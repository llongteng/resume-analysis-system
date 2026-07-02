export default function AIReport({ matchResult }) {
  if (!matchResult) return null

  const { ai_summary, risk_points, interview_questions } = matchResult

  if (!ai_summary && !risk_points?.length && !interview_questions?.length) return null

  return (
    <div className="ai-report">
      <h3>🤖 AI 评价报告</h3>

      {ai_summary && (
        <div className="report-section">
          <h4>综合评价</h4>
          <p className="summary-text">{ai_summary}</p>
        </div>
      )}

      {risk_points?.length > 0 && (
        <div className="report-section">
          <h4>⚠️ 风险点</h4>
          <ul className="risk-list">
            {risk_points.map((point, i) => (
              <li key={i}>{point}</li>
            ))}
          </ul>
        </div>
      )}

      {interview_questions?.length > 0 && (
        <div className="report-section">
          <h4>💡 面试追问建议</h4>
          <ol className="question-list">
            {interview_questions.map((q, i) => (
              <li key={i}>{q}</li>
            ))}
          </ol>
        </div>
      )}
    </div>
  )
}
