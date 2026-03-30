const BASE_URL = 'http://localhost:8000'

export async function fetchReagentLots() {
  const res = await fetch(`${BASE_URL}/lots/reagents`)
  if (!res.ok) throw new Error(`Fetch reagent lots failed: ${res.status}`)
  return res.json()
}

export async function createReagentLot(lotData) {
  const res = await fetch(`${BASE_URL}/lots/reagents`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(lotData),
  })
  if (!res.ok) throw new Error(`Create reagent lot failed: ${res.status}`)
  return res.json()
}

export async function fetchControlLots() {
  const res = await fetch(`${BASE_URL}/lots/controls`)
  if (!res.ok) throw new Error(`Fetch control lots failed: ${res.status}`)
  return res.json()
}

export async function createControlLot(lotData) {
  const res = await fetch(`${BASE_URL}/lots/controls`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(lotData),
  })
  if (!res.ok) throw new Error(`Create control lot failed: ${res.status}`)
  return res.json()
}
