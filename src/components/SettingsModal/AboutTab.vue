<template>
  <div class="settings-panel">
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
          <span class="about-value">{{ settings.ollamaModel || 'Не выбрана' }}</span>
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
</template>

<script setup>
defineProps({
  settings: { type: Object, required: true },
  ollamaTestOk: { type: Boolean, required: true },
  configuredKeys: { type: Number, required: true }
})
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
</style>