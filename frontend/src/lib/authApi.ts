import { apiRequest, setAuthToken, clearAuthToken } from './api';

// Type Definitions
export interface RegisterData {
    username: string;
    email: string;
    password: string;
    display_name: string;
    bio?: string;
    age?: number;
    gender?: string;
    tracks_menstrual_cycle?: boolean;
}

export interface LoginData {
    email: string;
    password: string;
}

export interface AuthResponse {
    access_token: string;
    token_type: string;
}

export interface UserResponse {
    id: number;
    username: string;
    email: string;
    display_name: string;
    bio: string | null;
    age: number | null;
    gender: string | null;
    created_at: string;
    resolution?: string;
    occupation?: string;
    occupation_details?: {
        title: string;
        work_hours: number;
        stress_level: string;
    };
}

/**
 * Register a new user account
 */
export async function registerUser(userData: RegisterData): Promise<UserResponse> {
    const response = await apiRequest<UserResponse>('/auth/register', {
        method: 'POST',
        body: JSON.stringify(userData),
    });

    return response;
}

/**
 * Login with email and password
 */
export async function loginUser(credentials: LoginData): Promise<AuthResponse> {
    const response = await apiRequest<AuthResponse>('/auth/login', {
        method: 'POST',
        body: JSON.stringify(credentials),
    });

    // Store the token
    if (response.access_token) {
        setAuthToken(response.access_token);
    }

    return response;
}

/**
 * Logout the current user
 */
export async function logoutUser(): Promise<void> {
    try {
        await apiRequest('/auth/logout', {
            method: 'POST',
        });
    } finally {
        // Always clear token, even if request fails
        clearAuthToken();
    }
}

/**
 * Get current authenticated user info
 */
export async function getCurrentUser(): Promise<UserResponse> {
    const response = await apiRequest<UserResponse>('/auth/me', {
        method: 'GET',
    });

    return response;
}
