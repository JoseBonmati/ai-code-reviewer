import { useState } from 'react'
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
    setResult(null)
    setError(null)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!file) return

    setLoading(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('http://localhost:8000/api/review', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Error processing the file on the server.')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <h1 className="app-title">AI Code Reviewer</h1>
      <p className="app-description">Upload a Python (.py) file for the agent to analyze.</p>

      <form onSubmit={handleSubmit} className="upload-form">
        <input 
          type="file" 
          accept=".py" 
          onChange={handleFileChange} 
        />
        <button type="submit" className="submit-button" disabled={!file || loading}>
          {loading ? 'Analyzing...' : 'Analyze Code'}
        </button>
      </form>

      {error && <div className="error-message">{error}</div>}

      {result && (
        <div className="report-container">
          <h2 className="report-title">Generated Report</h2>
          <p><strong>File:</strong> {result.file_analyzed}</p>
          <p><strong>Report path:</strong> {result.report_path}</p>
          <hr />
          <pre className="report-content">
            {result.review}
          </pre>
        </div>
      )}
    </div>
  )
}

export default App