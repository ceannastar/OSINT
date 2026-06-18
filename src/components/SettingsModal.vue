<template>
  <Teleport to="body">
    <div
      v-if="show"
      @click="$emit('close')"
      class="fixed inset-0 z-50 bg-overlay flex items-center justify-center p-4"
    >
      <div
        @click.stop
        class="bg-surface border border-app rounded-lg max-w-md w-full p-6 shadow-xl max-h-[88vh] overflow-y-auto c-fadein"
      >
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-sm font-medium">Settings</h2>
          <button
            @click="$emit('close')"
            class="w-7 h-7 flex items-center justify-center rounded-md text-muted hover:text-primary hover:bg-border-50 transition-colors"
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>

        <!-- AI Backend -->
        <p class="text-xs font-medium text-muted uppercase tracking-wider mb-3">AI Backend</p>
        <div class="bg-border-50 border border-app rounded-md p-3 mb-4 text-center">
          <span class="text-xs text-secondary">Ollama (local)</span>
          <span class="text-muted text-xs block mt-1">Model: {{ settings.ollamaModel }}</span>
        </div>

        <!-- Ollama settings -->
        <div class="bg-app border border-app rounded-md p-4 space-y-3 mb-4">
          <div>
            <label class="text-muted text-xs uppercase tracking-wider block mb-1.5">Model name</label>
            <input
              v-model="settings.ollamaModel"
              placeholder="llama3.2"
              class="w-full bg-surface border border-app rounded-md px-3 py-2 text-sm text-primary focus:outline-none transition-colors"
            />
          </div>
          <div>
            <label class="text-muted text-xs uppercase tracking-wider block mb-1.5">Host URL</label>
            <input
              v-model="settings.ollamaHost"
              placeholder="http://localhost:11434"
              class="w-full bg-surface border border-app rounded-md px-3 py-2 text-sm text-primary focus:outline-none transition-colors"
            />
          </div>
          <div class="flex items-center gap-3">
            <button
              @click="$emit('test-ollama')"
              class="px-3 py-1.5 rounded-md border border-app text-secondary hover:text-primary text-xs transition-all"
            >
              Test connection
            </button>
            <button
              @click="$emit('save-ollama-settings')"
              class="px-3 py-1.5 rounded-md border border-app text-secondary hover:text-primary text-xs transition-all"
            >
              Save settings
            </button>
            <span v-if="ollamaTestResult" :class="ollamaTestOk ? 'text-accent' : 'text-error'" class="text-xs font-mono">
              {{ ollamaTestResult }}
            </span>
          </div>
        </div>

        <div class="border-t border-app my-5"></div>

        <!-- API keys -->
        <p class="text-xs font-medium text-muted uppercase tracking-wider mb-3">API Keys</p>
        <div class="space-y-3">
          <div v-for="k in apiKeys" :key="k.key">
            <label class="text-secondary text-xs block mb-1">{{ k.label }}</label>
            <div class="relative">
              <input
                :type="showKeys[k.key] ? 'text' : 'password'"
                v-model="setupData[k.key]"
                :placeholder="k.placeholder"
                class="w-full bg-app border border-app rounded-md px-3 py-2 text-sm text-primary focus:outline-none transition-colors pr-9"
              />
              <button
                @click="$emit('toggle-show-key', k.key)"
                class="absolute right-2.5 top-1/2 -translate-y-1/2 text-muted hover:text-secondary transition-colors"
              >
                <svg v-if="!showKeys[k.key]" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>
                </svg>
                <svg v-else width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                  <line x1="1" y1="1" x2="23" y2="23"/>
                </svg>
              </button>
            </div>
          </div>
        </div>

        <div class="flex items-center gap-3 mt-4">
          <button
            @click="$emit('save-keys')"
            class="bg-accent hover:bg-accent-80 text-bg rounded-md px-4 py-2 text-xs font-medium transition-colors"
          >
            Save keys
          </button>
          <span v-if="setupMsg" :class="setupOk ? 'text-accent' : 'text-error'" class="text-xs font-mono">
            {{ setupMsg }}
          </span>
        </div>

        <!-- Sponsors -->
        <template v-if="featuredSponsors.length > 0">
          <div class="border-t border-app mt-4 pt-3">
            <p class="text-muted text-xs mb-2">Featured integrations</p>
            <a
              v-for="s in featuredSponsors"
              :key="s.name"
              :href="s.url"
              target="_blank"
              rel="noopener sponsored"
              class="flex items-center gap-2 text-secondary hover:text-primary text-xs transition-colors mb-1"
            >
              <span class="font-mono">{{ s.name }}</span>
              <span class="text-muted">·</span>
              <span class="text-muted truncate">{{ s.tagline }}</span>
            </a>
          </div>
        </template>

        <!-- Footer -->
      </div>
    </div>
  </Teleport>
</template>

<script setup>
defineProps({
  show: { type: Boolean, required: true },
  settings: { type: Object, required: true },
  apiKeys: { type: Array, required: true },
  showKeys: { type: Object, required: true },
  setupData: { type: Object, required: true },
  setupMsg: { type: String, required: true },
  setupOk: { type: Boolean, required: true },
  showAdvancedKeys: { type: Boolean, required: true },
  ollamaTestResult: { type: String, required: true },
  ollamaTestOk: { type: Boolean, required: true },
  featuredSponsors: { type: Array, required: true },
  version: { type: String, required: true }
})

defineEmits([
  'close',
  'save-keys',
  'test-ollama',
  'toggle-advanced-keys',
  'toggle-show-key',
  'save-ollama-settings'
])
</script>