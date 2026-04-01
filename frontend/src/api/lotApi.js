import { throwIfError } from './helpers'

const BASE_URL = 'http://localhost:8000'

export async function fetchReagentLots() {
  const res = await fetch(`${BASE_URL}/lots/reagents`)
  await throwIfError(res, 'Fetch reagent lots failed')
  return res.json()
}

export async function createReagentLot(lotData) {
  const res = await fetch(`${BASE_URL}/lots/reagents`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(lotData),
  })
  await throwIfError(res, 'Create reagent lot failed')
  return res.json()
}

export async function fetchControlLots() {
  const res = await fetch(`${BASE_URL}/lots/controls`)
  await throwIfError(res, 'Fetch control lots failed')
  return res.json()
}

export async function createControlLot(lotData) {
  const res = await fetch(`${BASE_URL}/lots/controls`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(lotData),
  })
  await throwIfError(res, 'Create control lot failed')
  return res.json()
}
