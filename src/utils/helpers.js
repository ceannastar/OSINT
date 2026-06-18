export const scrollToBottom = (element) => {
  if (element) {
    element.scrollTop = element.scrollHeight
  }
}

export const autoResize = (el) => {
  el.style.height = 'auto'
  el.style.height = Math.min(el.scrollHeight, 160) + 'px'
}

export const copyText = (text) => {
  navigator.clipboard.writeText(text || '').catch(() => {})
}

export const lineClass = (text) => {
  if (!text) return 'text-muted'
  if (text.startsWith('[+]')) return 'text-accent'
  if (text.startsWith('[-]') || text.startsWith('Scan error:') ||
      text.startsWith('Error:') || text.startsWith('Internal error:')) return 'text-error'
  if (text.startsWith('[!]') || text.includes('FLAGGED')) return 'text-warning'
  if (text.startsWith('[*]') || text.startsWith('[Censys]') ||
      text.startsWith('[Shodan]') || text.startsWith('[VirusTotal]') ||
      text.startsWith('[IP2Location]')) return 'text-secondary'
  return 'text-muted'
}