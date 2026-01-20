<template>
  <div class="flex items-center gap-2">
    <div
      v-if="score !== null && score !== undefined"
      :class="[
        'flex items-center gap-1.5 rounded-md px-2 py-1 text-sm font-medium',
        scoreColorClass,
      ]"
    >
      <svg
        class="h-4 w-4"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M13 10V3L4 14h7v7l9-11h-7z"
        />
      </svg>
      <span>{{ score }}/100</span>
      <Button
        v-if="showDetails"
        variant="ghost"
        class="!p-0 !h-4 !w-4"
        @click="$emit('show-breakdown')"
      >
        <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
      </Button>
    </div>
    <Button
      v-else-if="showScoreButton"
      variant="outline"
      :label="loading ? 'Scoring...' : 'Score Lead'"
      :loading="loading"
      @click="$emit('score-lead')"
    >
      <template #prefix>
        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M13 10V3L4 14h7v7l9-11h-7z"
          />
        </svg>
      </template>
    </Button>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Button } from 'frappe-ui'

const props = defineProps({
  score: {
    type: Number,
    default: null,
  },
  showDetails: {
    type: Boolean,
    default: true,
  },
  showScoreButton: {
    type: Boolean,
    default: true,
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['score-lead', 'show-breakdown'])

const scoreColorClass = computed(() => {
  if (props.score >= 80) {
    return 'bg-green-50 text-green-700 border border-green-200'
  } else if (props.score >= 60) {
    return 'bg-blue-50 text-blue-700 border border-blue-200'
  } else if (props.score >= 40) {
    return 'bg-yellow-50 text-yellow-700 border border-yellow-200'
  } else {
    return 'bg-red-50 text-red-700 border border-red-200'
  }
})
</script>
