/**
 * Throw an error with the backend's detail message if available,
 * otherwise fall back to a generic message with the HTTP status.
 */
export async function throwIfError(res, fallbackMsg) {
  if (res.ok) return
  const body = await res.json().catch(() => null)
  const detail = body?.detail
  if (typeof detail === 'string') {
    throw new Error(detail)
  }
  // FastAPI validation errors return detail as an array
  if (Array.isArray(detail) && detail.length > 0) {
    const msgs = detail.map(d => d.msg || JSON.stringify(d)).join('; ')
    throw new Error(msgs)
  }
  throw new Error(`${fallbackMsg}: ${res.status}`)
}
