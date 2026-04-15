<template>
  <SettingsPage
    doctype="CRM Twilio Settings"
    :title="__('Twilio settings')"
    :successMessage="__('Twilio settings updated')"
    :back="() => $emit('updateStep', 'telephony-settings')"
  />
</template>
<script setup>
import SettingsPage from '@/components/Settings/SettingsPage.vue'
</script>
