import { apiRequest } from './api';

export interface Notification {
    id: number;
    title: string;
    message: string;
    type: string;
    category: string;
    data: any;
    priority: string;
    read: boolean;
    created_at: string;
}

export interface NotificationListResponse {
    notifications: Notification[];
    unread_count: number;
}

export const fetchNotifications = async (limit: number = 20): Promise<NotificationListResponse> => {
    return await apiRequest<NotificationListResponse>(`/notifications?limit=${limit}`);
};

export const fetchUnreadNotifications = async (limit: number = 10): Promise<Notification[]> => {
    return await apiRequest<Notification[]>(`/notifications/unread?limit=${limit}`);
};

export const fetchUnreadCount = async (): Promise<number> => {
    const response = await apiRequest<{ count: number }>('/notifications/count');
    return response.count;
};

export const markAsRead = async (id: number): Promise<boolean> => {
    const response = await apiRequest<{ success: boolean }>(`/notifications/${id}/read`, {
        method: 'POST'
    });
    return response.success;
};

export const markAllAsRead = async (): Promise<number> => {
    const response = await apiRequest<{ success: boolean, count: number }>('/notifications/read-all', {
        method: 'POST'
    });
    return response.count;
};
