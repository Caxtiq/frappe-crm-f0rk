<template>
  <div v-if="emailContent" class="border-t bg-surface-gray-1 px-4 py-3">
    <div class="flex items-start justify-between gap-3">
      <div class="flex-1">
        <div class="mb-2 flex items-center gap-2">
          <svg class="h-4 w-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
            />
          </svg>
          <span class="text-sm font-medium text-ink-gray-6">AI Suggested Reply</span>
          <Button
            variant="ghost"
            class="!h-5 !w-5 !p-0"
            @click="$emit('close')"
          >
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </Button>
        </div>
        <div class="prose prose-sm max-w-none rounded-lg bg-white p-3 text-sm">
          <div v-html="emailContent"></div>
        </div>
      </div>
    </div>
    <div class="mt-3 flex gap-2">
      <Button
        variant="solid"
        :label="'Use This Reply'"
        @click="$emit('use-reply', emailContent)"
      >
        <template #prefix>
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M5 13l4 4L19 7"
            />
          </svg>
        </template>
      </Button>
      <Button
        variant="outline"
        :label="'Regenerate'"
        :loading="loading"
        @click="$emit('regenerate')"
      >
        <template #prefix>
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
            />
          </svg>
        </template>
      </Button>
      <Button
        variant="ghost"
        :label="'Dismiss'"
        @click="$emit('close')"
      />
    </div>
  </div>
</template>

<script setup>
import { Button } from 'frappe-ui'

defineProps({
  emailContent: {
    type: String,
    default: null,
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['use-reply', 'regenerate', 'close'])
</script>
