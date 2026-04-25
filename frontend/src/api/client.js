const API_URL = 'http://localhost:8000'

async function request(path, options) {
  const requestUrl = `${API_URL}${path}`

  try {
    const response = await fetch(requestUrl, options)
    const payload = await response.json()

    console.log('[API] Response', {
      path,
      status: response.status,
      ok: response.ok,
      payload
    })

    if (!response.ok) {
      throw new Error(payload?.detail || `Request failed (${response.status}) for ${path}`)
    }

    return payload
  } catch (error) {
    console.error('[API] Request failed', {
      path,
      requestUrl,
      error: error instanceof Error ? error.message : String(error)
    })
    throw error
  }
}

export const api = {
  getApiUrl: () => API_URL,
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
