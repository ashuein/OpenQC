<script setup>
import { onMounted, ref, computed } from 'vue'
import { useAuditStore } from '@/stores/auditStore'
import PageHeader from '@/components/shared/PageHeader.vue'
import StatusBadge from '@/components/shared/StatusBadge.vue'
import ExportButton from '@/components/shared/ExportButton.vue'
import AuditTable from '@/components/tables/AuditTable.vue'
import { Button } from '@/components/ui/button'
import { ShieldCheck, ChevronLeft, ChevronRight } from 'lucide-vue-next'
import { printReport } from '@/utils/printReport'

const store = useAuditStore()

const eventTypeFilter = ref('all')
const exporting = ref(false)
const verifying = ref(false)

const eventTypes = [
  { value: 'all', label: 'All Events' },
  { value: 'upload', label: 'Upload' },
  { value: 'view', label: 'View' },
  { value: 'export', label: 'Export' },
  { value: 'lot_change', label: 'Lot Change' },
  { value: 'settings', label: 'Settings' },
  { value: 'rag_query', label: 'RAG Query' },
]

function loadWithFilter() {
  const params = {}
  if (eventTypeFilter.value !== 'all') {
    params.event_type = eventTypeFilter.value
  }
  store.loadLog(params)
}

function onFilterChange() {
  store.pagination.page = 1
  loadWithFilter()
}

async function handleVerifyChain() {
  verifying.value = true
  try {
    await store.checkChain()
  } finally {
    verifying.value = false
  }
}

async function handleExport(format) {
  if (format === 'pdf') {
    printReport({
      title: 'Audit Trail Report',
      subtitle: `${store.entries.length} entries`,
    })
    return
  }
  exporting.value = true
  try {
    const data = await store.exportLog(format)
    if (format === 'json') {
      const blob = new Blob([JSON.stringify(data, null, 2)], {
        type: 'application/json',
      })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'audit-log.json'
      a.click()
      URL.revokeObjectURL(url)
    }
  } catch {
    // error is set in store
  } finally {
    exporting.value = false
  }
}

const chainBadgeStatus = computed(() => {
  if (!store.chainStatus) return null
  return store.chainStatus.valid ? 'pass' : 'fail'
})

const chainBadgeLabel = computed(() => {
  if (!store.chainStatus) return ''
  if (store.chainStatus.valid) return 'Chain Valid'
  return `Invalid at entry #${store.chainStatus.first_invalid_id}`
})

const totalPages = computed(() => {
  if (!store.pagination.total || !store.pagination.page_size) return 1
  return Math.ceil(store.pagination.total / store.pagination.page_size)
})

function goPage(page) {
  if (page < 1 || page > totalPages.value) return
  store.pagination.page = page
  loadWithFilter()
}

onMounted(() => {
  loadWithFilter()
})
</script>

<template>
  <div class="view">
    <PageHeader
      title="Audit Trail"
      subtitle="Immutable action log and compliance records"
    >
      <template #actions>
        <ExportButton label="JSON" :loading="exporting" @export="handleExport('json')" />
        <ExportButton label="PDF" :loading="exporting" @export="handleExport('pdf')" />
      </template>
    </PageHeader>

    <!-- Chain verification strip -->
    <div class="chain-strip">
      <div class="chain-strip__left">
        <Button
          variant="outline"
          size="sm"
          :disabled="verifying"
          @click="handleVerifyChain"
        >
          <ShieldCheck :size="15" :stroke-width="1.75" />
          {{ verifying ? 'Verifying...' : 'Verify Chain' }}
        </Button>
        <template v-if="store.chainStatus">
          <StatusBadge :status="chainBadgeStatus" />
          <span class="chain-strip__label">{{ chainBadgeLabel }}</span>
          <span v-if="store.chainStatus.entries_checked" class="chain-strip__meta">
            ({{ store.chainStatus.entries_checked }} entries checked)
          </span>
        </template>
      </div>
    </div>

    <!-- Filter bar -->
    <div class="filter-bar">
      <div class="filter-group">
        <label class="filter-label">Event Type</label>
        <select
          v-model="eventTypeFilter"
          class="filter-select"
          @change="onFilterChange"
        >
          <option v-for="et in eventTypes" :key="et.value" :value="et.value">
            {{ et.label }}
          </option>
        </select>
      </div>
    </div>

    <!-- Error display -->
    <div v-if="store.error" class="error-strip">
      <p class="error-strip__text">{{ store.error }}</p>
      <Button variant="ghost" size="sm" @click="store.clearError()">Dismiss</Button>
    </div>

    <!-- Audit table -->
    <div class="table-zone">
      <AuditTable :entries="store.entries" :loading="store.loading" />
    </div>

    <!-- Pagination -->
    <div v-if="store.entries.length > 0" class="pagination">
      <span class="pagination__info">
        Page {{ store.pagination.page }} of {{ totalPages }}
        <span class="pagination__total">({{ store.pagination.total }} entries)</span>
      </span>
      <div class="pagination__controls">
        <Button
          variant="ghost"
          size="icon"
          :disabled="store.pagination.page <= 1"
          @click="goPage(store.pagination.page - 1)"
        >
          <ChevronLeft :size="16" :stroke-width="1.75" />
        </Button>
        <Button
          variant="ghost"
          size="icon"
          :disabled="store.pagination.page >= totalPages"
          @click="goPage(store.pagination.page + 1)"
        >
          <ChevronRight :size="16" :stroke-width="1.75" />
        </Button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.view {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chain-strip {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 28px;
  border-bottom: 1px solid var(--border-subtle);
}

.chain-strip__left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.chain-strip__label {
  font-size: 13px;
  color: var(--text-secondary);
  font-weight: 450;
}

.chain-strip__meta {
  font-size: 12px;
  color: var(--text-muted);
}

.filter-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 28px;
  border-bottom: 1px solid var(--border-subtle);
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-label {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.filter-select {
  height: 32px;
  padding: 0 10px;
  border-radius: 4px;
  border: 1px solid var(--border-subtle);
  background-color: var(--bg-surface-2);
  color: var(--text-primary);
  font-size: 13px;
  font-family: inherit;
  outline: none;
  cursor: pointer;
  appearance: auto;
  color-scheme: dark;
}

.filter-select:focus {
  border-color: var(--border-strong);
}

.error-strip {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 28px;
  background-color: color-mix(in srgb, var(--color-danger) 8%, transparent);
  border-bottom: 1px solid color-mix(in srgb, var(--color-danger) 20%, transparent);
}

.error-strip__text {
  font-size: 13px;
  color: var(--color-danger);
}

.table-zone {
  flex: 1;
  overflow-y: auto;
  padding: 0 28px;
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 28px;
  border-top: 1px solid var(--border-subtle);
}

.pagination__info {
  font-size: 13px;
  color: var(--text-secondary);
}

.pagination__total {
  color: var(--text-muted);
}

.pagination__controls {
  display: flex;
  gap: 4px;
}
</style>
