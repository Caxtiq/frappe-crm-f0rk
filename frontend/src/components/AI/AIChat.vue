<template>
  <div class="ai-chat-container">
    <div class="ai-chat-header">
      <div class="flex items-center gap-2">
        <Icon name="sparkles" class="w-5 h-5 text-blue-500" />
        <h3 class="text-lg font-semibold">AI Assistant</h3>
      </div>
      <Button variant="ghost" @click="$emit('close')">
        <Icon name="x" class="w-4 h-4" />
      </Button>
    </div>

    <div class="ai-chat-messages" ref="messagesContainer">
      <div v-if="loading && messages.length === 0" class="text-center py-8">
        <div class="animate-spin w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full mx-auto"></div>
        <p class="text-sm text-gray-500 mt-2">Loading conversation...</p>
      </div>

      <div v-else-if="messages.length === 0" class="text-center py-8">
        <Icon name="sparkles" class="w-12 h-12 text-gray-300 mx-auto mb-3" />
        <p class="text-sm text-gray-500">Ask me anything about your CRM data</p>
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
              <Icon name="sparkles" class="w-4 h-4 text-white" />
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
            <Icon name="sparkles" class="w-4 h-4 text-white" />
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
        <Icon name="send" class="w-4 h-4" />
      </Button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import { createResource } from 'frappe-ui'
import { Icon, FormControl, Button, UserAvatar } from 'frappe-ui'

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
  height: 600px;
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.ai-chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.ai-chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
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
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.message-content {
  max-width: 70%;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.message-user .message-content {
  align-items: flex-end;
}

.message-text {
  padding: 0.75rem 1rem;
  border-radius: 12px;
  background: #f3f4f6;
  line-height: 1.5;
}

.message-user .message-text {
  background: #3b82f6;
  color: white;
}

.message-time {
  font-size: 0.75rem;
  color: #9ca3af;
  padding: 0 0.5rem;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 0.75rem 1rem;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #9ca3af;
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
  gap: 0.75rem;
  padding: 1rem;
  border-top: 1px solid #e5e7eb;
  background: #f9fafb;
}
</style>
