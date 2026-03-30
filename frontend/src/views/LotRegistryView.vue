<script setup>
import { onMounted, ref, computed } from 'vue'
import { useLotStore } from '@/stores/lotStore'
import PageHeader from '@/components/shared/PageHeader.vue'
import LotForm from '@/components/forms/LotForm.vue'
import { Button } from '@/components/ui/button'
import { Plus } from 'lucide-vue-next'

const store = useLotStore()

const activeTab = ref('reagent')
const showForm = ref(false)

const tabs = [
  { key: 'reagent', label: 'Reagent Lots' },
  { key: 'control', label: 'Control Lots' },
]

function switchTab(tabKey) {
  activeTab.value = tabKey
  showForm.value = false
  if (tabKey === 'reagent') {
    store.loadReagentLots()
  } else {
    store.loadControlLots()
  }
}

function toggleForm() {
  showForm.value = !showForm.value
}

async function handleSubmit(formData) {
  try {
    if (activeTab.value === 'reagent') {
      await store.addReagentLot(formData)
    } else {
      await store.addControlLot(formData)
    }
    showForm.value = false
  } catch {
    // error is set in store
  }
}

function handleCancel() {
  showForm.value = false
}

const currentLots = computed(() =>
  activeTab.value === 'reagent' ? store.reagentLots : store.controlLots
)

function formatDate(dateStr) {
  if (!dateStr) return '--'
  return new Date(dateStr).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
  })
}

function lotStatus(lot) {
  if (!lot.expiry_date) return 'info'
  const expiry = new Date(lot.expiry_date)
  const now = new Date()
  const daysUntilExpiry = (expiry - now) / (1000 * 60 * 60 * 24)
  if (daysUntilExpiry < 0) return 'fail'
  if (daysUntilExpiry < 30) return 'warning'
  return 'pass'
}

function lotStatusLabel(lot) {
  const s = lotStatus(lot)
  if (s === 'fail') return 'Expired'
  if (s === 'warning') return 'Expiring Soon'
  return 'Active'
}

onMounted(() => {
  store.loadReagentLots()
  store.loadControlLots()
})
</script>

<template>
  <div class="view">
    <PageHeader
      title="Lot Registry"
      subtitle="Reagent and control lot management"
    />

    <!-- Tabs -->
    <div class="tab-bar">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        class="tab-btn"
        :class="activeTab === tab.key ? 'tab-btn--active' : 'tab-btn--inactive'"
        @click="switchTab(tab.key)"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- Actions -->
    <div class="actions-bar">
      <Button size="sm" @click="toggleForm">
        <Plus :size="15" :stroke-width="1.75" />
        {{ showForm ? 'Cancel' : 'Add Lot' }}
      </Button>
    </div>

    <!-- Error display -->
    <div v-if="store.error" class="error-strip">
      <p class="error-strip__text">{{ store.error }}</p>
      <Button variant="ghost" size="sm" @click="store.clearError()">Dismiss</Button>
    </div>

    <!-- Inline form -->
    <div v-if="showForm" class="form-zone">
      <LotForm
        :type="activeTab"
        @submit="handleSubmit"
        @cancel="handleCancel"
      />
    </div>

    <!-- Table -->
    <div class="table-zone">
      <!-- Loading skeleton -->
      <table v-if="store.loading" class="lot-table">
        <thead>
          <tr>
            <th v-for="i in 5" :key="'sh-' + i">
              <span class="skeleton-cell skeleton-cell--sm"></span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="i in 6" :key="'sr-' + i">
            <td v-for="j in 5" :key="'sc-' + j">
              <span class="skeleton-cell skeleton-cell--md"></span>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Reagent table -->
      <table
        v-else-if="activeTab === 'reagent' && currentLots.length > 0"
        class="lot-table"
      >
        <thead>
          <tr>
            <th>Assay</th>
            <th>Lot Number</th>
            <th>Open Date</th>
            <th>Expiry Date</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="lot in currentLots" :key="lot.id || lot.lot_number">
            <td class="cell-name">{{ lot.assay_name }}</td>
            <td class="cell-mono">{{ lot.lot_number }}</td>
            <td>{{ formatDate(lot.open_date) }}</td>
            <td>{{ formatDate(lot.expiry_date) }}</td>
            <td>
              <span class="lot-status" :class="'lot-status--' + lotStatus(lot)">
                {{ lotStatusLabel(lot) }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Control table -->
      <table
        v-else-if="activeTab === 'control' && currentLots.length > 0"
        class="lot-table"
      >
        <thead>
          <tr>
            <th>Control Name</th>
            <th>Manufacturer</th>
            <th>Lot Number</th>
            <th>Mean</th>
            <th>SD</th>
            <th>Expiry Date</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="lot in currentLots" :key="lot.id || lot.lot_number">
            <td class="cell-name">{{ lot.control_name }}</td>
            <td>{{ lot.manufacturer || '--' }}</td>
            <td class="cell-mono">{{ lot.lot_number }}</td>
            <td class="cell-mono">{{ lot.assigned_mean }}</td>
            <td class="cell-mono">{{ lot.assigned_sd }}</td>
            <td>{{ formatDate(lot.expiry_date) }}</td>
            <td>
              <span class="lot-status" :class="'lot-status--' + lotStatus(lot)">
                {{ lotStatusLabel(lot) }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Empty state -->
      <div v-else-if="!store.loading" class="empty-state">
        <p class="empty-state__text">
          No {{ activeTab === 'reagent' ? 'reagent' : 'control' }} lots registered yet.
        </p>
        <Button v-if="!showForm" size="sm" variant="outline" @click="toggleForm">
          <Plus :size="15" :stroke-width="1.75" />
          Add your first lot
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

/* Tabs */
.tab-bar {
  display: flex;
  gap: 2px;
  padding: 12px 28px 0;
  border-bottom: 1px solid var(--border-subtle);
}

.tab-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px 6px 0 0;
  font-size: 13px;
  font-weight: 500;
  font-family: inherit;
  cursor: pointer;
  transition: background-color 0.15s ease, color 0.15s ease;
  position: relative;
  bottom: -1px;
}

.tab-btn--active {
  background-color: var(--tab-active-bg);
  color: var(--tab-active-text);
}

.tab-btn--inactive {
  background-color: var(--tab-inactive-bg);
  color: var(--tab-inactive-text);
}

.tab-btn--inactive:hover {
  color: var(--text-secondary);
  background-color: var(--bg-surface-2);
}

/* Actions */
.actions-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 28px;
  border-bottom: 1px solid var(--border-subtle);
}

/* Error strip */
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

/* Form zone */
.form-zone {
  padding: 16px 28px;
  border-bottom: 1px solid var(--border-subtle);
}

/* Table */
.table-zone {
  flex: 1;
  overflow-y: auto;
  padding: 0 28px;
}

.lot-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  margin-top: 4px;
}

.lot-table thead {
  border-bottom: 1px solid var(--border-subtle);
}

.lot-table th {
  text-align: left;
  padding: 10px 16px;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  white-space: nowrap;
}

.lot-table td {
  padding: 10px 16px;
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border-subtle);
  white-space: nowrap;
}

.lot-table tbody tr:hover {
  background-color: var(--bg-surface-2);
}

.cell-name {
  font-weight: 500;
  color: var(--text-primary);
}

.cell-mono {
  font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', monospace;
  font-size: 12px;
}

/* Lot status badge */
.lot-status {
  display: inline-flex;
  align-items: center;
  padding: 2px 8px;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 500;
  line-height: 1.5;
  white-space: nowrap;
}

.lot-status--pass {
  background-color: color-mix(in srgb, var(--color-success) 15%, transparent);
  color: var(--color-success);
}

.lot-status--warning {
  background-color: color-mix(in srgb, var(--color-warning) 15%, transparent);
  color: var(--color-warning);
}

.lot-status--fail {
  background-color: color-mix(in srgb, var(--color-danger) 15%, transparent);
  color: var(--color-danger);
}

.lot-status--info {
  background-color: var(--bg-highlight);
  color: var(--text-muted);
}

/* Empty state */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 14px;
  padding: 64px 16px;
}

.empty-state__text {
  font-size: 14px;
  color: var(--text-muted);
}

/* Skeleton */
.skeleton-cell {
  display: inline-block;
  height: 14px;
  border-radius: 4px;
  background-color: var(--bg-highlight);
  animation: skeleton-pulse 1.5s ease-in-out infinite;
}

.skeleton-cell--sm { width: 48px; }
.skeleton-cell--md { width: 80px; }

@keyframes skeleton-pulse {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 0.8; }
}
</style>
