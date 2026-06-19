<template>
  <div 
    class="app-container"
    @mousemove="handleMouseMove"
    @mouseleave="handleMouseLeave"
  >
    <!-- Затемнение при ошибке -->
    <div v-if="showError" class="error-overlay">
      <div class="error-modal glass-card">
        <svg class="error-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="12" cy="12" r="10"/>
          <line x1="12" y1="8" x2="12" y2="12"/>
          <line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
        <h2 class="error-title">Ошибка подключения</h2>
        <p class="error-message">{{ errorMessage }}</p>
        <p class="error-hint">Убедитесь, что сервер BFElite запущен и укажите правильный адрес</p>
        
        <!-- Поле для ввода IP адреса -->
        <div class="error-input-group">
          <label class="error-input-label">Адрес сервера</label>
          <div class="error-input-wrapper glass-card">
            <span class="error-input-prefix">http://</span>
            <input
              v-model="backendHost"
              placeholder="localhost:8080"
              class="error-input"
              @keydown.enter="retryConnection"
            />
          </div>
          <p class="error-input-hint">Пример: localhost:8080 или 192.168.1.100:8080</p>
        </div>

        <button class="error-btn btn-primary" @click="retryConnection">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M23 4v6h-6"/>
            <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
          </svg>
          Попробовать снова
        </button>
        <div class="error-details">
          <span class="error-detail-label">Статус:</span>
          <span class="error-detail-value">{{ errorStatus || 'Неизвестно' }}</span>
          <span class="error-detail-divider">·</span>
          <span class="error-detail-label">Хост:</span>
          <span class="error-detail-value">{{ backendHost }}</span>
        </div>
      </div>
    </div>

    <!-- Фоновые эффекты -->
    <div class="bg-effects">
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="orb orb-3"></div>
      <div class="grid-pattern"></div>
      <div 
        class="cursor-glow"
        :style="{
          left: cursorX + 'px',
          top: cursorY + 'px',
          opacity: cursorVisible ? 1 : 0,
          transform: `translate(-50%, -50%) scale(${cursorScale})`
        }"
      ></div>
    </div>

    <!-- Боковая панель -->
    <Sidebar
      v-if="!showError"
      :ai-backend="aiBackend"
      :settings="settings"
      :is-light="isLight"
      :messages-count="messages.length"
      :ollama-test-result="ollamaTestResult"
      :ollama-test-ok="ollamaTestOk"
      @toggle-theme="toggleTheme"
      @open-settings="showSettings = true"
      @clear-conversation="clearConversation"
      @new-conversation="newConversation"
    />

    <!-- Основной контент -->
    <div v-if="!showError" class="main-content">
      <SettingsModal
        :show="showSettings"
        :settings="settings"
        :api-keys="apiKeys"
        :show-keys="showKeys"
        :setup-data="setupData"
        :setup-msg="setupMsg"
        :setup-ok="setupOk"
        :show-advanced-keys="showAdvancedKeys"
        :ollama-test-result="ollamaTestResult"
        :ollama-test-ok="ollamaTestOk"
        @close="showSettings = false"
        @save-keys="saveApiKeys"
        @test-ollama="testOllama"
        @toggle-advanced-keys="showAdvancedKeys = !showAdvancedKeys"
        @toggle-show-key="(key) => showKeys[key] = !showKeys[key]"
        @save-ollama-settings="saveOllamaSettings"
      />

      <div class="chat-wrapper">
        <ChatArea
          :messages="messages"
          :suggestions="suggestions"
          :is-streaming="isStreaming"
          @send-suggestion="sendSuggestion"
        />
      </div>

      <InputBar
        v-model="input"
        :is-streaming="isStreaming"
        @send="sendMessage"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import Sidebar from './components/Sidebar.vue'
import SettingsModal from './components/SettingsModal.vue'
import ChatArea from './components/ChatArea.vue'
import InputBar from './components/InputBar.vue'
import { useTheme } from './composables/useTheme'
import { useSettings } from './composables/useSettings'
import { useApiKeys } from './composables/useApiKeys'
import { useChat } from './composables/useChat'
import { SUGGESTIONS } from './constants'

const { isLight, toggleTheme, loadTheme } = useTheme()
const { settings, loadSettings } = useSettings()
const { apiKeys, showKeys, setupData, setupMsg, setupOk, showAdvancedKeys, saveApiKeys } = useApiKeys()

const { messages, input, isStreaming, aiBackend, fetchHealth, sendSuggestion, sendMessage, clearConversation } = useChat(settings)

const showSettings = ref(false)
const ollamaTestResult = ref('Проверка...')
const ollamaTestOk = ref(false)
const suggestions = SUGGESTIONS

// Состояние ошибки
const showError = ref(false)
const errorMessage = ref('')
const errorStatus = ref('')

// Хост бэкенда (сохраняется в localStorage)
const BACKEND_STORAGE_KEY = 'bfelite_backend_host'
const backendHost = ref(localStorage.getItem(BACKEND_STORAGE_KEY) || 'localhost:8080')

// Полный URL для бэкенда
const backendUrl = computed(() => {
  let host = backendHost.value.trim()
  // Убираем http:// если есть
  host = host.replace(/^https?:\/\//, '')
  return `http://${host}`
})

// Cursor glow
const cursorX = ref(-100)
const cursorY = ref(-100)
const cursorVisible = ref(false)
const cursorScale = ref(1)
let animationFrame = null
let targetX = -100
let targetY = -100
let currentX = -100
let currentY = -100

const handleMouseMove = (event) => {
  const rect = event.currentTarget.getBoundingClientRect()
  targetX = event.clientX - rect.left
  targetY = event.clientY - rect.top
  cursorVisible.value = true
  cursorScale.value = 1.2
  setTimeout(() => {
    cursorScale.value = 1
  }, 100)
}

const handleMouseLeave = () => {
  cursorVisible.value = false
}

const animateCursor = () => {
  currentX += (targetX - currentX) * 0.1
  currentY += (targetY - currentY) * 0.1
  cursorX.value = currentX
  cursorY.value = currentY
  animationFrame = requestAnimationFrame(animateCursor)
}

const newConversation = () => {
  clearConversation()
}

// Проверка здоровья сервера
const checkServerHealth = async () => {
  try {
    const url = `${backendUrl.value}/api/health`
    const response = await fetch(url, {
      signal: AbortSignal.timeout(5000)
    })
    
    if (response.status === 200) {
      showError.value = false
      errorMessage.value = ''
      errorStatus.value = ''
      // Сохраняем хост в localStorage
      localStorage.setItem(BACKEND_STORAGE_KEY, backendHost.value)
      // Загружаем остальные данные после успешной проверки
      await fetchHealth()
      return true
    } else {
      showError.value = true
      errorMessage.value = 'Сервер вернул ошибку'
      errorStatus.value = `HTTP ${response.status}`
      return false
    }
  } catch (error) {
    showError.value = true
    errorMessage.value = error.message || 'Не удалось подключиться к серверу'
    errorStatus.value = 'Недоступен'
    return false
  }
}

// Тестирование Ollama
const testOllama = async () => {
  ollamaTestResult.value = 'Проверка...'
  ollamaTestOk.value = false
  
  try {
    const host = settings.ollamaHost.replace(/\/$/, '')
    const response = await fetch(`${host}/api/health`, {
      signal: AbortSignal.timeout(5000),
    })
    
    if (response.ok) {
      const data = await response.json()
      ollamaTestOk.value = true
      const modelCount = data.models?.length || 0
      ollamaTestResult.value = `Подключено (${modelCount} моделей)`
    } else {
      ollamaTestOk.value = false
      ollamaTestResult.value = `Ошибка ${response.status}`
    }
  } catch (error) {
    ollamaTestOk.value = false
    ollamaTestResult.value = error.message || 'Ошибка подключения'
  }
}

// Сохранение настроек Ollama
const saveOllamaSettings = async () => {
  ollamaTestResult.value = 'Сохранение...'
  ollamaTestOk.value = false
  
  const body = {
    OLLAMA_HOST: settings.ollamaHost.trim(),
    OLLAMA_MODEL: settings.ollamaModel.trim(),
  }
  
  try {
    const r = await fetch(`${backendUrl.value}/api/setup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
    if (!r.ok) throw new Error('Ошибка сохранения')
    ollamaTestOk.value = true
    ollamaTestResult.value = 'Сохранено ✓'
    await fetchHealth()
    // Повторно проверяем подключение к Ollama после сохранения
    await testOllama()
    setTimeout(() => {
      if (ollamaTestResult.value === 'Сохранено ✓') ollamaTestResult.value = ''
    }, 3000)
  } catch (e) {
    ollamaTestResult.value = 'Ошибка сохранения'
  }
}

// Повторная попытка подключения
const retryConnection = async () => {
  const isHealthy = await checkServerHealth()
  if (isHealthy) {
    // После восстановления соединения с сервером проверяем Ollama
    await testOllama()
  }
}

onMounted(async () => {
  loadTheme()
  loadSettings()
  
  // Сначала проверяем сервер
  const isHealthy = await checkServerHealth()
  
  if (isHealthy) {
    // Только после успешной проверки запускаем анимацию курсора и тест Ollama
    animateCursor()
    // Автоматический тест Ollama при загрузке
    await testOllama()
  }
})

onUnmounted(() => {
  if (animationFrame) {
    cancelAnimationFrame(animationFrame)
  }
})
</script>

<style scoped>
.app-container {
  display: flex;
  height: 100vh;
  height: 100dvh;
  background: var(--bg-primary);
  position: relative;
  overflow: hidden;
}

.bg-effects {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.15;
  animation: float 8s ease-in-out infinite;
}

.orb-1 {
  width: 400px;
  height: 400px;
  background: var(--accent-primary);
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.orb-2 {
  width: 300px;
  height: 300px;
  background: var(--accent-secondary);
  bottom: -50px;
  left: -50px;
  animation-delay: -3s;
}

.orb-3 {
  width: 200px;
  height: 200px;
  background: var(--accent-blue);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -5s;
  opacity: 0.08;
}

.cursor-glow {
  position: absolute;
  width: 300px;
  height: 300px;
  border-radius: 50%;
  pointer-events: none;
  background: radial-gradient(
    circle,
    rgba(0, 255, 200, 0.15) 0%,
    rgba(124, 58, 237, 0.08) 30%,
    rgba(59, 130, 246, 0.04) 60%,
    transparent 80%
  );
  transition: opacity 0.3s ease, transform 0.1s ease;
  will-change: transform;
  z-index: 0;
}

.cursor-glow::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: radial-gradient(
    circle,
    rgba(0, 255, 200, 0.3) 0%,
    rgba(0, 255, 200, 0) 70%
  );
  transform: translate(-50%, -50%);
}

.grid-pattern {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 40px 40px;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-left: 240px;
  position: relative;
  z-index: 1;
  min-width: 0;
}

.chat-wrapper {
  flex: 1;
  overflow: hidden;
  min-height: 0;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(10px, -20px) scale(1.05); }
  66% { transform: translate(-10px, 10px) scale(0.95); }
}

.app-container button,
.app-container input,
.app-container textarea,
.app-container a {
  cursor: pointer;
}

.app-container textarea {
  cursor: text;
}

/* Стили для ошибки */
.error-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  padding: 20px;
}

.error-modal {
  max-width: 480px;
  width: 100%;
  padding: 40px;
  text-align: center;
  background: var(--bg-glass);
  backdrop-filter: blur(30px);
  border: 1px solid rgba(248, 81, 73, 0.3);
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  animation: fadein 0.3s ease;
}

.error-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 16px;
  stroke: var(--red);
}

.error-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.error-message {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 16px;
}

.error-hint {
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 20px;
}

/* Поле ввода IP адреса */
.error-input-group {
  text-align: left;
  margin-bottom: 20px;
}

.error-input-label {
  display: block;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.error-input-wrapper {
  display: flex;
  align-items: center;
  padding: 0 12px;
  border-radius: 8px;
  background: var(--bg-glass);
  border: 1px solid var(--border-color);
  transition: border-color 0.3s ease;
}

.error-input-wrapper:focus-within {
  border-color: var(--accent-primary);
  box-shadow: 0 0 20px rgba(0, 255, 200, 0.05);
}

.error-input-prefix {
  color: var(--text-muted);
  font-size: 13px;
  font-family: 'Courier New', monospace;
  flex-shrink: 0;
}

.error-input {
  flex: 1;
  padding: 10px 8px;
  background: transparent;
  border: none;
  color: var(--text-primary);
  font-size: 14px;
  font-family: 'Courier New', monospace;
  outline: none;
}

.error-input::placeholder {
  color: var(--text-muted);
}

.error-input-hint {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 4px;
  opacity: 0.7;
}

.error-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  border: none;
  transition: all 0.3s ease;
  cursor: pointer;
  margin-bottom: 20px;
  width: 100%;
  justify-content: center;
}

.btn-primary {
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  color: var(--bg-primary);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 255, 200, 0.3);
}

.error-details {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding-top: 16px;
  border-top: 1px solid var(--border-color);
  font-size: 12px;
  color: var(--text-muted);
}

.error-detail-label {
  color: var(--text-muted);
}

.error-detail-value {
  color: var(--text-secondary);
  font-weight: 500;
}

.error-detail-divider {
  color: var(--border-color);
}

@keyframes fadein {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
</style>