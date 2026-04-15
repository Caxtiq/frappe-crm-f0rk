<template>
  <div class="ai-suggestions-container">
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center gap-2">
        <FeatherIcon name="lightbulb" class="w-5 h-5 text-ink-yellow-3" />
        <h3 class="text-lg font-semibold text-ink-gray-9">AI Suggestions</h3>
      </div>
      <Button variant="ghost" size="sm" @click="loadSuggestions">
        <FeatherIcon name="refresh-cw" class="w-4 h-4" />
      </Button>
    </div>

    <div v-if="loading" class="text-center py-8">
      <div class="animate-spin w-6 h-6 border-2 border-ink-blue-3 border-t-transparent rounded-full mx-auto"></div>
      <p class="text-sm text-ink-gray-5 mt-2">Loading suggestions...</p>
    </div>

    <div v-else-if="suggestions.length === 0" class="text-center py-8">
      <FeatherIcon name="lightbulb" class="w-12 h-12 text-ink-gray-4 mx-auto mb-3" />
      <p class="text-sm text-ink-gray-5">No suggestions available</p>
      <Button variant="subtle" size="sm" class="mt-3" @click="generateSuggestion">
        Generate Suggestion
      </Button>
    </div>

    <div v-else class="suggestions-list">
      <div
        v-for="suggestion in suggestions"
        :key="suggestion.name"
        class="suggestion-card"
        :class="{ 
          'accepted': suggestion.status === 'Accepted',
          'rejected': suggestion.status === 'Rejected'
        }"
      >
        <div class="suggestion-header">
          <div class="flex items-center gap-2">
            <Badge :label="suggestion.suggestion_type" variant="subtle" />
            <Badge
              :label="suggestion.status"
              :variant="
                suggestion.status === 'Accepted' ? 'success' :
                suggestion.status === 'Rejected' ? 'error' :
                'warning'
              "
            />
          </div>
          <div class="suggestion-actions">
            <Button
              v-if="suggestion.status === 'Pending'"
              variant="ghost"
              size="sm"
              @click="acceptSuggestion(suggestion.name)"
            >
              <FeatherIcon name="check" class="w-4 h-4 text-green-600" />
            </Button>
            <Button
              v-if="suggestion.status === 'Pending'"
              variant="ghost"
              size="sm"
              @click="rejectSuggestion(suggestion.name)"
            >
              <FeatherIcon name="x" class="w-4 h-4 text-red-600" />
            </Button>
          </div>
        </div>

        <div class="suggestion-content">
          <p class="suggestion-text">{{ suggestion.suggestion }}</p>
          <div class="suggestion-time">
            {{ formatTime(suggestion.creation) }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { createResource } from 'frappe-ui'
import { FeatherIcon, Button, Badge } from 'frappe-ui'

const props = defineProps({
  referenceDoctype: {
    type: String,
    required: true,
  },
  referenceName: {
    type: String,
    required: true,
  },
  suggestionType: String,
})

const suggestions = ref([])
const loading = ref(false)

// Get suggestions resource
const suggestionsResource = createResource({
  url: 'crm.api.ai.get_suggestions',
  params: {
    reference_doctype: props.referenceDoctype,
    reference_name: props.referenceName,
    suggestion_type: props.suggestionType,
  },
  auto: true,
  onSuccess(data) {
    suggestions.value = data || []
    loading.value = false
  },
})

// Accept suggestion
const acceptResource = createResource({
  url: 'crm.api.ai.accept_suggestion',
  onSuccess() {
    loadSuggestions()
  },
})

// Reject suggestion
const rejectResource = createResource({
  url: 'crm.api.ai.reject_suggestion',
  onSuccess() {
    loadSuggestions()
  },
})

const loadSuggestions = () => {
  loading.value = true
  suggestionsResource.reload()
}

const acceptSuggestion = (name) => {
  acceptResource.submit({ suggestion_name: name })
}

const rejectSuggestion = (name) => {
  // Could add a dialog for rejection reason
  rejectResource.submit({ suggestion_name: name })
}

const generateSuggestion = () => {
  // Trigger suggestion generation based on type
  if (props.referenceDoctype === 'CRM Lead') {
    createResource({
      url: 'crm.api.ai.score_lead',
      params: { lead_name: props.referenceName },
      auto: true,
      onSuccess() {
        loadSuggestions()
      },
    })
  } else if (props.referenceDoctype === 'CRM Deal') {
    createResource({
      url: 'crm.api.ai.analyze_deal',
      params: { deal_name: props.referenceName },
      auto: true,
      onSuccess() {
        loadSuggestions()
      },
    })
  }
}

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = Math.floor((now - date) / 1000) // seconds

  if (diff < 60) return 'Just now'
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
  return date.toLocaleDateString()
}

onMounted(() => {
  loadSuggestions()
})
</script>

<style scoped>
.ai-suggestions-container {
  padding: 1rem;
  background: var(--surface-white);
}

.suggestions-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.suggestion-card {
  border: 1px solid var(--outline-gray-2);
  border-radius: 8px;
  padding: 1rem;
  background: var(--surface-white);
  transition: all 0.2s;
}

.suggestion-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border-color: var(--outline-gray-3);
}

.suggestion-card.accepted {
  border-color: var(--ink-green-3);
  background: var(--surface-green-1);
}

.suggestion-card.rejected {
  border-color: var(--ink-red-3);
  background: var(--surface-red-1);
  opacity: 0.7;
}

.suggestion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.suggestion-actions {
  display: flex;
  gap: 0.5rem;
}

.suggestion-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.suggestion-text {
  color: var(--ink-gray-8);
  line-height: 1.6;
  white-space: pre-wrap;
}

.suggestion-time {
  font-size: 0.75rem;
  color: var(--ink-gray-5);
}
</style>
