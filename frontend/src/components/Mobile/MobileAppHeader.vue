<template>
  <div class="flex items-center gap-2 border-b border-[var(--crm-border)] bg-white/80 px-2 py-1 backdrop-blur">
    <div class="z-20 flex items-center justify-center">
      <Button
        class="size-8 rounded-xl border border-[var(--crm-border)] bg-white"
        variant="ghosted"
        @click="sidebarOpened = !sidebarOpened"
      >
        <MenuIcon class="h-4 text-[var(--crm-text)]" />
      </Button>
    </div>
    <div id="app-header" class="min-h-[44px] flex-1" />
    <div class="crm-panel rounded-xl px-1 py-0.5">
      <CallUI />
    </div>
  </div>
</template>

<script setup>
import MenuIcon from '@/components/Icons/MenuIcon.vue'
import CallUI from '@/components/Telephony/CallUI.vue'
import { mobileSidebarOpened as sidebarOpened } from '@/composables/settings'
</script>
