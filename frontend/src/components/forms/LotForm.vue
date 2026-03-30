<script setup>
import { reactive, computed } from 'vue'
import { Button } from '@/components/ui/button'

const props = defineProps({
  type: {
    type: String,
    required: true,
    validator: (v) => ['reagent', 'control'].includes(v),
  },
})

const emit = defineEmits(['submit', 'cancel'])

const reagentForm = reactive({
  assay_name: '',
  lot_number: '',
  expiry_date: '',
  open_date: '',
})

const controlForm = reactive({
  control_name: '',
  manufacturer: '',
  lot_number: '',
  assigned_mean: '',
  assigned_sd: '',
  expiry_date: '',
})

const currentForm = computed(() =>
  props.type === 'reagent' ? reagentForm : controlForm
)

const isValid = computed(() => {
  if (props.type === 'reagent') {
    return reagentForm.assay_name && reagentForm.lot_number && reagentForm.expiry_date
  }
  return (
    controlForm.control_name &&
    controlForm.lot_number &&
    controlForm.assigned_mean &&
    controlForm.assigned_sd &&
    controlForm.expiry_date
  )
})

function handleSubmit() {
  if (!isValid.value) return
  const data = { ...currentForm.value }
  if (props.type === 'control') {
    data.assigned_mean = parseFloat(data.assigned_mean)
    data.assigned_sd = parseFloat(data.assigned_sd)
  }
  emit('submit', data)
}

function handleCancel() {
  emit('cancel')
}
</script>

<template>
  <form class="lot-form" @submit.prevent="handleSubmit">
    <div class="lot-form__title">
      {{ type === 'reagent' ? 'Add Reagent Lot' : 'Add Control Lot' }}
    </div>

    <div class="lot-form__fields">
      <!-- Reagent fields -->
      <template v-if="type === 'reagent'">
        <div class="form-field">
          <label class="form-label">Assay Name</label>
          <input
            v-model="reagentForm.assay_name"
            type="text"
            class="form-input"
            placeholder="e.g. TSH, HbA1c"
          />
        </div>
        <div class="form-field">
          <label class="form-label">Lot Number</label>
          <input
            v-model="reagentForm.lot_number"
            type="text"
            class="form-input"
            placeholder="e.g. R-2024-001"
          />
        </div>
        <div class="form-field">
          <label class="form-label">Expiry Date</label>
          <input
            v-model="reagentForm.expiry_date"
            type="date"
            class="form-input"
          />
        </div>
        <div class="form-field">
          <label class="form-label">Open Date</label>
          <input
            v-model="reagentForm.open_date"
            type="date"
            class="form-input"
          />
        </div>
      </template>

      <!-- Control fields -->
      <template v-else>
        <div class="form-field">
          <label class="form-label">Control Name</label>
          <input
            v-model="controlForm.control_name"
            type="text"
            class="form-input"
            placeholder="e.g. Normal Control L1"
          />
        </div>
        <div class="form-field">
          <label class="form-label">Manufacturer</label>
          <input
            v-model="controlForm.manufacturer"
            type="text"
            class="form-input"
            placeholder="e.g. Bio-Rad"
          />
        </div>
        <div class="form-field">
          <label class="form-label">Lot Number</label>
          <input
            v-model="controlForm.lot_number"
            type="text"
            class="form-input"
            placeholder="e.g. C-2024-001"
          />
        </div>
        <div class="form-field">
          <label class="form-label">Assigned Mean</label>
          <input
            v-model="controlForm.assigned_mean"
            type="number"
            step="any"
            class="form-input"
            placeholder="0.00"
          />
        </div>
        <div class="form-field">
          <label class="form-label">Assigned SD</label>
          <input
            v-model="controlForm.assigned_sd"
            type="number"
            step="any"
            class="form-input"
            placeholder="0.00"
          />
        </div>
        <div class="form-field">
          <label class="form-label">Expiry Date</label>
          <input
            v-model="controlForm.expiry_date"
            type="date"
            class="form-input"
          />
        </div>
      </template>
    </div>

    <div class="lot-form__actions">
      <Button variant="ghost" size="sm" type="button" @click="handleCancel">
        Cancel
      </Button>
      <Button size="sm" type="submit" :disabled="!isValid">
        Save Lot
      </Button>
    </div>
  </form>
</template>

<style scoped>
.lot-form {
  background-color: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 6px;
  padding: 20px;
}

.lot-form__title {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 16px;
}

.lot-form__fields {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px 16px;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.form-label {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.form-input {
  height: 34px;
  padding: 0 10px;
  border-radius: 4px;
  border: 1px solid var(--border-subtle);
  background-color: var(--bg-surface-2);
  color: var(--text-primary);
  font-size: 13px;
  font-family: inherit;
  outline: none;
  transition: border-color 0.15s ease;
}

.form-input::placeholder {
  color: var(--text-muted);
  opacity: 0.6;
}

.form-input:focus {
  border-color: var(--border-strong);
}

/* Override native date input color scheme for dark theme */
.form-input[type='date'] {
  color-scheme: dark;
}

.lot-form__actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid var(--border-subtle);
}
</style>
