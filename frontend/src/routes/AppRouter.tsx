// frontend/src/routes/AppRouter.tsx
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import ProtectedRoute from './ProtectedRoute'

// Pages (ajusta paths según tu estructura)
import LoginPage from '../pages/LoginPage'
import TasksPage from '../pages/TasksPage'
import NotFoundPage from '../pages/NotFoundPage'

function getToken() {
  return localStorage.getItem('access_token')
}

export default function AppRouter() {
  const isAuthenticated = Boolean(getToken())

  return (
    <BrowserRouter>
      <Routes>
        {/* pública */}
        <Route path="/login" element={<LoginPage />} />

        {/* protegidas */}
        <Route
          element={<ProtectedRoute isAuthenticated={isAuthenticated} />}
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
    </BrowserRouter>
  )
}
