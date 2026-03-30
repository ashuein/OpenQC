<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: {
    type: String,
    required: true,
    validator: (v) => ['pass', 'fail', 'warning', 'reject', 'info'].includes(v),
  },
})

const label = computed(() => {
  const labels = {
    pass: 'Pass',
    fail: 'Fail',
    warning: 'Warning',
    reject: 'Reject',
    info: 'Info',
  }
  return labels[props.status] || props.status
})

const badgeClass = computed(() => `status-badge status-badge--${props.status}`)
</script>

<template>
  <span :class="badgeClass">{{ label }}</span>
</template>

<style scoped>
.status-badge {
  display: inline-flex;
  align-items: center;
  padding: 2px 8px;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 500;
  line-height: 1.5;
  white-space: nowrap;
}

.status-badge--pass {
  background-color: color-mix(in srgb, var(--color-success) 15%, transparent);
  color: var(--color-success);
}

.status-badge--fail,
.status-badge--reject {
  background-color: color-mix(in srgb, var(--color-danger) 15%, transparent);
  color: var(--color-danger);
}

.status-badge--warning {
  background-color: color-mix(in srgb, var(--color-warning) 15%, transparent);
  color: var(--color-warning);
}

.status-badge--info {
  background-color: var(--bg-highlight);
  color: var(--text-muted);
}
</style>
