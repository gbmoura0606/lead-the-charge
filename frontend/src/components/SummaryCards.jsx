export default function SummaryCards({ summary }) {
  const cards = [
    { label: 'Winrate', value: `${summary.winrate}%` },
    { label: 'Average KDA', value: summary.average_kda },
    { label: 'Total Games', value: summary.total_games },
    { label: 'W / L', value: `${summary.wins} / ${summary.losses}` }
  ]

  return (
    <section className="card-grid">
      {cards.map((card) => (
        <article key={card.label} className="panel">
          <p className="label">{card.label}</p>
          <p className="value">{card.value}</p>
        </article>
      ))}
    </section>
  )
}
