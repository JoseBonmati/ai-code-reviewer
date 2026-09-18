import { useState } from 'react'
import './FileUploadZone.css'

export default function FileUploadZone({ file, setFile, setError, setResult }) {
  const [isDragging, setIsDragging] = useState(false)

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
    setResult(null)
    setError(null)
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    
    const droppedFile = e.dataTransfer.files[0]
    
    // Security/Format validation: Ensure only Python files are accepted
    if (droppedFile && droppedFile.name.endsWith('.py')) {
      setFile(droppedFile)
      setResult(null)
      setError(null)
    } else {
      setError("Please upload a valid Python (.py) file.")
    }
  }

  return (
    <div 
      className={`drop-zone ${isDragging ? 'dragging' : ''}`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      onClick={() => document.getElementById('fileInput').click()}
    >
      <p>{file ? `${file.name}` : "Drag & drop your .py file here, or click to browse"}</p>
      <input 
        id="fileInput"
        type="file" 
        accept=".py" 
        onChange={handleFileChange} 
        style={{ display: 'none' }} 
      />
    </div>
  )
}