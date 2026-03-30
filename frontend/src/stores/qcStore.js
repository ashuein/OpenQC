import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { uploadQCFile, analyzeRun, fetchRuns, fetchRunDetail, deleteRun } from '@/api/qcApi'

export const useQcStore = defineStore('qc', () => {
  const runs = ref([])
  const currentRun = ref(null)
  const analysisResult = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const pagination = ref({ page: 1, page_size: 20, total: 0 })

  const recentRuns = computed(() => runs.value.slice(0, 5))
  const violationCount = computed(() =>
    runs.value.reduce((sum, r) => sum + (r.violation_count || 0), 0)
  )

  async function loadRuns(params = {}) {
    loading.value = true
    error.value = null
    try {
      const data = await fetchRuns({ page: pagination.value.page, page_size: pagination.value.page_size, ...params })
      runs.value = data.items
      pagination.value = { page: data.page, page_size: data.page_size, total: data.total }
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  async function upload(file, metadata) {
    loading.value = true
    error.value = null
    try {
      const run = await uploadQCFile(file, metadata)
      currentRun.value = run
      return run
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  async function analyze(runId) {
    loading.value = true
    error.value = null
    try {
      const result = await analyzeRun(runId)
      analysisResult.value = result
      return result
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  async function loadRunDetail(runId) {
    loading.value = true
    error.value = null
    try {
      currentRun.value = await fetchRunDetail(runId)
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  async function removeRun(runId) {
    await deleteRun(runId)
    runs.value = runs.value.filter(r => r.id !== runId)
  }

  function clearAnalysis() {
    analysisResult.value = null
  }

  function clearError() {
    error.value = null
  }

  return {
    runs, currentRun, analysisResult, loading, error, pagination,
    recentRuns, violationCount,
    loadRuns, upload, analyze, loadRunDetail, removeRun, clearAnalysis, clearError,
  }
})
