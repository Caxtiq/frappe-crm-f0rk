<template>
  <div class="sla-config-shell h-full">
    <SlaPolicyList v-if="step.screen == 'list'" />
    <SlaPolicyView v-else-if="step.screen == 'view'" />
  </div>
</template>

<script setup>
import SlaPolicyList from './SlaPolicyList.vue'
import SlaPolicyView from './SlaPolicyView.vue'
import { ref, provide, onUnmounted } from 'vue'
import { createListResource } from 'frappe-ui'

const slaSearchQuery = ref('')
const step = ref({ screen: 'list', data: null, fetchData: false })

const slaPolicyListData = createListResource({
  doctype: 'CRM Service Level Agreement',
  fields: ['name', 'default', 'enabled', 'apply_on'],
  cache: ['SLAPolicyList'],
  orderBy: 'modified desc',
  start: 0,
  pageLength: 999,
  auto: true,
})

provide('slaSearchQuery', slaSearchQuery)
provide('slaPolicyListResource', slaPolicyListData)
provide('step', step)
provide('updateStep', updateStep)

function updateStep(newStep, data, fetchData) {
  step.value = { screen: newStep, data, fetchData }
}

onUnmounted(() => {
  slaSearchQuery.value = ''
  slaPolicyListData.filters = {}
})
</script>

<style scoped>
.sla-config-shell {
  border: 1px solid color-mix(in oklab, var(--outline) 68%, white);
  border-radius: 1rem;
  margin: 1rem;
  background: linear-gradient(180deg, color-mix(in oklab, var(--surface-0) 94%, white), var(--surface-0));
  box-shadow: var(--shadow-soft);
  overflow: hidden;
}
</style>
