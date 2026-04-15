<template>
  <div class="ai-chat-container crm-fade-up">
    <div class="ai-chat-header">
      <div class="flex items-center gap-2">
        <svg class="h-5 w-5 text-[#1b8655]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
        </svg>
        <div>
          <h3 class="text-base font-semibold text-[var(--crm-text)]">AI Assistant</h3>
          <p class="text-xs text-[var(--crm-text-soft)]">Context-aware CRM copilot</p>
        </div>
      </div>
      <Button
        class="rounded-xl border border-[var(--crm-border)] bg-[var(--crm-surface)] text-[var(--crm-text)] hover:bg-[var(--crm-surface-2)]"
        variant="ghost"
        @click="$emit('close')"
      >
        <FeatherIcon name="x" class="w-4 h-4" />
      </Button>
    </div>

    <div class="ai-chat-messages" ref="messagesContainer">
      <div v-if="loading && messages.length === 0" class="py-8 text-center">
        <div class="mx-auto h-6 w-6 animate-spin rounded-full border-2 border-[#1b8655] border-t-transparent"></div>
        <p class="mt-2 text-sm text-[var(--crm-text-soft)]">Loading conversation...</p>
      </div>

      <div v-else-if="messages.length === 0" class="py-8 text-center">
        <svg class="mx-auto mb-3 h-12 w-12 text-[#89a798]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
        </svg>
        <p class="text-sm text-[var(--crm-text-soft)]">Ask me anything about your CRM data</p>
      </div>

      <div v-else>
        <div
          v-for="(message, index) in messages"
          :key="index"
          class="message"
          :class="message.role === 'user' ? 'message-user' : 'message-ai'"
        >
          <div class="message-avatar">
            <UserAvatar v-if="message.role === 'user'" :user="message.user || 'You'" size="sm" />
            <div v-else class="ai-avatar">
              <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
              </svg>
            </div>
          </div>
          <div class="message-content">
            <div class="message-text" v-html="formatMessage(message.content)"></div>
            <div class="message-time">{{ formatTime(message.timestamp) }}</div>
          </div>
        </div>
      </div>

      <div v-if="isProcessing" class="message message-ai">
        <div class="message-avatar">
          <div class="ai-avatar">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
            </svg>
          </div>
        </div>
        <div class="message-content">
          <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    </div>

    <div class="ai-chat-input">
      <FormControl
        v-model="inputMessage"
        type="textarea"
        placeholder="Ask a question..."
        :rows="2"
        @keydown.enter.prevent="handleSend"
      />
      <Button
        variant="solid"
        @click="handleSend"
        :loading="isProcessing"
        :disabled="!inputMessage.trim()"
      >
        <FeatherIcon name="send" class="w-4 h-4" />
      </Button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import { createResource } from 'frappe-ui'
import { FeatherIcon, FormControl, Button } from 'frappe-ui'
import UserAvatar from '@/components/UserAvatar.vue'

const props = defineProps({
  referenceDoctype: String,
  referenceName: String,
})

const emit = defineEmits(['close'])

const messages = ref([])
const inputMessage = ref('')
const isProcessing = ref(false)
const loading = ref(false)
const messagesContainer = ref(null)

// Load conversation history
const conversationHistory = createResource({
  url: 'crm.api.ai.get_conversation_history',
  params: {
    reference_doctype: props.referenceDoctype,
    reference_name: props.referenceName,
    limit: 50,
  },
  auto: true,
  onSuccess(data) {
    if (data && data.length > 0) {
      messages.value = data.reverse().map(conv => ([
        {
          role: 'user',
          content: conv.user_message,
          timestamp: conv.creation,
          user: conv.user,
        },
        {
          role: 'assistant',
          content: conv.ai_response,
          timestamp: conv.creation,
        }
      ])).flat()
    }
  },
})

// Send message to AI
const chatResource = createResource({
  url: 'crm.api.ai.chat',
  onSuccess(data) {
    messages.value.push({
      role: 'assistant',
      content: data.content,
      timestamp: data.timestamp,
    })
    isProcessing.value = false
    scrollToBottom()
  },
  onError(error) {
    console.error('AI chat error:', error)
    isProcessing.value = false
    messages.value.push({
      role: 'assistant',
      content: 'Sorry, I encountered an error. Please try again.',
      timestamp: new Date().toISOString(),
      error: true,
    })
  },
})

const handleSend = () => {
  if (!inputMessage.value.trim() || isProcessing.value) return

  const userMessage = inputMessage.value.trim()
  
  // Add user message to chat
  messages.value.push({
    role: 'user',
    content: userMessage,
    timestamp: new Date().toISOString(),
  })

  // Clear input
  inputMessage.value = ''
  isProcessing.value = true

  // Send to AI
  chatResource.submit({
    message: userMessage,
    reference_doctype: props.referenceDoctype,
    reference_name: props.referenceName,
  })

  scrollToBottom()
}

const formatMessage = (text) => {
  // Simple markdown-like formatting
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br>')
}

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

watch(messages, () => {
  scrollToBottom()
}, { deep: true })

onMounted(() => {
  scrollToBottom()
})
</script>

<style scoped>
.ai-chat-container {
  display: flex;
  flex-direction: column;
  height: min(72vh, 680px);
  min-height: 480px;
  border-radius: 18px;
  overflow: hidden;
  border: 1px solid var(--crm-border);
  box-shadow: var(--crm-shadow);
  background:
    radial-gradient(ellipse 72% 60% at 8% -12%, rgba(124, 108, 248, 0.22), transparent),
    radial-gradient(ellipse 55% 45% at 96% 8%, rgba(167, 139, 250, 0.16), transparent),
    radial-gradient(ellipse 40% 35% at 50% 100%, rgba(109, 86, 245, 0.1), transparent),
    linear-gradient(160deg, var(--crm-bg) 0%, var(--crm-bg-2) 100%);
}

.ai-chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.85rem 1rem;
  border-bottom: 1px solid var(--crm-border);
  background: color-mix(in oklab, var(--crm-surface) 90%, transparent);
  backdrop-filter: blur(10px);
}

.ai-chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem 0.9rem;
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}

.message {
  display: flex;
  gap: 0.75rem;
}

.message-user {
  flex-direction: row-reverse;
}

.message-avatar {
  flex-shrink: 0;
}

.ai-avatar {
  width: 32px;
  height: 32px;
  border-radius: 10px;
  background: linear-gradient(135deg, #1d8657 0%, #38ad73 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 18px rgba(22, 106, 67, 0.28);
}

.message-content {
  max-width: min(78%, 720px);
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.message-user .message-content {
  align-items: flex-end;
}

.message-text {
  padding: 0.7rem 0.9rem;
  border-radius: 14px;
  background:
    radial-gradient(ellipse 120% 100% at 0% 0%, color-mix(in oklab, var(--crm-brand) 14%, transparent), transparent),
    linear-gradient(160deg, color-mix(in oklab, var(--crm-surface) 96%, var(--crm-bg)), color-mix(in oklab, var(--crm-surface-2) 92%, var(--crm-bg-2)));
  color: var(--crm-text);
  line-height: 1.5;
  border: 1px solid var(--crm-border);
  box-shadow: var(--crm-shadow-sm);
}

.message-user .message-text {
  background: linear-gradient(145deg, #1b8655, #29a168);
  color: white;
  border-color: rgba(20, 107, 67, 0.7);
}

.message-time {
  font-size: 0.75rem;
  color: var(--crm-text-soft);
  padding: 0 0.5rem;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 0.75rem 0.9rem;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--crm-text-soft);
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    opacity: 0.3;
    transform: translateY(0);
  }
  30% {
    opacity: 1;
    transform: translateY(-4px);
  }
}

.ai-chat-input {
  display: flex;
  align-items: flex-end;
  gap: 0.75rem;
  padding: 0.85rem 1rem;
  border-top: 1px solid var(--crm-border);
  background: color-mix(in oklab, var(--crm-surface) 92%, transparent);
}

.ai-chat-input :deep(> div:first-child) {
  flex: 1;
}

@media (max-width: 640px) {
  .ai-chat-container {
    height: calc(100vh - 8rem);
    min-height: 420px;
    border-radius: 14px;
  }

  .message-content {
    max-width: 88%;
  }
}
</style>
