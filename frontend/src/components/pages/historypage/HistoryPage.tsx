'use client';

import React, { useEffect, useState } from 'react';
import {
    Mail,
    Search,
    Filter,
    Clock,
    Zap,
    Shield,
    Activity,
    Bell,
    Star,
    MoreVertical,
    CheckCircle2
} from 'lucide-react';
import Link from 'next/link';
import AppSidebar from '@/components/layout/AppSidebar';
import TopBar from '@/components/layout/TopBar';
import { useNotifications } from '@/hooks/useNotifications';
import { useAppDispatch } from '@/redux/hooks';

import { format } from 'date-fns';

/**
 * HistoryPage - Full-page Inbox for protocol logs and alerts.
 * Premium Inbox aesthetic inspired by modern email clients.
 */
export default function HistoryPage() {
    const { notifications, loading } = useNotifications();
    const dispatch = useAppDispatch();
    const [searchQuery, setSearchQuery] = useState('');
    const [filter, setFilter] = useState<'all' | 'unread' | 'intervention'>('all');

    const filteredNotifications = notifications.filter(n => {
        const matchesSearch = n.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
            n.message.toLowerCase().includes(searchQuery.toLowerCase());
        const matchesFilter = filter === 'all' ||
            (filter === 'unread' && !n.read) ||
            (filter === 'intervention' && n.type === 'intervention');
        return matchesSearch && matchesFilter;
    });

    const getIcon = (type: string) => {
        switch (type) {
            case 'intervention': return <Zap size={18} className="text-secondary" />;
            case 'safety': return <Shield size={18} className="text-red-500" />;
            case 'progress': return <Activity size={18} className="text-primary" />;
            default: return <Bell size={18} className="text-muted-foreground" />;
        }
    };

    return (
        <div className="flex h-screen bg-background overflow-hidden transition-colors duration-300">
            <AppSidebar />

            <div className="flex-1 flex flex-col min-w-0">
                <TopBar />

                <main className="flex-1 flex flex-col overflow-hidden bg-card/5">
                    {/* Inbox Header / Toolbar */}
                    <div className="px-8 py-6 border-b border-border bg-background/50 backdrop-blur-md flex items-center justify-between">
                        <div className="flex items-center gap-8">
                            <h2 className="text-2xl font-black text-foreground tracking-tight uppercase">Protocol Inbox</h2>

                            <div className="flex items-center gap-1 p-1 bg-foreground/5 rounded-lg border border-border">
                                {['all', 'unread', 'intervention'].map((f) => (
                                    <button
                                        key={f}
                                        onClick={() => setFilter(f as any)}
                                        className={`px-4 py-1.5 text-[10px] font-black uppercase tracking-widest rounded transition-all ${filter === f
                                                ? 'bg-background text-primary shadow-sm border border-border'
                                                : 'text-muted-foreground hover:text-foreground'
                                            }`}
                                    >
                                        {f}
                                    </button>
                                ))}
                            </div>
                        </div>

                        <div className="flex items-center gap-4">
                            <div className="relative group">
                                <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground group-focus-within:text-primary transition-colors" />
                                <input
                                    type="text"
                                    placeholder="Search logs..."
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                    className="bg-foreground/5 border border-border rounded-lg py-2 pl-10 pr-4 text-xs text-foreground placeholder-muted-foreground focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/20 w-64 transition-all"
                                />
                            </div>
                            <button className="p-2 text-muted-foreground hover:text-foreground hover:bg-foreground/5 rounded-lg border border-border transition-all">
                                <Filter size={18} />
                            </button>
                        </div>
                    </div>

                    {/* Inbox List Area */}
                    <div className="flex-1 overflow-y-auto custom-scrollbar">
                        <div className="max-w-6xl mx-auto py-8 px-8">
                            {loading ? (
                                <div className="flex flex-col items-center justify-center h-64 opacity-50">
                                    <div className="w-8 h-8 border-2 border-primary/20 border-t-primary rounded-full animate-spin mb-4" />
                                    <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-primary">Scanning Frequency...</p>
                                </div>
                            ) : filteredNotifications.length > 0 ? (
                                <div className="border border-border rounded-2xl bg-background overflow-hidden shadow-2xl shadow-black/20">
                                    {filteredNotifications.map((n, idx) => (
                                        <Link
                                            key={n.id}
                                            href={`/history/${n.id}`}
                                            className={`flex items-center gap-4 p-4 border-b border-border transition-all group hover:bg-primary/[0.02] ${!n.read ? 'bg-primary/[0.01]' : 'opacity-80'
                                                } ${idx === filteredNotifications.length - 1 ? 'border-b-0' : ''}`}
                                        >
                                            {/* Read Indicator */}
                                            <div className="w-1.5 h-1.5 rounded-full shrink-0">
                                                {!n.read && <div className="w-full h-full bg-primary rounded-full shadow-[0_0_8px_rgba(20,241,149,0.5)]" />}
                                            </div>

                                            {/* Checkbox (Visual only) */}
                                            <div className="w-5 h-5 border border-border rounded flex items-center justify-center text-transparent group-hover:border-primary/50 transition-colors">
                                                <CheckCircle2 size={12} />
                                            </div>

                                            {/* Star (Visual only) */}
                                            <button className="text-muted-foreground hover:text-yellow-500 transition-colors">
                                                <Star size={18} strokeWidth={1.5} />
                                            </button>

                                            {/* Category/Icon */}
                                            <div className="flex items-center gap-3 min-w-[140px]">
                                                <div className="w-8 h-8 rounded-lg bg-foreground/5 flex items-center justify-center">
                                                    {getIcon(n.type)}
                                                </div>
                                                <span className={`text-[10px] font-black uppercase tracking-widest ${!n.read ? 'text-foreground' : 'text-muted-foreground'}`}>
                                                    {n.category}
                                                </span>
                                            </div>

                                            {/* Subject & Preview */}
                                            <div className="flex-1 min-w-0 pr-4">
                                                <div className="flex items-center gap-2 mb-0.5">
                                                    <span className={`text-sm tracking-tight truncate ${!n.read ? 'font-black text-foreground' : 'font-medium text-muted-foreground'}`}>
                                                        {n.title}
                                                    </span>
                                                    {!n.read && <span className="px-1.5 py-0.5 bg-primary/10 text-primary text-[8px] font-black uppercase rounded">New</span>}
                                                </div>
                                                <p className="text-xs text-muted-foreground truncate opacity-60">
                                                    {n.message}
                                                </p>
                                            </div>

                                            {/* Time */}
                                            <div className="text-[10px] font-mono text-muted-foreground shrink-0 group-hover:text-primary transition-colors">
                                                {format(new Date(n.created_at), 'MMM dd')}
                                            </div>

                                            {/* Inline Actions */}
                                            <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity pl-4">
                                                <button className="p-1.5 hover:bg-foreground/5 rounded transition-all text-muted-foreground hover:text-foreground">
                                                    <Clock size={16} />
                                                </button>
                                                <button className="p-1.5 hover:bg-foreground/5 rounded transition-all text-muted-foreground hover:text-foreground">
                                                    <MoreVertical size={16} />
                                                </button>
                                            </div>
                                        </Link>
                                    ))}
                                </div>
                            ) : (
                                <div className="flex flex-col items-center justify-center py-20 text-center border-2 border-dashed border-border rounded-[3rem] bg-card/10">
                                    <Mail size={48} className="text-muted-foreground/20 mb-4" />
                                    <h3 className="text-xl font-black text-foreground uppercase tracking-tighter mb-2">Inbox Zero</h3>
                                    <p className="text-muted-foreground max-w-xs text-sm">No protocol logs found matching your current filter. Your system is perfectly synchronized.</p>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Footer Info */}
                    <div className="px-8 py-3 border-t border-border bg-background/50 flex items-center justify-between">
                        <div className="flex items-center gap-4">
                            <div className="flex items-center gap-2 text-[10px] font-bold text-muted-foreground uppercase tracking-widest">
                                <div className="w-2 h-2 rounded-full bg-primary" />
                                System Online
                            </div>
                            <span className="text-[10px] text-muted-foreground opacity-50">Storage: 0.1% / 10GB</span>
                        </div>
                        <p className="text-[10px] font-mono text-muted-foreground uppercase tracking-widest">
                            KEEP-UP // INBOX_V1.0
                        </p>
                    </div>
                </main>
            </div>
        </div>
    );
}
