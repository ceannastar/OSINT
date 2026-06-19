import { ref } from 'vue'

export function useOllama(settings) {
  const ollamaTestResult = ref('Проверка...')
  const ollamaTestOk = ref(false)
  const availableModels = ref([])
  const modelDetails = ref({})

  const updateModels = (models) => {
    availableModels.value = models || []
  }

  const testOllama = async () => {
    ollamaTestResult.value = 'Проверка...'
    ollamaTestOk.value = false
    
    try {
      const host = settings.ollamaHost.replace(/\/$/, '')
      // Используем /api/health для получения всех данных
      const response = await fetch(`${host}/api/health`, {
        signal: AbortSignal.timeout(5000),
      })
      
      if (response.ok) {
        const data = await response.json()
        
        const ollamaData = data.ollama || data
        const models = ollamaData.models || []
        
        availableModels.value = models
        
        const details = ollamaData.model_details || {}
        modelDetails.value = details
        
        ollamaTestOk.value = true
        const modelCount = models.length
        ollamaTestResult.value = `Подключено (${modelCount} моделей)`
      } else {
        ollamaTestOk.value = false
        ollamaTestResult.value = `Ошибка ${response.status}`
        availableModels.value = []
        modelDetails.value = {}
      }
    } catch (error) {
      ollamaTestOk.value = false
      ollamaTestResult.value = error.message || 'Ошибка подключения'
      availableModels.value = []
      modelDetails.value = {}
    }
  }

  const fetchModelDetails = async () => {
    try {
      const backendUrl = 'http://localhost:8080'
      const response = await fetch(`${backendUrl}/api/health`, {
        signal: AbortSignal.timeout(5000),
      })
      
      if (response.ok) {
        const data = await response.json()
        if (data.ollama && data.ollama.reachable) {
          const models = data.ollama.models || []
          availableModels.value = models
          
          modelDetails.value = data.ollama.model_details || {}
          
          ollamaTestOk.value = true
          const modelCount = models.length
          ollamaTestResult.value = `Подключено (${modelCount} моделей)`
          return data.ollama
        }
      }
    } catch (error) {
      console.error('Ошибка получения деталей моделей:', error)
    }
    return null
  }

  const saveOllamaSettings = async (backendUrl, fetchHealth) => {
    ollamaTestResult.value = 'Сохранение...'
    ollamaTestOk.value = false
    
    const body = {
      OLLAMA_HOST: settings.ollamaHost.trim(),
      OLLAMA_MODEL: settings.ollamaModel.trim(),
    }
    
    try {
      const r = await fetch(`${backendUrl}/api/setup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })
      if (!r.ok) throw new Error('Ошибка сохранения')
      ollamaTestOk.value = true
      ollamaTestResult.value = 'Сохранено ✓'
      await fetchHealth()
      await testOllama()
      setTimeout(() => {
        if (ollamaTestResult.value === 'Сохранено ✓') ollamaTestResult.value = ''
      }, 3000)
    } catch (e) {
      ollamaTestOk.value = false
      ollamaTestResult.value = 'Ошибка сохранения'
    }
  }

  return {
    ollamaTestResult,
    ollamaTestOk,
    availableModels,
    modelDetails,
    testOllama,
    saveOllamaSettings,
    updateModels,
    fetchModelDetails
  }
}