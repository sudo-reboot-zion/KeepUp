'use client';

import React from 'react';
import {
    X,
    ArrowLeft,
    Trash2,
    Mail,
    Clock,
    MoreVertical,
    Zap,
    Shield,
    Activity,
    User,
    ArrowRight,
    ChevronRight,
    Star,
    CornerUpLeft,
    Share2
} from 'lucide-react';
import { format } from 'date-fns';
import { Notification } from '@/lib/notificationApi';

interface NotificationDetailModalProps {
    notification: Notification | null;
    isOpen: boolean;
    onClose: () => void;
}

/**
 * NotificationDetailModal - Redesigned with "Inbox/Email" aesthetic.
 * High fidelity UI based on user's Encode Hackathon inspiration.
 */
export default function NotificationDetailModal({
    notification,
    isOpen,
    onClose
}: NotificationDetailModalProps) {
    if (!isOpen || !notification) return null;

    const getSenderInfo = () => {
        switch (notification.type) {
            case 'intervention': return { name: 'AI Intervention Agent', email: 'intervention@keepup.ai', icon: <Zap size={14} /> };
            case 'safety': return { name: 'Health Safety Guard', email: 'guardrails@keepup.ai', icon: <Shield size={14} /> };
            case 'progress': return { name: 'Performance Tracker', email: 'analytics@keepup.ai', icon: <Activity size={14} /> };
            default: return { name: 'AI Health Coach', email: 'coach@keepup.ai', icon: <User size={14} /> };
        }
    };

    const sender = getSenderInfo();

    return (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-0 md:p-8">
            {/* Backdrop */}
            <div
                className="absolute inset-0 bg-black/60 backdrop-blur-md transition-opacity duration-300"
                onClick={onClose}
            />

            {/* Modal Container: Inbox Style */}
            <div className="relative w-full max-w-5xl h-full md:h-[90vh] bg-background md:rounded-2xl shadow-[0_0_100px_rgba(0,0,0,0.5)] border border-border flex flex-col overflow-hidden animate-in slide-in-from-bottom-5 duration-300">

                {/* ACTION BAR (Top) */}
                <div className="flex items-center justify-between px-6 py-4 border-b border-border bg-card/30 backdrop-blur-xl sticky top-0 z-20">
                    <div className="flex items-center gap-6">
                        <button
                            onClick={onClose}
                            className="p-2 -ml-2 text-muted-foreground hover:text-foreground hover:bg-foreground/5 rounded-full transition-all"
                            title="Back to Inbox"
                        >
                            <ArrowLeft size={20} />
                        </button>
                        <div className="h-6 w-px bg-border mx-2" />
                        <div className="flex items-center gap-2">
                            <button className="p-2 text-muted-foreground hover:text-foreground hover:bg-foreground/5 rounded-full transition-all" title="Archive">
                                <Shield size={18} />
                            </button>
                            <button className="p-2 text-muted-foreground hover:text-foreground hover:bg-foreground/5 rounded-full transition-all" title="Report">
                                <Zap size={18} />
                            </button>
                            <button className="p-2 text-muted-foreground hover:text-foreground hover:bg-foreground/5 rounded-full transition-all" title="Delete">
                                <Trash2 size={18} />
                            </button>
                        </div>
                        <div className="h-6 w-px bg-border mx-2" />
                        <div className="flex items-center gap-2">
                            <button className="p-2 text-muted-foreground hover:text-foreground hover:bg-foreground/5 rounded-full transition-all" title="Mark as Unread">
                                <Mail size={18} />
                            </button>
                            <button className="p-2 text-muted-foreground hover:text-foreground hover:bg-foreground/5 rounded-full transition-all" title="Snooze">
                                <Clock size={18} />
                            </button>
                        </div>
                    </div>
                    <div className="flex items-center gap-4">
                        <div className="text-[10px] font-mono text-muted-foreground uppercase tracking-widest hidden sm:block">
                            {format(new Date(), 'HH:mm')} System Time
                        </div>
                        <button className="p-2 text-muted-foreground hover:text-foreground hover:bg-foreground/5 rounded-full transition-all">
                            <MoreVertical size={20} />
                        </button>
                    </div>
                </div>

                {/* EMAIL BODY AREA */}
                <div className="flex-1 overflow-y-auto custom-scrollbar bg-card/5">
                    <div className="max-w-4xl mx-auto px-8 py-10 space-y-10">

                        {/* SUBJECT LINE */}
                        <div className="flex items-start justify-between gap-6">
                            <h1 className="text-3xl md:text-4xl font-black text-foreground tracking-tight leading-tight">
                                {notification.title}
                            </h1>
                            <div className="flex items-center gap-4 pt-2">
                                <span className="text-[10px] font-bold uppercase py-1 px-3 bg-foreground/5 border border-border rounded-full text-muted-foreground">Inbox</span>
                                <button className="text-muted-foreground hover:text-yellow-500 transition-colors">
                                    <Star size={20} />
                                </button>
                            </div>
                        </div>

                        {/* SENDER INFO */}
                        <div className="flex items-center justify-between group">
                            <div className="flex items-center gap-4">
                                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-primary/30 to-secondary/30 border border-foreground/10 flex items-center justify-center text-foreground ring-2 ring-background ring-offset-2 ring-offset-border">
                                    {sender.icon}
                                </div>
                                <div>
                                    <div className="flex items-center gap-2">
                                        <span className="text-sm font-black text-foreground uppercase tracking-tight">{sender.name}</span>
                                        <span className="text-[10px] text-muted-foreground lowercase hidden sm:block">&lt;{sender.email}&gt;</span>
                                    </div>
                                    <div className="flex items-center gap-1 text-[11px] text-muted-foreground">
                                        <span>to me</span>
                                        <ChevronRight size={10} />
                                    </div>
                                </div>
                            </div>
                            <div className="flex items-center gap-4 text-xs text-muted-foreground">
                                <span className="font-mono">{format(new Date(notification.created_at), 'MMM dd, HH:mm')} ({format(new Date(notification.created_at), 'R')} hours ago)</span>
                                <div className="flex items-center gap-2">
                                    <button className="p-1 hover:bg-foreground/5 rounded transition-all"><CornerUpLeft size={16} /></button>
                                    <button className="p-1 hover:bg-foreground/5 rounded transition-all"><Share2 size={16} /></button>
                                </div>
                            </div>
                        </div>

                        {/* MAIN TEXT CONTENT */}
                        <div className="space-y-8 py-4">
                            <div className="text-base text-foreground leading-relaxed font-medium space-y-4">
                                {notification.message.split('\n').map((para, i) => (
                                    <p key={i}>{para}</p>
                                ))}
                            </div>

                            {/* SPECIAL DATA BOXES (e.g. Protocol Adjustments) */}
                            {notification.type === 'intervention' && notification.data && (
                                <div className="bg-foreground/[0.02] border border-border rounded-xl p-8 space-y-6">
                                    <div className="flex items-center justify-between border-b border-border pb-4">
                                        <h4 className="text-xs font-black uppercase tracking-[0.2em] text-primary">Protocol Adjustment Briefing</h4>
                                        <Zap size={16} className="text-primary animate-pulse" />
                                    </div>

                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                        <div className="space-y-1">
                                            <p className="text-[10px] font-bold uppercase text-muted-foreground tracking-widest">Intervention Type</p>
                                            <p className="text-lg font-black text-foreground">{notification.data.intervention_type || 'Autonomous'}</p>
                                        </div>
                                        <div className="space-y-1">
                                            <p className="text-[10px] font-bold uppercase text-muted-foreground tracking-widest">Confidence Score</p>
                                            <p className="text-lg font-black text-primary">0.98 / 1.0</p>
                                        </div>
                                    </div>

                                    {notification.data.actions && (
                                        <div className="space-y-4">
                                            <p className="text-[10px] font-bold uppercase text-muted-foreground tracking-widest">Sequence of Actions</p>
                                            <div className="space-y-2">
                                                {notification.data.actions.map((act: string, idx: number) => (
                                                    <div key={idx} className="flex items-center gap-3 p-3 bg-background border border-border rounded-lg group/act hover:border-primary/50 transition-all">
                                                        <span className="text-[10px] font-mono text-muted-foreground">0{idx + 1}</span>
                                                        <span className="text-sm font-bold text-foreground">{act}</span>
                                                        <ArrowRight size={14} className="ml-auto text-muted-foreground group-hover/act:text-primary transition-colors" />
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            )}

                            <div className="pt-10 space-y-4 text-muted-foreground border-t border-border">
                                <p className="text-sm font-medium">Looking forward to seeing your project evolve!</p>
                                <div className="space-y-1">
                                    <p className="text-sm font-black text-foreground uppercase tracking-tighter">Best,</p>
                                    <p className="text-sm font-black text-foreground uppercase tracking-tighter">{sender.name}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* FOOTER ACTIONS (Inbox Style) */}
                <div className="p-6 border-t border-border bg-card/30 flex items-center gap-3">
                    <button
                        onClick={onClose}
                        className="px-6 py-2.5 bg-primary text-black text-[11px] font-black uppercase tracking-widest rounded-lg flex items-center gap-2 hover:bg-primary/90 transition-all shadow-lg shadow-primary/20"
                    >
                        <CornerUpLeft size={14} /> Reply
                    </button>
                    <button
                        className="px-6 py-2.5 border border-border bg-foreground/5 text-foreground text-[11px] font-black uppercase tracking-widest rounded-lg flex items-center gap-2 hover:bg-foreground/10 transition-all"
                    >
                        <ArrowRight size={14} /> Forward
                    </button>
                </div>

            </div>
        </div>
    );
}
