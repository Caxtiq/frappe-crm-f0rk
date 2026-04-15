<template>
  <div class="email-config-shell flex-1 p-8">
    <div v-if="step === 'email-add'" class="h-full">
      <EmailAdd @update:step="updateStep" />
    </div>
    <div v-else-if="step === 'email-list'" class="h-full">
      <EmailAccountList @update:step="updateStep" />
    </div>
    <div v-else-if="step === 'email-edit'" class="h-full">
      <EmailEdit :account-data="accountData" @update:step="updateStep" />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import EmailAdd from "./EmailAdd.vue";
import EmailAccountList from "./EmailAccountList.vue";
import EmailEdit from "./EmailEdit.vue";

const step = ref("email-list");
const accountData = ref(null);
function updateStep(newStep, data) {
  step.value = newStep;
  accountData.value = data;
}
</script>

<style scoped>
.email-config-shell {
  border: 1px solid color-mix(in oklab, var(--outline) 68%, white);
  border-radius: 1rem;
  margin: 1rem;
  background: linear-gradient(180deg, color-mix(in oklab, var(--surface-0) 94%, white), var(--surface-0));
  box-shadow: var(--shadow-soft);
}
</style>
