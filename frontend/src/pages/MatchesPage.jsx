import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

export default function MatchesPage({ api }) {
  const [rows, setRows] = useState([])
  const [filters, setFilters] = useState({ champion: '', result: '', role: '' })

  useEffect(() => {
    api.getMatches().then((res) => setRows(res.matches))
  }, [api])

  const champions = useMemo(() => [...new Set(rows.map((row) => row.champion).filter(Boolean))], [rows])
  const roles = useMemo(() => [...new Set(rows.map((row) => row.role).filter(Boolean))], [rows])

  const filteredRows = rows.filter((row) => {
    if (filters.champion && row.champion !== filters.champion) return false
    if (filters.role && row.role !== filters.role) return false
    if (filters.result === 'win' && !row.win) return false
    if (filters.result === 'loss' && row.win) return false
    return true
  })

  return (
    <div className="stack-lg">
      <h2>Matches</h2>
      <section className="panel grid filters">
        <select value={filters.champion} onChange={(e) => setFilters((old) => ({ ...old, champion: e.target.value }))}>
          <option value="">All champions</option>
          {champions.map((champion) => (
            <option key={champion} value={champion}>{champion}</option>
          ))}
        </select>

        <select value={filters.role} onChange={(e) => setFilters((old) => ({ ...old, role: e.target.value }))}>
          <option value="">All roles</option>
          {roles.map((role) => (
            <option key={role} value={role}>{role}</option>
          ))}
        </select>

        <select value={filters.result} onChange={(e) => setFilters((old) => ({ ...old, result: e.target.value }))}>
          <option value="">All results</option>
          <option value="win">Win</option>
          <option value="loss">Loss</option>
        </select>
      </section>

      <section className="panel table">
        {filteredRows.map((row) => (
          <Link to={`/matches/${row.id}`} className="table-row link-row" key={row.id}>
            <span>{row.champion || 'Unknown'}</span>
            <span>{row.role || '-'}</span>
            <span>{row.kills}/{row.deaths}/{row.assists}</span>
            <span className={row.win ? 'pill win' : 'pill loss'}>{row.win ? 'Win' : 'Loss'}</span>
          </Link>
        ))}
      </section>
    </div>
  )
}
