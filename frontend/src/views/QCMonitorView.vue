<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { X } from 'lucide-vue-next'
import PageHeader from '@/components/shared/PageHeader.vue'
import ExportButton from '@/components/shared/ExportButton.vue'
import FileDropZone from '@/components/upload/FileDropZone.vue'
import LJChart from '@/components/charts/LJChart.vue'
import ViolationTable from '@/components/tables/ViolationTable.vue'
import RunSummaryTable from '@/components/tables/RunSummaryTable.vue'
import { Button } from '@/components/ui/button'
import { useQcStore } from '@/stores/qcStore'

const store = useQcStore()

// --- Instrument/experiment type config ---
const instrumentTypes = [
  {
    id: 'rt-pcr',
    label: 'RT-PCR / Molecular',
    instruments: ['QuantStudio 5', 'QuantStudio 7', 'Bio-Rad CFX96', 'Bio-Rad CFX Connect', 'Roche LightCycler 480', 'Cepheid GeneXpert', 'Other'],
    assays: ['SARS-CoV-2', 'HIV-1 RNA', 'HBV DNA', 'HCV RNA', 'TB/MTB', 'Influenza A/B', 'HPV', 'Other'],
    showChannel: true,
  },
  {
    id: 'chemistry',
    label: 'Clinical Chemistry',
    instruments: ['Cobas c501', 'Cobas c701', 'Vitros 5600', 'Architect c8000', 'AU5800', 'Other'],
    assays: ['Glucose', 'Creatinine', 'BUN', 'Total Cholesterol', 'HDL', 'LDL', 'Triglycerides', 'ALT', 'AST', 'ALP', 'Bilirubin', 'HbA1c', 'Other'],
    showChannel: false,
  },
  {
    id: 'hematology',
    label: 'Hematology',
    instruments: ['Sysmex XN-1000', 'Sysmex XN-2000', 'Beckman Coulter DxH 800', 'Mindray BC-6800', 'Other'],
    assays: ['CBC (WBC)', 'CBC (RBC)', 'Hemoglobin', 'Hematocrit', 'Platelet Count', 'MCV', 'MCH', 'MCHC', 'Other'],
    showChannel: false,
  },
  {
    id: 'immunoassay',
    label: 'Immunoassay',
    instruments: ['Cobas e801', 'Cobas e601', 'Architect i2000', 'Vitros ECi', 'Liaison XL', 'Other'],
    assays: ['TSH', 'FT4', 'FT3', 'Troponin I', 'CK-MB', 'BNP', 'PSA', 'CEA', 'CA-125', 'AFP', 'Ferritin', 'Vitamin D', 'Other'],
    showChannel: false,
  },
  {
    id: 'coagulation',
    label: 'Coagulation',
    instruments: ['Sysmex CS-5100', 'Sysmex CS-2500', 'Stago STA-R Max', 'ACL TOP', 'Other'],
    assays: ['PT/INR', 'APTT', 'Fibrinogen', 'D-Dimer', 'Other'],
    showChannel: false,
  },
  {
    id: 'other',
    label: 'Other / Custom',
    instruments: [],
    assays: [],
    showChannel: false,
  },
]

const selectedType = ref('')
const selectedInstrument = ref('')
const customInstrument = ref('')
const selectedAssay = ref('')
const customAssay = ref('')
const channel = ref('')
const reagentLotId = ref('')
const controlLotId = ref('')

const selectedFile = ref(null)
const uploadStatus = ref('idle')
const runsLoading = ref(false)

// Error toast
const errorMsg = ref('')
const showError = ref(false)

// Column mapping
const showColumnMapping = ref(false)
const colValue = ref('')
const colLevel = ref('')
const colMean = ref('')
const colSD = ref('')
const colTarget = ref('')

const currentConfig = computed(() => instrumentTypes.find(t => t.id === selectedType.value) || null)
const instrumentOptions = computed(() => currentConfig.value?.instruments || [])
const assayOptions = computed(() => currentConfig.value?.assays || [])
const showChannel = computed(() => currentConfig.value?.showChannel ?? false)

const effectiveInstrument = computed(() => {
  if (selectedInstrument.value === 'Other') return customInstrument.value || 'Other'
  return selectedInstrument.value || 'Unknown'
})

const effectiveAssay = computed(() => {
  if (selectedAssay.value === 'Other') return customAssay.value || 'Other'
  return selectedAssay.value || 'Unknown'
})

// Reset dependent fields when type changes
watch(selectedType, () => {
  selectedInstrument.value = ''
  customInstrument.value = ''
  selectedAssay.value = ''
  customAssay.value = ''
  channel.value = ''
})

function onFileSelected(file) {
  selectedFile.value = file
  uploadStatus.value = 'idle'
  showColumnMapping.value = false
  dismissError()
  store.clearAnalysis()
}

function showErrorToast(msg) {
  errorMsg.value = msg
  showError.value = true
}

function dismissError() {
  errorMsg.value = ''
  showError.value = false
}

async function handleUpload() {
  if (!selectedFile.value) return
  dismissError()

  const metadata = {
    instrument: effectiveInstrument.value,
    assay: effectiveAssay.value,
  }
  if (channel.value) metadata.channel = channel.value
  if (reagentLotId.value) metadata.reagent_lot_id = reagentLotId.value
  if (controlLotId.value) metadata.control_lot_id = controlLotId.value

  uploadStatus.value = 'uploading'

  try {
    const run = await store.upload(selectedFile.value, metadata)
    uploadStatus.value = 'parsing'
    await store.analyze(run.id)
    uploadStatus.value = 'complete'
    loadRuns()
  } catch (e) {
    uploadStatus.value = 'error'
    const msg = e.message || 'Upload or analysis failed.'
    showErrorToast(msg)
    if (msg.toLowerCase().includes('no data points could be parsed')) {
      showColumnMapping.value = true
    }
  }
}

async function retryUploadWithMapping() {
  if (!selectedFile.value) return
  dismissError()

  const mapping = {}
  if (colValue.value) mapping.value = colValue.value
  if (colLevel.value) mapping.level = colLevel.value
  if (colMean.value) mapping.mean = colMean.value
  if (colSD.value) mapping.sd = colSD.value
  if (colTarget.value) mapping.target = colTarget.value

  const metadata = {
    instrument: effectiveInstrument.value,
    assay: effectiveAssay.value,
    column_mapping: JSON.stringify(mapping),
  }
  if (channel.value) metadata.channel = channel.value
  if (reagentLotId.value) metadata.reagent_lot_id = reagentLotId.value
  if (controlLotId.value) metadata.control_lot_id = controlLotId.value

  uploadStatus.value = 'uploading'

  try {
    const run = await store.upload(selectedFile.value, metadata)
    showColumnMapping.value = false
    uploadStatus.value = 'parsing'
    await store.analyze(run.id)
    uploadStatus.value = 'complete'
    loadRuns()
  } catch (e) {
    uploadStatus.value = 'error'
    showErrorToast(e.message || 'Upload or analysis failed.')
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
  try { await store.loadRuns() } finally { runsLoading.value = false }
}

function handleSelectRun(runId) {
  store.loadRunDetail(runId)
}

onMounted(() => { loadRuns() })
</script>

<template>
  <div class="view">
    <PageHeader title="QC Monitor" subtitle="Westgard rule evaluation and Levey-Jennings charts">
      <template #actions>
        <ExportButton @export="() => {}" />
      </template>
    </PageHeader>

    <div class="view__body">
      <!-- Error Toast -->
      <Teleport to="body">
        <Transition name="toast">
          <div v-if="showError" class="error-toast">
            <span class="error-toast__text">{{ errorMsg }}</span>
            <button class="error-toast__close" @click="dismissError">
              <X :size="16" :stroke-width="2" />
            </button>
          </div>
        </Transition>
      </Teleport>

      <!-- Upload Section -->
      <section class="section">
        <h2 class="section__title">Upload QC Data</h2>

        <div class="upload-card">
          <!-- Step 1: Experiment type -->
          <div class="upload-row">
            <div class="field">
              <label class="field__label">Experiment Type</label>
              <select v-model="selectedType" class="field__select">
                <option value="" disabled>Select type...</option>
                <option v-for="t in instrumentTypes" :key="t.id" :value="t.id">{{ t.label }}</option>
              </select>
            </div>

            <div v-if="currentConfig" class="field">
              <label class="field__label">Instrument</label>
              <select v-if="instrumentOptions.length" v-model="selectedInstrument" class="field__select">
                <option value="" disabled>Select...</option>
                <option v-for="i in instrumentOptions" :key="i" :value="i">{{ i }}</option>
              </select>
              <input v-else v-model="customInstrument" class="field__input" placeholder="Instrument name" />
            </div>

            <div v-if="selectedInstrument === 'Other'" class="field">
              <label class="field__label">Instrument Name</label>
              <input v-model="customInstrument" class="field__input" placeholder="Enter name" />
            </div>

            <div v-if="currentConfig" class="field">
              <label class="field__label">Assay / Analyte</label>
              <select v-if="assayOptions.length" v-model="selectedAssay" class="field__select">
                <option value="" disabled>Select...</option>
                <option v-for="a in assayOptions" :key="a" :value="a">{{ a }}</option>
              </select>
              <input v-else v-model="customAssay" class="field__input" placeholder="Assay name" />
            </div>

            <div v-if="selectedAssay === 'Other'" class="field">
              <label class="field__label">Assay Name</label>
              <input v-model="customAssay" class="field__input" placeholder="Enter name" />
            </div>
          </div>

          <!-- Step 2: Optional fields -->
          <div v-if="currentConfig" class="upload-row">
            <div v-if="showChannel" class="field">
              <label class="field__label">Channel / Fluor</label>
              <input v-model="channel" class="field__input" placeholder="e.g. FAM" />
            </div>
            <div class="field">
              <label class="field__label">Reagent Lot</label>
              <input v-model="reagentLotId" class="field__input" placeholder="Lot #" />
            </div>
            <div class="field">
              <label class="field__label">Control Lot</label>
              <input v-model="controlLotId" class="field__input" placeholder="Lot #" />
            </div>
          </div>

          <!-- Step 3: File + Upload button -->
          <div class="upload-row upload-row--file">
            <div class="file-zone">
              <FileDropZone @file-selected="onFileSelected" />
            </div>
            <Button
              :disabled="!selectedFile || !selectedType || uploadStatus === 'uploading' || uploadStatus === 'parsing'"
              @click="handleUpload"
            >
              {{ uploadStatus === 'uploading' ? 'Uploading...' : uploadStatus === 'parsing' ? 'Analyzing...' : 'Upload and Analyze' }}
            </Button>
          </div>
        </div>
      </section>

      <!-- Column Mapping Fallback -->
      <section v-if="showColumnMapping" class="section">
        <div class="column-mapping">
          <h3 class="column-mapping__title">Column Mapping Required</h3>
          <p class="mapping-hint">Auto-detection failed. Specify which columns in your file contain the data:</p>
          <div class="mapping-grid">
            <div class="field">
              <label class="field__label">Value Column *</label>
              <input v-model="colValue" class="field__input" placeholder="e.g. Cq, Value, Result" />
            </div>
            <div class="field">
              <label class="field__label">Level Column</label>
              <input v-model="colLevel" class="field__input" placeholder="e.g. Level, Sample" />
            </div>
            <div class="field">
              <label class="field__label">Mean (optional)</label>
              <input v-model="colMean" class="field__input" placeholder="e.g. Mean" />
            </div>
            <div class="field">
              <label class="field__label">SD (optional)</label>
              <input v-model="colSD" class="field__input" placeholder="e.g. SD" />
            </div>
            <div class="field">
              <label class="field__label">Analyte (optional)</label>
              <input v-model="colTarget" class="field__input" placeholder="e.g. Analyte" />
            </div>
          </div>
          <Button :disabled="!colValue" @click="retryUploadWithMapping">Retry with Mapping</Button>
        </div>
      </section>

      <!-- LJ Chart -->
      <section v-if="chartData" class="section">
        <h2 class="section__title">Levey-Jennings Chart</h2>
        <div class="section__content">
          <LJChart :data-points="chartData.data_points || []" :mean="chartData.mean" :sd="chartData.sd" />
        </div>
      </section>

      <section v-else-if="store.loading && uploadStatus === 'parsing'" class="section">
        <h2 class="section__title">Levey-Jennings Chart</h2>
        <div class="skeleton skeleton--chart" />
      </section>

      <!-- Violations -->
      <section v-if="store.analysisResult" class="section">
        <h2 class="section__title">Violations</h2>
        <div class="section__content">
          <ViolationTable :violations="violations" />
        </div>
      </section>

      <!-- Run History -->
      <section class="section">
        <h2 class="section__title">Run History</h2>
        <div class="section__content">
          <template v-if="runsLoading && store.runs.length === 0">
            <div class="skeleton skeleton--table" />
          </template>
          <template v-else>
            <RunSummaryTable :runs="store.runs" @select-run="handleSelectRun" />
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

.section { padding-top: 24px; }

.section__title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.section__content {
  background-color: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  overflow: hidden;
}

/* Upload card */
.upload-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.upload-row {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: flex-end;
}

.upload-row--file {
  align-items: center;
  gap: 16px;
}

.file-zone {
  flex: 1;
  min-width: 200px;
  max-width: 400px;
}

/* Compact fields */
.field {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 140px;
  flex: 1;
  max-width: 220px;
}

.field__label {
  font-size: 11px;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.field__input {
  height: 32px;
  padding: 0 10px;
  font-size: 13px;
  color: var(--text-primary);
  background: var(--bg-surface-2);
  border: 1px solid var(--border-subtle);
  border-radius: 6px;
  outline: none;
  font-family: inherit;
  transition: border-color 0.15s;
}

.field__input:focus { border-color: var(--border-strong); }
.field__input::placeholder { color: var(--text-muted); }

.field__select {
  height: 32px;
  padding: 0 28px 0 10px;
  font-size: 13px;
  color: var(--text-primary);
  background: var(--bg-surface-2);
  border: 1px solid var(--border-subtle);
  border-radius: 6px;
  outline: none;
  font-family: inherit;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%238E97A3' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 8px center;
  transition: border-color 0.15s;
}

.field__select:focus { border-color: var(--border-strong); }

.field__select option {
  background: var(--bg-surface-2);
  color: var(--text-primary);
}

/* Column mapping */
.column-mapping {
  background: color-mix(in srgb, var(--color-warning) 6%, var(--bg-surface));
  border: 1px solid color-mix(in srgb, var(--color-warning) 25%, transparent);
  border-radius: 8px;
  padding: 20px;
}

.column-mapping__title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.mapping-hint {
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 16px;
}

.mapping-grid {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}

.mapping-grid .field { max-width: 180px; min-width: 120px; }

/* Error toast (fixed position) */
.error-toast {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  max-width: 480px;
  background: color-mix(in srgb, var(--color-danger) 15%, var(--bg-surface));
  border: 1px solid var(--color-danger);
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}

.error-toast__text {
  font-size: 13px;
  color: var(--color-danger);
  flex: 1;
  line-height: 1.4;
}

.error-toast__close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border: none;
  background: none;
  color: var(--text-muted);
  cursor: pointer;
  border-radius: 4px;
  flex-shrink: 0;
  transition: color 0.15s, background 0.15s;
}

.error-toast__close:hover {
  color: var(--color-danger);
  background: color-mix(in srgb, var(--color-danger) 10%, transparent);
}

.toast-enter-active { transition: all 0.3s ease; }
.toast-leave-active { transition: all 0.2s ease; }
.toast-enter-from { opacity: 0; transform: translateX(40px); }
.toast-leave-to { opacity: 0; transform: translateX(40px); }

/* Skeletons */
.skeleton {
  background-color: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  animation: pulse 1.5s ease-in-out infinite;
}
.skeleton--chart { height: 340px; }
.skeleton--table { height: 200px; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
</style>
