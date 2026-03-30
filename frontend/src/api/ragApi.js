const BASE_URL = 'http://localhost:8000'

export async function fetchRAGStatus() {
  const res = await fetch(`${BASE_URL}/rag/status`)
  if (!res.ok) throw new Error(`Fetch status failed: ${res.status}`)
  return res.json()
}

export async function triggerIngestion() {
  const res = await fetch(`${BASE_URL}/rag/ingest`, { method: 'POST' })
  if (!res.ok) throw new Error(`Ingestion failed: ${res.status}`)
  return res.json()
}

export async function queryRAG(question) {
  const res = await fetch(`${BASE_URL}/rag/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  })
  if (!res.ok) throw new Error(`Query failed: ${res.status}`)
  return res.json()
}
