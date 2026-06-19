<template>
  <Teleport to="body">
    <div
      v-if="show"
      @click="$emit('close')"
      class="fixed inset-0 z-50 bg-overlay flex items-center justify-center p-4"
    >
      <div @click.stop class="settings-modal glass-card">
        <!-- Заголовок -->
        <div class="settings-header">
          <div class="settings-header-left">
            <svg class="settings-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="12" cy="12" r="3"/>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l-.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
            </svg>
            <div>
              <h2 class="settings-title">Настройки</h2>
              <p class="settings-subtitle">Управление интеллектуальным движком</p>
            </div>
          </div>
          <button @click="$emit('close')" class="close-btn glass-card">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>

        <!-- Вкладки -->
        <Tabs
          :tabs="tabs"
          :active-tab="activeTab"
          @switch="activeTab = $event"
        />

        <!-- Контент -->
        <div class="settings-content">
          <ModelTab
            v-if="activeTab === 'model'"
            :settings="settings"
            :ollama-test-result="ollamaTestResult"
            :ollama-test-ok="ollamaTestOk"
            :available-models="availableModels"
            :is-testing="isTesting"
            :is-saving="isSaving"
            @test-ollama="handleTestConnection"
            @save-ollama-settings="handleSaveSettings"
            @select-model="handleSelectModel"
          />

          <ApiKeysTab
            v-if="activeTab === 'api'"
            :api-keys="apiKeys"
            :show-keys="showKeys"
            :setup-data="setupData"
            :setup-msg="setupMsg"
            :setup-ok="setupOk"
            @save-keys="$emit('save-keys')"
            @toggle-show-key="(key) => $emit('toggle-show-key', key)"
          />

          <AboutTab
            v-if="activeTab === 'about'"
            :settings="settings"
            :ollama-test-ok="ollamaTestOk"
            :configured-keys="configuredKeys"
          />
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed } from 'vue'
import Tabs from './SettingsModal/Tabs.vue'
import ModelTab from './SettingsModal/ModelTab.vue'
import ApiKeysTab from './SettingsModal/ApiKeysTab.vue'
import AboutTab from './SettingsModal/AboutTab.vue'

const props = defineProps({
  show: { type: Boolean, required: true },
  settings: { type: Object, required: true },
  apiKeys: { type: Array, required: true },
  showKeys: { type: Object, required: true },
  setupData: { type: Object, required: true },
  setupMsg: { type: String, required: true },
  setupOk: { type: Boolean, required: true },
  showAdvancedKeys: { type: Boolean, required: true },
  ollamaTestResult: { type: String, required: true },
  ollamaTestOk: { type: Boolean, required: true },
  availableModels: { type: Array, required: true },
  isSaving: { type: Boolean, required: true }
})

const emit = defineEmits([
  'close',
  'save-keys',
  'test-ollama',
  'toggle-advanced-keys',
  'toggle-show-key',
  'save-ollama-settings',
  'select-model'
])

const activeTab = ref('model')
const isTesting = ref(false)
const isSaving = ref(false)

const tabs = [
  { 
    id: 'model', 
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2a8 8 0 0 0-8 8c0 5 8 12 8 12s8-7 8-12a8 8 0 0 0-8-8z"/><circle cx="12" cy="10" r="3"/></svg>', 
    label: 'Модель' 
  },
  { 
    id: 'api', 
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>', 
    label: 'API Ключи' 
  },
  { 
    id: 'about', 
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="12" x2="12" y2="16"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>', 
    label: 'Об инструменте' 
  }
]

const configuredKeys = computed(() => {
  return props.apiKeys.filter(k => props.setupData[k.key] && props.setupData[k.key].trim()).length
})

const handleTestConnection = async () => {
  isTesting.value = true
  await emit('test-ollama')
  isTesting.value = false
}

const handleSaveSettings = async () => {
  isSaving.value = true
  await emit('save-ollama-settings')
  isSaving.value = false
}

const handleSelectModel = async (model) => {
  isSaving.value = true
  try {
    await emit('select-model', model)
  } finally {
    isSaving.value = false
  }
}
</script>

<style scoped>
.settings-modal {
  width: 100%;
  max-width: 560px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  background: var(--bg-glass);
  backdrop-filter: blur(30px);
  border: 1px solid var(--border-color);
  border-radius: 1rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  overflow: hidden;
}

.settings-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
  flex-shrink: 0;
}

.settings-header-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.settings-icon {
  width: 20px;
  height: 20px;
  stroke: var(--text-secondary);
  opacity: 0.6;
  flex-shrink: 0;
}

.settings-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.settings-subtitle {
  font-size: 0.7rem;
  color: var(--text-muted);
  margin: 0;
}

.close-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.5rem;
  background: var(--bg-glass);
  border: 1px solid var(--border-color);
  color: var(--text-muted);
  transition: all 0.3s ease;
  cursor: pointer;
}

.close-btn:hover {
  color: var(--text-primary);
  border-color: var(--accent-primary);
  transform: rotate(90deg);
}

.settings-content {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.settings-panel {
  animation: fadein 0.2s ease;
}

@keyframes fadein {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>