<template>
  <SettingsPage
    doctype="CRM Exotel Settings"
    :title="__('Exotel settings')"
    :successMessage="__('Exotel settings updated')"
    :back="() => $emit('updateStep', 'telephony-settings')"
  />
</template>
<script setup>
import SettingsPage from '@/components/Settings/SettingsPage.vue'
</script>
