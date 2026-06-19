import { ref } from 'vue'

export function useErrorHandler() {
  const showError = ref(false)
  const errorMessage = ref('')
  const errorStatus = ref('')

  const setError = (message, status = null) => {
    showError.value = true
    errorMessage.value = message
    errorStatus.value = status || 'Недоступен'
  }

  const clearError = () => {
    showError.value = false
    errorMessage.value = ''
    errorStatus.value = ''
  }

  return {
    showError,
    errorMessage,
    errorStatus,
    setError,
    clearError
  }
}