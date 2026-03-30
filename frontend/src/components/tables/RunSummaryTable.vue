<script setup>
import StatusBadge from '@/components/shared/StatusBadge.vue'

const props = defineProps({
  runs: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['select-run'])

function formatDate(dateStr) {
  if (!dateStr) return '-'
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

function mapStatus(status) {
  const map = {
    pass: 'pass',
    fail: 'fail',
    reject: 'reject',
    warning: 'warning',
    pending: 'info',
  }
  return map[status] || 'info'
}
</script>

<template>
  <div class="run-table">
    <template v-if="runs.length > 0">
      <table class="rtable">
        <thead>
          <tr>
            <th class="rtable__th">Date</th>
            <th class="rtable__th">Assay</th>
            <th class="rtable__th">Instrument</th>
            <th class="rtable__th">Status</th>
            <th class="rtable__th rtable__th--right">Violations</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="run in runs"
            :key="run.id"
            class="rtable__row"
            @click="emit('select-run', run.id)"
          >
            <td class="rtable__td">{{ formatDate(run.uploaded_at) }}</td>
            <td class="rtable__td">{{ run.assay || '-' }}</td>
            <td class="rtable__td">{{ run.instrument || '-' }}</td>
            <td class="rtable__td">
              <StatusBadge :status="mapStatus(run.run_status || 'pending')" />
            </td>
            <td class="rtable__td rtable__td--right rtable__td--mono">
              {{ run.violation_count ?? 0 }}
            </td>
          </tr>
        </tbody>
      </table>
    </template>

    <div v-else class="run-table__empty">
      <p class="run-table__empty-title">No QC runs yet</p>
      <p class="run-table__empty-text">Upload a QC data file to get started.</p>
    </div>
  </div>
</template>

<style scoped>
.run-table {
  width: 100%;
}

.rtable {
  width: 100%;
  border-collapse: collapse;
}

.rtable__th {
  text-align: left;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--text-muted);
  padding: 8px 12px;
  border-bottom: 1px solid var(--border-subtle);
}

.rtable__th--right {
  text-align: right;
}

.rtable__row {
  cursor: pointer;
  transition: background-color 0.1s ease;
}

.rtable__row:hover {
  background-color: var(--section-selected);
}

.rtable__td {
  font-size: 13px;
  color: var(--text-secondary);
  padding: 10px 12px;
  border-bottom: 1px solid var(--border-subtle);
}

.rtable__td--right {
  text-align: right;
}

.rtable__td--mono {
  font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', monospace;
  font-size: 12px;
}

.run-table__empty {
  padding: 40px 16px;
  text-align: center;
}

.run-table__empty-title {
  font-size: 15px;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: 4px;
}

.run-table__empty-text {
  font-size: 13px;
  color: var(--text-muted);
}
</style>
