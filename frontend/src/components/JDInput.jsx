export default function JDInput({ value, onChange, disabled }) {
  return (
    <div className="jd-area">
      <h3>💼 岗位 JD</h3>
      <p className="hint">粘贴岗位描述（可选，为空时仅解析简历）</p>
      <textarea
        className="jd-input"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="请输入岗位需求描述，例如：&#10;招聘 Python 后端开发工程师，要求熟悉 FastAPI、MySQL、Redis，了解 Serverless 架构..."
        rows={6}
        disabled={disabled}
      />
    </div>
  )
}
