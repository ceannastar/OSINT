<template>
  <aside class="sidebar glass">
    <!-- Логотип -->
    <div class="sidebar-header">
      <div class="logo-wrapper">
        <div class="logo-icon c-float">⬡</div>
        <div>
          <span class="logo-text gradient-text">BFElite</span>
          <span class="logo-sub">OSINT инструмент</span>
        </div>
      </div>
    </div>

    <!-- Статус -->
    <div class="status-section">
      <div class="status-item">
        <span class="status-dot" :class="{ connected: aiBackend === 'ollama' }"></span>
        <span class="status-label">Модель: </span>
        <span class="status-value" v-if="aiBackend === 'ollama'">{{ settings.ollamaModel }}</span>
        <span class="status-value" v-else>Offline</span>
      </div>
    </div>

    <!-- Быстрые действия -->
    <div class="quick-actions">
      <button class="action-btn glass-card" @click="$emit('new-conversation')">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M12 5v14M5 12h14"/>
        </svg>
        Новый чат
      </button>
      <button class="action-btn glass-card" @click="$emit('open-settings')">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="12" cy="12" r="3"/>
          <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
        </svg>
        Настройки
      </button>
    </div>

    <div class="sidebar-divider"></div>

    <!-- Информация о сессии -->
    <div class="session-info">
      <div class="info-item">
        <span class="info-label">Количество сообщений</span>
        <span class="info-value">{{ messagesCount }}</span>
      </div>
      <div class="info-item">
        <span class="info-label">Статус модели</span>
        <span class="info-value" :class="{ active: aiBackend === 'ollama' }">
          {{ aiBackend === 'ollama' ? 'Active' : 'Idle' }}
        </span>
      </div>
    </div>

    <div class="sidebar-divider"></div>

    <!-- Нижняя часть -->
    <div class="sidebar-footer">
      <button class="theme-toggle glass-card" @click="$emit('toggle-theme')" :title="isLight ? 'Dark mode' : 'Light mode'">
        <svg v-if="!isLight" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="12" cy="12" r="5"/>
          <line x1="12" y1="1" x2="12" y2="3"/>
          <line x1="12" y1="21" x2="12" y2="23"/>
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
          <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
          <line x1="1" y1="12" x2="3" y2="12"/>
          <line x1="21" y1="12" x2="23" y2="12"/>
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
          <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
        </svg>
        <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
        </svg>
      </button>
      <button class="clear-btn glass-card" @click="$emit('clear-conversation')" :disabled="messagesCount === 0">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <polyline points="3 6 5 6 21 6"/>
          <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
          <path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4h6v2"/>
        </svg>
      </button>
    </div>
  </aside>
</template>

<script setup>
defineProps({
  aiBackend: { type: String, required: true },
  settings: { type: Object, required: true },
  isLight: { type: Boolean, required: true },
  messagesCount: { type: Number, required: true }
})

defineEmits(['toggle-theme', 'open-settings', 'clear-conversation', 'new-conversation'])
</script>

<style scoped>
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: 240px;
  display: flex;
  flex-direction: column;
  padding: 1.5rem 1rem;
  background: var(--bg-glass);
  backdrop-filter: blur(20px);
  border-right: 1px solid var(--border-color);
  z-index: 20;
}

.sidebar-header {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.logo-wrapper {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-icon {
  font-size: 1.5rem;
  color: var(--accent-primary);
}

.logo-text {
  font-size: 1.25rem;
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
  line-height: 1.2;
}

.logo-sub {
  display: block;
  font-size: 0.6rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.2em;
  font-weight: 400;
  margin-top: -2px;
}

.status-section {
  background: var(--bg-secondary);
  border-radius: 0.5rem;
  padding: 0.5rem 0.75rem;
  margin-bottom: 1rem;
  border: 1px solid var(--border-color);
}

.status-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--text-muted);
  transition: all 0.3s ease;
}

.status-dot.connected {
  background: var(--accent-primary);
  box-shadow: 0 0 10px rgba(0, 255, 200, 0.4);
  animation: pulse-glow 1.5s ease-in-out infinite;
}

.status-label {
  color: var(--text-muted);
}

.status-value {
  color: var(--text-primary);
  font-weight: 500;
  margin-left: auto;
}

.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  background: var(--bg-glass);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  font-size: 0.8rem;
  transition: all 0.3s ease;
  cursor: pointer;
}

.action-btn:hover {
  color: var(--text-primary);
  border-color: var(--accent-primary);
  transform: translateX(4px);
  box-shadow: 0 4px 15px rgba(0, 255, 200, 0.05);
}

.sidebar-divider {
  height: 1px;
  background: var(--border-color);
  margin: 0.75rem 0;
}

.session-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  padding: 0.25rem 0;
}

.info-label {
  color: var(--text-muted);
}

.info-value {
  color: var(--text-secondary);
  font-weight: 500;
}

.info-value.active {
  color: var(--accent-primary);
}

.sidebar-footer {
  margin-top: auto;
  display: flex;
  gap: 0.5rem;
}

.theme-toggle,
.clear-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem;
  border-radius: 0.5rem;
  background: var(--bg-glass);
  border: 1px solid var(--border-color);
  color: var(--text-muted);
  transition: all 0.3s ease;
  cursor: pointer;
}

.theme-toggle:hover,
.clear-btn:hover:not(:disabled) {
  color: var(--text-primary);
  border-color: var(--accent-primary);
}

.clear-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

@keyframes pulse-glow {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}
</style>