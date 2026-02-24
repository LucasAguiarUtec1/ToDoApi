export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE'

export class ApiError extends Error {
    status: number
    details?: unknown

    constructor(message: string, status: number, details?: unknown) {
        super(message)
        this.name = 'ApiError'
        this.status = status
        this.details = details
    }
}

type RequestOptions<TBody> = {
    method?: HttpMethod
    body?: TBody
    token?: string
    headers?: Record<string, string>
    signal?: AbortSignal
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api'

export async function apiRequest<TResponse, TBody = unknown>(
  path: string,
  options: RequestOptions<TBody> = {}
): Promise<TResponse> {
  const { method = 'GET', body, token, headers, signal } = options

const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    signal,
    headers: {
        'Content-Type': 'application/json',
        ...(token ? {Authorization: `Bearer ${token}`} : {}),
        ...headers,
    },
    body: body !== undefined ? JSON.stringify(body) : undefined
})

const contentType = response.headers.get('content-type') ?? ''
const isJson = contentType.includes('application/json')
const data = isJson ? await response.json() : await response.text()

if (!response.ok) {
    const message = 
    typeof data === 'object' && data && 'msg' in data
    ? String((data as {msg?: string}).msg)
    : `HTTP ${response.status}`
    throw new ApiError(message, response.status, data)
}

return data as TResponse
}