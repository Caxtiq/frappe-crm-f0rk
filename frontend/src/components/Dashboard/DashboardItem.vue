<template>
  <div class="h-full w-full">
    <div
      v-if="item.type == 'number_chart'"
      class="dashboard-card-surface flex h-full w-full cursor-pointer overflow-hidden rounded"
    >
      <Tooltip :text="__(item.data.tooltip)">
        <NumberChart
          class="!items-start"
          v-if="item.data"
          :key="index"
          :config="item.data"
        />
      </Tooltip>
    </div>
    <div
      v-else-if="item.type == 'spacer'"
      class="dashboard-card-surface flex h-full items-center justify-center overflow-hidden rounded text-ink-gray-5"
      :class="editing ? 'border border-dashed border-outline-gray-2' : ''"
    >
      {{ editing ? __('Spacer') : '' }}
    </div>
    <div
      v-else-if="item.type == 'axis_chart'"
      class="dashboard-card-surface h-full w-full rounded-md"
    >
      <AxisChart v-if="item.data" :config="item.data" />
    </div>
    <div
      v-else-if="item.type == 'donut_chart'"
      class="dashboard-card-surface h-full w-full overflow-hidden rounded-md"
    >
      <DonutChart v-if="item.data" :config="item.data" />
    </div>
  </div>
</template>
<script setup>
import { AxisChart, DonutChart, NumberChart, Tooltip } from 'frappe-ui'

const props = defineProps({
  index: {
    type: Number,
    required: true,
  },
  item: {
    type: Object,
    required: true,
  },
  editing: {
    type: Boolean,
    default: false,
  },
})
</script>

<style scoped>
.dashboard-card-surface {
  position: relative;
  isolation: isolate;
  border: 1px solid color-mix(in oklab, var(--outline) 68%, white);
  border-radius: 0.75rem;
  background: linear-gradient(
    180deg,
    color-mix(in oklab, var(--surface-0) 96%, white),
    color-mix(in oklab, var(--surface-0) 92%, white)
  );
  box-shadow: 0 10px 24px rgba(24, 28, 44, 0.08);
  transition: transform 220ms ease, box-shadow 260ms ease, border-color 260ms ease;
}

.dashboard-card-surface::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: linear-gradient(120deg, color-mix(in oklab, var(--crm-brand) 8%, transparent) 0%, transparent 60%);
  opacity: 0.4;
  pointer-events: none;
}

.dashboard-card-surface:hover {
  border-color: color-mix(in oklab, var(--crm-brand) 34%, var(--outline));
  box-shadow: 0 16px 30px rgba(24, 28, 44, 0.12);
  transform: translateY(-1px);
}

.dashboard-card-surface :deep(.frappe-chart),
.dashboard-card-surface :deep(.chart-container),
.dashboard-card-surface :deep(.echarts-for-react),
.dashboard-card-surface :deep(canvas),
.dashboard-card-surface :deep(svg) {
  background: transparent !important;
}
</style>
