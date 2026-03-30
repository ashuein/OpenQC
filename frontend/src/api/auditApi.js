const BASE_URL = 'http://localhost:8000'

export async function fetchAuditLog(params = {}) {
  const query = new URLSearchParams(params).toString()
  const res = await fetch(`${BASE_URL}/audit/log${query ? '?' + query : ''}`)
  if (!res.ok) throw new Error(`Fetch audit log failed: ${res.status}`)
  return res.json()
}

export async function verifyFileHash(fileHash) {
  const res = await fetch(`${BASE_URL}/audit/verify/${fileHash}`)
  if (!res.ok) throw new Error(`Verification failed: ${res.status}`)
  return res.json()
}

export async function verifyChain() {
  const res = await fetch(`${BASE_URL}/audit/chain-verify`)
  if (!res.ok) throw new Error(`Chain verification failed: ${res.status}`)
  return res.json()
}

export async function exportAuditLog(format = 'json') {
  const res = await fetch(`${BASE_URL}/audit/export?format=${format}`)
  if (!res.ok) throw new Error(`Export failed: ${res.status}`)
  if (format === 'pdf') return res.blob()
  return res.json()
}
