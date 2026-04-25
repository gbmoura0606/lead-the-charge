import { useEffect, useMemo, useRef, useState } from 'react'

const defaultVodForm = { title: '', video_path: '', session_name: 'Default Session' }
const defaultNoteForm = { text: '', fundamental_ids: [] }

function formatSeconds(totalSeconds) {
  const safe = Math.max(0, Math.floor(totalSeconds || 0))
  const hours = Math.floor(safe / 3600)
  const minutes = Math.floor((safe % 3600) / 60)
  const seconds = safe % 60
  if (hours > 0) {
    return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
  }
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
}

export default function VodReviewPage({ api }) {
  const playerRef = useRef(null)
  const [vods, setVods] = useState([])
  const [selectedVodId, setSelectedVodId] = useState('')
  const [vodNotes, setVodNotes] = useState([])
  const [fundamentals, setFundamentals] = useState([])
  const [vodForm, setVodForm] = useState(defaultVodForm)
  const [noteForm, setNoteForm] = useState(defaultNoteForm)
  const [currentTime, setCurrentTime] = useState(0)
  const [localVideoUrl, setLocalVideoUrl] = useState('')

  const selectedVod = useMemo(() => vods.find((vod) => vod.id === selectedVodId), [vods, selectedVodId])

  async function loadVods() {
    const response = await api.getVods()
    setVods(response.vods)
    if (!selectedVodId && response.vods.length) {
      setSelectedVodId(response.vods[0].id)
    }
  }

  async function loadFundamentals() {
    const response = await api.getFundamentals()
    setFundamentals(response.fundamentals)
  }

  async function loadVodNotes(vodId) {
    if (!vodId) {
      setVodNotes([])
      return
    }
    const response = await api.getVodNotes(vodId)
    setVodNotes(response.notes)
  }

  useEffect(() => {
    loadVods()
    loadFundamentals()
  }, [])

  useEffect(() => {
    loadVodNotes(selectedVodId)
    setCurrentTime(0)
  }, [selectedVodId])

  async function createVod(event) {
    event.preventDefault()
    const created = await api.createVod(vodForm)
    setVodForm(defaultVodForm)
    await loadVods()
    setSelectedVodId(created.id)
  }

  async function createTimestampNote(event) {
    event.preventDefault()
    if (!selectedVodId || !noteForm.text.trim()) {
      return
    }

    await api.createVodNote(selectedVodId, {
      timestamp_seconds: currentTime,
      text: noteForm.text.trim(),
      fundamental_ids: noteForm.fundamental_ids,
      screenshot_ref: null
    })

    setNoteForm(defaultNoteForm)
    await loadVodNotes(selectedVodId)
  }

  function toggleFundamental(fundamentalId) {
    setNoteForm((current) => {
      const exists = current.fundamental_ids.includes(fundamentalId)
      return {
        ...current,
        fundamental_ids: exists
          ? current.fundamental_ids.filter((item) => item !== fundamentalId)
          : [...current.fundamental_ids, fundamentalId]
      }
    })
  }

  function jumpTo(timestampSeconds) {
    if (!playerRef.current) return
    playerRef.current.currentTime = timestampSeconds
    playerRef.current.play()
  }

  const vodsBySession = useMemo(() => {
    return vods.reduce((groups, vod) => {
      const sessionName = vod.session_name || 'Default Session'
      groups[sessionName] = groups[sessionName] || []
      groups[sessionName].push(vod)
      return groups
    }, {})
  }, [vods])

  const videoSource = localVideoUrl || selectedVod?.video_path || ''

  return (
    <div className="grid stack-lg">
      <section className="panel">
        <h2>VOD Review Workspace</h2>
        <form className="grid filters" onSubmit={createVod}>
          <input required placeholder="VOD title" value={vodForm.title} onChange={(event) => setVodForm({ ...vodForm, title: event.target.value })} />
          <input required placeholder="Video path or URL" value={vodForm.video_path} onChange={(event) => setVodForm({ ...vodForm, video_path: event.target.value })} />
          <input placeholder="Session block" value={vodForm.session_name} onChange={(event) => setVodForm({ ...vodForm, session_name: event.target.value })} />
          <button className="btn" type="submit">Create VOD</button>
        </form>
      </section>

      <section className="grid two-col">
        <article className="panel stack">
          <div className="between row">
            <h2>Sessions & Games</h2>
            <span className="timestamp">Now: {formatSeconds(currentTime)}</span>
          </div>

          {Object.entries(vodsBySession).map(([sessionName, sessionVods]) => (
            <div key={sessionName} className="stack-sm">
              <strong>{sessionName}</strong>
              {sessionVods.map((vod) => (
                <button
                  type="button"
                  key={vod.id}
                  className={vod.id === selectedVodId ? 'btn btn-ghost active' : 'btn btn-ghost'}
                  onClick={() => {
                    setSelectedVodId(vod.id)
                    setLocalVideoUrl('')
                  }}
                >
                  {vod.title}
                </button>
              ))}
            </div>
          ))}
        </article>

        <article className="panel stack-lg">
          <div className="stack-sm">
            <h2>{selectedVod?.title || 'Select a VOD'}</h2>
            <small>{selectedVod?.video_path || 'No video selected yet.'}</small>
          </div>

          <input
            type="file"
            accept="video/*,.mkv"
            onChange={(event) => {
              const file = event.target.files?.[0]
              if (file) {
                setLocalVideoUrl(URL.createObjectURL(file))
              }
            }}
          />

          {videoSource ? (
            <video
              ref={playerRef}
              controls
              className="vod-player"
              src={videoSource}
              onTimeUpdate={(event) => setCurrentTime(event.currentTarget.currentTime)}
            />
          ) : (
            <p className="label">Attach a local video file or select a saved VOD with a valid video path.</p>
          )}

          <form className="stack" onSubmit={createTimestampNote}>
            <textarea
              rows="4"
              required
              placeholder="What happened here?"
              value={noteForm.text}
              onChange={(event) => setNoteForm({ ...noteForm, text: event.target.value })}
            />
            <div className="tag-grid">
              {fundamentals.map((fundamental) => (
                <button
                  key={fundamental.id}
                  type="button"
                  onClick={() => toggleFundamental(fundamental.id)}
                  className={noteForm.fundamental_ids.includes(fundamental.id) ? 'tag-chip active' : 'tag-chip'}
                >
                  {fundamental.name}
                </button>
              ))}
            </div>
            <button className="btn" type="submit" disabled={!selectedVodId}>Add note @ {formatSeconds(currentTime)}</button>
          </form>
        </article>
      </section>

      <section className="panel stack">
        <h2>Timestamp Notes</h2>
        {vodNotes.map((note) => (
          <article key={note.id} className="item-row stack-sm">
            <div className="between row">
              <button type="button" className="btn btn-ghost" onClick={() => jumpTo(note.timestamp_seconds)}>
                Jump to {formatSeconds(note.timestamp_seconds)}
              </button>
              <small>{note.created_at}</small>
            </div>
            <p>{note.text}</p>
            <div className="tag-row">
              {note.fundamental_ids?.map((fundamentalId) => {
                const fundamental = fundamentals.find((item) => item.id === fundamentalId)
                return (
                  <span key={fundamentalId} className="tag-chip small active">{fundamental?.name || 'Unknown'}</span>
                )
              })}
            </div>
          </article>
        ))}
        {!vodNotes.length && <p className="label">No notes yet for this VOD.</p>}
      </section>
    </div>
  )
}
