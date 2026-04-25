import { useEffect, useState } from 'react'

import StatCards from '../components/StatCards'
import { SimpleBars } from '../components/SimpleBars'

export default function DashboardPage({ api }) {
  const [stats, setStats] = useState(null)
  const [matches, setMatches] = useState([])
  const [champions, setChampions] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    async function load() {
      try {
        const [statsRes, matchesRes, championsRes] = await Promise.all([
          api.getBasicStats(),
          api.getMatches(),
          api.getChampions()
        ])
        console.log('[Dashboard] Loaded initial data', { statsRes, matchesRes, championsRes })
        setStats(statsRes)
        setMatches(matchesRes.matches.slice(0, 8))
        setChampions(championsRes.champions)
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to load dashboard'
        console.error('[Dashboard] Failed to load data', err)
        setError(message)
      }
    }
    load()
  }, [api])

  async function testBackendConnection() {
    try {
      const response = await api.getMatches()
      console.log('[TEST] GET /matches success', response)
    } catch (err) {
      console.error('[TEST] GET /matches failed', err)
    }
  }

  if (error) {
    return <p className="error">{error}</p>
  }

  if (!stats) {
    return <p>Loading dashboard...</p>
  }

  return (
    <div className="stack-lg">
      <div className="row between">
        <h2>Data Dashboard</h2>
        <div className="row">
          <button className="btn" onClick={testBackendConnection}>Test backend connection</button>
          <button className="btn" onClick={() => api.sync().then(() => window.location.reload()).catch((err) => console.error('[Dashboard] Sync failed', err))}>
            Sync latest
          </button>
        </div>
      </div>
      <p className="label">API Base URL: {api.getApiUrl()}</p>
      <StatCards stats={stats} />

      <div className="grid two-col">
        <section className="panel">
          <h2>Recent Matches</h2>
          <div className="stack">
            {matches.map((match) => (
              <div key={match.id} className="row between item-row">
                <span>{match.champion || 'Unknown'} · {match.role || '-'}</span>
                <span className={match.win ? 'pill win' : 'pill loss'}>{match.win ? 'Win' : 'Loss'}</span>
              </div>
            ))}
          </div>
        </section>

        <SimpleBars title="Champion usage" data={champions} valueKey="games" labelKey="champion" />
      </div>
    </div>
  )
}
