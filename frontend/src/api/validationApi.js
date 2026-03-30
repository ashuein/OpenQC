const BASE_URL = 'http://localhost:8000'

export async function uploadValidationFile(file, validationType) {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('validation_type', validationType)
  const res = await fetch(`${BASE_URL}/validation/upload`, { method: 'POST', body: formData })
  if (!res.ok) throw new Error(`Upload failed: ${res.status}`)
  return res.json()
}

export async function runValidation(datasetId, acceptanceCriteria) {
  const res = await fetch(`${BASE_URL}/validation/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ dataset_id: datasetId, acceptance_criteria: acceptanceCriteria }),
  })
  if (!res.ok) throw new Error(`Validation failed: ${res.status}`)
  return res.json()
}

export async function fetchValidationReport(validationId) {
  const res = await fetch(`${BASE_URL}/validation/report/${validationId}`)
  if (!res.ok) throw new Error(`Fetch report failed: ${res.status}`)
  return res.json()
}
