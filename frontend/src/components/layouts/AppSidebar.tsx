'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
    LayoutDashboard, Calendar, Activity, Users, User,
    MessageSquare, PenTool, Target,
    Dumbbell, Apple, Moon, Brain, Heart,
    CheckCircle, Trophy, Award,
    Bell, Settings, HelpCircle, FileText, Lightbulb,
    ChevronDown, ChevronRight, LogOut
} from 'lucide-react';
import { cn } from '@/lib/utils';

// --- Configuration ---
const NAVIGATION = [
    { label: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
    { label: "Today's Plan", href: '/plan', icon: Calendar },
    { label: 'Track Progress', href: '/progress', icon: Activity },
    { label: 'Community', href: '/community', icon: Users },
    { label: 'My Profile', href: '/profile', icon: User },
];

const QUICK_ACTIONS = [
    { label: 'Chat with Agent', icon: MessageSquare, action: 'chat' },
    { label: 'Quick Log', icon: PenTool, action: 'log' },
    { label: 'View This Week', icon: Calendar, action: 'week' },
    { label: 'Check Goals', icon: Target, action: 'goals' },
];

const AGENTS = [
    { name: 'Drill Sergeant', role: 'Fitness', icon: Dumbbell },
    { name: 'Health Monitor', role: 'Health', icon: Activity },
    { name: 'Nutrition Guide', role: 'Nutrition', icon: Apple },
    { name: 'Sleep Coach', role: 'Sleep', icon: Moon },
    { name: 'Stress Manager', role: 'Stress', icon: Brain },
    { name: 'Emotional Support', role: 'Wellness', icon: Heart },
];

const ACTIVE_ITEMS = [
    { title: "Today's Workout", detail: "Upper Body - 45 min", status: 'pending' },
    { title: "Tonight's Sleep Target", detail: "7.5 hours (bed by 10 PM)", status: 'pending' },
    { title: "Pending Check-in", detail: "Morning wellness check", status: 'pending' },
];

export default function AppSidebar() {
    const pathname = usePathname();
    const [notifications, setNotifications] = useState({
        morning: true,
        workout: true,
        dnd: true
    });

    return (
        <aside className="hidden md:flex flex-col w-[320px] h-screen sticky top-0 border-r border-[var(--border)] bg-[var(--bg)] text-[var(--fg)] overflow-y-auto custom-scrollbar font-[family-name:var(--font-ppMontreal)]">
            {/* Logo */}
            <div className="py-8 px-6 flex justify-center border-b border-[var(--border)]">
                <img src="/assets/images/keep-up-fixed.svg" alt="Keep Up" className="w-32 h-auto nav-logo" />
            </div>

            <div className="flex-1 py-6 px-4 space-y-8">

                {/* 1. NAVIGATION */}
                <section>
                    <h3 className="text-xs font-bold opacity-40 uppercase tracking-wider mb-3 px-2">Navigation</h3>
                    <nav className="space-y-1">
                        {NAVIGATION.map((item) => {
                            const isActive = pathname === item.href;
                            return (
                                <Link
                                    key={item.href}
                                    href={item.href}
                                    className={cn(
                                        "flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200 group",
                                        isActive
                                            ? "bg-[var(--primary)] text-[var(--bg)] font-bold"
                                            : "hover:bg-[var(--muted)] opacity-70 hover:opacity-100"
                                    )}
                                >
                                    <item.icon size={18} />
                                    <span>{item.label}</span>
                                </Link>
                            );
                        })}
                    </nav>
                </section>

                {/* 2. QUICK ACTIONS */}
                <section>
                    <h3 className="text-xs font-bold opacity-40 uppercase tracking-wider mb-3 px-2 flex items-center gap-2">
                        <span className="text-[var(--accent)]">⚡</span> Quick Actions
                    </h3>
                    <div className="grid grid-cols-2 gap-2">
                        {QUICK_ACTIONS.map((action, idx) => (
                            <button key={idx} className="flex flex-col items-center justify-center gap-2 p-3 rounded-xl border border-[var(--border)] hover:bg-[var(--muted)] transition-colors text-center">
                                <action.icon size={20} className="text-[var(--primary)]" />
                                <span className="text-[10px] font-bold leading-tight">{action.label}</span>
                            </button>
                        ))}
                    </div>
                </section>

                {/* 3. YOUR AGENTS */}
                <section>
                    <h3 className="text-xs font-bold opacity-40 uppercase tracking-wider mb-3 px-2">Your Agents</h3>
                    <div className="space-y-2">
                        {AGENTS.map((agent, idx) => (
                            <button key={idx} className="w-full flex items-center gap-3 px-3 py-2 rounded-xl hover:bg-[var(--muted)] transition-colors group text-left">
                                <div className="w-8 h-8 rounded-full bg-[var(--muted)] flex items-center justify-center group-hover:bg-[var(--primary)] group-hover:text-[var(--bg)] transition-colors">
                                    <agent.icon size={14} />
                                </div>
                                <div className="flex-1">
                                    <p className="text-xs font-bold">{agent.name}</p>
                                    <p className="text-[10px] opacity-50">{agent.role}</p>
                                </div>
                                <ChevronRight size={14} className="opacity-0 group-hover:opacity-50" />
                            </button>
                        ))}
                    </div>
                    <p className="text-[10px] text-center opacity-40 mt-2">(Tap to chat)</p>
                </section>

                {/* 4. ACTIVE ITEMS */}
                <section>
                    <h3 className="text-xs font-bold opacity-40 uppercase tracking-wider mb-3 px-2">Active Items</h3>
                    <div className="space-y-3">
                        {ACTIVE_ITEMS.map((item, idx) => (
                            <div key={idx} className="bg-[var(--muted)]/50 rounded-xl p-3 border border-[var(--border)]">
                                <div className="flex items-start gap-2">
                                    <div className="mt-0.5 text-[var(--primary)]">
                                        <CheckCircle size={14} />
                                    </div>
                                    <div>
                                        <p className="text-xs font-bold">{item.title}</p>
                                        <p className="text-[10px] opacity-60">{item.detail}</p>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </section>

                {/* 5. ACHIEVEMENTS */}
                <section>
                    <h3 className="text-xs font-bold opacity-40 uppercase tracking-wider mb-3 px-2">Achievements</h3>
                    <div className="bg-[var(--card)] border border-[var(--border)] rounded-xl p-4 space-y-4">
                        <div>
                            <div className="flex justify-between text-xs font-bold mb-1">
                                <span>7-Day Streak</span>
                                <span className="text-[var(--primary)]">4/7</span>
                            </div>
                            <div className="h-1.5 w-full bg-[var(--muted)] rounded-full overflow-hidden">
                                <div className="h-full bg-[var(--primary)] w-[57%]" />
                            </div>
                        </div>
                        <div>
                            <div className="flex justify-between text-xs font-bold mb-1">
                                <span>Sleep Champion</span>
                                <span className="text-[var(--secondary)]">6/7</span>
                            </div>
                            <div className="h-1.5 w-full bg-[var(--muted)] rounded-full overflow-hidden">
                                <div className="h-full bg-[var(--secondary)] w-[85%]" />
                            </div>
                        </div>
                        <div className="pt-2 border-t border-[var(--border)] flex items-center gap-2">
                            <Trophy size={14} className="text-yellow-500" />
                            <span className="text-[10px] font-bold">Next: 14-day streak (2 days left!)</span>
                        </div>
                    </div>
                </section>

                {/* 6. ACCOUNTABILITY */}
                <section>
                    <h3 className="text-xs font-bold opacity-40 uppercase tracking-wider mb-3 px-2">Accountability</h3>
                    <div className="bg-[var(--muted)]/30 rounded-xl p-3 border border-[var(--border)]">
                        <div className="flex items-center justify-between mb-2">
                            <span className="text-xs font-bold">Partner: Alex M.</span>
                            <span className="text-[10px] text-green-500 font-bold">✓ Active</span>
                        </div>
                        <p className="text-[10px] opacity-60 mb-3">Their Streak: 🔥 15 days</p>
                        <div className="grid grid-cols-2 gap-2">
                            <button className="text-[10px] font-bold bg-[var(--bg)] border border-[var(--border)] py-1.5 rounded-lg hover:bg-[var(--primary)] hover:text-[var(--bg)] transition-colors">
                                Message
                            </button>
                            <button className="text-[10px] font-bold bg-[var(--bg)] border border-[var(--border)] py-1.5 rounded-lg hover:bg-[var(--muted)] transition-colors">
                                Find New
                            </button>
                        </div>
                    </div>
                </section>

                {/* 7. NOTIFICATIONS */}
                <section>
                    <h3 className="text-xs font-bold opacity-40 uppercase tracking-wider mb-3 px-2">Notifications</h3>
                    <div className="space-y-2">
                        {[
                            { label: 'Morning Briefing (7 AM)', key: 'morning' },
                            { label: 'Workout Reminders', key: 'workout' },
                            { label: 'Do Not Disturb (10PM-7AM)', key: 'dnd' },
                        ].map((item, idx) => (
                            <div key={idx} className="flex items-center justify-between px-2 py-1">
                                <span className="text-xs font-medium opacity-80">{item.label}</span>
                                <div className={`w-2 h-2 rounded-full ${notifications[item.key as keyof typeof notifications] ? 'bg-green-500' : 'bg-red-500'}`} />
                            </div>
                        ))}
                        <button className="w-full text-[10px] font-bold text-[var(--primary)] mt-2 hover:underline text-left px-2">
                            ⚙️ Manage Notifications
                        </button>
                    </div>
                </section>

                {/* 8. SETTINGS & SUPPORT */}
                <section>
                    <h3 className="text-xs font-bold opacity-40 uppercase tracking-wider mb-3 px-2">Settings & Support</h3>
                    <nav className="space-y-1">
                        {[
                            { label: 'App Settings', icon: Settings },
                            { label: 'Edit Goals', icon: Target },
                            { label: 'Weekly Reports', icon: FileText },
                            { label: 'Help & FAQs', icon: HelpCircle },
                        ].map((item, idx) => (
                            <button key={idx} className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-[var(--muted)] transition-colors text-left opacity-70 hover:opacity-100">
                                <item.icon size={16} />
                                <span className="text-xs font-medium">{item.label}</span>
                            </button>
                        ))}
                    </nav>
                </section>

                {/* 9. LATEST INSIGHT */}
                <section className="bg-gradient-to-br from-[var(--primary)]/10 to-[var(--secondary)]/10 border border-[var(--primary)]/20 rounded-xl p-4">
                    <div className="flex items-center gap-2 mb-2 text-[var(--primary)]">
                        <Lightbulb size={16} />
                        <span className="text-xs font-bold uppercase">Latest Insight</span>
                    </div>
                    <p className="text-xs font-medium leading-relaxed italic opacity-80 mb-3">
                        &quot;You perform 23% better on workouts after 7+ hrs sleep&quot;
                    </p>
                    <button className="text-[10px] font-bold text-[var(--fg)] opacity-60 hover:opacity-100 hover:underline">
                        View All Insights
                    </button>
                </section>

            </div>

            {/* Logout Footer */}
            <div className="p-4 border-t border-[var(--border)]">
                <button className="w-full flex items-center justify-center gap-2 py-2 text-xs font-bold text-red-500 hover:bg-red-500/10 rounded-xl transition-colors">
                    <LogOut size={14} />
                    Logout
                </button>
            </div>
        </aside>
    );
}
