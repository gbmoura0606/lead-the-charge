import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'

export default function MatchDetailPage({ api }) {
  const { id } = useParams()
  const [match, setMatch] = useState(null)

  useEffect(() => {
    api.getMatch(id).then(setMatch)
  }, [api, id])

  if (!match) {
    return <p>Loading match detail...</p>
  }

  return (
    <div className="stack-lg">
      <h2>Match {id}</h2>
      <section className="panel">
        <h3>Raw match payload</h3>
        <pre className="raw-block">{JSON.stringify(match, null, 2)}</pre>
      </section>
    </div>
  )
}
