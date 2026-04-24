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
        setStats(statsRes)
        setMatches(matchesRes.matches.slice(0, 8))
        setChampions(championsRes.champions)
      } catch (err) {
        setError(err.message)
      }
    }
    load()
  }, [api])

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
        <button className="btn" onClick={() => api.sync().then(() => window.location.reload())}>
          Sync latest
        </button>
      </div>
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
