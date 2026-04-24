import { useEffect, useState } from 'react'

import InsightsList from './components/InsightsList'
import PerformanceTable from './components/PerformanceTable'
import SummaryCards from './components/SummaryCards'
import { fetchInsights, fetchStats } from './services/api'

export default function App() {
  const [stats, setStats] = useState(null)
  const [insights, setInsights] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadDashboard() {
      try {
        const [statsData, insightsData] = await Promise.all([fetchStats(), fetchInsights()])
        setStats(statsData)
        setInsights(insightsData.insights)
      } catch (err) {
        setError('Unable to load dashboard data. Check if backend is running.')
      }
    }

    loadDashboard()
  }, [])

  return (
    <main className="container">
      <header>
        <p className="eyebrow">wave culture performance lab</p>
        <h1>Lead The Charge</h1>
      </header>

      {error && <p className="error">{error}</p>}

      {stats && (
        <>
          <SummaryCards summary={stats.summary} />
          <div className="split-grid">
            <PerformanceTable
              title="Champion Performance"
              rows={stats.champion_performance}
              labelKey="champion"
            />
            <PerformanceTable title="Role Performance" rows={stats.role_performance} labelKey="role" />
          </div>
          <InsightsList insights={insights} />
        </>
      )}
    </main>
  )
}
