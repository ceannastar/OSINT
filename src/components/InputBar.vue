<template>
  <div class="input-bar">
    <div class="input-container">
      <div class="input-wrapper glass-card">
        <div class="input-prefix">
          <span class="prompt-symbol">❯</span>
        </div>
        <textarea
          ref="textareaRef"
          v-model="model"
          :disabled="isStreaming"
          placeholder="Type your investigation query..."
          rows="1"
          class="input-textarea"
          @keydown.enter.exact.prevent="$emit('send')"
          @input="autoResize"
        ></textarea>
        <button
          @click="$emit('send')"
          :disabled="isStreaming || !model.trim()"
          class="send-btn"
        >
          <svg v-if="!isStreaming" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="19" x2="12" y2="5"/>
            <polyline points="5 12 12 5 19 12"/>
          </svg>
          <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="c-spin">
            <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import { autoResize as autoResizeFn } from '../utils/helpers'

const props = defineProps({
  modelValue: { type: String, required: true },
  isStreaming: { type: Boolean, required: true }
})

const emit = defineEmits(['update:modelValue', 'send'])

const model = ref(props.modelValue)
const textareaRef = ref(null)

watch(model, (val) => {
  emit('update:modelValue', val)
})

watch(() => props.modelValue, (val) => {
  if (val !== model.value) {
    model.value = val
  }
})

const autoResize = (event) => {
  const el = event?.target || textareaRef.value
  if (el) {
    autoResizeFn(el)
  }
}

nextTick(() => {
  textareaRef.value?.focus()
})
</script>

<style scoped>
.input-bar {
  flex-shrink: 0;
  padding: 1rem 1.5rem 1.5rem;
  position: relative;
  z-index: 1;
}

.input-container {
  max-width: 720px;
  margin: 0 auto;
}

.input-wrapper {
  display: flex;
  align-items: flex-end;
  gap: 0.75rem;
  padding: 0.5rem 0.75rem;
  border-radius: 0.75rem;
  background: var(--bg-glass);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.input-wrapper:focus-within {
  border-color: var(--accent-primary);
  box-shadow: 0 0 30px rgba(0, 255, 200, 0.05), inset 0 0 30px rgba(0, 255, 200, 0.02);
}

.input-prefix {
  flex-shrink: 0;
  padding-bottom: 0.125rem;
}

.prompt-symbol {
  color: var(--accent-primary);
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.875rem;
  opacity: 0.6;
}

.input-textarea {
  flex: 1;
  background: transparent;
  resize: none;
  font-size: 0.875rem;
  color: var(--text-primary);
  overflow-y: auto;
  font-family: 'Inter', system-ui, sans-serif;
  line-height: 1.625;
  border: none;
  min-height: 22px;
  max-height: 160px;
  padding: 0;
}

.input-textarea:disabled {
  opacity: 0.4;
}

.input-textarea::placeholder {
  color: var(--text-muted);
}

.input-textarea:focus {
  outline: none;
}

.send-btn {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  border-radius: 9999px;
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  color: var(--bg-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
  margin-bottom: 0.125rem;
}

.send-btn:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 0 30px rgba(0, 255, 200, 0.3);
}

.send-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
  transform: none;
}
</style>