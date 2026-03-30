<script setup>
import { ref } from 'vue'
import { Plus, X } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'

const emit = defineEmits(['submit'])

const props = defineProps({
  loading: {
    type: Boolean,
    default: false,
  },
})

function createRow() {
  return { metric: '', threshold: null, operator: 'lte' }
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
    (r) => r.metric.trim() !== '' && r.threshold !== null && r.threshold !== ''
  )
}

function handleSubmit() {
  if (!isValid()) return
  emit(
    'submit',
    rows.value.map((r) => ({
      metric: r.metric.trim(),
      threshold: Number(r.threshold),
      operator: r.operator,
    }))
  )
}
</script>

<template>
  <div class="acceptance-form">
    <div class="acceptance-form__header">
      <span class="acceptance-form__title">Acceptance Criteria</span>
      <Button variant="ghost" size="sm" @click="addRow">
        <Plus :size="16" :stroke-width="1.75" />
        <span>Add Criterion</span>
      </Button>
    </div>

    <div class="acceptance-form__table-wrap">
      <table class="acceptance-form__table">
        <thead>
          <tr>
            <th>Metric</th>
            <th>Threshold</th>
            <th>Operator</th>
            <th class="acceptance-form__th-action"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, i) in rows" :key="i">
            <td>
              <input
                v-model="row.metric"
                type="text"
                class="acceptance-form__input acceptance-form__input--text"
                placeholder="e.g. CV %"
              />
            </td>
            <td>
              <input
                v-model.number="row.threshold"
                type="number"
                class="acceptance-form__input"
                placeholder="0.0"
                step="0.01"
              />
            </td>
            <td>
              <select v-model="row.operator" class="acceptance-form__select">
                <option value="lte">&le; (at most)</option>
                <option value="gte">&ge; (at least)</option>
              </select>
            </td>
            <td class="acceptance-form__td-action">
              <button
                v-if="rows.length > 1"
                class="acceptance-form__remove-btn"
                @click="removeRow(i)"
                title="Remove criterion"
              >
                <X :size="16" :stroke-width="1.75" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="acceptance-form__actions">
      <Button :disabled="!isValid() || loading" @click="handleSubmit">
        {{ loading ? 'Running...' : 'Run Validation' }}
      </Button>
    </div>
  </div>
</template>

<style scoped>
.acceptance-form {
  padding: 20px 28px;
  border-bottom: 1px solid var(--border-subtle);
}

.acceptance-form__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.acceptance-form__title {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
}

.acceptance-form__table-wrap {
  overflow-x: auto;
}

.acceptance-form__table {
  width: 100%;
  border-collapse: collapse;
}

.acceptance-form__table th {
  text-align: left;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-muted);
  padding: 0 8px 8px 0;
  white-space: nowrap;
}

.acceptance-form__th-action {
  width: 40px;
}

.acceptance-form__table td {
  padding: 0 8px 8px 0;
}

.acceptance-form__td-action {
  width: 40px;
  vertical-align: middle;
}

.acceptance-form__input {
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

.acceptance-form__input--text {
  min-width: 160px;
}

.acceptance-form__input:focus {
  border-color: var(--border-strong);
}

.acceptance-form__input::placeholder {
  color: var(--text-muted);
  opacity: 0.6;
}

.acceptance-form__input[type='number']::-webkit-outer-spin-button,
.acceptance-form__input[type='number']::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
.acceptance-form__input[type='number'] {
  -moz-appearance: textfield;
}

.acceptance-form__select {
  width: 100%;
  min-width: 120px;
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

.acceptance-form__select:focus {
  border-color: var(--border-strong);
}

.acceptance-form__select option {
  background-color: var(--bg-surface-2);
  color: var(--text-primary);
}

.acceptance-form__remove-btn {
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

.acceptance-form__remove-btn:hover {
  color: var(--color-danger);
  background-color: var(--bg-surface-2);
}

.acceptance-form__actions {
  margin-top: 16px;
}
</style>
