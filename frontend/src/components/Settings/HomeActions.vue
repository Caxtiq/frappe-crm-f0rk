<template>
  <div class="home-actions-page flex h-full flex-col gap-6 p-8 text-ink-gray-8">
    <!-- Header -->
    <div class="home-actions-head flex justify-between text-ink-gray-8">
      <div class="flex flex-col gap-1">
        <h2 class="flex gap-2 text-xl font-semibold leading-none h-5">
          {{ __('Home actions') }}
        </h2>
        <p class="text-p-base text-ink-gray-6">
          {{ __('Configure actions that appear on the home dropdown') }}
        </p>
      </div>
      <div class="flex item-center space-x-2 w-3/12 justify-end">
        <Button
          :label="__('Update')"
          variant="solid"
          :disabled="!document.isDirty"
          :loading="document.loading"
          @click="updateSettings"
        />
      </div>
    </div>

    <!-- Fields -->
    <div class="home-actions-body flex flex-1 flex-col overflow-y-auto">
      <Grid
        v-model="document.doc.dropdown_items"
        doctype="CRM Dropdown Item"
        parentDoctype="FCRM Settings"
        parentFieldname="dropdown_items"
      />
    </div>
    <div v-if="errorMessage">
      <ErrorMessage :message="__(errorMessage)" />
    </div>
  </div>
</template>
<script setup>
import Grid from '@/components/Controls/Grid.vue'
import { ErrorMessage } from 'frappe-ui'
import { showSettings } from '@/composables/settings'
import { useDocument } from '@/data/document'
import { ref, provide } from 'vue'

const { document, triggerOnChange } = useDocument(
  'FCRM Settings',
  'FCRM Settings',
)

provide('triggerOnChange', triggerOnChange)

const emit = defineEmits(['updateStep'])
const errorMessage = ref('')

function updateSettings() {
  document.save.submit(null, {
    onSuccess: () => {
      showSettings.value = false
    },
  })
}
</script>

<style scoped>
.home-actions-head,
.home-actions-body {
  border: 1px solid color-mix(in oklab, var(--outline) 68%, white);
  border-radius: 1rem;
  background: linear-gradient(180deg, color-mix(in oklab, var(--surface-0) 92%, white), var(--surface-0));
  box-shadow: var(--shadow-soft);
}

.home-actions-head {
  padding: 0.85rem 1rem;
}

.home-actions-body {
  padding: 0.75rem;
}
</style>
