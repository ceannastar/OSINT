<template>
  <div class="empty-state">
    <div class="empty-content">
      <div class="empty-icon c-float">◆</div>
      <h1 class="empty-title">Начните расследование. Просто введите запрос</h1>
      <p class="empty-subtitle">Или нажмите на одну из кнопок ниже</p>
      <div class="suggestions-grid">
        <SuggestionButton
          v-for="s in suggestions"
          :key="s.title"
          :suggestion="s"
          @click="$emit('send', s.prompt)"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import SuggestionButton from './SuggestionButton.vue'

defineProps({
  suggestions: { type: Array, required: true }
})

defineEmits(['send'])
</script>

<style scoped>
.empty-state {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  max-width: 480px;
}

.empty-icon {
  font-size: 2.5rem;
  color: var(--accent-primary);
  margin-bottom: 1rem;
  opacity: 0.4;
}

.empty-title {
  font-size: 1.5rem;
  font-weight: 600;
  font-family: 'Inter', system-ui, sans-serif;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

.empty-subtitle {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.suggestions-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  justify-content: center;
  margin-bottom: 2rem;
}

.empty-hint {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  background: var(--bg-glass);
  border: 1px solid var(--border-color);
  font-size: 0.65rem;
  color: var(--text-muted);
}

.hint-key {
  font-family: 'JetBrains Mono', monospace;
  padding: 0.05rem 0.35rem;
  background: var(--bg-secondary);
  border-radius: 3px;
}

.hint-divider {
  color: var(--border-color);
}
</style>