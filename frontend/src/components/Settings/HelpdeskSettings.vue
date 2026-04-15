<template>
  <SettingsPage
    doctype="Helpdesk CRM Settings"
    :title="__('Helpdesk settings')"
    :successMessage="__('Helpdesk settings updated')"
  />
</template>
<script setup>
import SettingsPage from '@/components/Settings/SettingsPage.vue'
</script>