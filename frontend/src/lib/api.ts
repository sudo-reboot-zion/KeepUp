// API Configuration and Base Client
export const API_BASE_URL = 'http://localhost:8000/api';

/**
 * Get authentication token from localStorage
 */
const getAuthToken = (): string | null => {
    if (typeof window !== 'undefined') {
        return localStorage.getItem('token');
    }
    return null;
};

/**
 * API Error class for structured error handling
 */
export class ApiError extends Error {
    constructor(
        public status: number,
        public message: string,
        public detail?: string
    ) {
        super(message);
        this.name = 'ApiError';
    }
}

/**
 * Handle API error responses
 */
export function handleApiError(response: Response): ApiError {
    let errorMessage = 'An error occurred';
    const errorDetail = '';

    try {
        // This will be handled in the calling code after parsing JSON
        errorMessage = response.statusText;
    } catch {
        errorMessage = response.statusText;
    }

    return new ApiError(response.status, errorMessage, errorDetail);
}

/**
 * Generic API request wrapper with auth token injection
 */
export async function apiRequest<T>(
    endpoint: string,
    options: RequestInit = {}
): Promise<T> {
    const token = getAuthToken();

    const headers: Record<string, string> = {
        'Content-Type': 'application/json',
    };

    // Merge any existing headers
    if (options.headers) {
        const existingHeaders = new Headers(options.headers);
        existingHeaders.forEach((value, key) => {
            headers[key] = value;
        });
    }

    // Add auth token if available
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const config: RequestInit = {
        ...options,
        headers,
    };

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

        // Handle non-OK responses
        if (!response.ok) {
            let errorMessage = 'An error occurred';
            let errorDetail = '';

            try {
                const errorData = await response.json();
                errorMessage = errorData.message || errorData.detail || errorMessage;
                errorDetail = errorData.detail || '';
            } catch {
                // If error response is not JSON, use status text
                errorMessage = response.statusText;
            }

            throw new ApiError(response.status, errorMessage, errorDetail);
        }

        // Handle empty responses (204 No Content)
        if (response.status === 204) {
            return {} as T;
        }

        // Parse and return JSON response
        const data = await response.json();
        return data as T;
    } catch (error) {
        if (error instanceof ApiError) {
            throw error;
        }

        // Network or other errors
        throw new ApiError(
            0,
            'Network error. Please check your connection.',
            error instanceof Error ? error.message : 'Unknown error'
        );
    }
}

/**
 * Store authentication token
 */
export function setAuthToken(token: string): void {
    if (typeof window !== 'undefined') {
        localStorage.setItem('token', token);
    }
}

/**
 * Remove authentication token
 */
export function clearAuthToken(): void {
    if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
    }
}

