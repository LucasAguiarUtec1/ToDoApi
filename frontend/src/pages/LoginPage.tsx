import { useState } from "react"
import { login } from "../api/auth"
import { useAppStore } from "../store/AppStore"

export default function LoginPage() {

    const { dispatch } = useAppStore()
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    async function handleSubmit(e: React.FormEvent) {
  e.preventDefault()
  setLoading(true)
  try {
    const res = await login({ email, password })
    setError(null)
    dispatch({
      type: 'LOGIN_SUCCESS',
      payload: {
        token: res.accessToken,
        user: res.user
      }
    })
    console.log('Login exitoso:', res)
  } catch {
    setError('Error al iniciar sesión. Verifica tus credenciales e intenta nuevamente.')
  } finally {
    setLoading(false)
  }
}

    return (
    <main className="flex items-center min-h-screen bg-slate-950 px-4">
      <section className="mx-auto w-full max-w-md rounded-xl border border-slate-800 bg-neutral-800 p-6 shadow-lg">
        <h1 className="text-center text-2xl font-bold text-slate-100">
          Iniciar sesión
        </h1>

        <form className="mt-6 space-y-4" onSubmit={e => handleSubmit(e)}>
          <div className="space-y-1">
            <label htmlFor="email" className="text-sm text-slate-200">
              Email
            </label>
            <input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-slate-100 outline-none focus:ring-2 focus:ring-cyan-400"
            />
          </div>

          <div className="space-y-1">
            <label htmlFor="password" className="text-sm text-slate-200">
              Contraseña
            </label>
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-slate-100 outline-none focus:ring-2 focus:ring-cyan-400"
            />
          </div>

          {error && <p className="text-sm text-red-400">{error}</p>}

          <button
            type="submit"
            disabled={loading || !email || !password}
            className="w-full rounded-md bg-cyan-500 px-4 py-2 font-medium text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? 'Ingresando...' : 'Iniciar sesión'}
          </button>
        </form>
      </section>
    </main>
  )
}