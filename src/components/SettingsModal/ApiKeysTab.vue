<template>
  <div class="settings-panel">
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
</template>

<script setup>
defineProps({
  apiKeys: { type: Array, required: true },
  showKeys: { type: Object, required: true },
  setupData: { type: Object, required: true },
  setupMsg: { type: String, required: true },
  setupOk: { type: Boolean, required: true }
})

defineEmits(['save-keys', 'toggle-show-key'])
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

.form-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 0.5rem;
  flex-wrap: wrap;
}

.btn-primary {
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
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  color: var(--bg-primary);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 20px rgba(0, 255, 200, 0.3);
}

.save-feedback {
  font-size: 0.7rem;
  font-family: 'JetBrains Mono', monospace;
}
</style>