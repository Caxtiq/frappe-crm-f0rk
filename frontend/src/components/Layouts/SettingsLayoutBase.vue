<template>
  <div class="settings-layout-base flex flex-col h-full w-full text-ink-gray-8">
    <!-- Header -->
    <div class="settings-layout-head flex justify-between p-8 text-ink-gray-8">
      <div class="flex flex-col gap-1">
        <slot name="title">
          <h2 class="flex gap-2 text-xl font-semibold leading-none h-5">
            {{ title }}
          </h2>
        </slot>
        <slot
          name="description"
          v-if="Boolean($slots['description']) || Boolean(description)"
        >
          <p class="text-p-base text-ink-gray-6">
            {{ description }}
          </p>
        </slot>
      </div>
      <slot name="header-actions" v-if="Boolean($slots['header-actions'])" />
    </div>
    <div class="settings-layout-head-bottom p-8 pt-0" v-if="Boolean($slots['header-bottom'])">
      <slot name="header-bottom" />
    </div>
    <div class="settings-layout-body h-full overflow-y-auto p-8 pt-0">
      <slot name="content" />
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  title: {
    type: String,
  },
  description: {
    type: String,
  },
})
</script>

<style scoped>
.settings-layout-head,
.settings-layout-head-bottom,
.settings-layout-body {
  border: 1px solid color-mix(in oklab, var(--outline) 68%, white);
  border-radius: 1rem;
  background: linear-gradient(180deg, color-mix(in oklab, var(--surface-0) 92%, white), var(--surface-0));
  box-shadow: var(--shadow-soft);
}

.settings-layout-head {
  margin: 1rem;
  margin-bottom: 0.75rem;
  padding: 0.9rem 1rem;
}

.settings-layout-head-bottom {
  margin: 0 1rem 0.75rem;
  padding: 0.65rem;
}

.settings-layout-body {
  margin: 0 1rem 1rem;
  padding: 0.85rem;
}
</style>
