<template>
  <div class="settings-panel">
    <div class="panel-header">
      <h3 class="panel-title">AI Модель</h3>
      <p class="panel-desc">Настройка локального экземпляра Ollama</p>
    </div>

    <div class="status-card glass-card" :class="{ 
      'status-connected': ollamaTestOk, 
      'status-error': ollamaTestResult && !ollamaTestOk,
      'status-testing': ollamaTestResult === 'Проверка...'
    }">
      <div class="status-row">
        <span class="status-dot" :class="{ 
          connected: ollamaTestOk,
          testing: ollamaTestResult === 'Проверка...',
          error: ollamaTestResult && !ollamaTestOk && ollamaTestResult !== 'Проверка...'
        }"></span>
        <span class="status-text">
          <template v-if="ollamaTestResult === 'Проверка...'">
            Проверка подключения...
          </template>
          <template v-else-if="ollamaTestOk">
            <svg class="status-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 6L9 17l-5-5"/>
            </svg>
            Подключено к Ollama
          </template>
          <template v-else-if="ollamaTestResult">
            <svg class="status-cross" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
            {{ ollamaTestResult }}
          </template>
          <template v-else>
            <svg class="status-warning" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 9v4M12 17h.01"/>
              <path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"/>
            </svg>
            Нажмите «Проверить подключение»
          </template>
        </span>
        <span v-if="ollamaTestResult && ollamaTestResult !== 'Проверка...'" 
              class="status-result" 
              :class="ollamaTestOk ? 'text-accent' : 'text-error'">
          {{ ollamaTestOk ? '✓' : '✗' }}
        </span>
      </div>
    </div>

    <div class="settings-group">
      <div class="form-group">
        <label class="form-label">Текущая модель</label>
        <div class="input-wrapper glass-card" style="display: flex; gap: 0.5rem;">
          <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M12 2a8 8 0 0 0-8 8c0 5 8 12 8 12s8-7 8-12a8 8 0 0 0-8-8z"/>
            <circle cx="12" cy="10" r="3"/>
          </svg>
          <div class="select-wrapper" style="flex: 1;">
            <select
              v-model="selectedModel"
              class="form-select"
              :disabled="!ollamaTestOk || availableModels.length === 0 || isSaving"
            >
              <option v-if="availableModels.length === 0" value="" disabled>
                {{ ollamaTestOk ? 'Нет доступных моделей' : 'Подключитесь к Ollama' }}
              </option>
              <option
                v-for="model in availableModels"
                :key="model"
                :value="model"
              >
                {{ model }}
              </option>
            </select>
            <svg class="select-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="6 9 12 15 18 9"/>
            </svg>
          </div>
        </div>
        <p class="form-hint">
          <template v-if="ollamaTestOk && availableModels.length > 0">
            Выберите модель для выполнения запросов
          </template>
          <template v-else-if="ollamaTestOk && availableModels.length === 0">
            Нет доступных моделей. Загрузите модель командой: <code>ollama pull llama3.2</code>
          </template>
          <template v-else>
            Подключитесь к Ollama для выбора модели
          </template>
        </p>
      </div>

      <div class="form-group">
        <label class="form-label">Адрес сервера</label>
        <div class="input-wrapper glass-card">
          <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="12" r="10"/>
            <line x1="2" y1="12" x2="22" y2="12"/>
            <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
          </svg>
          <input
            v-model="settings.ollamaHost"
            placeholder="http://localhost:11434"
            class="form-input"
          />
        </div>
        <p class="form-hint">Эндпоинт сервера Ollama</p>
      </div>

      <div class="form-actions">
        <button
          @click="$emit('test-ollama')"
          class="btn-secondary"
          :disabled="isTesting"
        >
          <svg v-if="!isTesting" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
          <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="c-spin">
            <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
          </svg>
          {{ isTesting ? 'Проверка...' : 'Проверить подключение' }}
        </button>
        <button
          @click="applyModel"
          class="btn-primary"
          :disabled="!ollamaTestOk || !selectedModel || selectedModel === currentModel || isSaving"
        >
          <svg v-if="!isSaving" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 14.66V20a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h5.34"/>
            <polygon points="18 2 22 6 12 16 8 16 8 12 18 2"/>
          </svg>
          <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="c-spin">
            <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
          </svg>
          {{ isSaving ? 'Применение...' : 'Применить модель' }}
        </button>
      </div>

      <!-- Статус применения модели -->
      <div v-if="applyStatus" class="apply-status glass-card" :class="applyStatusOk ? 'status-connected' : 'status-error'">
        <span class="status-dot" :class="{ connected: applyStatusOk, error: !applyStatusOk }"></span>
        <span class="status-text">{{ applyStatus }}</span>
      </div>

      <div v-if="ollamaTestOk" class="connection-details glass-card">
        <div class="detail-row">
          <span class="detail-label">Текущая модель</span>
          <span class="detail-value" style="color: var(--accent-primary); font-weight: 600;">
            {{ settings.ollamaModel || 'Не выбрана' }}
          </span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Сервер</span>
          <span class="detail-value">{{ settings.ollamaHost }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Статус</span>
          <span class="detail-value status-online">
            <svg class="online-dot" viewBox="0 0 24 24" fill="currentColor">
              <circle cx="12" cy="12" r="10"/>
            </svg>
            Онлайн
          </span>
        </div>
        <div class="detail-row" v-if="availableModels.length > 0">
          <span class="detail-label">Доступно моделей</span>
          <span class="detail-value">{{ availableModels.length }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  settings: { type: Object, required: true },
  ollamaTestResult: { type: String, required: true },
  ollamaTestOk: { type: Boolean, required: true },
  availableModels: { type: Array, required: true },
  isTesting: { type: Boolean, required: true },
  isSaving: { type: Boolean, required: true }
})

const emit = defineEmits(['test-ollama', 'save-ollama-settings', 'select-model'])

const selectedModel = ref(props.settings.ollamaModel || '')
const currentModel = ref(props.settings.ollamaModel || '')
const applyStatus = ref('')
const applyStatusOk = ref(false)

watch(() => props.settings.ollamaModel, (newVal) => {
  if (newVal) {
    selectedModel.value = newVal
    currentModel.value = newVal
  }
})

const applyModel = async () => {
  if (!selectedModel.value || selectedModel.value === currentModel.value) return
  
  applyStatus.value = 'Применение модели...'
  applyStatusOk.value = false
  
  try {
    await emit('select-model', selectedModel.value)
    currentModel.value = selectedModel.value
    applyStatus.value = `Модель изменена на ${selectedModel.value}`
    applyStatusOk.value = true
    setTimeout(() => {
      applyStatus.value = ''
    }, 3000)
  } catch (error) {
    applyStatus.value = `Ошибка: ${error.message || 'Не удалось применить модель'}`
    applyStatusOk.value = false
  }
}
</script>

<style scoped>
.panel-header {
  margin-bottom: 1.25rem;
}

.panel-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 0.25rem 0;
}

.panel-desc {
  font-size: 0.75rem;
  color: var(--text-muted);
  margin: 0;
}

.status-card {
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1.25rem;
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.status-card.status-connected {
  border-color: var(--accent-primary);
  background: rgba(0, 255, 200, 0.05);
}

.status-card.status-error {
  border-color: var(--red);
  background: rgba(248, 81, 73, 0.05);
}

.status-card.status-testing {
  border-color: var(--accent-blue);
  background: rgba(59, 130, 246, 0.05);
}

.status-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--text-muted);
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.status-dot.connected {
  background: var(--accent-primary);
  box-shadow: 0 0 12px rgba(0, 255, 200, 0.5);
  animation: pulse-glow 1.5s ease-in-out infinite;
}

.status-dot.testing {
  background: var(--accent-blue);
  box-shadow: 0 0 12px rgba(59, 130, 246, 0.5);
  animation: pulse-glow 1s ease-in-out infinite;
}

.status-dot.error {
  background: var(--red);
  box-shadow: 0 0 12px rgba(248, 81, 73, 0.5);
}

.status-text {
  font-size: 0.75rem;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 4px;
}

.status-check,
.status-cross,
.status-warning {
  width: 14px;
  height: 14px;
  flex-shrink: 0;
}

.status-check {
  stroke: var(--accent-primary);
}

.status-cross {
  stroke: var(--red);
}

.status-warning {
  stroke: var(--yellow);
}

.status-result {
  font-size: 0.7rem;
  font-family: 'JetBrains Mono', monospace;
  margin-left: auto;
}

.settings-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.form-label {
  font-size: 0.7rem;
  font-weight: 500;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.input-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.35rem 0.5rem;
  border-radius: 0.5rem;
  background: var(--bg-glass);
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.input-wrapper:focus-within {
  border-color: var(--accent-primary);
  box-shadow: 0 0 20px rgba(0, 255, 200, 0.05);
}

.input-icon {
  width: 16px;
  height: 16px;
  stroke: var(--text-muted);
  opacity: 0.4;
  flex-shrink: 0;
}

.form-input {
  flex: 1;
  background: transparent;
  border: none;
  color: var(--text-primary);
  font-size: 0.8rem;
  padding: 0.25rem 0;
  outline: none;
}

.form-input::placeholder {
  color: var(--text-muted);
}

.select-wrapper {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
}

.form-select {
  flex: 1;
  background: transparent;
  border: none;
  color: var(--text-primary);
  font-size: 0.8rem;
  padding: 0.25rem 0;
  padding-right: 24px;
  outline: none;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  cursor: pointer;
  font-family: inherit;
  width: 100%;
}

.form-select:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.form-select option {
  background: var(--bg-secondary);
  color: var(--text-primary);
}

.select-arrow {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  stroke: var(--text-muted);
  pointer-events: none;
  transition: transform 0.2s ease;
}

.select-wrapper:focus-within .select-arrow {
  transform: translateY(-50%) rotate(180deg);
  stroke: var(--accent-primary);
}

.form-hint {
  font-size: 0.65rem;
  color: var(--text-muted);
  margin: 0;
}

.form-hint code {
  background: var(--bg-secondary);
  padding: 0.1rem 0.4rem;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  color: var(--accent-primary);
  font-size: 0.65rem;
}

.form-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 0.5rem;
  flex-wrap: wrap;
}

.btn-primary,
.btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.4rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.75rem;
  font-weight: 500;
  border: none;
  transition: all 0.3s ease;
  cursor: pointer;
}

.btn-primary {
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  color: var(--bg-primary);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 20px rgba(0, 255, 200, 0.3);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: var(--bg-glass);
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.btn-secondary:hover:not(:disabled) {
  color: var(--text-primary);
  border-color: var(--accent-primary);
}

.btn-secondary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.apply-status {
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  border: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.connection-details {
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  border: 1px solid var(--border-color);
  background: var(--bg-glass);
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.7rem;
}

.detail-label {
  color: var(--text-muted);
}

.detail-value {
  color: var(--text-secondary);
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 4px;
}

.detail-value.status-online {
  color: var(--accent-primary);
}

.online-dot {
  width: 10px;
  height: 10px;
  color: var(--accent-primary);
}

.c-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes pulse-glow {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}
</style>