<script setup>
import ViolationBadge from '@/components/shared/ViolationBadge.vue'

defineProps({
  violations: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <div class="violation-table">
    <template v-if="violations.length > 0">
      <div class="vtable-scroll">
      <table class="vtable">
        <thead>
          <tr>
            <th class="vtable__th">Point #</th>
            <th class="vtable__th">Control Level</th>
            <th class="vtable__th">Ct Value</th>
            <th class="vtable__th">Z-Score</th>
            <th class="vtable__th">Rules Triggered</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(v, idx) in violations" :key="idx" class="vtable__row">
            <td class="vtable__td vtable__td--mono">{{ v.point_index ?? v.sequence_index ?? '-' }}</td>
            <td class="vtable__td">{{ v.control_level ?? '-' }}</td>
            <td class="vtable__td vtable__td--mono">{{ v.ct_value != null ? v.ct_value.toFixed(2) : '-' }}</td>
            <td class="vtable__td vtable__td--mono">{{ v.z_score != null ? v.z_score.toFixed(2) : '-' }}</td>
            <td class="vtable__td">
              <div class="vtable__rules">
                <ViolationBadge
                  v-for="(rule, rIdx) in (v.rules || v.violations || [])"
                  :key="rIdx"
                  :rule="typeof rule === 'string' ? rule : rule.rule"
                  :severity="typeof rule === 'string' ? 'warning' : (rule.severity || 'warning')"
                />
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      </div>
    </template>

    <div v-else class="violation-table__empty">
      <p class="violation-table__empty-text">No violations detected in this run.</p>
    </div>
  </div>
</template>

<style scoped>
.violation-table {
  width: 100%;
}

.vtable-scroll {
  max-height: 400px;
  overflow-y: auto;
}

.vtable {
  width: 100%;
  border-collapse: collapse;
}

.vtable__th {
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

.vtable__row {
  transition: background-color 0.1s ease;
}

.vtable__row:hover {
  background-color: var(--bg-surface-2);
}

.vtable__td {
  font-size: 13px;
  color: var(--text-secondary);
  padding: 10px 12px;
  border-bottom: 1px solid var(--border-subtle);
}

.vtable__td--mono {
  font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', monospace;
  font-size: 12px;
}

.vtable__rules {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.violation-table__empty {
  padding: 32px 16px;
  text-align: center;
}

.violation-table__empty-text {
  font-size: 14px;
  color: var(--text-muted);
}
</style>
