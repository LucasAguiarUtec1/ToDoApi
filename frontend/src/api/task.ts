import { apiRequest } from "./client";

export type Task = {
    id: number;
    name: string;
    completed: boolean;
    createdAt: string;
    expiresIn: string;
}

export const getTasks = (token: string) =>
    apiRequest<Task[]>('/tasks', {
        method: 'GET',
        token
    })