import { NavLink } from 'react-router-dom'

const links = [
  { to: '/', label: 'Dashboard' },
  { to: '/matches', label: 'Matches' },
  { to: '/notes', label: 'Notes' },
  { to: '/daily-log', label: 'Daily Log' }
]

export default function Layout({ children }) {
  return (
    <main className="container">
      <header className="topbar">
        <div>
          <p className="eyebrow">wave culture data workspace</p>
          <h1>Lead The Charge</h1>
        </div>
        <nav>
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}
            >
              {link.label}
            </NavLink>
          ))}
        </nav>
      </header>
      {children}
    </main>
  )
}
