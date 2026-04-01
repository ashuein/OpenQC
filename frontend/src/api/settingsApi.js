import { throwIfError } from './helpers'

const BASE_URL = 'http://localhost:8000'

export async function getApiKeyStatus() {
  const res = await fetch(`${BASE_URL}/settings/api-key/status`)
  await throwIfError(res, 'Failed to check API key status')
  return res.json()
}

export async function setApiKey(apiKey) {
  const res = await fetch(`${BASE_URL}/settings/api-key`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ api_key: apiKey }),
  })
  await throwIfError(res, 'Failed to save API key')
  return res.json()
}

export async function removeApiKey() {
  const res = await fetch(`${BASE_URL}/settings/api-key`, { method: 'DELETE' })
  await throwIfError(res, 'Failed to remove API key')
  return res.json()
}
