<template>
  <div v-if="show" class="error-overlay">
    <div class="error-modal glass-card">
      <svg class="error-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <circle cx="12" cy="12" r="10"/>
        <line x1="12" y1="8" x2="12" y2="12"/>
        <line x1="12" y1="16" x2="12.01" y2="16"/>
      </svg>
      <h2 class="error-title">Ошибка подключения</h2>
      <p class="error-message">{{ message }}</p>
      <p class="error-hint">Убедитесь, что сервер BFElite запущен и укажите правильный адрес</p>
      
      <div class="error-input-group">
        <label class="error-input-label">Адрес сервера</label>
        <div class="error-input-wrapper glass-card">
          <span class="error-input-prefix">http://</span>
          <input
            :value="host"
            placeholder="localhost:8080"
            class="error-input"
            @input="$emit('update:host', $event.target.value)"
            @keydown.enter="$emit('retry')"
          />
        </div>
        <p class="error-input-hint">Пример: localhost:8080 или 192.168.1.100:8080</p>
      </div>

      <button class="error-btn btn-primary" @click="$emit('retry')">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M23 4v6h-6"/>
          <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
        </svg>
        Попробовать снова
      </button>
      <div class="error-details">
        <span class="error-detail-label">Статус:</span>
        <span class="error-detail-value">{{ status || 'Неизвестно' }}</span>
        <span class="error-detail-divider">·</span>
        <span class="error-detail-label">Хост:</span>
        <span class="error-detail-value">{{ host }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  show: { type: Boolean, required: true },
  message: { type: String, default: '' },
  status: { type: String, default: '' },
  host: { type: String, required: true }
})

const emit = defineEmits(['retry', 'update:host'])
</script>

<style scoped>
.error-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  padding: 20px;
}

.error-modal {
  max-width: 480px;
  width: 100%;
  padding: 40px;
  text-align: center;
  background: var(--bg-glass);
  backdrop-filter: blur(30px);
  border: 1px solid rgba(248, 81, 73, 0.3);
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  animation: fadein 0.3s ease;
}

.error-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 16px;
  stroke: var(--red);
}

.error-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.error-message {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 16px;
}

.error-hint {
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 20px;
}

.error-input-group {
  text-align: left;
  margin-bottom: 20px;
}

.error-input-label {
  display: block;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.error-input-wrapper {
  display: flex;
  align-items: center;
  padding: 0 12px;
  border-radius: 8px;
  background: var(--bg-glass);
  border: 1px solid var(--border-color);
  transition: border-color 0.3s ease;
}

.error-input-wrapper:focus-within {
  border-color: var(--accent-primary);
  box-shadow: 0 0 20px rgba(0, 255, 200, 0.05);
}

.error-input-prefix {
  color: var(--text-muted);
  font-size: 13px;
  font-family: 'Courier New', monospace;
  flex-shrink: 0;
}

.error-input {
  flex: 1;
  padding: 10px 8px;
  background: transparent;
  border: none;
  color: var(--text-primary);
  font-size: 14px;
  font-family: 'Courier New', monospace;
  outline: none;
}

.error-input::placeholder {
  color: var(--text-muted);
}

.error-input-hint {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 4px;
  opacity: 0.7;
}

.error-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  border: none;
  transition: all 0.3s ease;
  cursor: pointer;
  margin-bottom: 20px;
  width: 100%;
  justify-content: center;
}

.btn-primary {
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  color: var(--bg-primary);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 255, 200, 0.3);
}

.error-details {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding-top: 16px;
  border-top: 1px solid var(--border-color);
  font-size: 12px;
  color: var(--text-muted);
}

.error-detail-label {
  color: var(--text-muted);
}

.error-detail-value {
  color: var(--text-secondary);
  font-weight: 500;
}

.error-detail-divider {
  color: var(--border-color);
}

@keyframes fadein {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
</style>