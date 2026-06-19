import { ref, computed } from 'vue'

const BACKEND_STORAGE_KEY = 'bfelite_backend_host'

export function useBackend() {
  const host = ref(localStorage.getItem(BACKEND_STORAGE_KEY) || 'localhost:8080')
  
  const url = computed(() => {
    let h = host.value.trim()
    h = h.replace(/^https?:\/\//, '')
    return `http://${h}`
  })

  const saveHost = () => {
    localStorage.setItem(BACKEND_STORAGE_KEY, host.value)
  }

  const setHost = (newHost) => {
    host.value = newHost
    saveHost()
  }

  const checkHealth = async (timeout = 5000) => {
    try {
      const response = await fetch(`${url.value}/api/health`, {
        signal: AbortSignal.timeout(timeout)
      })
      return {
        ok: response.status === 200,
        status: response.status,
        data: response.status === 200 ? await response.json() : null
      }
    } catch (error) {
      return {
        ok: false,
        status: null,
        data: null,
        error: error.message
      }
    }
  }

  return {
    host,
    url,
    setHost,
    checkHealth,
    saveHost
  }
}