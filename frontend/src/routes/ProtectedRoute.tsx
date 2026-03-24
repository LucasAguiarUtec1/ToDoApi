import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAppStore } from "../store/AppStore";

export default function ProtectedRoute({
    redirectTo = '/login'
}: {redirectTo? : string}) {
    const {state: { token }} = useAppStore()
    const isAuthenticated = Boolean(token)
    const location = useLocation()
    if (!isAuthenticated) {
        return <Navigate to={redirectTo} replace state={{from: location}} />
    }

    return <Outlet/>
}