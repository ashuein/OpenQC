<script setup>
import { computed } from 'vue'

const props = defineProps({
  rule: {
    type: String,
    required: true,
  },
  severity: {
    type: String,
    required: true,
    validator: (v) => ['warning', 'reject'].includes(v),
  },
})

const chipClass = computed(() => `violation-badge violation-badge--${props.severity}`)
</script>

<template>
  <span :class="chipClass">{{ rule }}</span>
</template>

<style scoped>
.violation-badge {
  display: inline-flex;
  align-items: center;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', monospace;
  line-height: 1.5;
  white-space: nowrap;
  background: transparent;
}

.violation-badge--warning {
  border: 1px solid var(--color-warning);
  color: var(--color-warning);
}

.violation-badge--reject {
  border: 1px solid var(--color-danger);
  color: var(--color-danger);
}
</style>
