import { createSlice, PayloadAction, createAsyncThunk } from '@reduxjs/toolkit';
import { Notification, fetchUnreadCount, fetchUnreadNotifications, markAsRead, markAllAsRead as apiMarkAllAsRead } from '@/lib/notificationApi';

interface NotificationState {
    notifications: Notification[];
    unreadCount: number;
    loading: boolean;
    error: string | null;
}

const initialState: NotificationState = {
    notifications: [],
    unreadCount: 0,
    loading: false,
    error: null,
};

export const fetchInitialNotifications = createAsyncThunk(
    'notifications/fetchInitial',
    async (_, { rejectWithValue }) => {
        try {
            const [unreadCount, notifications] = await Promise.all([
                fetchUnreadCount(),
                fetchUnreadNotifications(10)
            ]);
            return { unreadCount, notifications };
        } catch (error: any) {
            return rejectWithValue(error.message);
        }
    }
);

const notificationSlice = createSlice({
    name: 'notifications',
    initialState,
    reducers: {
        addNotification: (state, action: PayloadAction<Notification>) => {
            state.notifications = [action.payload, ...state.notifications].slice(0, 20);
            state.unreadCount += 1;
        },
        setUnreadCount: (state, action: PayloadAction<number>) => {
            state.unreadCount = action.payload;
        },
        markRead: (state, action: PayloadAction<number>) => {
            const notification = state.notifications.find(n => n.id === action.payload);
            if (notification && !notification.read) {
                notification.read = true;
                state.unreadCount = Math.max(0, state.unreadCount - 1);
            }
        },
        markAllRead: (state) => {
            state.notifications.forEach(n => { n.read = true; });
            state.unreadCount = 0;
        }
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchInitialNotifications.pending, (state) => {
                state.loading = true;
            })
            .addCase(fetchInitialNotifications.fulfilled, (state, action) => {
                state.loading = false;
                state.notifications = action.payload.notifications;
                state.unreadCount = action.payload.unreadCount;
            })
            .addCase(fetchInitialNotifications.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload as string;
            });
    }
});

export const { addNotification, setUnreadCount, markRead, markAllRead } = notificationSlice.actions;
export default notificationSlice.reducer;
