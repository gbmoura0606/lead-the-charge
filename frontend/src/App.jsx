import { Navigate, Route, Routes } from 'react-router-dom'

import { api } from './api/client'
import Layout from './components/Layout'
import DailyLogPage from './pages/DailyLogPage'
import DashboardPage from './pages/DashboardPage'
import MatchDetailPage from './pages/MatchDetailPage'
import MatchesPage from './pages/MatchesPage'
import NotesPage from './pages/NotesPage'

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<DashboardPage api={api} />} />
        <Route path="/matches" element={<MatchesPage api={api} />} />
        <Route path="/matches/:id" element={<MatchDetailPage api={api} />} />
        <Route path="/notes" element={<NotesPage api={api} />} />
        <Route path="/daily-log" element={<DailyLogPage api={api} />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  )
}
