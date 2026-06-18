<template>
  <div class="empty-state">
    <h1 class="empty-title">Инструмент OSINT</h1>
    <p class="empty-subtitle">Данный инструмент работает на основе ИИ-агента. Введите любой запрос.</p>
    <div class="suggestions-grid">
      <SuggestionButton
        v-for="s in suggestions"
        :key="s.title"
        :suggestion="s"
        @click="$emit('send', s.prompt)"
      />
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
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 0;
}

.empty-title {
  font-size: 1.125rem;
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.empty-subtitle {
  color: var(--text-muted);
  font-size: 0.875rem;
  margin-bottom: 2rem;
}

.suggestions-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
}
</style>