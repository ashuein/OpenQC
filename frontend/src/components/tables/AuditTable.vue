<script setup>
import { computed } from 'vue'

const props = defineProps({
  entries: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

const skeletonRows = 8

function truncateHash(hash) {
  if (!hash) return '--'
  return hash.substring(0, 12)
}

function formatTimestamp(ts) {
  if (!ts) return '--'
  const d = new Date(ts)
  return d.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  })
}

const eventTypeColors = {
  upload: 'event-tag--upload',
  view: 'event-tag--view',
  export: 'event-tag--export',
  lot_change: 'event-tag--lot',
  settings: 'event-tag--settings',
  rag_query: 'event-tag--rag',
}

function eventTagClass(eventType) {
  return eventTypeColors[eventType] || 'event-tag--default'
}
</script>

<template>
  <div class="audit-table-wrapper">
    <table class="audit-table">
      <thead>
        <tr>
          <th class="col-id">ID</th>
          <th class="col-timestamp">Timestamp</th>
          <th class="col-event">Event Type</th>
          <th class="col-filename">File Name</th>
          <th class="col-action">Action</th>
          <th class="col-hash">Hash</th>
        </tr>
      </thead>
      <tbody v-if="loading">
        <tr v-for="i in skeletonRows" :key="'skel-' + i" class="skeleton-row">
          <td><span class="skeleton-cell skeleton-cell--sm"></span></td>
          <td><span class="skeleton-cell skeleton-cell--md"></span></td>
          <td><span class="skeleton-cell skeleton-cell--sm"></span></td>
          <td><span class="skeleton-cell skeleton-cell--lg"></span></td>
          <td><span class="skeleton-cell skeleton-cell--md"></span></td>
          <td><span class="skeleton-cell skeleton-cell--md"></span></td>
        </tr>
      </tbody>
      <tbody v-else-if="entries.length === 0">
        <tr>
          <td colspan="6" class="empty-cell">
            <p class="empty-text">No audit entries found</p>
          </td>
        </tr>
      </tbody>
      <tbody v-else>
        <tr v-for="entry in entries" :key="entry.id">
          <td class="cell-mono">{{ entry.id }}</td>
          <td class="cell-timestamp">{{ formatTimestamp(entry.timestamp) }}</td>
          <td>
            <span class="event-tag" :class="eventTagClass(entry.event_type)">
              {{ entry.event_type }}
            </span>
          </td>
          <td class="cell-filename">{{ entry.file_name || '--' }}</td>
          <td>{{ entry.action_detail || '--' }}</td>
          <td class="cell-mono cell-hash" :title="entry.entry_hash">
            {{ truncateHash(entry.entry_hash) }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.audit-table-wrapper {
  overflow-x: auto;
}

.audit-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.audit-table thead {
  border-bottom: 1px solid var(--border-subtle);
}

.audit-table th {
  text-align: left;
  padding: 10px 16px;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  white-space: nowrap;
}

.audit-table td {
  padding: 10px 16px;
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border-subtle);
  white-space: nowrap;
}

.audit-table tbody tr:hover {
  background-color: var(--bg-surface-2);
}

.col-id { width: 60px; }
.col-timestamp { width: 180px; }
.col-event { width: 120px; }
.col-filename { min-width: 160px; }
.col-action { min-width: 140px; }
.col-hash { width: 140px; }

.cell-mono {
  font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', monospace;
  font-size: 12px;
}

.cell-hash {
  color: var(--text-muted);
}

.cell-timestamp {
  font-variant-numeric: tabular-nums;
}

.cell-filename {
  max-width: 240px;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Event type tags */
.event-tag {
  display: inline-flex;
  align-items: center;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.event-tag--upload {
  background-color: color-mix(in srgb, var(--color-success) 12%, transparent);
  color: var(--color-success);
}

.event-tag--view {
  background-color: var(--bg-highlight);
  color: var(--text-muted);
}

.event-tag--export {
  background-color: color-mix(in srgb, var(--color-warning) 12%, transparent);
  color: var(--color-warning);
}

.event-tag--lot {
  background-color: var(--bg-highlight);
  color: var(--text-secondary);
}

.event-tag--settings {
  background-color: var(--bg-highlight);
  color: var(--text-muted);
}

.event-tag--rag {
  background-color: var(--bg-highlight);
  color: var(--text-secondary);
}

.event-tag--default {
  background-color: var(--bg-highlight);
  color: var(--text-muted);
}

/* Empty state */
.empty-cell {
  text-align: center;
  padding: 48px 16px !important;
}

.empty-text {
  font-size: 14px;
  color: var(--text-muted);
}

/* Skeleton loading */
.skeleton-row td {
  padding: 12px 16px;
}

.skeleton-cell {
  display: inline-block;
  height: 14px;
  border-radius: 4px;
  background-color: var(--bg-highlight);
  animation: skeleton-pulse 1.5s ease-in-out infinite;
}

.skeleton-cell--sm { width: 48px; }
.skeleton-cell--md { width: 96px; }
.skeleton-cell--lg { width: 140px; }

@keyframes skeleton-pulse {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 0.8; }
}
</style>
