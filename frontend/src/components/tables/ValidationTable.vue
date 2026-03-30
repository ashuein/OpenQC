<script setup>
import { computed } from 'vue'
import StatusBadge from '@/components/shared/StatusBadge.vue'

const props = defineProps({
  metrics: {
    type: Array,
    required: true,
    default: () => [],
  },
})

const operatorLabels = {
  lte: '\u2264',
  gte: '\u2265',
  lt: '<',
  gt: '>',
  eq: '=',
}

function formatOperator(op) {
  return operatorLabels[op] || op
}

const overallStatus = computed(() => {
  if (!props.metrics.length) return 'info'
  const allPass = props.metrics.every((m) => m.status === 'pass')
  return allPass ? 'pass' : 'fail'
})
</script>

<template>
  <div class="validation-table">
    <table class="validation-table__table">
      <thead>
        <tr>
          <th>Metric</th>
          <th>Value</th>
          <th>Threshold</th>
          <th>Operator</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(m, i) in metrics" :key="i">
          <td class="validation-table__metric">{{ m.metric }}</td>
          <td class="validation-table__value">{{ m.value }}</td>
          <td class="validation-table__threshold">{{ m.threshold }}</td>
          <td class="validation-table__operator">{{ formatOperator(m.operator) }}</td>
          <td>
            <StatusBadge :status="m.status" />
          </td>
        </tr>
      </tbody>
      <tfoot v-if="metrics.length">
        <tr>
          <td class="validation-table__overall-label" colspan="4">Overall</td>
          <td>
            <StatusBadge :status="overallStatus" />
          </td>
        </tr>
      </tfoot>
    </table>
  </div>
</template>

<style scoped>
.validation-table {
  overflow-x: auto;
}

.validation-table__table {
  width: 100%;
  border-collapse: collapse;
}

.validation-table__table th {
  text-align: left;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-muted);
  padding: 8px 16px;
  border-bottom: 1px solid var(--border-subtle);
  white-space: nowrap;
}

.validation-table__table td {
  font-size: 13px;
  color: var(--text-primary);
  padding: 10px 16px;
  border-bottom: 1px solid var(--border-subtle);
}

.validation-table__metric {
  font-weight: 500;
}

.validation-table__value {
  font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', monospace;
  font-size: 12px;
}

.validation-table__threshold {
  font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', monospace;
  font-size: 12px;
  color: var(--text-secondary);
}

.validation-table__operator {
  font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', monospace;
  font-size: 13px;
  color: var(--text-muted);
}

.validation-table__table tfoot td {
  border-bottom: none;
  border-top: 2px solid var(--border-strong);
}

.validation-table__overall-label {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
}
</style>
