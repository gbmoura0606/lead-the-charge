const configuredApiUrl = import.meta.env.VITE_API_URL?.trim()
const isBrowser = typeof window !== 'undefined'
const isLocalhost = isBrowser && ['localhost', '127.0.0.1'].includes(window.location.hostname)

const API_URL = configuredApiUrl || (isLocalhost ? 'http://localhost:8000' : '')

async function request(path) {
  const targetUrl = `${API_URL}${path}`
  const response = await fetch(targetUrl)

  if (!response.ok) {
    throw new Error(`Request failed (${response.status}) at ${targetUrl}`)
  }

  return response.json()
}

export function fetchStats() {
  return request('/stats')
}

export function fetchInsights() {
  return request('/insights')
}

export function getResolvedApiUrl() {
  return API_URL || '(same-origin)'
}
