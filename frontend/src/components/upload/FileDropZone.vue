<script setup>
import { ref } from 'vue'
import { Upload, FileSpreadsheet, X } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'

const emit = defineEmits(['file-selected'])

const selectedFile = ref(null)
const fileInputRef = ref(null)

function isValidFile(file) {
  const ext = file.name.substring(file.name.lastIndexOf('.')).toLowerCase()
  return ['.xlsx', '.xls'].includes(ext)
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
  // Reset so same file can be re-selected
  e.target.value = ''
}

function handleDrop(e) {
  e.preventDefault()
  const file = e.dataTransfer.files[0]
  if (file && isValidFile(file)) {
    selectedFile.value = file
    emit('file-selected', file)
  }
}

function clearFile() {
  selectedFile.value = null
}

function formatSize(bytes) {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}
</script>

<template>
  <div
    class="file-picker"
    @dragover.prevent
    @drop="handleDrop"
  >
    <input
      ref="fileInputRef"
      type="file"
      accept=".xlsx,.xls"
      class="file-picker__input"
      @change="handleFileInput"
    />

    <template v-if="selectedFile">
      <div class="file-picker__selected">
        <FileSpreadsheet :size="16" :stroke-width="1.75" class="file-picker__icon" />
        <span class="file-picker__name">{{ selectedFile.name }}</span>
        <span class="file-picker__size">{{ formatSize(selectedFile.size) }}</span>
        <button class="file-picker__clear" @click.stop="clearFile" title="Remove file">
          <X :size="14" :stroke-width="2" />
        </button>
      </div>
    </template>
    <template v-else>
      <Button size="sm" variant="outline" @click="handleClick">
        <Upload :size="14" :stroke-width="1.75" />
        Choose File
      </Button>
      <span class="file-picker__hint">.xlsx / .xls — or drop here</span>
    </template>
  </div>
</template>

<style scoped>
.file-picker {
  display: flex;
  align-items: center;
  gap: 10px;
  min-height: 36px;
}

.file-picker__input {
  display: none;
}

.file-picker__selected {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 8px 4px 10px;
  background: var(--bg-surface-2);
  border: 1px solid var(--border-subtle);
  border-radius: 6px;
  max-width: 320px;
}

.file-picker__icon {
  color: var(--color-success);
  flex-shrink: 0;
}

.file-picker__name {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 180px;
}

.file-picker__size {
  font-size: 11px;
  color: var(--text-muted);
  flex-shrink: 0;
}

.file-picker__clear {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border: none;
  background: none;
  color: var(--text-muted);
  cursor: pointer;
  border-radius: 4px;
  flex-shrink: 0;
}

.file-picker__clear:hover {
  color: var(--color-danger);
  background: color-mix(in srgb, var(--color-danger) 10%, transparent);
}

.file-picker__hint {
  font-size: 11px;
  color: var(--text-muted);
}
</style>
