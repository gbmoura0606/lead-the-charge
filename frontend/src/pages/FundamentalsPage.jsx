import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

const defaultForm = { name: '', description: '' }

export default function FundamentalsPage({ api }) {
  const [fundamentals, setFundamentals] = useState([])
  const [form, setForm] = useState(defaultForm)

  async function loadFundamentals() {
    const response = await api.getFundamentals()
    setFundamentals(response.fundamentals)
  }

  useEffect(() => {
    loadFundamentals()
  }, [])

  async function submit(event) {
    event.preventDefault()
    await api.createFundamental(form)
    setForm(defaultForm)
    loadFundamentals()
  }

  return (
    <div className="grid two-col">
      <section className="panel stack">
        <h2>Add Fundamental</h2>
        <form className="stack" onSubmit={submit}>
          <input required placeholder="Name" value={form.name} onChange={(event) => setForm({ ...form, name: event.target.value })} />
          <textarea rows="4" placeholder="Description (optional)" value={form.description} onChange={(event) => setForm({ ...form, description: event.target.value })} />
          <button className="btn" type="submit">Create</button>
        </form>
      </section>

      <section className="panel stack">
        <h2>Fundamentals</h2>
        {fundamentals.map((fundamental) => (
          <Link key={fundamental.id} to={`/fundamentals/${fundamental.id}`} className="item-row stack-sm link-row">
            <strong>{fundamental.name}</strong>
            <small>{fundamental.description || 'No description yet.'}</small>
          </Link>
        ))}
      </section>
    </div>
  )
}
