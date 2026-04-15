<template>
  <div
    class="relative flex h-full flex-col px-2 py-2 transition-all duration-300 ease-in-out"
    :class="isSidebarCollapsed ? 'w-12' : 'w-[220px]'"
  >
    <div class="flex-1 overflow-y-auto pt-1">
      <div class="flex flex-col">
        <SidebarLink
          id="notifications-btn"
          :label="__('Notifications')"
          :icon="LucideBell"
          :isCollapsed="isSidebarCollapsed"
          @click="() => toggleNotificationPanel()"
          class="relative mx-1 my-0.5"
        >
          <template #right>
            <Badge
              v-if="!isSidebarCollapsed && unreadNotificationsCount"
              :label="unreadNotificationsCount"
              variant="subtle"
            />
            <div
              v-else-if="unreadNotificationsCount"
              class="absolute -left-1.5 top-1 z-20 h-[5px] w-[5px] translate-x-6 translate-y-1 rounded-full bg-[var(--crm-brand)] ring-1 ring-[#0d0f17]"
            />
          </template>
        </SidebarLink>
      </div>
      <div v-for="view in allViews" :key="view.label">
        <div class="mx-1 my-2 border-t border-[var(--crm-border)] opacity-60" />
        <CollapsibleSection
          :label="view.name"
          :hideLabel="view.hideLabel"
          :opened="view.opened"
        >
          <template #header="{ opened, hide, toggle }">
            <div
              v-if="!hide"
              class="flex cursor-pointer items-center gap-1.5 text-[11px] font-bold tracking-widest text-[var(--crm-text-muted)] uppercase transition-all duration-300 ease-in-out select-none"
              :class="
                isSidebarCollapsed
                  ? 'h-0 overflow-hidden opacity-0'
                  : 'w-auto px-3 pb-2 pt-3 opacity-100'
              "
              @click="toggle()"
            >
              <FeatherIcon
                name="chevron-right"
                class="h-4 text-[var(--crm-text)] transition-all duration-300 ease-in-out"
                :class="{ 'rotate-90': opened }"
              />
              <span>{{ __(view.name) }}</span>
            </div>
          </template>
          <nav class="flex flex-col">
            <SidebarLink
              v-for="link in view.views"
              :icon="link.icon"
              :label="__(link.label)"
              :to="link.to"
              :isCollapsed="isSidebarCollapsed"
              class="mx-1 my-0.5"
            />
          </nav>
        </CollapsibleSection>
      </div>
    </div>
    <div class="m-1 mt-2 flex flex-col gap-1.5 rounded-xl border border-[var(--crm-border-strong)] p-1.5" style="background: rgba(20, 22, 38, 0.75); backdrop-filter: blur(10px);">
      <UserDropdown :isCollapsed="isSidebarCollapsed" />
      <div class="border-t border-[var(--crm-border)] opacity-50 mx-0.5" />
      <div class="mb-1 flex flex-col gap-2">
        <SignupBanner
          v-if="isDemoSite"
          :isSidebarCollapsed="isSidebarCollapsed"
          :afterSignup="() => capture('signup_from_demo_site')"
        />
        <TrialBanner
          v-if="isFCSite"
          :isSidebarCollapsed="isSidebarCollapsed"
          :afterUpgrade="() => capture('upgrade_plan_from_trial_banner')"
        />
        <GettingStartedBanner
          v-if="!isOnboardingStepsCompleted"
          :isSidebarCollapsed="isSidebarCollapsed"
        />
      </div>
      <SidebarLink
        v-if="isOnboardingStepsCompleted"
        :label="__('Help')"
        :isCollapsed="isSidebarCollapsed"
        @click="
          () => {
            showHelpModal = minimize ? true : !showHelpModal
            minimize = !showHelpModal
          }
        "
      >
        <template #icon>
          <LucideHelp class="h-4 w-4" />
        </template>
      </SidebarLink>
      <SidebarLink
        :label="isSidebarCollapsed ? __('Expand') : __('Collapse')"
        :isCollapsed="isSidebarCollapsed"
        @click="isSidebarCollapsed = !isSidebarCollapsed"
        class=""
      >
        <template #icon>
          <span class="grid h-4 w-4 flex-shrink-0 place-items-center">
            <CollapseSidebar
              class="h-4 w-4 text-[var(--crm-text-soft)] duration-300 ease-in-out"
              :class="{ '[transform:rotateY(180deg)]': isSidebarCollapsed }"
            />
          </span>
        </template>
      </SidebarLink>
    </div>
    <Notifications />
    <Settings />
    <HelpModal
      v-if="showHelpModal"
      v-model="showHelpModal"
      v-model:articles="articles"
      :logo="CRMLogo"
      :afterSkip="(step) => capture('onboarding_step_skipped_' + step)"
      :afterSkipAll="() => capture('onboarding_steps_skipped')"
      :afterReset="(step) => capture('onboarding_step_reset_' + step)"
      :afterResetAll="() => capture('onboarding_steps_reset')"
      docsLink="https://docs.frappe.io/crm"
    />
    <IntermediateStepModal
      v-model="showIntermediateModal"
      :currentStep="currentStep"
    />
  </div>
</template>

<script setup>
import LucideLayoutDashboard from '~icons/lucide/gauge'
import LucideLeads from '~icons/lucide/user-round-plus'
import LucideDeals from '~icons/lucide/briefcase'
import LucideContacts from '~icons/lucide/users-round'
import LucideOrganizations from '~icons/lucide/building-2'
import LucideNotes from '~icons/lucide/sticky-note'
import LucideTasks from '~icons/lucide/list-checks'
import LucideCalendar from '~icons/lucide/calendar-days'
import LucidePhone from '~icons/lucide/phone-call'
import LucideBell from '~icons/lucide/bell'
import LucideHelp from '~icons/lucide/circle-help'
import LucideFlaskConical from '~icons/lucide/flask-conical'
import LucidePin from '~icons/lucide/pin'
import CollapsibleSection from '@/components/CollapsibleSection.vue'
import CollapseSidebar from '@/components/Icons/CollapseSidebar.vue'
import UserDropdown from '@/components/UserDropdown.vue'
import CRMLogo from '@/components/Icons/CRMLogo.vue'
import InviteIcon from '@/components/Icons/InviteIcon.vue'
import ConvertIcon from '@/components/Icons/ConvertIcon.vue'
import CommentIcon from '@/components/Icons/CommentIcon.vue'
import EmailIcon from '@/components/Icons/EmailIcon.vue'
import StepsIcon from '@/components/Icons/StepsIcon.vue'
import SquareAsterisk from '@/components/Icons/SquareAsterisk.vue'
import LeadsIcon from '@/components/Icons/LeadsIcon.vue'
import NoteIcon from '@/components/Icons/NoteIcon.vue'
import TaskIcon from '@/components/Icons/TaskIcon.vue'
import SidebarLink from '@/components/SidebarLink.vue'
import Notifications from '@/components/Notifications.vue'
import Settings from '@/components/Settings/Settings.vue'
import { viewsStore } from '@/stores/views'
import {
  unreadNotificationsCount,
  notificationsStore,
} from '@/stores/notifications'
import { usersStore } from '@/stores/users'
import { sessionStore } from '@/stores/session'
import { showSettings, activeSettingsPage } from '@/composables/settings'
import { showChangePasswordModal } from '@/composables/modals'
import { FeatherIcon, call } from 'frappe-ui'
import {
  SignupBanner,
  TrialBanner,
  HelpModal,
  GettingStartedBanner,
  useOnboarding,
  showHelpModal,
  minimize,
  IntermediateStepModal,
} from 'frappe-ui/frappe'
import { capture } from '@/telemetry'
import router from '@/router'
import { useStorage } from '@vueuse/core'
import { ref, reactive, computed, markRaw, onMounted } from 'vue'

const { getPinnedViews, getPublicViews } = viewsStore()
const { toggle: toggleNotificationPanel } = notificationsStore()

const isSidebarCollapsed = useStorage('isSidebarCollapsed', true)

const isFCSite = ref(window.is_fc_site)
const isDemoSite = ref(window.is_demo_site)

const links = [
  {
    label: 'Dashboard',
    icon: LucideLayoutDashboard,
    to: 'Dashboard',
  },
  {
    label: 'Leads',
    icon: LucideLeads,
    to: 'Leads',
  },
  {
    label: 'Deals',
    icon: LucideDeals,
    to: 'Deals',
  },
  {
    label: 'Contacts',
    icon: LucideContacts,
    to: 'Contacts',
  },
  {
    label: 'Organizations',
    icon: LucideOrganizations,
    to: 'Organizations',
  },
  {
    label: 'Notes',
    icon: LucideNotes,
    to: 'Notes',
  },
  {
    label: 'Tasks',
    icon: LucideTasks,
    to: 'Tasks',
  },
  {
    label: 'Calendar',
    icon: LucideCalendar,
    to: 'Calendar',
  },
  {
    label: 'Call Logs',
    icon: LucidePhone,
    to: 'Call Logs',
  },
  {
    label: 'Research Lab',
    icon: LucideFlaskConical,
    to: 'Research Lab',
  },
]

const allViews = computed(() => {
  let _views = [
    {
      name: 'All Views',
      hideLabel: true,
      opened: true,
      views: links.filter((link) => {
        if (link.condition) {
          return link.condition()
        }
        return true
      }),
    },
  ]
  if (getPublicViews().length) {
    _views.push({
      name: 'Public views',
      opened: true,
      views: parseView(getPublicViews()),
    })
  }

  if (getPinnedViews().length) {
    _views.push({
      name: 'Pinned views',
      opened: true,
      views: parseView(getPinnedViews()),
    })
  }
  return _views
})

function parseView(views) {
  return views.map((view) => {
    return {
      label: view.label,
      icon: getIcon(view.route_name, view.icon),
      to: {
        name: view.route_name,
        params: { viewType: view.type || 'list' },
        query: { view: view.name },
      },
    }
  })
}

function getIcon(routeName, icon) {
  if (icon) return icon

  switch (routeName) {
    case 'Leads':
      return LucideLeads
    case 'Deals':
      return LucideDeals
    case 'Contacts':
      return LucideContacts
    case 'Organizations':
      return LucideOrganizations
    case 'Notes':
      return LucideNotes
    case 'Call Logs':
      return LucidePhone
    case 'Research Lab':
      return LucideFlaskConical
    default:
      return LucidePin
  }
}

// onboarding
const { user } = sessionStore()
const { users, isManager } = usersStore()
const { isOnboardingStepsCompleted, setUp } = useOnboarding('frappecrm')

async function getFirstLead() {
  let firstLead = localStorage.getItem('firstLead' + user)
  if (firstLead) return firstLead
  return await call('crm.api.onboarding.get_first_lead')
}

async function getFirstDeal() {
  let firstDeal = localStorage.getItem('firstDeal' + user)
  if (firstDeal) return firstDeal
  return await call('crm.api.onboarding.get_first_deal')
}

const showIntermediateModal = ref(false)
const currentStep = ref({})

const steps = reactive([
  {
    name: 'setup_your_password',
    title: __('Setup your password'),
    icon: markRaw(SquareAsterisk),
    completed: false,
    onClick: () => {
      minimize.value = true
      showChangePasswordModal.value = true
    },
  },
  {
    name: 'create_first_lead',
    title: __('Create your first lead'),
    icon: markRaw(LeadsIcon),
    completed: false,
    onClick: () => {
      minimize.value = true
      router.push({ name: 'Leads' })
    },
  },
  {
    name: 'invite_your_team',
    title: __('Invite your team'),
    icon: markRaw(InviteIcon),
    completed: false,
    onClick: () => {
      minimize.value = true
      showSettings.value = true
      activeSettingsPage.value = 'Invite User'
    },
    condition: () => isManager(),
  },
  {
    name: 'convert_lead_to_deal',
    title: __('Convert lead to deal'),
    icon: markRaw(ConvertIcon),
    completed: false,
    dependsOn: 'create_first_lead',
    onClick: async () => {
      minimize.value = true

      currentStep.value = {
        title: __('Convert lead to deal'),
        buttonLabel: __('Convert'),
        videoURL: '/assets/crm/videos/convertToDeal.mov',
        onClick: async () => {
          showIntermediateModal.value = false
          currentStep.value = {}

          let lead = await getFirstLead()
          if (lead) {
            router.push({ name: 'Lead', params: { leadId: lead } })
          } else {
            router.push({ name: 'Leads' })
          }
        },
      }
      showIntermediateModal.value = true
    },
  },
  {
    name: 'create_first_task',
    title: __('Create your first task'),
    icon: markRaw(TaskIcon),
    completed: false,
    onClick: async () => {
      minimize.value = true
      let deal = await getFirstDeal()

      if (deal) {
        router.push({
          name: 'Deal',
          params: { dealId: deal },
          hash: '#tab-tasks',
        })
      } else {
        router.push({ name: 'Tasks' })
      }
    },
  },
  {
    name: 'create_first_note',
    title: __('Create your first note'),
    icon: markRaw(NoteIcon),
    completed: false,
    onClick: async () => {
      minimize.value = true
      let deal = await getFirstDeal()

      if (deal) {
        router.push({
          name: 'Deal',
          params: { dealId: deal },
          hash: '#tab-notes',
        })
      } else {
        router.push({ name: 'Notes' })
      }
    },
  },
  {
    name: 'add_first_comment',
    title: __('Add your first comment'),
    icon: markRaw(CommentIcon),
    completed: false,
    dependsOn: 'create_first_lead',
    onClick: async () => {
      minimize.value = true
      let deal = await getFirstDeal()

      if (deal) {
        router.push({
          name: 'Deal',
          params: { dealId: deal },
          hash: '#tab-comments',
        })
      } else {
        router.push({ name: 'Leads' })
      }
    },
  },
  {
    name: 'send_first_email',
    title: __('Send email'),
    icon: markRaw(EmailIcon),
    completed: false,
    dependsOn: 'create_first_lead',
    onClick: async () => {
      minimize.value = true
      let deal = await getFirstDeal()

      if (deal) {
        router.push({
          name: 'Deal',
          params: { dealId: deal },
          hash: '#tab-emails',
        })
      } else {
        router.push({ name: 'Leads' })
      }
    },
  },
  {
    name: 'change_deal_status',
    title: __('Change deal status'),
    icon: markRaw(StepsIcon),
    completed: false,
    dependsOn: 'convert_lead_to_deal',
    onClick: async () => {
      minimize.value = true

      currentStep.value = {
        title: __('Change deal status'),
        buttonLabel: __('Change'),
        videoURL: '/assets/crm/videos/changeDealStatus.mov',
        onClick: async () => {
          showIntermediateModal.value = false
          currentStep.value = {}

          let deal = await getFirstDeal()
          if (deal) {
            router.push({
              name: 'Deal',
              params: { dealId: deal },
              hash: '#tab-activity',
            })
          } else {
            router.push({ name: 'Leads' })
          }
        },
      }
      showIntermediateModal.value = true
    },
  },
])

onMounted(async () => {
  await users.promise

  const filteredSteps = steps.filter((step) => {
    if (step.condition) {
      return step.condition()
    }
    return true
  })

  setUp(filteredSteps)
})

// help center
const articles = ref([
  {
    title: __('Introduction'),
    opened: false,
    subArticles: [
      { name: 'introduction', title: __('Introduction') },
      { name: 'setting-up', title: __('Setting up') },
    ],
  },
  {
    title: __('Settings'),
    opened: false,
    subArticles: [
      { name: 'profile', title: __('Profile') },
      { name: 'custom-branding', title: __('Custom branding') },
      { name: 'home-actions', title: __('Home actions') },
      { name: 'invite-users', title: __('Invite users') },
    ],
  },
  {
    title: __('Masters'),
    opened: false,
    subArticles: [
      { name: 'lead', title: __('Lead') },
      { name: 'deal', title: __('Deal') },
      { name: 'contact', title: __('Contact') },
      { name: 'organization', title: __('Organization') },
      { name: 'note', title: __('Note') },
      { name: 'task', title: __('Task') },
      { name: 'call-log', title: __('Call log') },
      { name: 'email-template', title: __('Email template') },
    ],
  },
  {
    title: __('Capturing leads'),
    opened: false,
    subArticles: [{ name: 'web-form', title: __('Web form') }],
  },
  {
    title: __('Views'),
    opened: false,
    subArticles: [
      { name: 'view', title: __('Saved view') },
      { name: 'public-view', title: __('Public view') },
      { name: 'pinned-view', title: __('Pinned view') },
    ],
  },
  {
    title: __('Other features'),
    opened: false,
    subArticles: [
      { name: 'email-communication', title: __('Email communication') },
      { name: 'comment', title: __('Comment') },
      { name: 'data', title: __('Data') },
      { name: 'service-level-agreement', title: __('Service level agreement') },
      { name: 'assignment-rule', title: __('Assignment rule') },
      { name: 'notification', title: __('Notification') },
    ],
  },
  {
    title: __('Customization'),
    opened: false,
    subArticles: [
      { name: 'custom-fields', title: __('Custom fields') },
      { name: 'custom-actions', title: __('Custom actions') },
      { name: 'custom-statuses', title: __('Custom statuses') },
      { name: 'custom-list-actions', title: __('Custom list actions') },
      { name: 'quick-entry-layout', title: __('Quick entry layout') },
    ],
  },
  {
    title: __('Integration'),
    opened: false,
    subArticles: [
      { name: 'twilio', title: __('Twilio') },
      { name: 'exotel', title: __('Exotel') },
      { name: 'whatsapp', title: __('WhatsApp') },
      { name: 'erpnext', title: __('ERPNext') },
    ],
  },
  {
    title: __('Frappe CRM mobile'),
    opened: false,
    subArticles: [
      { name: 'mobile-app-installation', title: __('Mobile app installation') },
    ],
  },
])
</script>
