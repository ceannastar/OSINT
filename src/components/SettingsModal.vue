<template>
  <Teleport to="body">
    <div
      v-if="show"
      @click="$emit('close')"
      class="fixed inset-0 z-50 bg-overlay flex items-center justify-center p-4"
    >
      <div
        @click.stop
        class="settings-modal glass-card"
      >
        <!-- Заголовок -->
        <div class="settings-header">
          <div class="settings-header-left">
            <svg class="settings-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="12" cy="12" r="3"/>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
            </svg>
            <div>
              <h2 class="settings-title">Настройки</h2>
              <p class="settings-subtitle">Управление интеллектуальным движком</p>
            </div>
          </div>
          <button
            @click="$emit('close')"
            class="close-btn glass-card"
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>

        <!-- Навигация по вкладкам -->
        <div class="settings-tabs">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            class="settings-tab"
            :class="{ active: activeTab === tab.id }"
          >
            <span class="tab-icon" v-html="tab.icon"></span>
            <span class="tab-label">{{ tab.label }}</span>
            <span v-if="tab.badge" class="tab-badge">{{ tab.badge }}</span>
          </button>
        </div>

        <!-- Контент -->
        <div class="settings-content">
          <!-- Вкладка: Модель -->
          <div v-if="activeTab === 'model'" class="settings-panel">
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
                <label class="form-label">Название модели</label>
                <div class="input-wrapper glass-card">
                  <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M12 2a8 8 0 0 0-8 8c0 5 8 12 8 12s8-7 8-12a8 8 0 0 0-8-8z"/>
                    <circle cx="12" cy="10" r="3"/>
                  </svg>
                  <input
                    v-model="settings.ollamaModel"
                    placeholder="llama3.2"
                    class="form-input"
                  />
                </div>
                <p class="form-hint">Модель для выполнения запросов</p>
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
                  @click="handleTestConnection"
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
                  @click="handleSaveSettings"
                  class="btn-primary"
                >
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
                    <polyline points="17 21 17 13 7 13 7 21"/>
                    <polyline points="7 3 7 8 15 8"/>
                  </svg>
                  Сохранить настройки
                </button>
              </div>

              <!-- Детали соединения -->
              <div v-if="ollamaTestOk" class="connection-details glass-card">
                <div class="detail-row">
                  <span class="detail-label">Сервер</span>
                  <span class="detail-value">{{ settings.ollamaHost }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">Модель</span>
                  <span class="detail-value">{{ settings.ollamaModel }}</span>
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
              </div>
            </div>
          </div>

          <!-- Вкладка: API Ключи -->
          <div v-if="activeTab === 'api'" class="settings-panel">
            <div class="panel-header">
              <h3 class="panel-title">API Ключи</h3>
              <p class="panel-desc">Подключение к внешним сервисам разведки</p>
            </div>

            <div class="settings-group">
              <div
                v-for="k in apiKeys"
                :key="k.key"
                class="api-key-item"
              >
                <div class="api-key-header">
                <span class="api-key-label">{{ k.label }}</span>
                <span class="api-key-status" :class="{ filled: setupData[k.key] }">
                  <template v-if="setupData[k.key]">
                    <svg class="status-filled" viewBox="0 0 24 24" fill="currentColor">
                      <circle cx="12" cy="12" r="10"/>
                    </svg>
                    Настроен
                  </template>
                  <template v-else>
                    <svg class="status-empty" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                      <circle cx="12" cy="12" r="10"/>
                    </svg>
                    Пусто
                  </template>
                </span>
              </div>
                <div class="input-wrapper glass-card">
                  <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                  </svg>
                  <input
                    :type="showKeys[k.key] ? 'text' : 'password'"
                    v-model="setupData[k.key]"
                    :placeholder="k.placeholder"
                    class="form-input"
                  />
                  <button
                    @click="$emit('toggle-show-key', k.key)"
                    class="input-toggle"
                  >
                    <svg v-if="!showKeys[k.key]" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                      <circle cx="12" cy="12" r="3"/>
                    </svg>
                    <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                      <line x1="1" y1="1" x2="23" y2="23"/>
                    </svg>
                  </button>
                </div>
              </div>

              <div class="form-actions">
                <button
                  @click="$emit('save-keys')"
                  class="btn-primary"
                  style="width: 100%;"
                >
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
                    <polyline points="17 21 17 13 7 13 7 21"/>
                    <polyline points="7 3 7 8 15 8"/>
                  </svg>
                  Сохранить все ключи
                </button>
                <span v-if="setupMsg" :class="setupOk ? 'text-accent' : 'text-error'" class="save-feedback">
                  {{ setupMsg }}
                </span>
              </div>
            </div>
          </div>

          <!-- Вкладка: Интеграции -->
          <div v-if="activeTab === 'integrations'" class="settings-panel">
            <div class="panel-header">
              <h3 class="panel-title">Интеграции</h3>
              <p class="panel-desc">Рекомендуемые сервисы разведки</p>
            </div>

            <div v-if="featuredSponsors.length > 0" class="integrations-grid">
              <a
                v-for="s in featuredSponsors"
                :key="s.name"
                :href="s.url"
                target="_blank"
                rel="noopener sponsored"
                class="integration-card glass-card"
              >
                <svg class="integration-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
                  <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
                </svg>
                <div class="integration-info">
                  <span class="integration-name">{{ s.name }}</span>
                  <span class="integration-tagline">{{ s.tagline }}</span>
                </div>
                <span class="integration-arrow">-></span>
              </a>
            </div>

            <div v-else class="empty-integrations">
              <svg class="empty-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="8" x2="12" y2="12"/>
                <line x1="12" y1="16" x2="12.01" y2="16"/>
              </svg>
              <p class="empty-text">Нет доступных интеграций</p>
            </div>
          </div>

          <div v-if="activeTab === 'about'" class="settings-panel">
            <div class="panel-header">
              <h3 class="panel-title">Об инструменте</h3>
              <p class="panel-desc">BFElite</p>
            </div>

            <div class="about-content">
              <div class="about-logo">
                <svg class="about-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                  <path d="M2 17l10 5 10-5"/>
                  <path d="M2 12l10 5 10-5"/>
                </svg>
                <div>
                  <span class="about-name gradient-text">BFElite</span>
                </div>
              </div>

              <div class="about-grid">
                <div class="about-item">
                  <span class="about-label">Статус</span>
                  <span class="about-value" :class="{ active: ollamaTestOk }">
                    <template v-if="ollamaTestOk">
                      <svg class="status-online-dot" viewBox="0 0 24 24" fill="currentColor">
                        <circle cx="12" cy="12" r="10"/>
                      </svg>
                      Онлайн
                    </template>
                    <template v-else>
                      <svg class="status-offline-dot" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/>
                      </svg>
                      Офлайн
                    </template>
                  </span>
                </div>
                <div class="about-item">
                  <span class="about-label">Модель</span>
                  <span class="about-value">{{ settings.ollamaModel }}</span>
                </div>
                <div class="about-item">
                  <span class="about-label">Сервер</span>
                  <span class="about-value">{{ settings.ollamaHost }}</span>
                </div>
                <div class="about-item">
                  <span class="about-label">API ключи</span>
                  <span class="about-value">{{ configuredKeys }} настроено</span>
                </div>
              </div>

              <div class="about-footer">
                <a
                  href="https://github.com/ceannastar/OSINT"
                  target="_blank"
                  rel="noopener"
                  class="about-link"
                >
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/>
                  </svg>
                  By ceannastar
                </a>
                <span class="about-divider">·</span>
                <span class="about-copy">BreachForumsElite.</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed } from 'vue'

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
  featuredSponsors: { type: Array, required: true }
})

const emit = defineEmits([
  'close',
  'save-keys',
  'test-ollama',
  'toggle-advanced-keys',
  'toggle-show-key',
  'save-ollama-settings'
])

const activeTab = ref('model')
const isTesting = ref(false)

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
    id: 'integrations', 
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>', 
    label: 'Интеграции' 
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

// Обработчик тестирования соединения
const handleTestConnection = async () => {
  isTesting.value = true
  await emit('test-ollama')
  isTesting.value = false
}

// Обработчик сохранения настроек
const handleSaveSettings = async () => {
  await emit('save-ollama-settings')
}
</script>

<style scoped>
/* Все стили остаются без изменений */
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

/* Заголовок */
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

/* Вкладки */
.settings-tabs {
  display: flex;
  gap: 0.25rem;
  padding: 0.75rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
  flex-shrink: 0;
  background: var(--bg-secondary);
}

.settings-tab {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.4rem 0.75rem;
  border-radius: 0.5rem;
  border: none;
  background: transparent;
  color: var(--text-muted);
  font-size: 0.75rem;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
}

.settings-tab:hover {
  color: var(--text-secondary);
  background: var(--bg-glass);
}

.settings-tab.active {
  color: var(--text-primary);
  background: var(--bg-glass);
  border: 1px solid var(--border-color);
}

.settings-tab.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 2px;
  background: var(--accent-primary);
  border-radius: 1px;
}

.tab-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
}

.tab-icon :deep(svg) {
  width: 16px;
  height: 16px;
  stroke: currentColor;
}

.tab-label {
  font-weight: 500;
}

.tab-badge {
  font-size: 0.55rem;
  padding: 0.05rem 0.4rem;
  border-radius: 9999px;
  background: var(--accent-primary);
  color: var(--bg-primary);
  font-weight: 600;
}

/* Контент */
.settings-content {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.settings-panel {
  animation: fadein 0.2s ease;
}

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

/* Статус карточка */
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

/* Формы */
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

.input-toggle {
  background: none;
  border: none;
  color: var(--text-muted);
  padding: 0.15rem;
  cursor: pointer;
  transition: color 0.3s ease;
}

.input-toggle:hover {
  color: var(--text-primary);
}

.form-hint {
  font-size: 0.65rem;
  color: var(--text-muted);
  margin: 0;
}

/* Детали соединения */
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

/* Действия */
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

.save-feedback {
  font-size: 0.7rem;
  font-family: 'JetBrains Mono', monospace;
}

/* API Keys */
.api-key-item {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.api-key-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.api-key-label {
  font-size: 0.7rem;
  color: var(--text-secondary);
}

.api-key-status {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.6rem;
  color: var(--text-muted);
  font-weight: 500;
}

.api-key-status.filled {
  color: var(--accent-primary);
}

.status-filled,
.status-empty {
  width: 10px;
  height: 10px;
}

.status-filled {
  color: var(--accent-primary);
}

.status-empty {
  stroke: var(--text-muted);
}

/* Integrations */
.integrations-grid {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.integration-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  border: 1px solid var(--border-color);
  text-decoration: none;
  transition: all 0.3s ease;
}

.integration-card:hover {
  border-color: var(--accent-primary);
  transform: translateX(4px);
  box-shadow: 0 4px 20px rgba(0, 255, 200, 0.05);
}

.integration-icon {
  width: 20px;
  height: 20px;
  stroke: var(--text-muted);
  opacity: 0.4;
  flex-shrink: 0;
}

.integration-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.integration-name {
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--text-primary);
}

.integration-tagline {
  font-size: 0.65rem;
  color: var(--text-muted);
}

.integration-arrow {
  color: var(--text-muted);
  font-size: 0.7rem;
  transition: all 0.3s ease;
}

.integration-card:hover .integration-arrow {
  color: var(--accent-primary);
  transform: translateX(4px);
}

.empty-integrations {
  text-align: center;
  padding: 2rem 1rem;
}

.empty-icon {
  width: 40px;
  height: 40px;
  margin: 0 auto 0.5rem;
  stroke: var(--text-muted);
  opacity: 0.3;
  display: block;
}

.empty-text {
  font-size: 0.75rem;
  color: var(--text-muted);
}

/* About */
.about-content {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.about-logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  border-radius: 0.5rem;
  background: var(--bg-glass);
  border: 1px solid var(--border-color);
}

.about-icon {
  width: 32px;
  height: 32px;
  stroke: var(--accent-primary);
  flex-shrink: 0;
}

.about-name {
  font-size: 1.1rem;
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
}

.about-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.about-item {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  background: var(--bg-glass);
  border: 1px solid var(--border-color);
}

.about-label {
  font-size: 0.55rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-muted);
}

.about-value {
  font-size: 0.75rem;
  color: var(--text-secondary);
  font-weight: 500;
  word-break: break-all;
  display: flex;
  align-items: center;
  gap: 4px;
}

.about-value.active {
  color: var(--accent-primary);
}

.status-online-dot,
.status-offline-dot {
  width: 12px;
  height: 12px;
  flex-shrink: 0;
}

.status-online-dot {
  color: var(--accent-primary);
}

.status-offline-dot {
  stroke: var(--red);
}

.about-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--border-color);
  font-size: 0.65rem;
  color: var(--text-muted);
}

.about-link {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  color: var(--text-muted);
  text-decoration: none;
  transition: color 0.3s ease;
}

.about-link:hover {
  color: var(--text-primary);
}

.about-divider {
  color: var(--border-color);
}

.about-copy {
  opacity: 0.6;
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

@keyframes fadein {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>