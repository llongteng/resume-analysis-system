import { useState, useRef } from 'react'

export default function UploadArea({ onUpload, disabled }) {
  const [fileName, setFileName] = useState('')
  const [fileSize, setFileSize] = useState(0)
  const [error, setError] = useState('')
  const [dragging, setDragging] = useState(false)
  const fileRef = useRef(null)

  const MAX_SIZE = 10 * 1024 * 1024

  const validateFile = (file) => {
    if (!file) return '请选择文件'
    if (!file.name.toLowerCase().endsWith('.pdf')) return '仅支持 PDF 文件'
    if (file.type && file.type !== 'application/pdf') return '仅支持 PDF 文件'
    if (file.size > MAX_SIZE) return '文件大小超过 10MB 限制'
    return ''
  }

  const handleFile = (file) => {
    const err = validateFile(file)
    if (err) {
      setError(err)
      setFileName('')
      setFileSize(0)
      return
    }
    setError('')
    setFileName(file.name)
    setFileSize(file.size)
    onUpload(file)
  }

  const handleChange = (e) => {
    const file = e.target.files?.[0]
    if (file) handleFile(file)
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    setDragging(true)
  }

  const handleDragLeave = () => setDragging(false)

  const handleDrop = (e) => {
    e.preventDefault()
    setDragging(false)
    const file = e.dataTransfer.files?.[0]
    if (file) handleFile(file)
  }

  const formatSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
  }

  return (
    <div className="upload-area">
      <h3>📄 上传简历</h3>
      <p className="hint">支持 PDF 格式，最大 10MB，最多 5 页</p>
      <div
        className={`upload-dropzone ${dragging ? 'dragging' : ''} ${error ? 'has-error' : ''}`}
        onClick={() => !disabled && fileRef.current?.click()}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <input
          ref={fileRef}
          type="file"
          accept=".pdf"
          onChange={handleChange}
          style={{ display: 'none' }}
          disabled={disabled}
        />
        {fileName ? (
          <div className="file-info">
            <span className="file-icon">📎</span>
            <span className="file-name">{fileName}</span>
            <span className="file-size">({formatSize(fileSize)})</span>
          </div>
        ) : (
          <div className="upload-placeholder">
            <span className="upload-icon">📁</span>
            <span>拖拽或点击上传 PDF 简历</span>
          </div>
        )}
      </div>
      {error && <p className="error-text">{error}</p>}
    </div>
  )
}
