<template>
  <header class="top-bar">
    <div class="top-bar-left">
      <span class="logo">OpenOSINT</span>
      <span class="version">{{ version }}</span>
    </div>

    <div class="top-bar-center">
      <button @click="$emit('open-settings')" class="status-button">
        <span v-if="aiBackend === 'ollama'">Ollama {{ settings.ollamaModel }}</span>
        <span v-else>Not configured</span>
      </button>
    </div>

    <div class="top-bar-right">
      <button
        @click="$emit('toggle-theme')"
        :title="isLight ? 'Switch to dark theme' : 'Switch to light theme'"
        class="icon-button"
      >
        <svg v-if="!isLight" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
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
        <svg v-else width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
        </svg>
      </button>

      <button @click="$emit('open-settings')" title="Settings" class="icon-button">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="12" cy="12" r="3"/>
          <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
        </svg>
      </button>

      <button
        @click="$emit('clear-conversation')"
        :disabled="messagesCount === 0"
        title="Clear conversation"
        class="icon-button"
        :class="{ 'disabled': messagesCount === 0 }"
      >
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
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
  version: { type: String, required: true },
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
  height: 48px;
  background-color: var(--surface);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  padding: 0 1rem;
  gap: 0.75rem;
  z-index: 10;
}

.top-bar-left {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.logo {
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-weight: 500;
  font-size: 0.875rem;
  color: var(--text-primary);
}

.version {
  color: var(--text-muted);
  font-size: 0.75rem;
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  margin-left: 0.5rem;
}

.top-bar-center {
  flex: 1;
  display: flex;
  justify-content: center;
}

.status-button {
  font-size: 0.75rem;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  border: 1px solid var(--border);
  color: var(--text-secondary);
  background: transparent;
  transition: color 0.2s;
  cursor: pointer;
}

.status-button:hover {
  color: var(--text-primary);
}

.top-bar-right {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  flex-shrink: 0;
}

.icon-button {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.375rem;
  color: var(--text-muted);
  background: transparent;
  border: none;
  transition: color 0.2s, background-color 0.2s;
  cursor: pointer;
}

.icon-button:hover {
  color: var(--text-primary);
  background-color: var(--surface);
}

.icon-button.disabled {
  opacity: 0.25;
  cursor: not-allowed;
}

.icon-button.disabled:hover {
  color: var(--text-muted);
  background: transparent;
}
</style>