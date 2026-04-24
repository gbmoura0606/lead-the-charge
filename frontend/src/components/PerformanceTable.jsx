function Bar({ value }) {
  return (
    <div className="bar-wrap">
      <div className="bar" style={{ width: `${Math.max(value, 3)}%` }} />
      <span>{value}%</span>
    </div>
  )
}

export default function PerformanceTable({ title, rows, labelKey }) {
  return (
    <section className="panel">
      <h2>{title}</h2>
      <div className="table">
        {rows.map((row) => (
          <div key={row[labelKey]} className="table-row">
            <div>
              <p className="row-name">{row[labelKey]}</p>
              <p className="row-subtext">
                {row.games} games · KDA {row.average_kda}
              </p>
            </div>
            <Bar value={row.winrate} />
          </div>
        ))}
      </div>
    </section>
  )
}
