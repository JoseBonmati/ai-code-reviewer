import { useState } from 'react'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism'
import './RefactorSection.css'

export default function RefactorSection({ threadId, originalFileName, originalCode, setError }) {
  const [isRefactoring, setIsRefactoring] = useState(false)
  const [refactoredCode, setRefactoredCode] = useState(null)

  const handleRefactor = async () => {
    if (!threadId) return

    setIsRefactoring(true)
    setError(null)

    try {
      const response = await fetch('http://localhost:8000/api/refactor', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ thread_id: threadId }),
      })

      if (!response.ok) {
        throw new Error('Error generating the refactored code.')
      }

      const data = await response.json()
      setRefactoredCode(data.refactored_code)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsRefactoring(false)
    }
  }

  const handleDownloadPython = () => {
    if (!refactoredCode) return

    // Create a virtual file in memory for the python code
    const blob = new Blob([refactoredCode], { type: 'text/x-python' })
    const url = URL.createObjectURL(blob)
    
    const a = document.createElement('a')
    a.href = url
    
    // Append '_fixed' to the original filename
    const baseName = originalFileName.replace('.py', '')
    a.download = `${baseName}_fixed.py` 
    
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <div className="refactor-section">
      {!refactoredCode ? (
        <button 
          onClick={handleRefactor} 
          className="refactor-trigger-button"
          disabled={isRefactoring}
        >
          {isRefactoring ? 'Fixing Code...' : 'Fix Code (Auto-Refactor)'}
        </button>
      ) : (
        <div className="refactored-code-container">
          <h3 className="refactor-title">Code Comparison</h3>
          
          <div className="code-comparison-grid">
            <div className="code-column">
              <h4>Original Code</h4>
              <SyntaxHighlighter
                style={vscDarkPlus}
                language="python"
                PreTag="div"
                className="code-block"
              >
                {originalCode || "No original code available."}
              </SyntaxHighlighter>
            </div>
            
            <div className="code-column">
              <h4>Refactored Code</h4>
              <SyntaxHighlighter
                style={vscDarkPlus}
                language="python"
                PreTag="div"
                className="code-block"
              >
                {refactoredCode}
              </SyntaxHighlighter>
            </div>
          </div>
          
          <button onClick={handleDownloadPython} className="download-python-button">
            Download Fixed Code (.py)
          </button>
        </div>
      )}
    </div>
  )
}