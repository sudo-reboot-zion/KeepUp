'use client';

import { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

interface Notification {
    id: number;
    type: string;
    title: string;
    message: string;
    created_at: string;
    is_read: boolean;
}

export default function NotificationBell() {
    const router = useRouter();
    const [showDropdown, setShowDropdown] = useState(false);
    const [notifications] = useState<Notification[]>([]);
    const dropdownRef = useRef<HTMLDivElement>(null);

    // Close dropdown when clicking outside
    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                setShowDropdown(false);
            }
        };

        if (showDropdown) {
            document.addEventListener('mousedown', handleClickOutside);
        }

        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [showDropdown]);



    const getNotificationIcon = (type: string): string => {
        const icons: Record<string, string> = {
            'milestone_achieved': '🏆',
            'partnership_created': '🤝',
            'new_message': '💬',
            'encouragement_received': '💪',
            'streak_reminder': '🔥',
            'group_milestone': '🎉',
        };
        return icons[type] || '📢';
    };

    const unreadCount = notifications.filter(n => !n.is_read).length;

    return (
        <div className="relative" ref={dropdownRef}>
            {/* Bell Icon Button */}
            <button
                onClick={() => setShowDropdown(!showDropdown)}
                className="relative p-2 rounded-full hover:bg-[var(--muted)] transition-colors"
                aria-label="Notifications"
            >
                {/* Bell Icon */}
                <svg
                    className="w-6 h-6 text-[var(--fg)] opacity-60 hover:opacity-100 transition-opacity"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
                    />
                </svg>

                {/* Unread Badge */}
                {unreadCount > 0 && (
                    <div className="absolute -top-1 -right-1 w-5 h-5 bg-[var(--secondary)] rounded-full flex items-center justify-center">
                        <span className="text-xs font-bold text-[var(--bg)]">{unreadCount > 9 ? '9+' : unreadCount}</span>
                    </div>
                )}
            </button>

            {/* Dropdown */}
            {showDropdown && (
                <div className="absolute right-0 mt-2 w-80 bg-[var(--card)] backdrop-blur-xl border border-[var(--border)] rounded-2xl shadow-2xl overflow-hidden z-50">
                    {/* Header */}
                    <div className="px-4 py-3 border-b border-[var(--border)] flex items-center justify-between">
                        <h3 className="font-bold text-[var(--fg)]">Notifications</h3>
                        {unreadCount > 0 && (
                            <span className="text-xs text-[var(--primary)]">{unreadCount} new</span>
                        )}
                    </div>

                    {/* Notifications List */}
                    <div className="max-h-96 overflow-y-auto">
                        {notifications.length === 0 ? (
                            <div className="px-4 py-8 text-center">
                                <div className="text-4xl mb-2">🔔</div>
                                <p className="text-sm text-[var(--fg)] opacity-60">No notifications yet</p>
                            </div>
                        ) : (
                            notifications.map((notification) => (
                                <div
                                    key={notification.id}
                                    className={`px-4 py-3 hover:bg-[var(--muted)] cursor-pointer transition-colors border-b border-[var(--border)] ${!notification.is_read ? 'bg-[var(--primary)]/5' : ''
                                        }`}
                                    onClick={() => {
                                        setShowDropdown(false);
                                        router.push('/notifications');
                                    }}
                                >
                                    <div className="flex items-start gap-3">
                                        <div className="text-2xl flex-shrink-0">{getNotificationIcon(notification.type)}</div>
                                        <div className="flex-1 min-w-0">
                                            <p className="font-medium text-sm text-[var(--fg)] truncate">{notification.title}</p>
                                            <p className="text-xs text-[var(--fg)] opacity-60 truncate mt-0.5">{notification.message}</p>
                                            <p className="text-xs text-[var(--fg)] opacity-40 mt-1">
                                                {new Date(notification.created_at).toLocaleTimeString([], {
                                                    hour: '2-digit',
                                                    minute: '2-digit',
                                                })}
                                            </p>
                                        </div>
                                        {!notification.is_read && (
                                            <div className="w-2 h-2 rounded-full bg-[var(--primary)] flex-shrink-0 mt-1" />
                                        )}
                                    </div>
                                </div>
                            ))
                        )}
                    </div>

                    {/* Footer */}
                    {notifications.length > 0 && (
                        <div className="px-4 py-3 border-t border-[var(--border)]">
                            <Link
                                href="/notifications"
                                onClick={() => setShowDropdown(false)}
                                className="block text-center text-sm text-[var(--primary)] hover:underline"
                            >
                                View all notifications
                            </Link>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
