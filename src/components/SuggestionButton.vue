<template>
  <button
    @click="$emit('click')"
    class="suggestion-btn"
  >
    <span class="suggestion-icon" v-html="suggestion.svgIcon"></span>
    <span class="suggestion-text">{{ suggestion.title }}</span>
    <span class="suggestion-badge">→</span>
  </button>
</template>

<script setup>
defineProps({
  suggestion: { type: Object, required: true }
})

defineEmits(['click'])
</script>

<style>
/* Убираем scoped, чтобы v-html работал корректно */
.suggestion-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.8rem 0.4rem 0.6rem;
  border-radius: 8px;
  font-size: 0.75rem;
  color: var(--text-secondary);
  background: var(--bg-glass);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border-color);
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Inter', system-ui, sans-serif;
  position: relative;
  overflow: hidden;
}

.suggestion-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.suggestion-btn:hover::before {
  opacity: 0.08;
}

.suggestion-btn:hover {
  color: var(--text-primary);
  border-color: var(--accent-primary);
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 255, 200, 0.1);
}

.suggestion-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 14px;
  height: 14px;
  opacity: 0.4;
  transition: opacity 0.3s ease;
  position: relative;
  z-index: 1;
}

.suggestion-btn:hover .suggestion-icon {
  opacity: 0.8;
}

.suggestion-icon svg {
  width: 14px;
  height: 14px;
  stroke: currentColor;
}

.suggestion-text {
  font-weight: 500;
  position: relative;
  z-index: 1;
}

.suggestion-badge {
  font-size: 0.6rem;
  opacity: 0;
  transition: all 0.3s ease;
  color: var(--accent-primary);
  position: relative;
  z-index: 1;
}

.suggestion-btn:hover .suggestion-badge {
  opacity: 1;
  transform: translateX(2px);
}
</style>