import './DownloadButton.css'

export default function DownloadButton({ result }) {
  const handleDownload = () => {
    if (!result || !result.review) return

    // Create a virtual file in memory
    const blob = new Blob([result.review], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    
    // Create an invisible link to trigger the download
    const a = document.createElement('a')
    a.href = url
    
    // Strip '.py' and append '_report.md' for a cleaner filename
    const baseName = result.file_analyzed.replace('.py', '')
    a.download = `review_${baseName}_report.md` 
    
    // Simulate click and clean up memory to prevent leaks
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <button onClick={handleDownload} className="download-button">
      Download Report (.md)
    </button>
  )
}