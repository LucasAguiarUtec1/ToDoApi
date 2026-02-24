import { Navigate, Outlet, useLocation } from "react-router-dom";

type ProctectedRouteProps = {
    isAuthenticated: boolean
    redirectTo?: string
}

export default function ProtectedRoute({
    isAuthenticated,
    redirectTo = '/login'
}: ProctectedRouteProps) {
    const location = useLocation()
    if (!isAuthenticated) {
        return <Navigate to={redirectTo} replace state={{from: location}} />
    }

    return <Outlet/>
}