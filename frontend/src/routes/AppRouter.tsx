import { Navigate, Route, Routes } from 'react-router-dom'
import ProtectedRoute from './ProtectedRoute'
import { useAppStore } from '../store/AppStore'

import LoginPage from '../pages/LoginPage'
import TasksPage from '../pages/TasksPage'
import NotFoundPage from '../pages/NotFoundPage'

export default function AppRouter() {
  const {
    state: { token },
  } = useAppStore()

  const isAuthenticated = Boolean(token)

  return (
      <Routes>
        <Route path="/login" element={<LoginPage />} />

        {/* protegidas */}
        <Route
          element={<ProtectedRoute />}
        >
          <Route path="/tasks" element={<TasksPage />} />
        </Route>

        {/* home */}
        <Route
          path="/"
          element={
            <Navigate to={isAuthenticated ? '/tasks' : '/login'} replace />
          }
        />

        {/* 404 */}
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
  )
}
