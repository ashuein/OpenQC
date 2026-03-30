import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fetchAuditLog, verifyChain, exportAuditLog } from '@/api/auditApi'

export const useAuditStore = defineStore('audit', () => {
  const entries = ref([])
  const pagination = ref({ page: 1, page_size: 50, total: 0 })
  const chainStatus = ref(null)
  const loading = ref(false)
  const error = ref(null)

  async function loadLog(params = {}) {
    loading.value = true
    error.value = null
    try {
      const data = await fetchAuditLog({
        page: pagination.value.page,
        page_size: pagination.value.page_size,
        ...params,
      })
      entries.value = data.items
      pagination.value = {
        page: data.page,
        page_size: data.page_size,
        total: data.total,
      }
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  async function checkChain() {
    loading.value = true
    error.value = null
    try {
      chainStatus.value = await verifyChain()
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  async function exportLog(format) {
    try {
      return await exportAuditLog(format)
    } catch (e) {
      error.value = e.message
      throw e
    }
  }

  function clearError() {
    error.value = null
  }

  return {
    entries,
    pagination,
    chainStatus,
    loading,
    error,
    loadLog,
    checkChain,
    exportLog,
    clearError,
  }
})
