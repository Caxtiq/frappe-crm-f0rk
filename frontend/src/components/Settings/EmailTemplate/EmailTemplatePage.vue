<template>
  <div class="email-template-shell h-full">
    <NewEmailTemplate
      v-if="step === 'new-template'"
      :templateData="template"
      @updateStep="updateStep"
    />
    <EmailTemplates
      v-else-if="step === 'template-list'"
      @updateStep="updateStep"
    />
    <EditEmailTemplate
      v-else-if="step === 'edit-template'"
      :templateData="template"
      @updateStep="updateStep"
    />
  </div>
</template>

<script setup>
import NewEmailTemplate from './NewEmailTemplate.vue'
import EditEmailTemplate from './EditEmailTemplate.vue'
import EmailTemplates from './EmailTemplates.vue'
import { createListResource } from 'frappe-ui'
import { provide, ref } from 'vue'

const step = ref('template-list')
const template = ref(null)

const templates = createListResource({
  type: 'list',
  doctype: 'Email Template',
  cache: 'emailTemplates',
  fields: [
    'name',
    'enabled',
    'use_html',
    'reference_doctype',
    'subject',
    'response',
    'response_html',
    'modified',
    'owner',
  ],
  auto: true,
  filters: { reference_doctype: ['in', ['CRM Lead', 'CRM Deal']] },
  orderBy: 'modified desc',
  pageLength: 20,
})

provide('templates', templates)

function updateStep(newStep, data) {
  step.value = newStep
  template.value = data
}
</script>

<style scoped>
.email-template-shell {
  border: 1px solid color-mix(in oklab, var(--outline) 68%, white);
  border-radius: 1rem;
  margin: 1rem;
  background: linear-gradient(180deg, color-mix(in oklab, var(--surface-0) 94%, white), var(--surface-0));
  box-shadow: var(--shadow-soft);
  overflow: hidden;
}
</style>
