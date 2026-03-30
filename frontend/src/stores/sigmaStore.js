import { defineStore } from 'pinia'
import { ref } from 'vue'
import { calculateSigma, fetchSigmaHistory } from '@/api/sigmaApi'

export const useSigmaStore = defineStore('sigma', () => {
  const results = ref([])
  const history = ref({ assay: '', entries: [] })
  const loading = ref(false)
  const error = ref(null)

  async function calculate(inputs) {
    loading.value = true
    error.value = null
    try {
      const data = await calculateSigma(inputs)
      // Merge input values (tea_percent, bias_percent, cv_percent) into results
      // so the UI table can display them alongside calculated fields
      results.value = data.results.map((r) => {
        const input = inputs.find((i) => i.assay === r.assay)
        return {
          ...r,
          tea_percent: input?.tea_percent,
          bias_percent: input?.bias_percent,
          cv_percent: input?.cv_percent,
        }
      })
      return data
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  async function loadHistory(assay) {
    loading.value = true
    error.value = null
    try {
      history.value = await fetchSigmaHistory({ assay })
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  function clearResults() {
    results.value = []
    error.value = null
  }

  return { results, history, loading, error, calculate, loadHistory, clearResults }
})
