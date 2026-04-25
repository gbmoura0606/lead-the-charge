import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'

export default function FundamentalDetailPage({ api }) {
  const { id } = useParams()
  const [fundamental, setFundamental] = useState(null)
  const [notes, setNotes] = useState([])
  const [text, setText] = useState('')

  async function load() {
    const [fundamentalResponse, notesResponse] = await Promise.all([
      api.getFundamental(id),
      api.getFundamentalNotes(id)
    ])
    setFundamental(fundamentalResponse)
    setNotes(notesResponse.notes)
  }

  useEffect(() => {
    load()
  }, [id])

  async function submit(event) {
    event.preventDefault()
    if (!text.trim()) return
    await api.createFundamentalNote(id, { text: text.trim() })
    setText('')
    load()
  }

  return (
    <section className="panel stack">
      <div className="stack-sm">
        <h2>{fundamental?.name || 'Fundamental'}</h2>
        <p className="label">{fundamental?.description || 'Use this page for fast free-form brainstorming notes.'}</p>
      </div>

      <form className="row" onSubmit={submit}>
        <input
          className="grow"
          placeholder="Quick thought, pattern, or reminder..."
          value={text}
          onChange={(event) => setText(event.target.value)}
        />
        <button className="btn" type="submit">Add note</button>
      </form>

      <div className="stack">
        {notes.map((note) => (
          <article key={note.id} className="item-row stack-sm">
            <p>{note.text}</p>
            <small>{note.created_at}</small>
          </article>
        ))}
        {!notes.length && <p className="label">No brainstorm notes yet.</p>}
      </div>
    </section>
  )
}
