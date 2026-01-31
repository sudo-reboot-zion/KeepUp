import { useEffect, useCallback } from 'react';
import { io, Socket } from 'socket.io-client';
import { useAppDispatch, useAppSelector } from '@/redux/hooks';
import {
    addNotification,
    setUnreadCount,
    fetchInitialNotifications,
    markAllRead
} from '@/redux/slices/notificationSlice';

let socket: Socket | null = null;

export const useNotifications = () => {
    const dispatch = useAppDispatch();
    const { user, token } = useAppSelector(state => state.auth);
    const { notifications, unreadCount, loading } = useAppSelector(state => state.notifications);

    const markAllReadCallback = useCallback(() => {
        dispatch(markAllRead());
    }, [dispatch]);

    useEffect(() => {
        if (!user || !token) return;

        // Fetch initial state
        dispatch(fetchInitialNotifications());

        // Initialize Socket.IO
        let socketUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        // If the URL ends with /api, strip it for the socket connection
        if (socketUrl.endsWith('/api')) {
            socketUrl = socketUrl.slice(0, -4);
        }

        socket = io(socketUrl, {
            path: '/socket.io',
            auth: { token }
        });

        socket.on('connected', (data) => {
            console.log('✅ Connected to real-time system:', data);
        });

        socket.on('notification', (notification) => {
            console.log('📢 New notification received:', notification);
            dispatch(addNotification(notification));
        });

        socket.on('notification_count', (data) => {
            console.log('🔢 Notification count update:', data);
            dispatch(setUnreadCount(data.count));
        });

        socket.on('connect_error', (error) => {
            console.error('❌ Socket connection error:', error);
        });

        return () => {
            if (socket) {
                socket.disconnect();
                socket = null;
            }
        };
    }, [user, token, dispatch]);

    return {
        notifications,
        unreadCount,
        loading,
        markAllRead: markAllReadCallback
    };
};
