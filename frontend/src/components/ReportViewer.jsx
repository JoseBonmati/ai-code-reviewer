import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism'
import './ReportViewer.css'

export default function ReportViewer({ reviewText }) {
  if (!reviewText) return null

  return (
    <div className="report-content">
      <ReactMarkdown
        components={{
          // Custom renderer for code blocks to apply syntax highlighting
          code({node, inline, className, children, ...props}) {
            const match = /language-(\w+)/.exec(className || '')
            return !inline && match ? (
              <SyntaxHighlighter
                {...props}
                style={vscDarkPlus}
                language={match[1]}
                PreTag="div"
              >
                {String(children).replace(/\n$/, '')}
              </SyntaxHighlighter>
            ) : (
              // Standard inline code
              <code {...props} className={className}>
                {children}
              </code>
            )
          }
        }}
      >
        {reviewText}
      </ReactMarkdown>
    </div>
  )
}