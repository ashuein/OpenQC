<script setup>
import { ref } from 'vue'
import { Trash2 } from 'lucide-vue-next'
import StatusBadge from '@/components/shared/StatusBadge.vue'
import { Button } from '@/components/ui/button'

const props = defineProps({
  runs: { type: Array, default: () => [] },
  maxHeight: { type: String, default: '400px' },
})

const emit = defineEmits(['select-run', 'delete-run'])

const confirmDeleteId = ref(null)

function formatDate(dateStr) {
  if (!dateStr) return '-'
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
}

function mapStatus(status) {
  const map = { pass: 'pass', fail: 'fail', reject: 'reject', warning: 'warning', pending: 'info' }
  return map[status] || 'info'
}

function requestDelete(runId, e) {
  e.stopPropagation()
  confirmDeleteId.value = runId
}

function confirmDelete(e) {
  e.stopPropagation()
  emit('delete-run', confirmDeleteId.value)
  confirmDeleteId.value = null
}

function cancelDelete(e) {
  e.stopPropagation()
  confirmDeleteId.value = null
}
</script>

<template>
  <div class="run-table">
    <template v-if="runs.length > 0">
      <div class="run-table__scroll" :style="{ maxHeight }">
        <table class="rtable">
          <thead>
            <tr>
              <th class="rtable__th">Date</th>
              <th class="rtable__th">Assay</th>
              <th class="rtable__th">Instrument</th>
              <th class="rtable__th">Status</th>
              <th class="rtable__th rtable__th--right">Violations</th>
              <th class="rtable__th rtable__th--center" style="width: 60px;"></th>
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
              <td class="rtable__td rtable__td--center">
                <template v-if="confirmDeleteId === run.id">
                  <div class="confirm-delete">
                    <Button size="sm" variant="destructive" @click="confirmDelete">Yes</Button>
                    <Button size="sm" variant="ghost" @click="cancelDelete">No</Button>
                  </div>
                </template>
                <template v-else>
                  <button class="delete-btn" title="Delete run" @click="requestDelete(run.id, $event)">
                    <Trash2 :size="14" :stroke-width="1.75" />
                  </button>
                </template>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>

    <div v-else class="run-table__empty">
      <p class="run-table__empty-title">No QC runs yet</p>
      <p class="run-table__empty-text">Upload a QC data file to get started.</p>
    </div>
  </div>
</template>

<style scoped>
.run-table { width: 100%; }

.run-table__scroll {
  overflow-y: auto;
  overflow-x: auto;
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
  position: sticky;
  top: 0;
  background: var(--bg-surface);
  z-index: 1;
}

.rtable__th--right { text-align: right; }
.rtable__th--center { text-align: center; }

.rtable__row {
  cursor: pointer;
  transition: background-color 0.1s ease;
}

.rtable__row:hover { background-color: var(--section-selected); }

.rtable__td {
  font-size: 13px;
  color: var(--text-secondary);
  padding: 10px 12px;
  border-bottom: 1px solid var(--border-subtle);
}

.rtable__td--right { text-align: right; }
.rtable__td--center { text-align: center; }

.rtable__td--mono {
  font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', monospace;
  font-size: 12px;
}

.delete-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border: none;
  background: none;
  color: var(--text-muted);
  cursor: pointer;
  border-radius: 4px;
  transition: color 0.15s, background 0.15s;
}

.delete-btn:hover {
  color: var(--color-danger);
  background: color-mix(in srgb, var(--color-danger) 10%, transparent);
}

.confirm-delete {
  display: flex;
  gap: 4px;
  align-items: center;
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
