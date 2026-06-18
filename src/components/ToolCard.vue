<template>
  <div class="bg-surface border border-app rounded-md mb-2 overflow-hidden">
    <div class="px-3 py-2 flex items-center justify-between">
      <button
        @click="part.collapsed = !part.collapsed"
        class="flex items-center gap-2 min-w-0 flex-1 text-left"
      >
        <span class="font-mono text-xs text-secondary flex-none">{{ part.tool }}</span>
        <span class="text-muted text-xs truncate">{{ part.input || '' }}</span>
      </button>

      <div class="flex items-center gap-2 flex-none ml-3">
        <span
          class="text-xs font-mono"
          :class="{
            'text-warning': part.status === 'running',
            'text-accent': part.status === 'done',
            'text-error': part.status === 'error'
          }"
        >
          <span v-if="part.status === 'running'" class="inline-flex items-center gap-1">
            <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="c-spin">
              <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
            </svg>
            running
          </span>
          <span v-else-if="part.status === 'done'">{{ part.elapsed ? part.elapsed + 's' : 'done' }}</span>
          <span v-else>error</span>
        </span>

        <button
          v-if="part.output"
          @click.stop="copyText(part.output)"
          class="text-muted hover:text-secondary transition-colors p-0.5"
        >
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
          </svg>
        </button>

        <button
          @click.stop="part.collapsed = !part.collapsed"
          class="text-muted hover:text-secondary transition-colors p-0.5"
        >
          <svg
            width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"
            :class="part.collapsed ? '' : 'rotate-180'"
            class="transition-transform"
          >
            <polyline points="6 9 12 15 18 9"/>
          </svg>
        </button>
      </div>
    </div>

    <div v-if="!part.collapsed && part.output" class="border-t border-app bg-app px-3 py-2 max-h-64 overflow-y-auto">
      <div
        v-for="(line, index) in part.output.split('\n')"
        :key="index"
        class="font-mono text-xs leading-relaxed whitespace-pre-wrap break-all"
        :class="lineClass(line || ' ')"
      >
        {{ line || ' ' }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { copyText, lineClass } from '../utils/helpers'

defineProps({
  part: {
    type: Object,
    required: true,
    validator: (value) => {
      return value.type === 'tool' && typeof value.tool === 'string'
    }
  }
})
</script>