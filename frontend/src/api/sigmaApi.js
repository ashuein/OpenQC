const BASE_URL = 'http://localhost:8000'

export async function calculateSigma(sigmaInputs) {
  const res = await fetch(`${BASE_URL}/sigma/calculate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ inputs: sigmaInputs }),
  })
  if (!res.ok) throw new Error(`Sigma calculation failed: ${res.status}`)
  return res.json()
}

export async function fetchSigmaHistory(params = {}) {
  const query = new URLSearchParams(params).toString()
  const res = await fetch(`${BASE_URL}/sigma/history${query ? '?' + query : ''}`)
  if (!res.ok) throw new Error(`Fetch history failed: ${res.status}`)
  return res.json()
}
