<script setup>
import { ref, onMounted, computed } from 'vue'
import PageHeader from '@/components/shared/PageHeader.vue'
import ExportButton from '@/components/shared/ExportButton.vue'
import FileDropZone from '@/components/upload/FileDropZone.vue'
import UploadProgress from '@/components/upload/UploadProgress.vue'
import LJChart from '@/components/charts/LJChart.vue'
import ViolationTable from '@/components/tables/ViolationTable.vue'
import RunSummaryTable from '@/components/tables/RunSummaryTable.vue'
import { Button } from '@/components/ui/button'
import { useQcStore } from '@/stores/qcStore'

const store = useQcStore()

const selectedFile = ref(null)
const uploadStatus = ref('idle')
const uploadMessage = ref('')

const instrument = ref('')
const assay = ref('')
const channel = ref('')
const reagentLotId = ref('')
const controlLotId = ref('')

const runsLoading = ref(false)

function onFileSelected(file) {
  selectedFile.value = file
  uploadStatus.value = 'idle'
  uploadMessage.value = ''
  store.clearAnalysis()
}

async function handleUpload() {
  if (!selectedFile.value) return

  const metadata = {}
  if (instrument.value) metadata.instrument = instrument.value
  if (assay.value) metadata.assay = assay.value
  if (channel.value) metadata.channel = channel.value
  if (reagentLotId.value) metadata.reagent_lot_id = reagentLotId.value
  if (controlLotId.value) metadata.control_lot_id = controlLotId.value

  uploadStatus.value = 'uploading'
  uploadMessage.value = ''

  try {
    const run = await store.upload(selectedFile.value, metadata)
    uploadStatus.value = 'parsing'
    uploadMessage.value = 'File uploaded. Running analysis...'

    await store.analyze(run.id)
    uploadStatus.value = 'complete'
    uploadMessage.value = 'Analysis complete.'
    loadRuns()
  } catch (e) {
    uploadStatus.value = 'error'
    uploadMessage.value = e.message || 'Upload or analysis failed.'
  }
}

const chartData = computed(() => {
  const result = store.analysisResult
  if (!result || !result.evaluated_points || result.evaluated_points.length === 0) return null
  return {
    data_points: result.evaluated_points,
    mean: result.summary_stats?.mean ?? null,
    sd: result.summary_stats?.sd ?? null,
  }
})

const violations = computed(() => {
  const result = store.analysisResult
  if (!result) return []
  return result.violations || []
})

async function loadRuns() {
  runsLoading.value = true
  try {
    await store.loadRuns()
  } finally {
    runsLoading.value = false
  }
}

function handleSelectRun(runId) {
  store.loadRunDetail(runId)
}

onMounted(() => {
  loadRuns()
})
</script>

<template>
  <div class="view">
    <PageHeader title="QC Monitor" subtitle="Westgard rule evaluation and Levey-Jennings charts">
      <template #actions>
        <ExportButton @export="() => {}" />
      </template>
    </PageHeader>

    <div class="view__body">
      <!-- Upload Section -->
      <section class="section">
        <h2 class="section__title">Upload QC Data</h2>
        <div class="upload-grid">
          <div class="upload-grid__dropzone">
            <FileDropZone @file-selected="onFileSelected" />
            <UploadProgress
              v-if="uploadStatus !== 'idle' || selectedFile"
              :status="uploadStatus"
              :file-name="selectedFile?.name || ''"
              :message="uploadMessage"
            />
          </div>
          <div class="upload-grid__form">
            <div class="form-field">
              <label class="form-field__label">Instrument</label>
              <input
                v-model="instrument"
                type="text"
                class="form-field__input"
                placeholder="e.g. Cobas 6000"
              />
            </div>
            <div class="form-field">
              <label class="form-field__label">Assay</label>
              <input
                v-model="assay"
                type="text"
                class="form-field__input"
                placeholder="e.g. Glucose"
              />
            </div>
            <div class="form-field">
              <label class="form-field__label">Channel</label>
              <input
                v-model="channel"
                type="text"
                class="form-field__input"
                placeholder="e.g. FAM"
              />
            </div>
            <div class="form-field">
              <label class="form-field__label">Reagent Lot ID</label>
              <input
                v-model="reagentLotId"
                type="text"
                class="form-field__input"
                placeholder="Lot number"
              />
            </div>
            <div class="form-field">
              <label class="form-field__label">Control Lot ID</label>
              <input
                v-model="controlLotId"
                type="text"
                class="form-field__input"
                placeholder="Lot number"
              />
            </div>
            <Button
              :disabled="!selectedFile || uploadStatus === 'uploading' || uploadStatus === 'parsing'"
              @click="handleUpload"
            >
              Upload and Analyze
            </Button>
          </div>
        </div>
      </section>

      <!-- Error Display -->
      <div v-if="store.error" class="error-bar">
        <span class="error-bar__text">{{ store.error }}</span>
        <button class="error-bar__dismiss" @click="store.clearError">Dismiss</button>
      </div>

      <!-- LJ Chart Section -->
      <section v-if="chartData" class="section">
        <h2 class="section__title">Levey-Jennings Chart</h2>
        <div class="section__content">
          <LJChart
            :data-points="chartData.data_points || []"
            :mean="chartData.mean"
            :sd="chartData.sd"
          />
        </div>
      </section>

      <!-- Loading skeleton for chart -->
      <section v-else-if="store.loading && uploadStatus === 'parsing'" class="section">
        <h2 class="section__title">Levey-Jennings Chart</h2>
        <div class="skeleton skeleton--chart" />
      </section>

      <!-- Violations Section -->
      <section v-if="store.analysisResult" class="section">
        <h2 class="section__title">Violations</h2>
        <div class="section__content">
          <ViolationTable :violations="violations" />
        </div>
      </section>

      <!-- Run History Section -->
      <section class="section">
        <h2 class="section__title">Run History</h2>
        <div class="section__content">
          <template v-if="runsLoading && store.runs.length === 0">
            <div class="skeleton skeleton--table" />
          </template>
          <template v-else>
            <RunSummaryTable
              :runs="store.runs"
              @select-run="handleSelectRun"
            />
          </template>
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

.upload-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}

@media (max-width: 900px) {
  .upload-grid {
    grid-template-columns: 1fr;
  }
}

.upload-grid__dropzone {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.upload-grid__form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-field__label {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-muted);
  letter-spacing: 0.01em;
}

.form-field__input {
  padding: 8px 12px;
  font-size: 13px;
  color: var(--text-primary);
  background-color: var(--bg-surface);
  border: 1px solid var(--border-strong);
  border-radius: 6px;
  outline: none;
  transition: border-color 0.15s ease;
  font-family: inherit;
}

.form-field__input::placeholder {
  color: var(--text-muted);
}

.form-field__input:focus {
  border-color: var(--text-muted);
}

.error-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 16px;
  margin-top: 16px;
  background-color: color-mix(in srgb, var(--color-danger) 10%, var(--bg-surface));
  border: 1px solid color-mix(in srgb, var(--color-danger) 30%, transparent);
  border-radius: 6px;
}

.error-bar__text {
  font-size: 13px;
  color: var(--color-danger);
}

.error-bar__dismiss {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-muted);
  background: none;
  border: none;
  cursor: pointer;
  padding: 2px 8px;
  font-family: inherit;
}

.error-bar__dismiss:hover {
  color: var(--text-secondary);
}

.skeleton {
  background-color: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  animation: pulse 1.5s ease-in-out infinite;
}

.skeleton--chart {
  height: 340px;
}

.skeleton--table {
  height: 200px;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
</style>
