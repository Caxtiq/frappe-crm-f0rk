<template>
  <header class="crm-topbar flex h-[54px] shrink-0 items-center border-b border-[var(--crm-border)] px-4">
    <!-- ── Brand marker ── -->
    <div class="flex items-center gap-2 select-none flex-shrink-0 mr-3">
      <span class="relative flex h-2.5 w-2.5">
        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-[var(--crm-brand)] opacity-40" />
        <span class="relative inline-flex h-2.5 w-2.5 rounded-full bg-[var(--crm-brand)]" />
      </span>
      <span class="text-[10px] font-black uppercase tracking-[0.22em] text-[var(--crm-text-muted)]">CRM</span>
    </div>

    <!-- ── Divider ── -->
    <div class="h-4 w-px bg-[var(--crm-border-strong)] flex-shrink-0 mr-3" />

    <!-- ── Page header teleport target (breadcrumbs / action buttons from child pages) ── -->
    <div id="app-header" class="flex-1 min-w-0" />

    <!-- ── Search trigger ── -->
    <button
      class="crm-search-bar flex h-8 items-center gap-2 rounded-lg px-3 mr-3 text-xs text-[var(--crm-text-muted)] transition-all hover:text-[var(--crm-text)] flex-shrink-0"
    >
      <FeatherIcon name="search" class="h-3.5 w-3.5 flex-shrink-0" />
      <span class="hidden sm:block" style="width:88px;text-align:left;">Search…</span>
      <kbd class="hidden sm:inline-flex items-center gap-0.5 text-[9px] font-mono px-1 py-0.5 rounded border border-[var(--crm-border)] text-[var(--crm-text-muted)]">⌘K</kbd>
    </button>

    <!-- ── Right slot: call widget + user avatar ── -->
    <div class="flex items-center gap-2 flex-shrink-0">
      <!-- Telephony -->
      <div class="crm-panel rounded-xl px-2 py-1">
        <CallUI />
      </div>
      <!-- User avatar -->
      <button
        class="crm-avatar-btn h-[30px] w-[30px] rounded-full overflow-hidden ring-1 ring-[var(--crm-border)] hover:ring-[var(--crm-brand)] transition-all duration-200"
      >
        <UserAvatar :user="currentUser" size="sm" class="h-full w-full" />
      </button>
    </div>
  </header>
</template>

<script setup>
import CallUI from '@/components/Telephony/CallUI.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import { sessionStore } from '@/stores/session'
import { FeatherIcon } from 'frappe-ui'

const { user: currentUser } = sessionStore()
</script>

<style scoped>
.crm-topbar {
  background: rgba(8, 9, 18, 0.96);
  backdrop-filter: blur(20px) saturate(1.4);
  position: relative;
  z-index: 20;
  /* Subtle violet accent along bottom edge */
  box-shadow: inset 0 -1px 0 rgba(124, 108, 248, 0.18);
}

.crm-search-bar {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--crm-border);
  width: 172px;
}

.crm-search-bar:hover {
  background: rgba(255, 255, 255, 0.055);
  border-color: var(--crm-border-strong);
}

.crm-avatar-btn:hover {
  box-shadow: 0 0 0 3px rgba(124, 108, 248, 0.2);
}
</style>

