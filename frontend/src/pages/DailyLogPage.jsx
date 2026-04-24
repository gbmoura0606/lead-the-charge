import { useEffect, useState } from 'react'

const initial = { date: '', games: 0, feeling: '', notes: '' }

export default function DailyLogPage({ api }) {
  const [form, setForm] = useState(initial)
  const [logs, setLogs] = useState([])

  async function load() {
    const res = await api.getDailyLogs()
    setLogs(res.dailyLogs)
  }

  useEffect(() => {
    load()
  }, [])

  async function submit(event) {
    event.preventDefault()
    await api.createDailyLog({ ...form, games: Number(form.games) })
    setForm(initial)
    load()
  }

  return (
    <div className="grid two-col">
      <section className="panel">
        <h2>Daily log</h2>
        <form className="stack" onSubmit={submit}>
          <input type="date" required value={form.date} onChange={(e) => setForm({ ...form, date: e.target.value })} />
          <input type="number" min="0" required placeholder="Number of games" value={form.games} onChange={(e) => setForm({ ...form, games: e.target.value })} />
          <input required placeholder="General feeling" value={form.feeling} onChange={(e) => setForm({ ...form, feeling: e.target.value })} />
          <textarea rows="5" placeholder="Notes" value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} />
          <button className="btn" type="submit">Save daily log</button>
        </form>
      </section>

      <section className="panel stack">
        <h2>History</h2>
        {logs.map((log) => (
          <article key={log.id} className="item-row stack-sm">
            <strong>{log.date} · {log.games} games</strong>
            <p>{log.feeling}</p>
            <p>{log.notes}</p>
          </article>
        ))}
      </section>
    </div>
  )
}
