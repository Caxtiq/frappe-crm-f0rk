<template>
  <!--
    Full-bleed layout:
    ┌─────────────────────────────────────────────────┐
    │  AppHeader (spans full viewport width)          │
    ├───────────┬─────────────────────────────────────┤
    │  Sidebar  │  Content                            │
    │  (flush)  │  (fills rest)                       │
    └───────────┴─────────────────────────────────────┘
  -->
  <div class="crm-shell flex flex-col h-screen w-screen overflow-hidden">
    <!-- Full-width top bar -->
    <AppHeader />
    <!-- Body row -->
    <div class="flex flex-1 min-h-0 overflow-hidden">
      <div class="crm-shell-sidebar shrink-0 h-full overflow-hidden">
        <AppSidebar />
      </div>
      <main class="crm-shell-content crm-fade-up flex-1 min-w-0 overflow-auto">
        <slot />
      </main>
    </div>
    <GlobalModals />
  </div>
</template>

<script setup>
import AppSidebar from '@/components/Layouts/AppSidebar.vue'
import AppHeader from '@/components/Layouts/AppHeader.vue'
import GlobalModals from '@/components/Modals/GlobalModals.vue'
</script>

<style scoped>
.crm-shell {
  position: relative;
  background: var(--crm-bg);
}

/* ── ambient violet blobs ── */
.crm-shell::before,
.crm-shell::after {
  content: '';
  position: absolute;
  z-index: 0;
  border-radius: 999px;
  filter: blur(90px);
  pointer-events: none;
}

.crm-shell::before {
  top: 0;
  right: 20%;
  width: 26rem;
  height: 20rem;
  background: rgba(124, 108, 248, 0.16);
}

.crm-shell::after {
  bottom: -6rem;
  left: 20%;
  width: 30rem;
  height: 24rem;
  background: rgba(157, 130, 245, 0.10);
}

/* ── sidebar: flush left, glowing right border ── */
.crm-shell-sidebar {
  position: relative;
  z-index: 10;
  background: rgba(8, 9, 18, 0.97);
  border-right: 1px solid rgba(124, 108, 248, 0.15);
  box-shadow: 2px 0 20px rgba(0, 0, 0, 0.4);
}

/* ── content area: subtle gradient + left glow ── */
.crm-shell-content {
  position: relative;
  z-index: 1;
  box-shadow: inset 4px 0 24px rgba(0, 0, 0, 0.25);
  background:
    linear-gradient(180deg,
      rgba(124, 108, 248, 0.04) 0px,
      transparent 80px
    );
}
</style>

