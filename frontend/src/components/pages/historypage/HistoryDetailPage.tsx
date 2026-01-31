'use client';

import React, { useEffect, useState } from 'react';
import {
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
    Share2,
    AlertCircle
} from 'lucide-react';
import { format } from 'date-fns';
import { useParams, useRouter } from 'next/navigation';
import AppSidebar from '@/components/layout/AppSidebar';
import TopBar from '@/components/layout/TopBar';
import { Notification, fetchNotifications, markAsRead } from '@/lib/notificationApi';
import { useAppDispatch } from '@/redux/hooks';
import { markRead } from '@/redux/slices/notificationSlice';

/**
 * HistoryDetailPage - Full-page detail view for protocol logs.
 * High fidelity "Inbox Detail" aesthetic.
 */
export default function HistoryDetailPage() {
    const { id } = useParams();
    const router = useRouter();
    const dispatch = useAppDispatch();
    const [notification, setNotification] = useState<Notification | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const loadDetail = async () => {
            try {
                setLoading(true);
                // We fetch all to find the specific one (or we could add a get-by-id endpoint if needed)
                // For now, API has a get by limiting, but we might want a specific endpoint in real use.
                // Assuming we can just find it in the list for this demo.
                const response = await fetchNotifications(100);
                const found = response.notifications.find(n => n.id === Number(id));

                if (found) {
                    setNotification(found);
                    // Mark as read automatically when viewing detail
                    if (!found.read) {
                        await markAsRead(found.id);
                        dispatch(markRead(found.id));
                    }
                } else {
                    setError('Notification not found in protocol logs.');
                }
            } catch (err) {
                setError('Failed to retrieve protocol data.');
            } finally {
                setLoading(false);
            }
        };

        if (id) loadDetail();
    }, [id, dispatch]);

    const getSenderInfo = (type: string) => {
        switch (type) {
            case 'intervention': return { name: 'AI Intervention Agent', email: 'intervention@keepup.ai', icon: <Zap size={14} /> };
            case 'safety': return { name: 'Health Safety Guard', email: 'guardrails@keepup.ai', icon: <Shield size={14} /> };
            case 'progress': return { name: 'Performance Tracker', email: 'analytics@keepup.ai', icon: <Activity size={14} /> };
            default: return { name: 'AI Health Coach', email: 'coach@keepup.ai', icon: <User size={14} /> };
        }
    };

    if (loading) {
        return (
            <div className="flex h-screen bg-background">
                <AppSidebar />
                <div className="flex-1 flex flex-col">
                    <TopBar />
                    <div className="flex-1 flex items-center justify-center">
                        <div className="w-8 h-8 border-2 border-primary/20 border-t-primary rounded-full animate-spin" />
                    </div>
                </div>
            </div>
        );
    }

    if (error || !notification) {
        return (
            <div className="flex h-screen bg-background">
                <AppSidebar />
                <div className="flex-1 flex flex-col">
                    <TopBar />
                    <div className="flex-1 flex items-center justify-center p-8">
                        <div className="max-w-md w-full p-8 border border-border bg-card rounded-2xl text-center">
                            <AlertCircle size={48} className="text-red-500 mx-auto mb-4" />
                            <h3 className="text-xl font-black text-foreground uppercase tracking-tight mb-2">Protocol Error</h3>
                            <p className="text-muted-foreground mb-6">{error || 'Data corrupted.'}</p>
                            <button onClick={() => router.push('/history')} className="px-8 py-3 bg-foreground/5 border border-border text-foreground font-black uppercase tracking-widest text-xs rounded-lg hover:bg-foreground/10 transition-all">
                                Return to Inbox
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    const sender = getSenderInfo(notification.type);

    return (
        <div className="flex h-screen bg-background overflow-hidden transition-colors duration-300">
            <AppSidebar />

            <div className="flex-1 flex flex-col min-w-0">
                <TopBar />

                <main className="flex-1 flex flex-col overflow-hidden">
                    {/* INBOX ACTION BAR */}
                    <div className="flex items-center justify-between px-8 py-4 border-b border-border bg-card/30 backdrop-blur-xl">
                        <div className="flex items-center gap-6">
                            <button
                                onClick={() => router.push('/history')}
                                className="p-2 -ml-2 text-muted-foreground hover:text-foreground hover:bg-foreground/5 rounded-full transition-all"
                            >
                                <ArrowLeft size={20} />
                            </button>
                            <div className="h-6 w-px bg-border mx-2" />
                            <div className="flex items-center gap-2">
                                <button className="p-2 text-muted-foreground hover:text-foreground hover:bg-foreground/5 rounded-full transition-all"><Shield size={18} /></button>
                                <button className="p-2 text-muted-foreground hover:text-foreground hover:bg-foreground/5 rounded-full transition-all"><Zap size={18} /></button>
                                <button className="p-2 text-muted-foreground hover:text-foreground hover:bg-foreground/5 rounded-full transition-all"><Trash2 size={18} /></button>
                            </div>
                            <div className="h-6 w-px bg-border mx-2" />
                            <div className="flex items-center gap-2">
                                <button className="p-2 text-muted-foreground hover:text-foreground hover:bg-foreground/5 rounded-full transition-all"><Mail size={18} /></button>
                                <button className="p-2 text-muted-foreground hover:text-foreground hover:bg-foreground/5 rounded-full transition-all"><Clock size={18} /></button>
                            </div>
                        </div>
                        <div className="flex items-center gap-4">
                            <div className="text-[10px] font-mono text-muted-foreground uppercase tracking-widest">
                                Log ID: PRTCL_{notification.id}
                            </div>
                            <button className="p-2 text-muted-foreground hover:text-foreground hover:bg-foreground/5 rounded-full transition-all">
                                <MoreVertical size={20} />
                            </button>
                        </div>
                    </div>

                    {/* CONTENT AREA */}
                    <div className="flex-1 overflow-y-auto custom-scrollbar bg-card/5">
                        <div className="max-w-5xl mx-auto px-12 py-12 space-y-12">

                            {/* SUBJECT */}
                            <div className="flex items-start justify-between gap-8">
                                <h1 className="text-4xl md:text-5xl font-black text-foreground tracking-tighter leading-tight">
                                    {notification.title}
                                </h1>
                                <div className="flex items-center gap-4 pt-3">
                                    <span className="text-[10px] font-black uppercase py-1 px-4 bg-foreground/5 border border-border rounded-full text-muted-foreground tracking-widest">Inbox</span>
                                    <button className="text-muted-foreground hover:text-yellow-500 transition-colors">
                                        <Star size={24} strokeWidth={1.5} />
                                    </button>
                                </div>
                            </div>

                            {/* SENDER */}
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-5">
                                    <div className="w-14 h-14 rounded-full bg-gradient-to-br from-primary/30 to-secondary/30 border border-foreground/10 flex items-center justify-center text-foreground ring-2 ring-background ring-offset-2 ring-offset-border">
                                        {sender.icon}
                                    </div>
                                    <div>
                                        <div className="flex items-center gap-2">
                                            <span className="text-lg font-black text-foreground uppercase tracking-tight">{sender.name}</span>
                                            <span className="text-xs text-muted-foreground lowercase hidden sm:block">&lt;{sender.email}&gt;</span>
                                        </div>
                                        <div className="flex items-center gap-1 text-xs text-muted-foreground">
                                            <span>to me</span>
                                            <ChevronRight size={12} />
                                        </div>
                                    </div>
                                </div>
                                <div className="flex items-center gap-6 text-sm text-muted-foreground">
                                    <div className="font-mono text-right">
                                        <p>{format(new Date(notification.created_at), 'MMM dd, yyyy')}</p>
                                        <p className="opacity-60">{format(new Date(notification.created_at), 'HH:mm')}</p>
                                    </div>
                                    <div className="flex items-center gap-3">
                                        <button className="p-2 hover:bg-foreground/5 rounded transition-all"><CornerUpLeft size={20} /></button>
                                        <button className="p-2 hover:bg-foreground/5 rounded transition-all"><Share2 size={20} /></button>
                                    </div>
                                </div>
                            </div>

                            {/* BODY */}
                            <div className="space-y-10 py-6 border-t border-border">
                                <div className="text-lg text-foreground leading-relaxed font-medium space-y-6">
                                    {notification.message.split('\n').map((para, i) => (
                                        <p key={i}>{para}</p>
                                    ))}
                                </div>

                                {/* STRUCTURED PROTOCOL DATA */}
                                {notification.type === 'intervention' && notification.data && (
                                    <div className="bg-foreground/[0.02] border border-border rounded-[2rem] p-10 space-y-8">
                                        <div className="flex items-center justify-between border-b border-border pb-6">
                                            <h4 className="text-sm font-black uppercase tracking-[0.3em] text-primary">Protocol Adjustment Briefing</h4>
                                            <Zap size={20} className="text-primary animate-pulse" />
                                        </div>

                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
                                            <div className="space-y-2">
                                                <p className="text-[10px] font-bold uppercase text-muted-foreground tracking-[0.2em]">Intervention Type</p>
                                                <p className="text-2xl font-black text-foreground uppercase tracking-tight">{notification.data.intervention_type || 'Autonomous'}</p>
                                            </div>
                                            <div className="space-y-2">
                                                <p className="text-[10px] font-bold uppercase text-muted-foreground tracking-[0.2em]">System Confidence</p>
                                                <p className="text-2xl font-black text-primary font-mono tracking-tighter">0.98 / 1.0</p>
                                            </div>
                                        </div>

                                        {notification.data.actions && (
                                            <div className="space-y-6">
                                                <p className="text-[10px] font-bold uppercase text-muted-foreground tracking-[0.2em]">Action Sequence</p>
                                                <div className="grid grid-cols-1 gap-3">
                                                    {notification.data.actions.map((act: string, idx: number) => (
                                                        <div key={idx} className="flex items-center gap-4 p-5 bg-background border border-border rounded-xl group/act hover:border-primary/50 transition-all shadow-sm">
                                                            <span className="text-xs font-mono text-muted-foreground opacity-40">0{idx + 1}</span>
                                                            <span className="text-base font-bold text-foreground">{act}</span>
                                                            <ArrowRight size={18} className="ml-auto text-muted-foreground group-hover/act:text-primary transition-colors" />
                                                        </div>
                                                    ))}
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                )}

                                <div className="pt-16 space-y-4 text-muted-foreground border-t border-border">
                                    <p className="text-lg font-medium italic">Protocol execution complete. Intelligence logs updated.</p>
                                    <div className="space-y-1">
                                        <p className="text-base font-black text-foreground uppercase tracking-tighter">Best regards,</p>
                                        <p className="text-base font-black text-primary uppercase tracking-tighter underline underline-offset-4 decoration-primary/30">{sender.name}</p>
                                    </div>
                                </div>
                            </div>

                            {/* FOOTER ACTIONS */}
                            <div className="pt-10 flex items-center gap-4">
                                <button className="px-10 py-4 bg-primary text-black text-xs font-black uppercase tracking-widest rounded-xl flex items-center gap-3 hover:bg-primary/90 transition-all shadow-xl shadow-primary/20">
                                    <CornerUpLeft size={18} /> Reply
                                </button>
                                <button className="px-10 py-4 border border-border bg-foreground/5 text-foreground text-xs font-black uppercase tracking-widest rounded-xl flex items-center gap-3 hover:bg-foreground/10 transition-all">
                                    <ArrowRight size={18} /> Forward
                                </button>
                            </div>
                        </div>
                    </div>
                </main>
            </div>
        </div>
    );
}
