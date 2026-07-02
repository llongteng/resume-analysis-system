import { useState } from 'react'

export default function JSONViewer({ data }) {
  const [expanded, setExpanded] = useState(false)

  if (!data) return null

  const formatted = JSON.stringify(data, null, 2)

  return (
    <div className="json-viewer">
      <div className="json-header" onClick={() => setExpanded(!expanded)}>
        <h3>{'{ }'} 原始 JSON 结果</h3>
        <span className="toggle-icon">{expanded ? '▼' : '▶'}</span>
      </div>
      {expanded && (
        <pre className="json-content">
          <code>{formatted}</code>
        </pre>
      )}
    </div>
  )
}
