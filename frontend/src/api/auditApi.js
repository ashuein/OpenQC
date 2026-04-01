import { throwIfError } from './helpers'

const BASE_URL = 'http://localhost:8000'

export async function fetchAuditLog(params = {}) {
  const query = new URLSearchParams(params).toString()
  const res = await fetch(`${BASE_URL}/audit/log${query ? '?' + query : ''}`)
  await throwIfError(res, 'Fetch audit log failed')
  return res.json()
}

export async function verifyFileHash(fileHash) {
  const res = await fetch(`${BASE_URL}/audit/verify/${fileHash}`)
  await throwIfError(res, 'Verification failed')
  return res.json()
}

export async function verifyChain() {
  const res = await fetch(`${BASE_URL}/audit/chain-verify`)
  await throwIfError(res, 'Chain verification failed')
  return res.json()
}

export async function exportAuditLog(format = 'json') {
  const res = await fetch(`${BASE_URL}/audit/export?format=${format}`)
  await throwIfError(res, 'Export failed')
  if (format === 'pdf') return res.blob()
  return res.json()
}
