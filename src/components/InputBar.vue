<template>
  <div class="input-bar">
    <div class="input-container">
      <div class="input-wrapper">
        <textarea
          ref="textareaRef"
          v-model="model"
          :disabled="isStreaming"
          placeholder="Исследуйте цель или задайте вопрос..."
          rows="1"
          class="input-textarea"
          @keydown.enter.exact.prevent="$emit('send')"
          @input="autoResize"
        ></textarea>

        <button
          @click="$emit('send')"
          :disabled="isStreaming || !model.trim()"
          class="send-button"
        >
          <svg v-if="!isStreaming" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/>
          </svg>
          <svg v-else width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="c-spin">
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
  background-color: var(--bg);
  border-top: 1px solid var(--border);
  padding: 0.75rem 1rem;
}

.input-container {
  max-width: 672px;
  margin: 0 auto;
}

.input-wrapper {
  border: 1px solid var(--border);
  border-radius: 0.375rem;
  display: flex;
  align-items: flex-end;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  transition: border-color 0.2s;
}

.input-wrapper:focus-within {
  border-color: var(--accent);
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

.send-button {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  border-radius: 9999px;
  background-color: var(--accent);
  color: var(--bg);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
  border: none;
  cursor: pointer;
  margin-bottom: 0.125rem;
}

.send-button:hover:not(:disabled) {
  background-color: color-mix(in srgb, var(--accent) 80%, black);
}

.send-button:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}
</style>