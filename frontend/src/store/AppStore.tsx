import {
    createContext,
    useContext,
    useMemo,
    useReducer,
    type Dispatch,
    type ReactNode
} from 'react'

type AuthUser = {
    id: number,
    username: string
}

type AppState = {
    token: string | null,
    user: AuthUser | null,
    menuOpen: boolean
}

type AppAction = 
    | {type: 'LOGIN_SUCCESS'; payload: {token: string, user: AuthUser}}
    | {type: 'LOGOUT'}
    | {type: 'TOGGLE_MENU'}
    | {type: 'CLOSE_MENU'}

type AppStoreContextValue = {
    state: AppState
    dispatch: Dispatch<AppAction>
}

const TOKEN_STORAGE_KEY = 'access_token'
const USER_STORAGE_KEY = 'auth_user'

function loadInitialState(): AppState {
    const token = localStorage.getItem(TOKEN_STORAGE_KEY)
    const rawUser = localStorage.getItem(USER_STORAGE_KEY)

    let user: AuthUser | null = null
    if (rawUser) {
        try {
            user = JSON.parse(rawUser) as AuthUser
        } catch {
            localStorage.removeItem(USER_STORAGE_KEY)
        }
    }

    return {
        token,
        user,
        menuOpen: false
    }
}

function appReducer(state: AppState, action: AppAction): AppState {
    switch (action.type) {
        case 'LOGIN_SUCCESS': {
            localStorage.setItem(TOKEN_STORAGE_KEY, action.payload.token)
            localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(action.payload.user))
            return {
                ...state,
                token: action.payload.token,
                user: action.payload.user
            }
        }
            
        case 'LOGOUT': {
            localStorage.removeItem(TOKEN_STORAGE_KEY)
            localStorage.removeItem(USER_STORAGE_KEY)
            return {
                token: null,
                user: null,
                menuOpen: false
            }
        }
        
        case 'TOGGLE_MENU': {
            return {
                ...state,
                menuOpen: !state.menuOpen
            }
        }

        case 'CLOSE_MENU': {
            return {
                ...state,
                menuOpen: false
            }
        }

        default:
            return state
    }
}

const AppStoreContext = createContext<AppStoreContextValue | undefined>(undefined)

export function AppStoreProvider({children}: {children: ReactNode}) {
    const [state, dispatch] = useReducer(appReducer, undefined, loadInitialState)
    const value = useMemo(() => ({state, dispatch}), [state])

    return (<AppStoreContext.Provider value={value}>{children}</AppStoreContext.Provider>)
}

export function useAppStore() {
    const context = useContext(AppStoreContext)

    if (!context) {
        throw new Error('useAppStore debe usarse dentro de un AppStoreProvider')
    }
    return context
}