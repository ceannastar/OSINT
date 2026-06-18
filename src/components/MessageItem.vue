<template>
  <div class="c-fadein">
    <!-- User message -->
    <div v-if="message.role === 'user'" class="flex flex-col items-end mb-4">
      <p class="text-primary text-sm leading-relaxed whitespace-pre-wrap max-w-[80%] text-right">{{ message.content }}</p>
      <span class="text-muted text-xs mt-1 font-mono">{{ message.time || '' }}</span>
    </div>

    <!-- Assistant message -->
    <div v-else class="mb-6">
      <!-- Thinking state -->
      <div v-if="message.parts.length === 0" class="flex items-center gap-1.5 text-muted text-xs font-mono">
        <span class="inline-block c-blink">_</span>thinking
      </div>

      <div class="space-y-3">
        <template v-for="(part, index) in message.parts" :key="index">
          <!-- Text part -->
          <div v-if="part.type === 'text'" class="text-sm text-primary leading-relaxed">
            <div class="md" v-html="renderMarkdown(part.content)"></div>
            <span v-if="part.streaming" class="text-accent ml-0.5 inline-block c-blink">|</span>
          </div>

          <!-- Tool part -->
          <ToolCard v-else-if="part.type === 'tool'" :part="part" />
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { renderMarkdown } from '../utils/markdown'
import ToolCard from './ToolCard.vue'

defineProps({
  message: { type: Object, required: true },
  isStreaming: { type: Boolean, required: true }
})
</script>