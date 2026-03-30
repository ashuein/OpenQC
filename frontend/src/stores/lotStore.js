import { defineStore } from 'pinia'
import { ref } from 'vue'
import {
  fetchReagentLots,
  createReagentLot,
  fetchControlLots,
  createControlLot,
} from '@/api/lotApi'

export const useLotStore = defineStore('lot', () => {
  const reagentLots = ref([])
  const controlLots = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function loadReagentLots() {
    loading.value = true
    error.value = null
    try {
      reagentLots.value = await fetchReagentLots()
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  async function addReagentLot(data) {
    loading.value = true
    error.value = null
    try {
      const lot = await createReagentLot(data)
      reagentLots.value.unshift(lot)
      return lot
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  async function loadControlLots() {
    loading.value = true
    error.value = null
    try {
      controlLots.value = await fetchControlLots()
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  async function addControlLot(data) {
    loading.value = true
    error.value = null
    try {
      const lot = await createControlLot(data)
      controlLots.value.unshift(lot)
      return lot
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  function clearError() {
    error.value = null
  }

  return {
    reagentLots,
    controlLots,
    loading,
    error,
    loadReagentLots,
    addReagentLot,
    loadControlLots,
    addControlLot,
    clearError,
  }
})
