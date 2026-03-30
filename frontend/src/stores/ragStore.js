import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fetchRAGStatus, triggerIngestion, queryRAG } from '@/api/ragApi'

export const useRAGStore = defineStore('rag', () => {
  const status = ref(null)
  const answer = ref(null)
  const loading = ref(false)
  const ingesting = ref(false)
  const error = ref(null)

  async function loadStatus() {
    try {
      status.value = await fetchRAGStatus()
    } catch (e) {
      error.value = e.message
    }
  }

  async function ingest() {
    ingesting.value = true
    error.value = null
    try {
      const result = await triggerIngestion()
      status.value = {
        ...status.value,
        status: 'ready',
        chunk_count: result.chunks_created,
      }
      return result
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      ingesting.value = false
    }
  }

  async function ask(question) {
    loading.value = true
    error.value = null
    answer.value = null
    try {
      answer.value = await queryRAG(question)
      return answer.value
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  function clearAnswer() {
    answer.value = null
    error.value = null
  }

  function clearError() {
    error.value = null
  }

  return {
    status,
    answer,
    loading,
    ingesting,
    error,
    loadStatus,
    ingest,
    ask,
    clearAnswer,
    clearError,
  }
})
