import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './styles/index.css'
import AppRouter from './routes/AppRouter.tsx'
import Navbar from './components/Navbar.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Navbar/>
      <AppRouter/>
  </StrictMode>,
)
