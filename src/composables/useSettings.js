import { ref, reactive, watch } from 'vue'

const STORAGE_KEY = 'openosint_settings'

export function useSettings() {
  const settings = reactive({
    ollamaModel: 'llama3.2',
    ollamaHost: 'http://localhost:11434',
  })

  const loadSettings = () => {
    try {
      const s = localStorage.getItem(STORAGE_KEY)
      if (s) {
        const parsed = JSON.parse(s)
        Object.assign(settings, parsed)
      }
    } catch {}
  }

  const saveLocalSettings = () => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(settings))
    } catch {}
  }

  watch(settings, saveLocalSettings, { deep: true })

  return {
    settings,
    loadSettings,
    saveLocalSettings
  }
}