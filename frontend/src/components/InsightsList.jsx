export default function InsightsList({ insights }) {
  return (
    <section className="panel">
      <h2>Insights</h2>
      <ul className="insights-list">
        {insights.map((insight) => (
          <li key={insight}>{insight}</li>
        ))}
      </ul>
    </section>
  )
}
