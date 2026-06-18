<template>
  <button
    @click="$emit('click')"
    class="suggestion-btn"
  >
    <svg 
      width="14" 
      height="14" 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke="currentColor" 
      stroke-width="1.5"
      v-html="suggestion.svgIcon"
    ></svg>
    <span>{{ suggestion.title }}</span>
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
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--border);
  border-radius: 0.375rem;
  font-size: 0.875rem;
  color: var(--text-secondary);
  background: transparent;
  cursor: pointer;
  transition: all 0.2s ease;
}

.suggestion-btn:hover {
  border-color: color-mix(in srgb, var(--accent) 40%, transparent);
  color: var(--text-primary);
}

.suggestion-btn svg {
  flex-shrink: 0;
  width: 14px;
  height: 14px;
}
</style>