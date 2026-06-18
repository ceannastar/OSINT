<template>
  <div 
    class="app-container"
    @mousemove="handleMouseMove"
    @mouseleave="handleMouseLeave"
    @click="handleClick"
  >
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
      :version="version"
      :ai-backend="aiBackend"
      :settings="settings"
      :is-light="isLight"
      :messages-count="messages.length"
      @toggle-theme="toggleTheme"
      @open-settings="showSettings = true"
      @clear-conversation="clearConversation"
      @new-conversation="newConversation"
    />

    <!-- Основной контент -->
    <div class="main-content">
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
        :featured-sponsors="featuredSponsors"
        :version="version"
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

    <!-- Искры -->
    <div class="sparks-container">
      <div
        v-for="(spark, index) in sparks"
        :key="index"
        class="spark"
        :style="{
          left: spark.x + 'px',
          top: spark.y + 'px',
          width: spark.size + 'px',
          height: spark.size + 'px',
          background: spark.color,
          animation: `spark-fly ${spark.duration}ms ease-out forwards`
        }"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Sidebar from './components/Sidebar.vue'
import SettingsModal from './components/SettingsModal.vue'
import ChatArea from './components/ChatArea.vue'
import InputBar from './components/InputBar.vue'
import { useTheme } from './composables/useTheme'
import { useSettings } from './composables/useSettings'
import { useApiKeys } from './composables/useApiKeys'
import { useSponsors } from './composables/useSponsors'
import { useChat } from './composables/useChat'
import { SUGGESTIONS } from './constants'

const { isLight, toggleTheme, loadTheme } = useTheme()
const { settings, loadSettings } = useSettings()
const { apiKeys, showKeys, setupData, setupMsg, setupOk, showAdvancedKeys, saveApiKeys } = useApiKeys()
const { featuredSponsors, fetchSponsors } = useSponsors()
const { messages, input, isStreaming, version, aiBackend, fetchHealth, sendSuggestion, sendMessage, clearConversation } = useChat(settings)

const showSettings = ref(false)
const ollamaTestResult = ref('')
const ollamaTestOk = ref(false)
const suggestions = SUGGESTIONS
const sparks = ref([])

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

const handleClick = (event) => {
  const rect = event.currentTarget.getBoundingClientRect()
  const x = event.clientX - rect.left
  const y = event.clientY - rect.top
  
  const colors = [
    'var(--accent-primary)',
    'var(--accent-secondary)',
    'var(--accent-blue)',
    'var(--accent-pink)',
    'var(--accent-orange)'
  ]
  
  for (let i = 0; i < 12; i++) {
    const angle = (Math.PI * 2 * i) / 12 + Math.random() * 0.5
    const distance = 40 + Math.random() * 60
    const size = 2 + Math.random() * 4
    
    sparks.value.push({
      x: x + Math.cos(angle) * distance,
      y: y + Math.sin(angle) * distance,
      size: size,
      color: colors[Math.floor(Math.random() * colors.length)],
      duration: 600 + Math.random() * 400
    })
  }
  
  setTimeout(() => {
    sparks.value = []
  }, 1000)
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

onMounted(() => {
  loadTheme()
  loadSettings()
  fetchHealth()
  fetchSponsors()
  animateCursor()
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

/* Фоновые эффекты */
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

/* Основной контент */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-left: 240px; /* Ширина боковой панели */
  position: relative;
  z-index: 1;
  min-width: 0;
}

.chat-wrapper {
  flex: 1;
  overflow: hidden;
  min-height: 0;
}

.sparks-container {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 100;
}

.spark {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
  transform: translate(-50%, -50%);
}

@keyframes spark-fly {
  0% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1);
  }
  100% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0);
  }
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(10px, -20px) scale(1.05); }
  66% { transform: translate(-10px, 10px) scale(0.95); }
}

.app-container * {

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