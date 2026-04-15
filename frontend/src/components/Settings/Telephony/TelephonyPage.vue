<template>
  <div class="telephony-page-shell h-full">
    <TelephonySettings
      v-if="step === 'telephony-settings'"
      @updateStep="updateStep"
    />
    <TwilioSettings
      v-else-if="step === 'twilio-settings'"
      @updateStep="updateStep"
    />
    <ExotelSettings
      v-else-if="step === 'exotel-settings'"
      @updateStep="updateStep"
    />
  </div>
</template>
<script setup>
import TelephonySettings from './TelephonySettings.vue'
import ExotelSettings from './ExotelSettings.vue'
import TwilioSettings from './TwilioSettings.vue'
import { ref } from 'vue'

const step = ref('telephony-settings')

function updateStep(newStep) {
  step.value = newStep
}
</script>

<style scoped>
.telephony-page-shell {
  border: 1px solid color-mix(in oklab, var(--outline) 68%, white);
  border-radius: 1rem;
  margin: 1rem;
  background: linear-gradient(180deg, color-mix(in oklab, var(--surface-0) 94%, white), var(--surface-0));
  box-shadow: var(--shadow-soft);
  overflow: hidden;
}
</style>
