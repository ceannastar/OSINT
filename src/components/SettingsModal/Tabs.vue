<template>
  <div class="settings-tabs">
    <button
      v-for="tab in tabs"
      :key="tab.id"
      @click="$emit('switch', tab.id)"
      class="settings-tab"
      :class="{ active: activeTab === tab.id }"
    >
      <span class="tab-icon" v-html="tab.icon"></span>
      <span class="tab-label">{{ tab.label }}</span>
      <span v-if="tab.badge" class="tab-badge">{{ tab.badge }}</span>
    </button>
  </div>
</template>

<script setup>
defineProps({
  tabs: { type: Array, required: true },
  activeTab: { type: String, required: true }
})

defineEmits(['switch'])
</script>

<style scoped>
.settings-tabs {
  display: flex;
  gap: 0.25rem;
  padding: 0.75rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
  flex-shrink: 0;
  background: var(--bg-secondary);
}

.settings-tab {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.4rem 0.75rem;
  border-radius: 0.5rem;
  border: none;
  background: transparent;
  color: var(--text-muted);
  font-size: 0.75rem;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
}

.settings-tab:hover {
  color: var(--text-secondary);
  background: var(--bg-glass);
}

.settings-tab.active {
  color: var(--text-primary);
  background: var(--bg-glass);
  border: 1px solid var(--border-color);
}

.settings-tab.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 2px;
  background: var(--accent-primary);
  border-radius: 1px;
}

.tab-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
}

.tab-icon :deep(svg) {
  width: 16px;
  height: 16px;
  stroke: currentColor;
}

.tab-label {
  font-weight: 500;
}

.tab-badge {
  font-size: 0.55rem;
  padding: 0.05rem 0.4rem;
  border-radius: 9999px;
  background: var(--accent-primary);
  color: var(--bg-primary);
  font-weight: 600;
}
</style>