import { useState } from 'react'
import logo from '../assets/logo-iremember.svg'

const links = ['Salir']

export default function Navbar() {
  const [open, setOpen] = useState(false)
  const userName = 'Lucas'

  return (
    <nav className="fixed start-0 top-0 z-20 w-full rounded-b-lg bg-slate-950">
      <div className="mx-auto flex items-center justify-between gap-3 p-4">
        <a href="#" className="flex items-center shrink-0">
          <img src={logo} className="h-10" alt="IRemember Logo" />
        </a>

        <span className="hidden sm:block text-slate-100 text-sm md:text-base lg:text-lg font-medium truncate max-w-[9rem] md:max-w-[12rem] lg:max-w-none">
          Bienvenido {userName}
        </span>

        <button
          type="button"
          onClick={() => setOpen((v) => !v)}
          className="inline-flex h-10 w-10 items-center justify-center rounded-md p-2 text-slate-200 hover:bg-slate-800 md:hidden"
          aria-controls="navbar-default"
          aria-expanded={open}
          aria-label="Open main menu"
        >
          <svg
            className="h-6 w-6"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <path
              stroke="currentColor"
              strokeLinecap="round"
              strokeWidth={2}
              d="M5 7h14M5 12h14M5 17h14"
            />
          </svg>
        </button>

        <div
          id="navbar-default"
          className={`${open ? 'block' : 'hidden'} w-full md:block md:w-auto`}
        >
          <ul className="mt-4 flex flex-col gap-1 rounded-lg border border-slate-800 bg-slate-900 p-4 text-sm md:mt-0 md:flex-row md:items-center md:gap-6 md:border-0 md:bg-transparent md:p-0">
            {links.map((item) => (
              <li key={item}>
                <a
                  href="#"
                  onClick={() => setOpen(false)}
                  className="block rounded px-3 py-2 text-slate-100 hover:bg-slate-800 md:px-0 md:py-0 md:hover:bg-transparent md:hover:text-cyan-400"
                >
                  {item}
                </a>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </nav>
  )
}