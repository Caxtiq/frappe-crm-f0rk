<template>
  <div class="flex h-screen w-screen p-2">
    <MobileSidebar />
    <div
      class="crm-glass flex h-full flex-1 flex-col overflow-hidden rounded-2xl"
    >
      <MobileAppHeader />
      <section class="flex-1 overflow-auto rounded-b-2xl bg-white/70">
        <slot />
      </section>
    </div>
    <GlobalModals />
  </div>
</template>
<script setup>
import MobileSidebar from '@/components/Mobile/MobileSidebar.vue'
import MobileAppHeader from '@/components/Mobile/MobileAppHeader.vue'
import GlobalModals from '@/components/Modals/GlobalModals.vue'
</script>
