<script setup>
import { onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Activity, TrendingUp, Shield } from 'lucide-vue-next'
import PageHeader from '@/components/shared/PageHeader.vue'
import RunSummaryTable from '@/components/tables/RunSummaryTable.vue'
import { Button } from '@/components/ui/button'
import { useQcStore } from '@/stores/qcStore'

const router = useRouter()
const store = useQcStore()

const totalRuns = computed(() => store.pagination.total || store.runs.length)
const totalViolations = computed(() => store.violationCount)
const lastRunDate = computed(() => {
  if (store.runs.length === 0) return 'No runs yet'
  const latest = store.runs[0]
  const dateStr = latest.uploaded_at
  if (!dateStr) return 'N/A'
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
})

function handleSelectRun(runId) {
  router.push('/qc')
  store.loadRunDetail(runId)
}

async function handleDeleteRun(runId) {
  try {
    await store.removeRun(runId)
    store.loadRuns()
  } catch {
    // silently fail on dashboard
  }
}

onMounted(() => {
  store.loadRuns()
})
</script>

<template>
  <div class="view">
    <PageHeader title="Dashboard" subtitle="System overview and summary metrics" />

    <div class="view__body">
      <!-- Stats Cards -->
      <section class="stats-row">
        <div class="stat-card">
          <span class="stat-card__label">Total Runs</span>
          <span class="stat-card__value">
            <template v-if="store.loading">--</template>
            <template v-else>{{ totalRuns }}</template>
          </span>
        </div>
        <div class="stat-card">
          <span class="stat-card__label">Total Violations</span>
          <span class="stat-card__value" :class="{ 'stat-card__value--danger': totalViolations > 0 }">
            <template v-if="store.loading">--</template>
            <template v-else>{{ totalViolations }}</template>
          </span>
        </div>
        <div class="stat-card">
          <span class="stat-card__label">Last Run</span>
          <span class="stat-card__value stat-card__value--text">
            <template v-if="store.loading">--</template>
            <template v-else>{{ lastRunDate }}</template>
          </span>
        </div>
      </section>

      <!-- Recent QC Runs -->
      <section class="section">
        <h2 class="section__title">Recent QC Runs</h2>
        <div class="section__content">
          <template v-if="store.loading && store.runs.length === 0">
            <div class="skeleton skeleton--table" />
          </template>
          <template v-else>
            <RunSummaryTable
              :runs="store.recentRuns"
              max-height="300px"
              @select-run="handleSelectRun"
              @delete-run="handleDeleteRun"
            />
          </template>
        </div>
      </section>

      <!-- Quick Actions -->
      <section class="section">
        <h2 class="section__title">Quick Actions</h2>
        <div class="actions-row">
          <Button @click="router.push('/qc')">
            <Activity :size="16" :stroke-width="1.75" />
            <span>Upload QC Data</span>
          </Button>
          <Button variant="ghost" @click="router.push('/sigma')">
            <TrendingUp :size="16" :stroke-width="1.75" />
            <span>View Sigma</span>
          </Button>
          <Button variant="ghost" @click="router.push('/audit')">
            <Shield :size="16" :stroke-width="1.75" />
            <span>Audit Trail</span>
          </Button>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.view {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.view__body {
  flex: 1;
  overflow-y: auto;
  padding: 0 28px 40px;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  padding-top: 24px;
}

@media (max-width: 700px) {
  .stats-row {
    grid-template-columns: 1fr;
  }
}

.stat-card {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 20px;
  background-color: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
}

.stat-card__label {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.stat-card__value {
  font-size: 28px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', monospace;
}

.stat-card__value--text {
  font-size: 16px;
  font-family: inherit;
  font-weight: 500;
}

.stat-card__value--danger {
  color: var(--color-danger);
}

.section {
  padding-top: 24px;
}

.section__title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 12px;
  letter-spacing: -0.01em;
}

.section__content {
  background-color: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  overflow: hidden;
}

.actions-row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.skeleton {
  background-color: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  animation: pulse 1.5s ease-in-out infinite;
}

.skeleton--table {
  height: 200px;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
</style>
