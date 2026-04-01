import { throwIfError } from './helpers'

const BASE_URL = 'http://localhost:8000'

export async function uploadQCFile(file, lotMetadata) {
  const formData = new FormData()
  formData.append('file', file)
  if (lotMetadata) {
    Object.entries(lotMetadata).forEach(([key, value]) => {
      if (value != null) formData.append(key, value)
    })
  }
  const res = await fetch(`${BASE_URL}/qc/upload`, { method: 'POST', body: formData })
  await throwIfError(res, 'Upload failed')
  return res.json()
}

export async function analyzeRun(runId) {
  const res = await fetch(`${BASE_URL}/qc/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ run_id: runId }),
  })
  await throwIfError(res, 'Analysis failed')
  return res.json()
}

export async function fetchRuns(params = {}) {
  const query = new URLSearchParams(params).toString()
  const res = await fetch(`${BASE_URL}/qc/runs${query ? '?' + query : ''}`)
  await throwIfError(res, 'Fetch runs failed')
  return res.json()
}

export async function fetchRunDetail(runId) {
  const res = await fetch(`${BASE_URL}/qc/run/${runId}`)
  await throwIfError(res, 'Fetch run failed')
  return res.json()
}

export async function deleteRun(runId) {
  const res = await fetch(`${BASE_URL}/qc/run/${runId}`, { method: 'DELETE' })
  await throwIfError(res, 'Delete failed')
  return res.json()
}
