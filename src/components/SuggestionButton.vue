<template>
  <button
    @click="$emit('click')"
    class="suggestion-btn glass-card"
  >
    <span class="suggestion-icon" v-html="suggestion.svgIcon"></span>
    <span class="suggestion-text">{{ suggestion.title }}</span>
    <span class="suggestion-arrow">→</span>
  </button>
</template>

<script setup>
defineProps({
  suggestion: { type: Object, required: true }
})

defineEmits(['click'])
</script>

<style scoped>
.suggestion-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  font-size: 0.8rem;
  color: var(--text-secondary);
  background: var(--bg-glass);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border-color);
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Inter', system-ui, sans-serif;
}

.suggestion-btn:hover {
  color: var(--text-primary);
  border-color: var(--accent-primary);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 255, 200, 0.1);
}

.suggestion-btn:hover .suggestion-arrow {
  transform: translateX(2px);
  opacity: 1;
}

.suggestion-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 14px;
  height: 14px;
  opacity: 0.5;
  transition: opacity 0.3s ease;
}

.suggestion-btn:hover .suggestion-icon {
  opacity: 1;
}

.suggestion-icon :deep(svg) {
  width: 14px;
  height: 14px;
  stroke: currentColor;
}

.suggestion-text {
  font-weight: 500;
}

.suggestion-arrow {
  opacity: 0;
  transition: all 0.3s ease;
  color: var(--accent-primary);
  font-size: 0.7rem;
}
</style>