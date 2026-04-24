export function SimpleBars({ title, data, valueKey, labelKey }) {
  return (
    <section className="panel">
      <h2>{title}</h2>
      <div className="stack">
        {data.map((item) => (
          <div key={item[labelKey]} className="bar-row">
            <span>{item[labelKey]}</span>
            <div className="bar-shell">
              <div className="bar" style={{ width: `${Math.max(item[valueKey], 4)}%` }} />
            </div>
            <span>{item[valueKey]}</span>
          </div>
        ))}
      </div>
    </section>
  )
}
