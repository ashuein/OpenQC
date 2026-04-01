import { throwIfError } from './helpers'

const BASE_URL = 'http://localhost:8000'

export async function fetchRAGStatus() {
  const res = await fetch(`${BASE_URL}/rag/status`)
  await throwIfError(res, 'Fetch status failed')
  return res.json()
}

export async function triggerIngestion() {
  const res = await fetch(`${BASE_URL}/rag/ingest`, { method: 'POST' })
  await throwIfError(res, 'Ingestion failed')
  return res.json()
}

export async function queryRAG(question) {
  const res = await fetch(`${BASE_URL}/rag/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  })
  await throwIfError(res, 'Query failed')
  return res.json()
}
