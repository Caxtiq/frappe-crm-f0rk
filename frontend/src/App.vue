<template>
  <FrappeUIProvider>
    <NotPermitted v-if="$route.name === 'Not Permitted'" />
    <Layout class="isolate" v-else-if="session().isLoggedIn">
      <router-view :key="$route.fullPath" />
    </Layout>
    <Dialogs />
    <EventNotificationPopup />
  </FrappeUIProvider>
</template>

<script setup>
import NotPermitted from '@/pages/NotPermitted.vue'
import EventNotificationPopup from '@/components/EventNotificationPopup.vue'
import { Dialogs } from '@/utils/dialogs'
import { sessionStore as session } from '@/stores/session'
import { FrappeUIProvider, setConfig, useTheme } from 'frappe-ui'
import { computed, defineAsyncComponent, onMounted } from 'vue'

const MobileLayout = defineAsyncComponent(
  () => import('./components/Layouts/MobileLayout.vue'),
)
const DesktopLayout = defineAsyncComponent(
  () => import('./components/Layouts/DesktopLayout.vue'),
)

const isDesktopForced = () => {
  const params = new URLSearchParams(window.location.search)
  return params.get('desktop') === '1' || localStorage.getItem('crm_force_desktop') === '1'
}

const Layout = computed(() => {
  if (!isDesktopForced() && window.innerWidth < 640) {
    return MobileLayout
  } else {
    return DesktopLayout
  }
})

setConfig('systemTimezone', window.timezone?.system || null)
setConfig('localTimezone', window.timezone?.user || null)

// Force dark theme globally so Frappe-UI component variables activate dark mode
const { setTheme } = useTheme()
onMounted(() => {
  setTheme('dark')
})
</script>
