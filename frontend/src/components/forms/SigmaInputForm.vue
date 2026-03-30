<script setup>
import { ref } from 'vue'
import { Plus, X } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'

const emit = defineEmits(['submit'])

function createRow() {
  return { assay: '', tea_percent: null, bias_percent: null, cv_percent: null }
}

const rows = ref([createRow()])

function addRow() {
  rows.value.push(createRow())
}

function removeRow(index) {
  if (rows.value.length > 1) {
    rows.value.splice(index, 1)
  }
}

function isValid() {
  return rows.value.every(
    (r) =>
      r.assay.trim() !== '' &&
      r.tea_percent !== null &&
      r.tea_percent > 0 &&
      r.bias_percent !== null &&
      r.cv_percent !== null &&
      r.cv_percent > 0
  )
}

function handleSubmit() {
  if (!isValid()) return
  emit(
    'submit',
    rows.value.map((r) => ({
      assay: r.assay.trim(),
      tea_percent: Number(r.tea_percent),
      bias_percent: Number(r.bias_percent),
      cv_percent: Number(r.cv_percent),
    }))
  )
}
</script>

<template>
  <div class="sigma-form">
    <div class="sigma-form__header">
      <span class="sigma-form__title">Sigma Inputs</span>
      <Button variant="ghost" size="sm" @click="addRow">
        <Plus :size="16" :stroke-width="1.75" />
        <span>Add Row</span>
      </Button>
    </div>

    <div class="sigma-form__table-wrap">
      <table class="sigma-form__table">
        <thead>
          <tr>
            <th>Assay</th>
            <th>TEa %</th>
            <th>Bias %</th>
            <th>CV %</th>
            <th class="sigma-form__th-action"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, i) in rows" :key="i">
            <td>
              <input
                v-model="row.assay"
                type="text"
                class="sigma-form__input sigma-form__input--text"
                placeholder="e.g. Glucose"
              />
            </td>
            <td>
              <input
                v-model.number="row.tea_percent"
                type="number"
                class="sigma-form__input"
                placeholder="0.0"
                step="0.1"
                min="0"
              />
            </td>
            <td>
              <input
                v-model.number="row.bias_percent"
                type="number"
                class="sigma-form__input"
                placeholder="0.0"
                step="0.1"
              />
            </td>
            <td>
              <input
                v-model.number="row.cv_percent"
                type="number"
                class="sigma-form__input"
                placeholder="0.0"
                step="0.1"
                min="0"
              />
            </td>
            <td class="sigma-form__td-action">
              <button
                v-if="rows.length > 1"
                class="sigma-form__remove-btn"
                @click="removeRow(i)"
                title="Remove row"
              >
                <X :size="16" :stroke-width="1.75" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="sigma-form__actions">
      <Button :disabled="!isValid()" @click="handleSubmit">
        Calculate Sigma
      </Button>
    </div>
  </div>
</template>

<style scoped>
.sigma-form {
  padding: 20px 28px;
  border-bottom: 1px solid var(--border-subtle);
}

.sigma-form__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.sigma-form__title {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
}

.sigma-form__table-wrap {
  overflow-x: auto;
}

.sigma-form__table {
  width: 100%;
  border-collapse: collapse;
}

.sigma-form__table th {
  text-align: left;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-muted);
  padding: 0 8px 8px 0;
  white-space: nowrap;
}

.sigma-form__th-action {
  width: 40px;
}

.sigma-form__table td {
  padding: 0 8px 8px 0;
}

.sigma-form__td-action {
  width: 40px;
  vertical-align: middle;
}

.sigma-form__input {
  width: 100%;
  min-width: 80px;
  padding: 7px 10px;
  font-size: 13px;
  font-family: inherit;
  color: var(--text-primary);
  background-color: var(--bg-surface-2);
  border: 1px solid var(--border-subtle);
  border-radius: 6px;
  outline: none;
  transition: border-color 0.15s ease;
}

.sigma-form__input--text {
  min-width: 160px;
}

.sigma-form__input:focus {
  border-color: var(--border-strong);
}

.sigma-form__input::placeholder {
  color: var(--text-muted);
  opacity: 0.6;
}

/* Hide number input spinners */
.sigma-form__input[type='number']::-webkit-outer-spin-button,
.sigma-form__input[type='number']::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
.sigma-form__input[type='number'] {
  -moz-appearance: textfield;
}

.sigma-form__remove-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border: none;
  border-radius: 4px;
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  transition: color 0.15s ease, background-color 0.15s ease;
}

.sigma-form__remove-btn:hover {
  color: var(--color-danger);
  background-color: var(--bg-surface-2);
}

.sigma-form__actions {
  margin-top: 16px;
}
</style>
