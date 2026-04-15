<template>
  <div class="dashboard-shell flex h-full flex-col overflow-hidden px-3 pb-3 sm:px-5 sm:pb-5">
    <LayoutHeader>
      <template #left-header>
        <ViewBreadcrumbs routeName="Dashboard" />
      </template>
      <template #right-header>
        <Button
          v-if="!editing"
          :label="__('Refresh')"
          :iconLeft="LucideRefreshCcw"
          @click="dashboardItems.reload"
        />
        <Button
          v-if="!editing && isAdmin()"
          :label="__('Edit')"
          :iconLeft="LucidePenLine"
          @click="enableEditing"
        />
        <Button
          v-if="editing"
          :label="__('Chart')"
          iconLeft="plus"
          @click="showAddChartModal = true"
        />
        <Button
          v-if="editing && isAdmin()"
          :label="__('Reset to default')"
          :iconLeft="LucideUndo2"
          @click="resetToDefault"
        />
        <Button v-if="editing" :label="__('Cancel')" @click="cancel" />
        <Button
          v-if="editing"
          variant="solid"
          :label="__('Save')"
          :disabled="!dirty"
          :loading="saveDashboard.loading"
          @click="save"
        />
      </template>
    </LayoutHeader>

    <div class="dashboard-filters mt-3 flex items-center gap-4 rounded-2xl px-4 py-3">
      <Dropdown
        v-if="!showDatePicker"
        :options="options"
        class="form-control"
        v-model="preset"
        :placeholder="__('Select range')"
        :button="{
          label: __(preset),
          class:
            '!w-full justify-start [&>span]:mr-auto [&>svg]:text-ink-gray-5 ',
          variant: 'outline',
          iconRight: 'chevron-down',
          iconLeft: 'calendar',
        }"
      />
      <DateRangePicker
        v-else
        class="!w-48"
        ref="datePickerRef"
        :value="filters.period"
        variant="outline"
        :placeholder="__('Period')"
        @change="
          (v) =>
            updateFilter('period', v, () => {
              showDatePicker = false
              if (!v) {
                filters.period = getLastXDays()
                preset = 'Last 30 Days'
              } else {
                preset = formatter(v)
              }
            })
        "
        :formatter="formatRange"
      >
        <template #prefix>
          <LucideCalendar class="size-4 text-ink-gray-5 mr-2" />
        </template>
      </DateRangePicker>
      <Link
        v-if="isAdmin() || isManager()"
        class="form-control w-48"
        variant="outline"
        :value="filters.user && getUser(filters.user).full_name"
        doctype="User"
        :filters="{ name: ['in', users.data.crmUsers?.map((u) => u.name)] }"
        @change="(v) => updateFilter('user', v)"
        :placeholder="__('Sales user')"
        :hideMe="true"
      >
        <template #prefix>
          <UserAvatar
            v-if="filters.user"
            class="mr-2"
            :user="filters.user"
            size="sm"
          />
        </template>
        <template #item-prefix="{ option }">
          <UserAvatar class="mr-2" :user="option.value" size="sm" />
        </template>
        <template #item-label="{ option }">
          <Tooltip :text="option.value">
            <div class="cursor-pointer">
              {{ getUser(option.value).full_name }}
            </div>
          </Tooltip>
        </template>
      </Link>
    </div>

    <div class="dashboard-grid-wrap mt-3 w-full overflow-y-auto rounded-2xl">
      <DashboardGrid
        class="pt-2"
        v-if="!dashboardItems.loading && dashboardItems.data"
        v-model="dashboardItems.data"
        :editing="editing"
      />
    </div>
  </div>
  <AddChartModal
    v-if="showAddChartModal"
    v-model="showAddChartModal"
    v-model:items="dashboardItems.data"
  />
</template>

<script setup lang="ts">
import AddChartModal from '@/components/Dashboard/AddChartModal.vue'
import LucideRefreshCcw from '~icons/lucide/refresh-ccw'
import LucideUndo2 from '~icons/lucide/undo-2'
import LucidePenLine from '~icons/lucide/pen-line'
import DashboardGrid from '@/components/Dashboard/DashboardGrid.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import ViewBreadcrumbs from '@/components/ViewBreadcrumbs.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
import Link from '@/components/Controls/Link.vue'
import { usersStore } from '@/stores/users'
import { copy } from '@/utils'
import { getLastXDays, formatter, formatRange } from '@/utils/dashboard'
import {
  usePageMeta,
  createResource,
  DateRangePicker,
  Dropdown,
  Tooltip,
} from 'frappe-ui'
import { ref, reactive, computed, provide } from 'vue'

const { users, getUser, isManager, isAdmin } = usersStore()

const editing = ref(false)

const showDatePicker = ref(false)
const datePickerRef = ref(null)
const preset = ref('Last 30 Days')
const showAddChartModal = ref(false)

const filters = reactive({
  period: getLastXDays(),
  user: null,
})

const fromDate = computed(() => {
  if (!filters.period) return null
  return filters.period.split(',')[0]
})

const toDate = computed(() => {
  if (!filters.period) return null
  return filters.period.split(',')[1]
})

function updateFilter(key: string, value: any, callback?: () => void) {
  filters[key] = value
  callback?.()
  dashboardItems.reload()
}

const options = computed(() => [
  {
    group: 'Presets',
    hideLabel: true,
    items: [
      {
        label: 'Last 7 Days',
        onClick: () => {
          preset.value = 'Last 7 Days'
          filters.period = getLastXDays(7)
          dashboardItems.reload()
        },
      },
      {
        label: 'Last 30 Days',
        onClick: () => {
          preset.value = 'Last 30 Days'
          filters.period = getLastXDays(30)
          dashboardItems.reload()
        },
      },
      {
        label: 'Last 60 Days',
        onClick: () => {
          preset.value = 'Last 60 Days'
          filters.period = getLastXDays(60)
          dashboardItems.reload()
        },
      },
      {
        label: 'Last 90 Days',
        onClick: () => {
          preset.value = 'Last 90 Days'
          filters.period = getLastXDays(90)
          dashboardItems.reload()
        },
      },
    ],
  },
  {
    label: 'Custom Range',
    onClick: () => {
      showDatePicker.value = true
      setTimeout(() => datePickerRef.value?.open(), 0)
      preset.value = 'Custom Range'
      filters.period = null // Reset period to allow custom date selection
    },
  },
])

const dashboardItems = createResource({
  url: 'crm.api.dashboard.get_dashboard',
  makeParams() {
    return {
      from_date: fromDate.value,
      to_date: toDate.value,
      user: filters.user,
    }
  },
  auto: true,
})

const dirty = computed(() => {
  if (!editing.value) return false
  return JSON.stringify(dashboardItems.data) !== JSON.stringify(oldItems.value)
})

const oldItems = ref([])

provide('fromDate', fromDate)
provide('toDate', toDate)
provide('filters', filters)

function enableEditing() {
  editing.value = true
  oldItems.value = copy(dashboardItems.data)
}

function cancel() {
  editing.value = false
  dashboardItems.data = copy(oldItems.value)
}

const saveDashboard = createResource({
  url: 'frappe.client.set_value',
  method: 'POST',
  onSuccess: () => {
    dashboardItems.reload()
    editing.value = false
  },
})

function save() {
  const dashboardItemsCopy = copy(dashboardItems.data)

  dashboardItemsCopy.forEach((item: any) => {
    delete item.data
  })

  saveDashboard.submit({
    doctype: 'CRM Dashboard',
    name: 'Manager Dashboard',
    fieldname: 'layout',
    value: JSON.stringify(dashboardItemsCopy),
  })
}

function resetToDefault() {
  createResource({
    url: 'crm.api.dashboard.reset_to_default',
    auto: true,
    onSuccess: () => {
      dashboardItems.reload()
      editing.value = false
    },
  })
}

usePageMeta(() => {
  return { title: __('CRM dashboard') }
})
</script>

<style scoped>
.dashboard-shell {
  background:
    radial-gradient(ellipse 60% 45% at 12% -12%, rgba(124, 108, 248, 0.22), transparent),
    radial-gradient(ellipse 42% 38% at 96% 10%, rgba(167, 139, 250, 0.16), transparent),
    linear-gradient(180deg, rgba(11, 14, 28, 0.72), rgba(8, 10, 20, 0.42));
}

.dashboard-filters {
  border: 1px solid var(--crm-border-strong);
  background: rgba(18, 20, 34, 0.75);
  box-shadow:
    0 4px 24px rgba(0, 0, 0, 0.30),
    inset 0 1px 0 rgba(124, 108, 248, 0.10);
  backdrop-filter: blur(14px);
}

.dashboard-grid-wrap {
  border: 1px solid var(--crm-border);
  background:
    radial-gradient(120% 90% at 0% 0%, rgba(124, 108, 248, 0.08), transparent),
    linear-gradient(180deg, rgba(14, 17, 32, 0.72), rgba(10, 12, 24, 0.62));
  box-shadow:
    0 14px 48px rgba(0, 0, 0, 0.40),
    inset 0 1px 0 rgba(124, 108, 248, 0.06);
  backdrop-filter: blur(10px);
}

.dashboard-shell :deep(.text-xs) {
  font-size: 0.82rem !important;
}

.dashboard-shell :deep(.text-sm) {
  font-size: 0.95rem !important;
}

.dashboard-shell :deep(.text-base) {
  font-size: 1.06rem !important;
}
</style>
