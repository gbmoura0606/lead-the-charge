const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function request(path) {
  const response = await fetch(`${API_URL}${path}`)
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`)
  }
  return response.json()
}

export function fetchStats() {
  return request('/stats')
}

export function fetchInsights() {
  return request('/insights')
}
