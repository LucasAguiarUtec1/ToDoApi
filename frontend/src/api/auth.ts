import { apiRequest } from "./client";

export type LoginRequest = {
    email: string
    password: string
}

export type LoginResponse = {
    access_token: string
    user: {
        id: number
        username: string
    }
}

export const login = (payload: LoginRequest) => 
    apiRequest<LoginResponse, LoginRequest>('/users/login', {
        method: 'POST',
        body: payload
    })