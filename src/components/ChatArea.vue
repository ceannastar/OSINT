<template>
  <div id="chat-area" class="chat-area">
    <div class="chat-inner">
      <EmptyState v-if="messages.length === 0" :suggestions="suggestions" @send="sendSuggestion" />

      <div v-else class="messages-list">
        <MessageItem
          v-for="(msg, index) in messages"
          :key="index"
          :message="msg"
          :is-streaming="isStreaming"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import EmptyState from './EmptyState.vue'
import MessageItem from './MessageItem.vue'

defineProps({
  messages: { type: Array, required: true },
  suggestions: { type: Array, required: true },
  isStreaming: { type: Boolean, required: true }
})

defineEmits(['send-suggestion'])
</script>

<style scoped>
.chat-area {
  height: 100%;
  overflow-y: auto;
  background-color: var(--bg);
}

.chat-inner {
  max-width: 672px;
  margin: 0 auto;
  padding: 1.5rem 1rem;
  min-height: 100%;
  display: flex;
  flex-direction: column;
}

.messages-list {
  flex: 1;
  padding-bottom: 1rem;
}
</style>