const LEVEL_LABELS = {
  high: '高度匹配',
  medium: '中等匹配',
  low: '匹配度低',
}

const LEVEL_COLORS = {
  high: '#52c41a',
  medium: '#faad14',
  low: '#ff4d4f',
}

const ITEM_LABELS = {
  skill_match: '技能匹配度',
  project_match: '项目经验匹配度',
  experience_match: '工作背景匹配度',
  keyword_coverage: '关键词覆盖度',
}

export default function ScoreCard({ matchResult }) {
  if (!matchResult) return null

  const { match_score, score_level, score_items, matched_keywords, missing_keywords } = matchResult

  return (
    <div className="score-card">
      <h3>📊 匹配评分</h3>

      {/* 总分 */}
      <div className="total-score">
        <span className="score-number" style={{ color: LEVEL_COLORS[score_level] }}>
          {match_score}
        </span>
        <span className="score-label">/ 100</span>
        <span className="score-level" style={{ background: LEVEL_COLORS[score_level] }}>
          {LEVEL_LABELS[score_level] || score_level}
        </span>
      </div>

      {/* 分项评分 */}
      {score_items && (
        <div className="score-items">
          {Object.entries(score_items).map(([key, item]) => (
            <div key={key} className="score-item">
              <div className="score-item-header">
                <span className="score-item-name">{ITEM_LABELS[key] || key}</span>
                <span className="score-item-value">{item.score}</span>
              </div>
              <div className="score-bar-bg">
                <div
                  className="score-bar-fill"
                  style={{
                    width: `${item.score}%`,
                    background: item.score >= 75 ? '#52c41a' : item.score >= 50 ? '#faad14' : '#ff4d4f',
                  }}
                />
              </div>
              <span className="score-item-weight">权重 {(item.weight * 100).toFixed(0)}%</span>
            </div>
          ))}
        </div>
      )}

      {/* 关键词 */}
      <div className="keywords-section">
        {matched_keywords?.length > 0 && (
          <div className="keyword-group">
            <span className="keyword-label">✅ 匹配关键词：</span>
            {matched_keywords.map((kw, i) => (
              <span key={i} className="keyword-tag matched">{kw}</span>
            ))}
          </div>
        )}
        {missing_keywords?.length > 0 && (
          <div className="keyword-group">
            <span className="keyword-label">❌ 缺失关键词：</span>
            {missing_keywords.map((kw, i) => (
              <span key={i} className="keyword-tag missing">{kw}</span>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
