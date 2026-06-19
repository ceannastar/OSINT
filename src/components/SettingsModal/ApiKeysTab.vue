<template>
  <div class="settings-panel">
    <div class="panel-header">
      <h3 class="panel-title">API Ключи</h3>
      <p class="panel-desc">Подключение к внешним сервисам разведки</p>
    </div>

    <div class="settings-group">
      <!-- VK Token -->
      <div class="api-key-item">
        <div class="api-key-header">
          <span class="api-key-label">VK Token</span>
          <span class="api-key-status" :class="{ filled: vkData.token }">
            <template v-if="vkData.token">
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
            <path d="M17 2a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5h10z"/>
            <path d="M12 8v8M8 12h8"/>
          </svg>
          <input
            :type="showVkToken ? 'text' : 'password'"
            v-model="vkData.token"
            placeholder="vk1.a.xxxxxxxx..."
            class="form-input"
          />
          <button
            @click="showVkToken = !showVkToken"
            class="input-toggle"
          >
            <svg v-if="!showVkToken" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
              <circle cx="12" cy="12" r="3"/>
            </svg>
            <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
              <line x1="1" y1="1" x2="23" y2="23"/>
            </svg>
          </button>
        </div>
        <p class="form-hint">Получите токен в настройках приложения <code>VK Developers</code></p>
      </div>

      <!-- Разделитель -->
      <div class="section-divider">
        <span class="section-divider-text">Telegram API</span>
      </div>

      <!-- Telegram API ID -->
      <div class="api-key-item">
        <div class="api-key-header">
          <span class="api-key-label">Telegram API ID</span>
          <span class="api-key-status" :class="{ filled: telegramData.api_id }">
            <template v-if="telegramData.api_id">
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
            <path d="M12 2a8 8 0 0 0-8 8c0 5 8 12 8 12s8-7 8-12a8 8 0 0 0-8-8z"/>
            <circle cx="12" cy="10" r="3"/>
          </svg>
          <input
            :type="showTelegramKeys.api_id ? 'text' : 'password'"
            v-model="telegramData.api_id"
            placeholder="Введите API ID (например: 123456)"
            class="form-input"
          />
          <button
            @click="showTelegramKeys.api_id = !showTelegramKeys.api_id"
            class="input-toggle"
          >
            <svg v-if="!showTelegramKeys.api_id" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
              <circle cx="12" cy="12" r="3"/>
            </svg>
            <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
              <line x1="1" y1="1" x2="23" y2="23"/>
            </svg>
          </button>
        </div>
        <p class="form-hint">Получите API ID на <code>my.telegram.org</code></p>
      </div>

      <!-- Telegram API Hash -->
      <div class="api-key-item">
        <div class="api-key-header">
          <span class="api-key-label">Telegram API Hash</span>
          <span class="api-key-status" :class="{ filled: telegramData.api_hash }">
            <template v-if="telegramData.api_hash">
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
            <path d="M12 2a8 8 0 0 0-8 8c0 5 8 12 8 12s8-7 8-12a8 8 0 0 0-8-8z"/>
            <circle cx="12" cy="10" r="3"/>
          </svg>
          <input
            :type="showTelegramKeys.api_hash ? 'text' : 'password'"
            v-model="telegramData.api_hash"
            placeholder="Введите API Hash (например: 12345abcde...)"
            class="form-input"
          />
          <button
            @click="showTelegramKeys.api_hash = !showTelegramKeys.api_hash"
            class="input-toggle"
          >
            <svg v-if="!showTelegramKeys.api_hash" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
              <circle cx="12" cy="12" r="3"/>
            </svg>
            <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
              <line x1="1" y1="1" x2="23" y2="23"/>
            </svg>
          </button>
        </div>
        <p class="form-hint">Получите API Hash на <code>my.telegram.org</code></p>
      </div>

      <!-- Telegram Phone Number -->
      <div class="api-key-item">
        <div class="api-key-header">
          <span class="api-key-label">Телефон для Telegram</span>
          <span class="api-key-status" :class="{ filled: telegramData.phone }">
            <template v-if="telegramData.phone">
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
            <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.362 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.574 2.81.7A2 2 0 0 1 22 16.92z"/>
          </svg>
          <input
            :type="showTelegramKeys.phone ? 'text' : 'password'"
            v-model="telegramData.phone"
            placeholder="+7 900 123 45 67"
            class="form-input"
          />
          <button
            @click="showTelegramKeys.phone = !showTelegramKeys.phone"
            class="input-toggle"
          >
            <svg v-if="!showTelegramKeys.phone" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
              <circle cx="12" cy="12" r="3"/>
            </svg>
            <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
              <line x1="1" y1="1" x2="23" y2="23"/>
            </svg>
          </button>
        </div>
        <p class="form-hint">Номер телефона, привязанный к аккаунту Telegram</p>
      </div>

      <!-- Кнопка сохранения -->
      <div class="form-actions">
        <button
          @click="saveAllKeys"
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
        <span v-if="saveMessage" :class="saveMessageOk ? 'text-accent' : 'text-error'" class="save-feedback">
          {{ saveMessage }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  apiKeys: { type: Array, required: true },
  showKeys: { type: Object, required: true },
  setupData: { type: Object, required: true },
  setupMsg: { type: String, required: true },
  setupOk: { type: Boolean, required: true }
})

const emit = defineEmits(['save-keys', 'toggle-show-key'])

const vkData = ref({
  token: ''
})

const telegramData = ref({
  api_id: '',
  api_hash: '',
  phone: ''
})

const showVkToken = ref(false)
const showTelegramKeys = ref({
  api_id: false,
  api_hash: false,
  phone: false
})

const saveMessage = ref('')
const saveMessageOk = ref(false)

const loadSavedData = () => {
  try {
    // VK
    const savedVk = localStorage.getItem('vk_data')
    if (savedVk) {
      vkData.value = JSON.parse(savedVk)
    }
    
    // Telegram
    const savedTelegram = localStorage.getItem('telegram_api_data')
    if (savedTelegram) {
      telegramData.value = JSON.parse(savedTelegram)
    }
  } catch {}
}

const saveToLocalStorage = () => {
  try {
    localStorage.setItem('vk_data', JSON.stringify(vkData.value))
    localStorage.setItem('telegram_api_data', JSON.stringify(telegramData.value))
  } catch {}
}

const saveAllKeys = async () => {
  saveMessage.value = 'Сохранение...'
  saveMessageOk.value = false
  
  saveToLocalStorage()
  
  try {
    const vkResponse = await fetch('/api/vk/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token: vkData.value.token })
    })
    
    if (!vkResponse.ok) {
      throw new Error('Ошибка сохранения VK токена')
    }
  } catch (error) {
    saveMessage.value = `Ошибка VK: ${error.message}`
    saveMessageOk.value = false
    setTimeout(() => { saveMessage.value = '' }, 3000)
    return
  }
  
  try {
    const tgResponse = await fetch('/api/telegram/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(telegramData.value)
    })
    
    if (!tgResponse.ok) {
      throw new Error('Ошибка сохранения Telegram данных')
    }
    
    saveMessage.value = 'Все ключи сохранены ✓'
    saveMessageOk.value = true
  } catch (error) {
    saveMessage.value = `Ошибка Telegram: ${error.message}`
    saveMessageOk.value = false
  }
  
  setTimeout(() => {
    saveMessage.value = ''
  }, 3000)
}

onMounted(() => {
  loadSavedData()
})

watch([vkData, telegramData], () => {
  saveToLocalStorage()
}, { deep: true })
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

.settings-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

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
  font-size: 0.6rem;
  color: var(--text-muted);
  margin-top: 0.2rem;
}

.form-hint code {
  background: var(--bg-secondary);
  padding: 0.05rem 0.3rem;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  color: var(--accent-primary);
  font-size: 0.6rem;
}

.section-divider {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin: 0.5rem 0;
}

.section-divider::before,
.section-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border-color);
}

.section-divider-text {
  font-size: 0.7rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  white-space: nowrap;
}

.form-actions {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.75rem;
  font-weight: 500;
  border: none;
  transition: all 0.3s ease;
  cursor: pointer;
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  color: var(--bg-primary);
  width: 100%;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 20px rgba(0, 255, 200, 0.3);
}

.save-feedback {
  font-size: 0.7rem;
  font-family: 'JetBrains Mono', monospace;
}

.text-accent {
  color: var(--accent-primary);
}

.text-error {
  color: var(--red);
}
</style>