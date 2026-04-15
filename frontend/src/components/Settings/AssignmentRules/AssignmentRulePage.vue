<template>
  <div class="assignment-rule-shell h-full">
    <AssignmentRules v-if="step.screen === 'list'" />
    <AssignmentRuleView v-else-if="step.screen === 'view'" />
  </div>
</template>

<script setup>
import { ref, provide } from 'vue'
import AssignmentRules from './AssignmentRules.vue'
import AssignmentRuleView from './AssignmentRuleView.vue'

const step = ref({ screen: 'list', data: null })

provide('step', step)
provide('updateStep', updateStep)

function updateStep(newStep, data) {
  step.value = { screen: newStep, data }
}
</script>

<style scoped>
.assignment-rule-shell {
  border: 1px solid color-mix(in oklab, var(--outline) 68%, white);
  border-radius: 1rem;
  margin: 1rem;
  background: linear-gradient(180deg, color-mix(in oklab, var(--surface-0) 94%, white), var(--surface-0));
  box-shadow: var(--shadow-soft);
  overflow: hidden;
}
</style>
