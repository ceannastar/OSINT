export const renderMarkdown = (text) => {
  if (!text) return ''
  let h = text
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/```([\s\S]*?)```/g, (_, inner) => {
      const code = inner.replace(/^[^\n]*\n/, '')
      return `<pre><code>${code}</code></pre>`
    })
    .replace(/`([^`\n]+)`/g, '<code>$1</code>')
    .replace(/\*\*([^*\n]+)\*\*/g, '<strong>$1</strong>')
    .replace(/\*([^*\n]+)\*/g, '<em>$1</em>')
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    .replace(/^[*\-] (.+)$/gm, '<li>$1</li>')
    .replace(/^\d+\. (.+)$/gm, '<li>$1</li>')
    .replace(/(<li>[\s\S]*?<\/li>\n?)+/g, m => `<ul>${m}</ul>`)
    .replace(/\n\n+/g, '</p><p>')
    .replace(/\n/g, '<br>')

  if (!h.startsWith('<h') && !h.startsWith('<ul') && !h.startsWith('<pre'))
    h = `<p>${h}</p>`
  return h
}