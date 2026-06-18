import { ref } from 'vue'
import { API_KEYS } from '../constants'

export function useApiKeys() {
  const showKeys = ref({})
  const setupData = ref({})
  const setupMsg = ref('')
  const setupOk = ref(false)
  const showAdvancedKeys = ref(false)

  const apiKeys = API_KEYS

  const saveApiKeys = async () => {
    setupMsg.value = ''
    const body = {}
    for (const k of apiKeys) {
      const v = (setupData.value[k.key] || '').trim()
      if (v) body[k.key] = v
    }
    if (!Object.keys(body).length) {
      setupOk.value = false
      setupMsg.value = 'Enter at least one key.'
      return
    }
    try {
      const r = await fetch('/api/setup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })
      if (!r.ok) throw new Error('Save failed')
      setupData.value = {}
      setupOk.value = true
      setupMsg.value = 'Saved'
      setTimeout(() => { setupMsg.value = '' }, 3000)
    } catch (e) {
      setupOk.value = false
      setupMsg.value = e.message || 'Failed to save.'
    }
  }

  return {
    apiKeys,
    showKeys,
    setupData,
    setupMsg,
    setupOk,
    showAdvancedKeys,
    saveApiKeys
  }
}