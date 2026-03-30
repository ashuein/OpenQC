const BASE_URL = 'http://localhost:8000'

export async function getApiKeyStatus() {
  const res = await fetch(`${BASE_URL}/settings/api-key/status`)
  if (!res.ok) throw new Error(`Failed to check API key status: ${res.status}`)
  return res.json()
}

export async function setApiKey(apiKey) {
  const res = await fetch(`${BASE_URL}/settings/api-key`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ api_key: apiKey }),
  })
  if (!res.ok) throw new Error(`Failed to save API key: ${res.status}`)
  return res.json()
}

export async function removeApiKey() {
  const res = await fetch(`${BASE_URL}/settings/api-key`, { method: 'DELETE' })
  if (!res.ok) throw new Error(`Failed to remove API key: ${res.status}`)
  return res.json()
}
