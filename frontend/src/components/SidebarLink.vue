<template>
  <button
    class="group relative flex h-9 w-full cursor-pointer items-center rounded-xl border border-transparent text-[var(--crm-text)] duration-200 ease-out focus:outline-none focus:transition-none focus-visible:ring-2 focus-visible:ring-[var(--crm-border-strong)]"
    :class="
      isActive
        ? 'border-[rgba(124,108,248,0.2)] bg-[rgba(124,108,248,0.1)]'
        : 'hover:border-[var(--crm-border)] hover:bg-white/[0.04]'
    "
    @click="handleClick"
  >
    <!-- Active left accent glow bar -->
    <span
      v-if="isActive"
      class="absolute left-[5px] top-1/2 -translate-y-1/2 h-[18px] w-[3px] rounded-full bg-[var(--crm-brand)] shadow-[0_0_8px_rgba(124,108,248,0.9)] flex-shrink-0"
    />

    <div
      class="flex w-full items-center justify-between duration-200 ease-out"
      :class="isCollapsed ? 'p-1.5' : 'px-2.5 py-[9px]'"
    >
      <div class="flex items-center truncate">
        <Tooltip :text="label" placement="right" :disabled="!isCollapsed">
          <slot name="icon">
            <Icon
              :icon="icon"
              class="size-4 flex items-center transition-all duration-200"
              :class="
                isActive
                  ? 'text-[var(--crm-brand)] drop-shadow-[0_0_6px_rgba(124,108,248,0.8)]'
                  : 'text-[var(--crm-text-soft)] group-hover:text-[var(--crm-text)]'
              "
            />
          </slot>
        </Tooltip>
        <Tooltip :text="label" placement="right" :disabled="isCollapsed" :hoverDelay="1.5">
          <span
            class="flex-1 flex-shrink-0 truncate text-[0.95rem] font-medium duration-200 ease-out"
            :class="[
              isCollapsed
                ? 'ml-0 w-0 overflow-hidden opacity-0'
                : 'ml-2.5 w-auto opacity-100',
              isActive ? 'text-[var(--crm-text)] font-semibold' : ''
            ]"
          >
            {{ label }}
          </span>
        </Tooltip>
      </div>
      <slot name="right" />
    </div>
  </button>
</template>

<script setup>
import Icon from '@/components/Icon.vue'
import { Tooltip } from 'frappe-ui'
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { isMobileView, mobileSidebarOpened } from '@/composables/settings'

const router = useRouter()
const route = useRoute()

const props = defineProps({
  icon: {
    type: [Object, String, Function],
  },
  label: {
    type: String,
    default: '',
  },
  to: {
    type: [Object, String],
    default: '',
  },
  isCollapsed: {
    type: Boolean,
    default: false,
  },
})

function handleClick() {
  if (!props.to) return
  if (typeof props.to === 'object') {
    router.push(props.to)
  } else {
    router.push({ name: props.to })
  }
  if (isMobileView.value) {
    mobileSidebarOpened.value = false
  }
}

let isActive = computed(() => {
  if (route.query.view) {
    return route.query.view == props.to?.query?.view
  }
  return route.name === props.to
})
</script>
