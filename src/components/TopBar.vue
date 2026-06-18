<template>
  <header class="top-bar glass">
    <div class="top-bar-left">
      <div class="logo-wrapper">
        <div class="logo-icon">✦</div>
        <span class="logo-text gradient-text">BFElite</span>
      </div>
    </div>

    <div class="top-bar-center">
      <div class="status-indicator">
        <span class="status-dot" :class="{ connected: aiBackend === 'ollama' }"></span>
        <button @click="$emit('open-settings')" class="status-button">
          <span v-if="aiBackend === 'ollama'">
            <span class="status-label">Model </span>
            <span class="status-value">{{ settings.ollamaModel }}</span>
          </span>
          <span v-else class="status-value">Not configured</span>
        </button>
      </div>
    </div>

    <div class="top-bar-right">
      <button @click="$emit('toggle-theme')" class="icon-btn glass-card" :title="isLight ? 'Dark mode' : 'Light mode'">
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

      <button @click="$emit('open-settings')" class="icon-btn glass-card" title="Settings">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="12" cy="12" r="3"/>
          <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
        </svg>
      </button>

      <button
        @click="$emit('clear-conversation')"
        :disabled="messagesCount === 0"
        class="icon-btn glass-card"
        :class="{ disabled: messagesCount === 0 }"
        title="Clear chat"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <polyline points="3 6 5 6 21 6"/>
          <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
          <path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4h6v2"/>
        </svg>
      </button>
    </div>
  </header>
</template>

<script setup>
defineProps({
  aiBackend: { type: String, required: true },
  settings: { type: Object, required: true },
  isLight: { type: Boolean, required: true },
  messagesCount: { type: Number, required: true }
})

defineEmits(['toggle-theme', 'open-settings', 'clear-conversation'])
</script>

<style scoped>
.top-bar {
  flex-shrink: 0;
  height: 56px;
  display: flex;
  align-items: center;
  padding: 0 1.5rem;
  gap: 1rem;
  position: relative;
  z-index: 10;
  border-bottom: 1px solid var(--border-color);
}

.top-bar-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-shrink: 0;
}

.logo-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.logo-icon {
  font-size: 1.25rem;
  color: var(--accent-primary);
  animation: pulse-glow 2s ease-in-out infinite;
}

.logo-text {
  font-size: 1.1rem;
  font-weight: 600;
  font-family: 'JetBrains Mono', monospace;
}

.version-badge {
  font-size: 0.65rem;
  padding: 0.15rem 0.5rem;
  border-radius: 9999px;
  background: var(--bg-glass);
  border: 1px solid var(--border-color);
  color: var(--text-muted);
  font-family: 'JetBrains Mono', monospace;
}

.top-bar-center {
  flex: 1;
  display: flex;
  justify-content: center;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  background: var(--bg-glass);
  border: 1px solid var(--border-color);
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--text-muted);
  transition: background 0.3s ease;
}

.status-dot.connected {
  background: var(--accent-primary);
  box-shadow: 0 0 10px rgba(0, 255, 200, 0.4);
  animation: pulse-glow 1.5s ease-in-out infinite;
}

.status-button {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  font-size: 0.75rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0;
}

.status-label {
  color: var(--text-muted);
}

.status-value {
  color: var(--text-primary);
  font-weight: 500;
}

.top-bar-right {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
}

.icon-btn {
  width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 9999px;
  color: var(--text-muted);
  background: var(--bg-glass);
  border: 1px solid var(--border-color);
  transition: all 0.2s ease;
  cursor: pointer;
}

.icon-btn:hover:not(.disabled) {
  color: var(--text-primary);
  border-color: var(--accent-primary);
  box-shadow: 0 0 20px rgba(0, 255, 200, 0.1);
}

.icon-btn.disabled {
  opacity: 0.3;
  cursor: not-allowed;
}
</style>