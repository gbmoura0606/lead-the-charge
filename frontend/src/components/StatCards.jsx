export default function StatCards({ stats }) {
  const cards = [
    { label: 'Total Games', value: stats.totalGames },
    { label: 'Winrate', value: `${stats.winrate}%` },
    { label: 'Average KDA', value: stats.averageKda },
    { label: 'W / L', value: `${stats.wins} / ${stats.losses}` }
  ]

  return (
    <section className="grid cards">
      {cards.map((card) => (
        <article key={card.label} className="panel">
          <p className="label">{card.label}</p>
          <p className="value">{card.value}</p>
        </article>
      ))}
    </section>
  )
}
