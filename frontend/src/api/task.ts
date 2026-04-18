import { apiRequest } from "./client";

export type Task = {
    id: number;
    name: string;
    completed: boolean;
    created_at: string;
    expires_in: string;
    user_id: number;
    expired: boolean;
}

export type PaginatedTasksResponse = {
    tasks: Task[];
    total: number;
    pages: number;
    current_page: number;
}

export const getTasks = (userId: number, token: string, page = 1, perPage = 10) =>
    apiRequest<PaginatedTasksResponse>(`/tasks/user/${userId}?page=${page}&per_page=${perPage}`, {
        method: 'GET',
        token
    })