<template>
  <Teleport to="#app-header" v-if="showHeader">
    <slot>
      <header
        class="crm-fade-up flex min-h-[54px] items-center justify-between px-3 py-2 sm:px-5"
      >
        <div class="flex items-center gap-2.5">
          <slot name="left-header" />
        </div>
        <div class="flex items-center gap-2.5">
          <slot name="right-header" class="flex items-center gap-2" />
        </div>
      </header>
    </slot>
  </Teleport>
</template>
<script setup>
import { ref, nextTick } from 'vue'

const showHeader = ref(false)

nextTick(() => {
  showHeader.value = true
})
</script>
