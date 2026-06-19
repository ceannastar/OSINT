import { ref } from 'vue'
import { scrollToBottom } from '../utils/helpers'

export function useChat(settings) {
  const messages = ref([])
  const chatHistory = ref([])
  const input = ref('')
  const isStreaming = ref(false)
  const version = ref('2.11.0')
  const aiBackend = ref('ollama')
  const currentChatId = ref(null)
  const chats = ref([])

  const BACKEND_URL = 'http://localhost:8080'

  const fetchChats = async () => {
    try {
      const r = await fetch(`${BACKEND_URL}/api/chats`)
      if (r.ok) {
        const data = await r.json()
        chats.value = data.chats || []
      }
    } catch (error) {
      console.error('Ошибка загрузки чатов:', error)
    }
  }

  // Создание нового чата
  const createChat = async (name = null) => {
    try {
      const r = await fetch(`${BACKEND_URL}/api/chats`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
      })
      if (r.ok) {
        const data = await r.json()
        await fetchChats()
        return data.id
      }
    } catch (error) {
      console.error('Ошибка создания чата:', error)
    }
    return null
  }

  // Загрузка чата (ТОЛЬКО ЗАГРУЗКА, без отправки сообщений!)
  const loadChat = async (chatId) => {
    try {
      const r = await fetch(`${BACKEND_URL}/api/chats/${chatId}`)
      if (r.ok) {
        const data = await r.json()
        currentChatId.value = chatId
        
        // Преобразуем сообщения из бэкенда в формат для фронтенда
        const loadedMessages = []
        for (const msg of data.messages || []) {
          if (msg.role === 'user') {
            loadedMessages.push({
              role: 'user',
              content: msg.content,
              time: msg.timestamp ? new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '',
              parts: msg.parts || []
            })
          } else if (msg.role === 'assistant') {
            // Если есть parts, используем их, иначе создаём текстовый блок
            const parts = msg.parts && msg.parts.length > 0 
              ? msg.parts 
              : [{ type: 'text', content: msg.content, streaming: false }]
            
            loadedMessages.push({
              role: 'assistant',
              parts: parts
            })
          }
        }
        
        messages.value = loadedMessages
        chatHistory.value = data.messages || []
        return true
      }
    } catch (error) {
      console.error('Ошибка загрузки чата:', error)
    }
    return false
  }

  // Переименование чата
  const renameChat = async (chatId, name) => {
    try {
      const r = await fetch(`${BACKEND_URL}/api/chats/${chatId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
      })
      if (r.ok) {
        await fetchChats()
        return true
      }
    } catch (error) {
      console.error('Ошибка переименования чата:', error)
    }
    return false
  }

  // Удаление чата
  const deleteChat = async (chatId) => {
    try {
      const r = await fetch(`${BACKEND_URL}/api/chats/${chatId}`, {
        method: 'DELETE'
      })
      if (r.ok) {
        await fetchChats()
        if (currentChatId.value === chatId) {
          currentChatId.value = null
          messages.value = []
          chatHistory.value = []
        }
        return true
      }
    } catch (error) {
      console.error('Ошибка удаления чата:', error)
    }
    return false
  }

  const fetchHealth = async () => {
    try {
      const r = await fetch(`${BACKEND_URL}/api/health`)
      if (!r.ok) return
      const d = await r.json()
      version.value = d.version || version.value
      if (d.ollama_host) settings.ollamaHost = d.ollama_host
      fetchChats()
    } catch {}
  }

  const sendSuggestion = (prompt) => {
    input.value = prompt
    sendMessage()
  }

  const pushError = (msg) => {
    messages.value.push({
      role: 'assistant',
      parts: [{ type: 'text', content: msg, streaming: false }]
    })
  }

  const sendMessage = async () => {
    const text = input.value.trim()
    if (!text || isStreaming.value) return

    // Если нет активного чата, создаём новый
    if (!currentChatId.value) {
      const newId = await createChat()
      if (newId) {
        currentChatId.value = newId
        await fetchChats()
      } else {
        pushError('Не удалось создать чат')
        return
      }
    }

    input.value = ''

    const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    messages.value.push({ role: 'user', content: text, time: now })
    chatHistory.value.push({ role: 'user', content: text })

    const msgIdx = messages.value.length
    messages.value.push({ role: 'assistant', parts: [] })
    isStreaming.value = true
    scrollToBottom(document.getElementById('chat-area'))

    const payload = {
      message: text,
      chat_id: currentChatId.value
    }

    let fullText = ''
    try {
      const resp = await fetch(`${BACKEND_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })

      if (!resp.ok) {
        let errDetail = `HTTP ${resp.status}`
        try { const e = await resp.json(); errDetail += ': ' + (e.detail || JSON.stringify(e)) } catch {}
        messages.value[msgIdx].parts.push({ type: 'text', content: `Ошибка сервера: ${errDetail}`, streaming: false })
        isStreaming.value = false
        return
      }

      if (!resp.body) {
        messages.value[msgIdx].parts.push({ type: 'text', content: 'Ошибка: тело ответа пустое (браузер может не поддерживать streaming).', streaming: false })
        isStreaming.value = false
        return
      }

      const reader = resp.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''
      let curText = null

      const flushText = () => {
        if (curText) {
          curText.streaming = false
          curText = null
        }
      }

      outer: while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop()

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue
          const raw = line.slice(6).trim()
          if (!raw) continue
          let evt
          try { evt = JSON.parse(raw) } catch { continue }

          if (evt.type === 'text') {
            if (!curText) {
              messages.value[msgIdx].parts.push({ type: 'text', content: '', streaming: true })
              curText = messages.value[msgIdx].parts[messages.value[msgIdx].parts.length - 1]
            }
            curText.content += evt.content
            fullText += evt.content
            scrollToBottom(document.getElementById('chat-area'))

          } else if (evt.type === 'tool_start') {
            flushText()
            messages.value[msgIdx].parts.push({
              type: 'tool',
              tool: evt.tool,
              input: evt.input || '',
              status: 'running',
              output: '',
              elapsed: null,
              collapsed: false,
            })
            scrollToBottom(document.getElementById('chat-area'))

          } else if (evt.type === 'tool_result') {
            const parts = messages.value[msgIdx].parts
            for (let i = parts.length - 1; i >= 0; i--) {
              if (parts[i].type === 'tool' && parts[i].tool === evt.tool && parts[i].status === 'running') {
                parts[i].output = evt.output || ''
                parts[i].elapsed = evt.elapsed
                parts[i].status = 'done'
                break
              }
            }
            scrollToBottom(document.getElementById('chat-area'))

          } else if (evt.type === 'done') {
            flushText()
            break outer

          } else if (evt.type === 'error') {
            flushText()
            messages.value[msgIdx].parts.push({ type: 'text', content: `Ошибка: ${evt.message}`, streaming: false })
            break outer
          }
        }
      }
      flushText()
      if (messages.value[msgIdx].parts.length === 0) {
        messages.value[msgIdx].parts.push({ type: 'text', content: 'Ответ от сервера не получен.', streaming: false })
      }

      if (fullText.trim()) {
        chatHistory.value.push({ role: 'assistant', content: fullText.trim() })
      } else if (messages.value[msgIdx].parts.some(p => p.type === 'tool')) {
        const summary = messages.value[msgIdx].parts
          .filter(p => p.type === 'tool')
          .map(p => `[Использован ${p.tool} для "${p.input}"]`).join(' ')
        chatHistory.value.push({ role: 'assistant', content: summary })
      }

      // Обновляем список чатов
      await fetchChats()

    } catch (err) {
      messages.value[msgIdx].parts.push({ type: 'text', content: `Ошибка соединения: ${err.message}`, streaming: false })
    }

    isStreaming.value = false
    scrollToBottom(document.getElementById('chat-area'))
  }

  const clearConversation = () => {
    messages.value = []
    chatHistory.value = []
    currentChatId.value = null
  }

  return {
    messages,
    chatHistory,
    input,
    isStreaming,
    version,
    aiBackend,
    currentChatId,
    chats,
    fetchHealth,
    sendSuggestion,
    sendMessage,
    clearConversation,
    pushError,
    fetchChats,
    createChat,
    loadChat,
    renameChat,
    deleteChat
  }
}