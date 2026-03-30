<script setup>
import { ref, computed, defineAsyncComponent } from 'vue'
import PageHeader from '@/components/shared/PageHeader.vue'
import FileDropZone from '@/components/upload/FileDropZone.vue'
import AcceptanceForm from '@/components/forms/AcceptanceForm.vue'
import ValidationTable from '@/components/tables/ValidationTable.vue'
import { useValidationStore } from '@/stores/validationStore'

const LinearityChart = defineAsyncComponent(() =>
  import('@/components/charts/LinearityChart.vue')
)

const validation = useValidationStore()

const validationTypes = [
  { value: 'lod', label: 'LOD' },
  { value: 'loq', label: 'LOQ' },
  { value: 'precision_intra', label: 'Precision (Intra)' },
  { value: 'precision_inter', label: 'Precision (Inter)' },
  { value: 'linearity', label: 'Linearity' },
]

const selectedType = ref('lod')

const hasDataset = computed(() => validation.dataset !== null)
const hasResult = computed(() => validation.result !== null)

const isLinearity = computed(() => selectedType.value === 'linearity')

const linearityData = computed(() => {
  if (!hasResult.value || !isLinearity.value) return null
  const r = validation.result
  const raw = r.raw_summary || {}
  // The validation engine returns linearity results in raw_summary
  if (raw.levels && raw.slope !== undefined) {
    return {
      levels: raw.levels,
      regression: {
        slope: raw.slope,
        intercept: raw.intercept,
        r_squared: raw.r_squared,
      },
    }
  }
  return null
})

const resultMetrics = computed(() => {
  if (!hasResult.value) return []
  return validation.result.metrics || []
})

async function handleFileSelected(file) {
  try {
    await validation.upload(file, selectedType.value)
  } catch {
    // error stored in validation.error
  }
}

async function handleRunValidation(criteria) {
  if (!validation.dataset?.dataset_id) return
  try {
    await validation.validate(validation.dataset.dataset_id, criteria)
  } catch {
    // error stored in validation.error
  }
}

function handleReset() {
  validation.reset()
}
</script>

<template>
  <div class="view">
    <PageHeader title="Assay Validation" subtitle="Method validation protocols and linearity studies" />

    <!-- Upload Section -->
    <div class="section">
      <div class="section__header">
        <span class="section__title">Upload Dataset</span>
        <button
          v-if="hasDataset || hasResult"
          class="section__reset-btn"
          @click="handleReset"
        >
          Start Over
        </button>
      </div>

      <div class="upload-row">
        <div class="type-selector">
          <label class="type-selector__label">Validation Type</label>
          <select
            v-model="selectedType"
            class="type-selector__select"
            :disabled="hasDataset"
          >
            <option
              v-for="t in validationTypes"
              :key="t.value"
              :value="t.value"
            >
              {{ t.label }}
            </option>
          </select>
        </div>

        <div class="upload-zone-wrap">
          <FileDropZone @file-selected="handleFileSelected" />
        </div>
      </div>
    </div>

    <!-- Loading skeleton -->
    <div v-if="validation.loading" class="section section--loading">
      <div class="skeleton skeleton--block"></div>
    </div>

    <!-- Error -->
    <div v-else-if="validation.error" class="section section--error">
      <p class="error-text">{{ validation.error }}</p>
    </div>

    <!-- Acceptance Criteria (when dataset uploaded, before results) -->
    <template v-else-if="hasDataset && !hasResult">
      <div class="section section--upload-status">
        <p class="upload-status-text">
          Dataset uploaded: <strong>{{ validation.dataset.file_name || 'file' }}</strong>
          <span v-if="validation.dataset.row_count">({{ validation.dataset.row_count }} rows)</span>
        </p>
      </div>
      <AcceptanceForm :loading="validation.loading" @submit="handleRunValidation" />
    </template>

    <!-- Validation Results -->
    <template v-else-if="hasResult">
      <div class="section section--upload-status">
        <p class="upload-status-text">
          Dataset: <strong>{{ validation.dataset?.file_name || 'file' }}</strong>
          | Type: <strong>{{ validationTypes.find(t => t.value === selectedType)?.label }}</strong>
        </p>
      </div>

      <div class="section">
        <div class="section__header">
          <span class="section__title">Validation Results</span>
        </div>
        <ValidationTable :metrics="resultMetrics" />
      </div>

      <LinearityChart
        v-if="linearityData"
        :levels="linearityData.levels"
        :regression="linearityData.regression"
      />
    </template>

    <!-- Empty state -->
    <div v-else class="view__empty">
      <p class="view__empty-text">Select a validation type and upload a dataset to begin.</p>
    </div>
  </div>
</template>

<style scoped>
.view {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.view__empty {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.view__empty-text {
  font-size: 15px;
  color: var(--text-muted);
  font-weight: 400;
}

.section {
  padding: 20px 28px;
  border-bottom: 1px solid var(--border-subtle);
}

.section--loading {
  padding: 20px 28px;
}

.section--error {
  padding: 20px 28px;
}

.section--upload-status {
  padding: 12px 28px;
  background-color: var(--bg-surface);
}

.section__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.section__title {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
}

.section__reset-btn {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-muted);
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: color 0.15s ease, background-color 0.15s ease;
}

.section__reset-btn:hover {
  color: var(--text-primary);
  background-color: var(--bg-surface-2);
}

.upload-row {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.type-selector {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex-shrink: 0;
  min-width: 180px;
}

.type-selector__label {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-muted);
}

.type-selector__select {
  padding: 7px 10px;
  font-size: 13px;
  font-family: inherit;
  color: var(--text-primary);
  background-color: var(--bg-surface-2);
  border: 1px solid var(--border-subtle);
  border-radius: 6px;
  outline: none;
  cursor: pointer;
  transition: border-color 0.15s ease;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%238E97A3' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  padding-right: 28px;
}

.type-selector__select:focus {
  border-color: var(--border-strong);
}

.type-selector__select:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.type-selector__select option {
  background-color: var(--bg-surface-2);
  color: var(--text-primary);
}

.upload-zone-wrap {
  flex: 1;
  min-width: 0;
}

.upload-status-text {
  font-size: 13px;
  color: var(--text-secondary);
}

.upload-status-text strong {
  color: var(--text-primary);
  font-weight: 500;
}

.skeleton {
  border-radius: 6px;
  background: linear-gradient(
    90deg,
    var(--bg-surface-2) 25%,
    var(--bg-highlight) 50%,
    var(--bg-surface-2) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

.skeleton--block {
  height: 120px;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.error-text {
  font-size: 13px;
  color: var(--color-danger);
}
</style>
