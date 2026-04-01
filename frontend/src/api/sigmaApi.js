import { throwIfError } from './helpers'

const BASE_URL = 'http://localhost:8000'

export async function calculateSigma(sigmaInputs) {
  const res = await fetch(`${BASE_URL}/sigma/calculate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ inputs: sigmaInputs }),
  })
  await throwIfError(res, 'Sigma calculation failed')
  return res.json()
}

export async function fetchSigmaHistory(params = {}) {
  const query = new URLSearchParams(params).toString()
  const res = await fetch(`${BASE_URL}/sigma/history${query ? '?' + query : ''}`)
  await throwIfError(res, 'Fetch history failed')
  return res.json()
}
