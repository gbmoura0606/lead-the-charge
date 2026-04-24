import { useEffect, useState } from 'react'

const defaultForm = {
  title: '',
  content: '',
  tags: '',
  match_id: '',
  champion: '',
  scope: 'general'
}

export default function NotesPage({ api }) {
  const [notes, setNotes] = useState([])
  const [form, setForm] = useState(defaultForm)

  async function loadNotes() {
    const response = await api.getNotes()
    setNotes(response.notes)
  }

  useEffect(() => {
    loadNotes()
  }, [])

  async function submit(event) {
    event.preventDefault()
    await api.createNote({
      ...form,
      tags: form.tags
        .split(',')
        .map((tag) => tag.trim())
        .filter(Boolean)
    })
    setForm(defaultForm)
    loadNotes()
  }

  return (
    <div className="grid two-col">
      <section className="panel">
        <h2>Create Note</h2>
        <form className="stack" onSubmit={submit}>
          <input required placeholder="Title" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} />
          <textarea required rows="6" placeholder="Content" value={form.content} onChange={(e) => setForm({ ...form, content: e.target.value })} />
          <input placeholder="Tags comma separated" value={form.tags} onChange={(e) => setForm({ ...form, tags: e.target.value })} />
          <input placeholder="Match ID (optional)" value={form.match_id} onChange={(e) => setForm({ ...form, match_id: e.target.value })} />
          <input placeholder="Champion (optional)" value={form.champion} onChange={(e) => setForm({ ...form, champion: e.target.value })} />
          <select value={form.scope} onChange={(e) => setForm({ ...form, scope: e.target.value })}>
            <option value="general">General</option>
            <option value="match">Match</option>
            <option value="champion">Champion</option>
          </select>
          <button className="btn" type="submit">Save note</button>
        </form>
      </section>

      <section className="panel stack">
        <h2>Notes</h2>
        {notes.map((note) => (
          <article key={note.id} className="item-row stack-sm">
            <strong>{note.title}</strong>
            <p>{note.content}</p>
            <small>{note.date}</small>
          </article>
        ))}
      </section>
    </div>
  )
}
