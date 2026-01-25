'use client';

import React from 'react';
import {
    LayoutDashboard,
    Calendar,
    BarChart3,
    Settings,
    LogOut,
    ChevronRight,
    User,
    History
} from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

const navItems = [
    { icon: LayoutDashboard, label: 'Dashboard', href: '/dashboard', active: true },
    { icon: Calendar, label: 'Schedules', href: '#', active: false },
    { icon: BarChart3, label: 'Analytics', href: '#', active: false },
    { icon: History, label: 'History', href: '#', active: false },
    { icon: User, label: 'Profile', href: '/profile', active: false },
    { icon: Settings, label: 'Settings', href: '#', active: false },
];

/**
 * AppSidebar - Primary navigation sidebar for the application.
 * High-contrast, Solana-inspired aesthetic.
 */
export default function AppSidebar() {
    const pathname = usePathname();

    return (
        <aside className="w-64 h-screen bg-background border-r border-border flex flex-col z-50 transition-colors duration-300">
            {/* Logo Section */}
            <div className="p-8 border-b border-border">
                <Link href="/" className="flex items-center gap-3">
                    <img
                        src="/assets/images/keep-up-fixed.svg"
                        alt="Keep Up Logo"
                        className="w-44 h-auto object-contain nav-logo transition-all duration-300"
                    />
                </Link>
            </div>

            {/* Navigation Links */}
            <nav className="flex-1 py-8 px-4 space-y-2">
                <p className="text-[10px] font-bold text-muted-foreground uppercase tracking-[0.2em] px-4 mb-4">
                    Protocol Menu
                </p>
                {navItems.map((item) => {
                    const isActive = item.active || pathname === item.href;
                    return (
                        <Link
                            key={item.label}
                            href={item.href}
                            className={`flex items-center justify-between px-4 py-3 rounded transition-all group ${isActive
                                ? 'bg-primary/10 text-primary border border-primary/20'
                                : 'text-muted-foreground hover:text-foreground hover:bg-foreground/5'
                                }`}
                        >
                            <div className="flex items-center gap-3">
                                <item.icon size={18} className={isActive ? 'text-primary' : 'text-muted-foreground group-hover:text-foreground'} />
                                <span className="text-sm font-bold uppercase tracking-widest">{item.label}</span>
                            </div>
                            {isActive && <div className="w-1 h-4 bg-primary rounded-full" />}
                            {!isActive && <ChevronRight size={14} className="opacity-0 group-hover:opacity-100 transition-opacity" />}
                        </Link>
                    );
                })}
            </nav>

            {/* Footer / User Actions */}
            <div className="p-4 border-t border-border">
                <button className="w-full flex items-center gap-3 px-4 py-3 text-muted-foreground hover:text-red-500 hover:bg-red-500/5 rounded transition-all group">
                    <LogOut size={18} className="group-hover:text-red-500" />
                    <span className="text-sm font-bold uppercase tracking-widest">Terminate Session</span>
                </button>
            </div>
        </aside>
    );
}
