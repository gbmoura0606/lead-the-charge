const configuredApiUrl = import.meta.env.VITE_API_URL?.trim()
const isBrowser = typeof window !== 'undefined'
const isLocalhost = isBrowser && ['localhost', '127.0.0.1'].includes(window.location.hostname)

const API_URL = configuredApiUrl || (isLocalhost ? 'http://localhost:8000' : '')

async function request(path, options) {
  const response = await fetch(`${API_URL}${path}`, options)
  if (!response.ok) {
    throw new Error(`Request failed (${response.status}) for ${path}`)
  }
  return response.json()
}

export const api = {
  getApiUrl: () => API_URL || '(same-origin)',
  sync: () => request('/sync'),
  getMatches: () => request('/matches'),
  getMatch: (id) => request(`/matches/${id}`),
  getBasicStats: () => request('/stats/basic'),
  getChampions: () => request('/champions'),
  getNotes: () => request('/notes'),
  getNote: (id) => request(`/notes/${id}`),
  createNote: (payload) =>
    request('/notes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }),
  updateNote: (id, payload) =>
    request(`/notes/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }),
  getDailyLogs: () => request('/daily-logs'),
  createDailyLog: (payload) =>
    request('/daily-logs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }),
  getVods: () => request('/vods'),
  createVod: (payload) =>
    request('/vod', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }),
  getVodNotes: (id) => request(`/vod/${id}/notes`),
  createVodNote: (id, payload) =>
    request(`/vod/${id}/notes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }),
  getFundamentals: () => request('/fundamentals'),
  getFundamental: (id) => request(`/fundamentals/${id}`),
  createFundamental: (payload) =>
    request('/fundamentals', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }),
  getFundamentalNotes: (id) => request(`/fundamentals/${id}/notes`),
  createFundamentalNote: (id, payload) =>
    request(`/fundamentals/${id}/notes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

}
