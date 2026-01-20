<template>
  <Dialog
    v-model="show"
    :options="{
      title: 'Lead Score Breakdown',
      size: 'xl',
    }"
  >
    <template #body-content>
      <div v-if="loading" class="flex items-center justify-center py-8">
        <LoadingIndicator class="h-6 w-6 text-ink-gray-4" />
      </div>
      <div v-else-if="scoreData" class="space-y-6">
        <!-- Overall Score -->
        <div class="flex items-center justify-between border-b pb-4">
          <div>
            <h3 class="text-lg font-semibold">Overall Lead Score</h3>
            <p class="text-sm text-ink-gray-4">
              {{ scoreData.summary || 'AI-generated lead quality score' }}
            </p>
          </div>
          <div
            :class="[
              'flex h-16 w-16 items-center justify-center rounded-full text-2xl font-bold',
              scoreColorClass,
            ]"
          >
            {{ scoreData.score }}
          </div>
        </div>

        <!-- Score Factors -->
        <div class="space-y-4">
          <h4 class="font-semibold">Score Factors</h4>
          <div
            v-for="factor in scoreData.factors"
            :key="factor.name"
            class="space-y-2"
          >
            <div class="flex items-center justify-between">
              <span class="text-sm font-medium">{{ factor.name }}</span>
              <span class="text-sm font-semibold">{{ factor.score }}/{{ factor.max_score }}</span>
            </div>
            <div class="h-2 w-full rounded-full bg-surface-gray-3">
              <div
                :class="[
                  'h-2 rounded-full transition-all',
                  getProgressColor(factor.score, factor.max_score),
                ]"
                :style="{ width: `${(factor.score / factor.max_score) * 100}%` }"
              ></div>
            </div>
            <p class="text-xs text-ink-gray-4">{{ factor.reason }}</p>
          </div>
        </div>

        <!-- Recommendations -->
        <div v-if="scoreData.recommendations?.length" class="space-y-3">
          <h4 class="font-semibold">Recommendations</h4>
          <ul class="space-y-2">
            <li
              v-for="(rec, index) in scoreData.recommendations"
              :key="index"
              class="flex gap-2 text-sm"
            >
              <svg
                class="mt-0.5 h-4 w-4 flex-shrink-0 text-ink-gray-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 5l7 7-7 7"
                />
              </svg>
              <span>{{ rec }}</span>
            </li>
          </ul>
        </div>

        <!-- Next Best Action -->
        <div v-if="scoreData.next_action" class="rounded-lg bg-blue-50 p-4">
          <h4 class="mb-2 font-semibold text-blue-900">Next Best Action</h4>
          <p class="text-sm text-blue-700">{{ scoreData.next_action }}</p>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { computed } from 'vue'
import { Dialog } from 'frappe-ui'
import LoadingIndicator from '@/components/Icons/LoadingIndicator.vue'

const props = defineProps({
  modelValue: Boolean,
  scoreData: {
    type: Object,
    default: null,
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:modelValue'])

const show = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value),
})

const scoreColorClass = computed(() => {
  const score = props.scoreData?.score || 0
  if (score >= 80) {
    return 'bg-green-100 text-green-700'
  } else if (score >= 60) {
    return 'bg-blue-100 text-blue-700'
  } else if (score >= 40) {
    return 'bg-yellow-100 text-yellow-700'
  } else {
    return 'bg-red-100 text-red-700'
  }
})

function getProgressColor(score, maxScore) {
  const percentage = (score / maxScore) * 100
  if (percentage >= 80) {
    return 'bg-green-500'
  } else if (percentage >= 60) {
    return 'bg-blue-500'
  } else if (percentage >= 40) {
    return 'bg-yellow-500'
  } else {
    return 'bg-red-500'
  }
}
</script>
