// Backwards-compatible API helpers.
// New code should import from `src/api/client.js`.
import { api } from '../api/client'

export function fetchStats() {
  return api.getBasicStats()
}

export function fetchInsights() {
  // Insight endpoint was removed in favor of pure data exploration.
  return Promise.resolve({ insights: [] })
}

export function fetchMatches() {
  return api.getMatches()
}

export function fetchMatchById(id) {
  return api.getMatch(id)
}

export function getResolvedApiUrl() {
  return api.getApiUrl()
}
