import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import {
    loginUser,
    registerUser,
    logoutUser,
    getCurrentUser,
    type LoginData,
    type RegisterData,
    type UserResponse
} from '@/lib/authApi';
import { clearAuthToken } from '@/lib/api';

interface User {
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

interface AuthState {
    user: User | null;
    token: string | null;
    isLoggedIn: boolean;
    isLoading: boolean;
    error: string | null;
}

const initialState: AuthState = {
    user: null,
    token: null,
    isLoggedIn: false,
    isLoading: false,
    error: null,
};

// Async Thunks

/**
 * Login user with email and password
 */
export const loginAsync = createAsyncThunk(
    'auth/login',
    async (credentials: LoginData, { rejectWithValue }) => {
        try {
            const authResponse = await loginUser(credentials);
            // Fetch user data after successful login
            const user = await getCurrentUser();
            return { user, token: authResponse.access_token };
        } catch (error: unknown) {
            return rejectWithValue((error as Error).message || 'Login failed');
        }
    }
);

/**
 * Register new user account
 */
export const registerAsync = createAsyncThunk(
    'auth/register',
    async (userData: RegisterData, { rejectWithValue }) => {
        try {
            const user = await registerUser(userData);
            // After registration, login to get token
            const authResponse = await loginUser({
                email: userData.email,
                password: userData.password,
            });
            return { user, token: authResponse.access_token };
        } catch (error: unknown) {
            return rejectWithValue((error as Error).message || 'Registration failed');
        }
    }
);

/**
 * Logout current user
 */
export const logoutAsync = createAsyncThunk(
    'auth/logout',
    async (_, { rejectWithValue }) => {
        try {
            await logoutUser();
            return;
        } catch (error: unknown) {
            // Still clear local state even if API call fails
            clearAuthToken();
            return rejectWithValue((error as Error).message || 'Logout failed');
        }
    }
);

/**
 * Check authentication status on app load
 */
export const checkAuthAsync = createAsyncThunk(
    'auth/checkAuth',
    async (_, { rejectWithValue }) => {
        try {
            // Try to get current user with stored token
            const user = await getCurrentUser();
            const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
            return { user, token };
        } catch (error: unknown) {
            // Token invalid or expired, clear it
            clearAuthToken();
            return rejectWithValue((error as Error).message || 'Authentication check failed');
        }
    }
);

// Slice

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        setLoading: (state, action: PayloadAction<boolean>) => {
            state.isLoading = action.payload;
        },
        setCredentials: (state, action: PayloadAction<{ user: UserResponse; token: string }>) => {
            state.user = action.payload.user;
            state.token = action.payload.token;
            state.isLoggedIn = true;
            state.error = null;
        },
        logout: (state) => {
            state.user = null;
            state.token = null;
            state.isLoggedIn = false;
            state.error = null;
            clearAuthToken();
        },
        setError: (state, action: PayloadAction<string | null>) => {
            state.error = action.payload;
        },
        clearError: (state) => {
            state.error = null;
        },
    },
    extraReducers: (builder) => {
        // Login
        builder
            .addCase(loginAsync.pending, (state) => {
                state.isLoading = true;
                state.error = null;
            })
            .addCase(loginAsync.fulfilled, (state, action) => {
                state.isLoading = false;
                state.user = action.payload.user;
                state.token = action.payload.token;
                state.isLoggedIn = true;
                state.error = null;
            })
            .addCase(loginAsync.rejected, (state, action) => {
                state.isLoading = false;
                state.error = action.payload as string;
            });

        // Register
        builder
            .addCase(registerAsync.pending, (state) => {
                state.isLoading = true;
                state.error = null;
            })
            .addCase(registerAsync.fulfilled, (state, action) => {
                state.isLoading = false;
                state.user = action.payload.user;
                state.token = action.payload.token;
                state.isLoggedIn = true;
                state.error = null;
            })
            .addCase(registerAsync.rejected, (state, action) => {
                state.isLoading = false;
                state.error = action.payload as string;
            });

        // Logout
        builder
            .addCase(logoutAsync.pending, (state) => {
                state.isLoading = true;
            })
            .addCase(logoutAsync.fulfilled, (state) => {
                state.isLoading = false;
                state.user = null;
                state.token = null;
                state.isLoggedIn = false;
                state.error = null;
            })
            .addCase(logoutAsync.rejected, (state) => {
                // Still clear state even on error
                state.isLoading = false;
                state.user = null;
                state.token = null;
                state.isLoggedIn = false;
            });

        // Check Auth
        builder
            .addCase(checkAuthAsync.pending, (state) => {
                state.isLoading = true;
            })
            .addCase(checkAuthAsync.fulfilled, (state, action) => {
                state.isLoading = false;
                state.user = action.payload.user;
                state.token = action.payload.token;
                state.isLoggedIn = true;
                state.error = null;
            })
            .addCase(checkAuthAsync.rejected, (state) => {
                state.isLoading = false;
                state.user = null;
                state.token = null;
                state.isLoggedIn = false;
            });
    },
});

export const { setLoading, setCredentials, logout, setError, clearError } = authSlice.actions;
export default authSlice.reducer;
