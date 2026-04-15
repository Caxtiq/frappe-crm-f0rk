<template>
  <Dialog
    v-model="show"
    :options="{
      title: 'Compose Email with AI',
      size: 'xl',
    }"
  >
    <template #body-content>
      <div class="email-composer">
        <div class="form-section">
          <FormControl
            v-model="recipientName"
            label="Recipient Name"
            placeholder="John Doe"
          />
          <FormControl
            v-model="company"
            label="Company"
            placeholder="Acme Corp"
          />
          <FormControl
            v-model="purpose"
            type="textarea"
            label="Email Purpose"
            placeholder="Describe the purpose of this email..."
            :rows="3"
          />
          <FormControl
            v-model="tone"
            type="select"
            label="Tone"
            :options="toneOptions"
          />
        </div>

        <div class="mt-4">
          <Button
            variant="solid"
            @click="generateEmail"
            :loading="generating"
            class="w-full"
          >
            <template #prefix>
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
              </svg>
            </template>
            Generate Email
          </Button>
        </div>

        <div v-if="generatedEmail" class="email-preview mt-6">
          <div class="flex items-center justify-between mb-3">
            <h4 class="font-semibold text-ink-gray-9">Generated Email</h4>
            <Button variant="ghost" size="sm" @click="copyToClipboard">
              <FeatherIcon name="copy" class="w-4 h-4" />
            </Button>
          </div>
          <div class="email-content">
            <div class="email-text" v-html="formatEmail(generatedEmail)"></div>
          </div>
        </div>
      </div>
    </template>

    <template #actions>
      <Button variant="subtle" @click="show = false">Cancel</Button>
      <Button
        v-if="generatedEmail"
        variant="solid"
        @click="useEmail"
      >
        Use This Email
      </Button>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import { createResource } from 'frappe-ui'
import { Dialog, FormControl, Button, FeatherIcon } from 'frappe-ui'

const props = defineProps({
  modelValue: Boolean,
  referenceDoctype: String,
  referenceName: String,
})

const emit = defineEmits(['update:modelValue', 'emailGenerated'])

const show = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value),
})

const recipientName = ref('')
const company = ref('')
const purpose = ref('')
const tone = ref('professional')
const generatedEmail = ref('')
const generating = ref(false)

const toneOptions = [
  { label: 'Professional', value: 'professional' },
  { label: 'Friendly', value: 'friendly' },
  { label: 'Urgent', value: 'urgent' },
  { label: 'Casual', value: 'casual' },
  { label: 'Formal', value: 'formal' },
]

const emailResource = createResource({
  url: 'crm.api.ai.compose_email',
  onSuccess(data) {
    generatedEmail.value = data.content
    generating.value = false
  },
  onError(error) {
    console.error('Email generation error:', error)
    generating.value = false
  },
})

const generateEmail = () => {
  if (!recipientName.value || !company.value || !purpose.value) {
    alert('Please fill in all required fields')
    return
  }

  generating.value = true
  emailResource.submit({
    recipient_name: recipientName.value,
    company: company.value,
    purpose: purpose.value,
    tone: tone.value,
    reference_doctype: props.referenceDoctype,
    reference_name: props.referenceName,
  })
}

const formatEmail = (text) => {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br>')
}

const copyToClipboard = () => {
  navigator.clipboard.writeText(generatedEmail.value)
  // Could show a toast notification here
}

const useEmail = () => {
  emit('emailGenerated', generatedEmail.value)
  show.value = false
}
</script>

<style scoped>
.email-composer {
  padding: 1rem;
  background: var(--surface-white);
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.email-preview {
  border: 1px solid var(--outline-gray-2);
  border-radius: 8px;
  padding: 1rem;
  background: var(--surface-gray-2);
}

.email-content {
  background: var(--surface-white);
  border: 1px solid var(--outline-gray-2);
  border-radius: 6px;
  padding: 1rem;
}

.email-text {
  line-height: 1.6;
  color: var(--ink-gray-8);
}
</style>
