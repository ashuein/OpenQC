import { defineStore } from 'pinia'
import { ref } from 'vue'
import { uploadValidationFile, runValidation, fetchValidationReport } from '@/api/validationApi'

export const useValidationStore = defineStore('validation', () => {
  const dataset = ref(null)
  const result = ref(null)
  const loading = ref(false)
  const error = ref(null)

  async function upload(file, validationType) {
    loading.value = true
    error.value = null
    try {
      dataset.value = await uploadValidationFile(file, validationType)
      return dataset.value
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  async function validate(datasetId, criteria) {
    loading.value = true
    error.value = null
    try {
      result.value = await runValidation(datasetId, criteria)
      return result.value
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  async function loadReport(validationId) {
    loading.value = true
    try {
      return await fetchValidationReport(validationId)
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  function reset() {
    dataset.value = null
    result.value = null
    error.value = null
  }

  return { dataset, result, loading, error, upload, validate, loadReport, reset }
})
