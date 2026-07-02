export default function HistoryList({ items, onSelect }) {
  if (!items || items.length === 0) {
    return (
      <div className="history-section">
        <h3>📋 最近分析记录</h3>
        <p className="placeholder-text">暂无记录</p>
      </div>
    )
  }

  return (
    <div className="history-section">
      <h3>📋 最近分析记录</h3>
      <div className="history-table-wrap">
        <table className="history-table">
          <thead>
            <tr>
              <th>候选人</th>
              <th>文件名</th>
              <th>岗位</th>
              <th>评分</th>
              <th>等级</th>
              <th>时间</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr
                key={item.id}
                className="history-row"
                onClick={() => onSelect?.(item.id)}
              >
                <td>{item.candidate_name || '-'}</td>
                <td>{item.file_name || '-'}</td>
                <td>{item.job_title || '-'}</td>
                <td className="score-cell">{item.match_score ?? '-'}</td>
                <td>
                  <span className={`level-badge level-${item.score_level}`}>
                    {item.score_level === 'high' ? '高' : item.score_level === 'medium' ? '中' : item.score_level === 'low' ? '低' : '-'}
                  </span>
                </td>
                <td className="time-cell">{item.created_at || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
