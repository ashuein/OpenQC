<script setup>
import { ref } from 'vue'
import { Upload } from 'lucide-vue-next'

const emit = defineEmits(['file-selected'])

const isDragOver = ref(false)
const selectedFile = ref(null)
const fileInputRef = ref(null)

const acceptedTypes = [
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  'application/vnd.ms-excel',
]
const acceptedExtensions = ['.xlsx', '.xls']

function isValidFile(file) {
  if (acceptedTypes.includes(file.type)) return true
  const ext = file.name.substring(file.name.lastIndexOf('.')).toLowerCase()
  return acceptedExtensions.includes(ext)
}

function handleDragOver(e) {
  e.preventDefault()
  isDragOver.value = true
}

function handleDragLeave() {
  isDragOver.value = false
}

function handleDrop(e) {
  e.preventDefault()
  isDragOver.value = false
  const file = e.dataTransfer.files[0]
  if (file && isValidFile(file)) {
    selectedFile.value = file
    emit('file-selected', file)
  }
}

function handleClick() {
  fileInputRef.value?.click()
}

function handleFileInput(e) {
  const file = e.target.files[0]
  if (file && isValidFile(file)) {
    selectedFile.value = file
    emit('file-selected', file)
  }
}

function formatSize(bytes) {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}
</script>

<template>
  <div
    class="drop-zone"
    :class="{ 'drop-zone--active': isDragOver, 'drop-zone--has-file': selectedFile }"
    @dragover="handleDragOver"
    @dragleave="handleDragLeave"
    @drop="handleDrop"
    @click="handleClick"
  >
    <input
      ref="fileInputRef"
      type="file"
      accept=".xlsx,.xls"
      class="drop-zone__input"
      @change="handleFileInput"
    />

    <template v-if="selectedFile">
      <div class="drop-zone__file-info">
        <Upload :size="20" :stroke-width="1.75" class="drop-zone__icon" />
        <div class="drop-zone__file-details">
          <span class="drop-zone__file-name">{{ selectedFile.name }}</span>
          <span class="drop-zone__file-size">{{ formatSize(selectedFile.size) }}</span>
        </div>
      </div>
      <span class="drop-zone__hint">Click or drop to replace</span>
    </template>

    <template v-else>
      <Upload :size="24" :stroke-width="1.5" class="drop-zone__icon" />
      <span class="drop-zone__label">Drop an Excel file here, or click to browse</span>
      <span class="drop-zone__hint">Accepts .xlsx and .xls files</span>
    </template>
  </div>
</template>

<style scoped>
.drop-zone {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 32px 24px;
  border: 1px dashed var(--border-strong);
  border-radius: 8px;
  background-color: var(--bg-surface);
  cursor: pointer;
  transition: border-color 0.15s ease, background-color 0.15s ease;
  min-height: 160px;
}

.drop-zone:hover {
  border-color: var(--text-muted);
  background-color: var(--bg-surface-2);
}

.drop-zone--active {
  border-color: var(--text-secondary);
  background-color: var(--bg-highlight);
}

.drop-zone--has-file {
  border-style: solid;
  border-color: var(--border-strong);
}

.drop-zone__input {
  display: none;
}

.drop-zone__icon {
  color: var(--text-muted);
}

.drop-zone__label {
  font-size: 14px;
  font-weight: 450;
  color: var(--text-secondary);
}

.drop-zone__hint {
  font-size: 12px;
  color: var(--text-muted);
}

.drop-zone__file-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.drop-zone__file-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.drop-zone__file-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.drop-zone__file-size {
  font-size: 12px;
  color: var(--text-muted);
}
</style>
