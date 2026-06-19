<template>
  <div 
    class="app-container"
    @mousemove="handleMouseMove"
    @mouseleave="handleMouseLeave"
  >
    <!-- Компонент ошибки -->
    <ErrorOverlay
      :show="showError"
      :message="errorMessage"
      :status="errorStatus"
      :host="backendHost"
      @retry="retryConnection"
      @update:host="backendHost = $event"
    />

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
      :chats="chats"
      :current-chat-id="currentChatId"
      @toggle-theme="toggleTheme"
      @open-settings="showSettings = true"
      @clear-conversation="clearConversation"
      @new-conversation="createNewChat"
      @select-chat="selectChat"
      @delete-chat="deleteChat"
    />

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
        :available-models="availableModels"
        @close="showSettings = false"
        @save-keys="saveApiKeys"
        @test-ollama="testOllama"
        @toggle-advanced-keys="showAdvancedKeys = !showAdvancedKeys"
        @toggle-show-key="(key) => showKeys[key] = !showKeys[key]"
        @save-ollama-settings="saveOllamaSettings"
        @select-model="selectModel"
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
import { ref, onMounted, onUnmounted } from 'vue'
import Sidebar from './components/Sidebar.vue'
import SettingsModal from './components/SettingsModal.vue'
import ChatArea from './components/ChatArea.vue'
import InputBar from './components/InputBar.vue'
import ErrorOverlay from './components/ErrorOverlay.vue'
import { useTheme } from './composables/useTheme'
import { useSettings } from './composables/useSettings'
import { useApiKeys } from './composables/useApiKeys'
import { useChat } from './composables/useChat'
import { useBackend } from './composables/useBackend'
import { useOllama } from './composables/useOllama'
import { useErrorHandler } from './composables/useErrorHandler'
import { SUGGESTIONS } from './constants'

// Theme
const { isLight, toggleTheme, loadTheme } = useTheme()

// Settings
const { settings, loadSettings } = useSettings()

// API Keys
const { apiKeys, showKeys, setupData, setupMsg, setupOk, showAdvancedKeys, saveApiKeys } = useApiKeys()

// Backend
const { host: backendHost, url: backendUrl, setHost, checkHealth } = useBackend()

// Error handler
const { showError, errorMessage, errorStatus, setError, clearError } = useErrorHandler()

// Chat
const { 
  messages, 
  input, 
  isStreaming, 
  aiBackend, 
  fetchHealth, 
  sendSuggestion, 
  sendMessage, 
  clearConversation,
  chats,
  currentChatId,
  fetchChats,
  createChat,
  loadChat,
  deleteChat: deleteChatFromServer
} = useChat(settings)

// Ollama
const { 
  ollamaTestResult, 
  ollamaTestOk, 
  availableModels,
  testOllama, 
  saveOllamaSettings 
} = useOllama(settings)

// Local state
const showSettings = ref(false)
const suggestions = SUGGESTIONS

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

const selectModel = async (model) => {
  try {
    const response = await fetch(`${backendUrl.value}/api/model/select`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model })
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Ошибка смены модели')
    }
    
    const data = await response.json()
    // Обновляем настройки
    settings.ollamaModel = data.current_model
    // Показываем уведомление об успехе
    console.log(`Модель изменена на ${data.current_model}`)
    
    // Обновляем статус Ollama
    await testOllama()
    
    return data
  } catch (error) {
    console.error('Ошибка смены модели:', error)
    throw error
  }
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

// Chat management
const createNewChat = async () => {
  const chatId = await createChat()
  if (chatId) {
    await fetchChats()
    await loadChat(chatId)
  }
}

const selectChat = async (chatId) => {
  await loadChat(chatId)
}

const deleteChat = async (chatId) => {
  const success = await deleteChatFromServer(chatId)
  if (success) {
    await fetchChats()
    if (currentChatId.value === chatId) {
      currentChatId.value = null
      messages.value = []
    }
  }
}

// Server connection
const checkServerHealth = async () => {
  const result = await checkHealth()
  
  if (result.ok) {
    clearError()
    setHost(backendHost.value)
    await fetchHealth()
    await fetchChats()
    return true
  } else {
    setError(
      result.error || 'Сервер вернул ошибку',
      result.status ? `HTTP ${result.status}` : null
    )
    return false
  }
}

const retryConnection = async () => {
  const isHealthy = await checkServerHealth()
  if (isHealthy) {
    await testOllama()
  }
}

// Lifecycle
onMounted(async () => {
  loadTheme()
  loadSettings()
  
  const isHealthy = await checkServerHealth()
  
  if (isHealthy) {
    animateCursor()
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
</style>