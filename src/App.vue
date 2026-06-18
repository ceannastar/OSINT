<template>
  <div class="app-container">
    <TopBar
      :version="version"
      :ai-backend="aiBackend"
      :settings="settings"
      :is-light="isLight"
      :messages-count="messages.length"
      @toggle-theme="toggleTheme"
      @open-settings="showSettings = true"
      @clear-conversation="clearConversation"
    />

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
</template>

<script setup>
import { ref, onMounted } from 'vue'
import TopBar from './components/TopBar.vue'
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

const testOllama = async () => {
  ollamaTestResult.value = 'Testing...'
  ollamaTestOk.value = false
  try {
    const r = await fetch(settings.ollamaHost.replace(/\/$/, '') + '/api/tags', {
      signal: AbortSignal.timeout(3000),
    })
    if (r.ok) {
      ollamaTestOk.value = true
      ollamaTestResult.value = 'Connected'
    } else {
      ollamaTestResult.value = `HTTP ${r.status}`
    }
  } catch (e) {
    ollamaTestResult.value = e.message
  }
}

const saveOllamaSettings = async () => {
  ollamaTestResult.value = 'Saving...'
  ollamaTestOk.value = false
  
  const body = {
    OLLAMA_HOST: settings.ollamaHost.trim(),
    OLLAMA_MODEL: settings.ollamaModel.trim(),
  }
  
  try {
    const r = await fetch('/api/setup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
    if (!r.ok) throw new Error('Save failed')
    ollamaTestOk.value = true
    ollamaTestResult.value = 'Saved'
    await fetchHealth()
    setTimeout(() => {
      if (ollamaTestResult.value === 'Saved') ollamaTestResult.value = ''
    }, 3000)
  } catch (e) {
    ollamaTestResult.value = e.message || 'Failed to save.'
  }
}

onMounted(() => {
  loadTheme()
  loadSettings()
  fetchHealth()
  fetchSponsors()
})
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  height: 100dvh;
  background-color: var(--bg);
  color: var(--text-primary);
  font-family: 'Inter', system-ui, sans-serif;
  font-size: 0.875rem;
  overflow: hidden;
}

.chat-wrapper {
  flex: 1;
  overflow: hidden;
  min-height: 0;
}
</style>