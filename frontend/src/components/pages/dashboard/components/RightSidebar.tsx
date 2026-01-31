'use client';

import React from 'react';
import { Bell, Mail, Plus } from 'lucide-react';
import { motion } from 'framer-motion';

interface Agent {
    name: string;
    role: string;
    icon: React.ElementType;
}

interface RightSidebarProps {
    user: {
        name: string;
        sleepScore: number;
        streak: number;
    };
    agents: Agent[];
}

export default function RightSidebar({ user, agents }: RightSidebarProps) {
    return (
        <aside className="hidden xl:flex flex-col w-[350px] h-screen sticky top-0 border-l border-[var(--border)] bg-[var(--bg)] p-6 gap-8 overflow-y-auto custom-scrollbar">
            {/* Header: Notifications & Profile */}
            <div className="flex items-center justify-end gap-4">
                <button className="p-2 rounded-full bg-[var(--bg)] border border-[var(--border)] text-[var(--fg)] hover:bg-[var(--muted)] transition-colors relative">
                    <Bell size={18} />
                    <span className="absolute top-0 right-0 w-2.5 h-2.5 bg-red-500 rounded-full border-2 border-[var(--bg)]"></span>
                </button>
                <div className="flex items-center gap-3 pl-2">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[var(--primary)] to-[var(--secondary)] flex items-center justify-center text-[var(--bg)] font-bold">
                        {user.name[0]}
                    </div>
                    <span className="font-semibold text-sm">{user.name}</span>
                </div>
            </div>

            {/* Statistics Card */}
            <div>
                <div className="flex items-center justify-between mb-4">
                    <h3 className="font-bold text-lg">Statistic</h3>
                    <button className="text-[var(--fg)] opacity-40 hover:opacity-100">•••</button>
                </div>
                <div className="bg-[var(--card)] border border-[var(--border)] rounded-3xl p-6 flex flex-col items-center text-center shadow-sm">
                    {/* Circular Progress Placeholder */}
                    <div className="relative w-32 h-32 mb-4 flex items-center justify-center">
                        <svg className="w-full h-full transform -rotate-90">
                            <circle
                                cx="64"
                                cy="64"
                                r="56"
                                stroke="currentColor"
                                strokeWidth="12"
                                fill="transparent"
                                className="text-[var(--muted)]"
                            />
                            <circle
                                cx="64"
                                cy="64"
                                r="56"
                                stroke="var(--secondary)"
                                strokeWidth="12"
                                fill="transparent"
                                strokeDasharray={351.86}
                                strokeDashoffset={351.86 * (1 - user.sleepScore / 100)}
                                strokeLinecap="round"
                            />
                        </svg>
                        <div className="absolute inset-0 flex items-center justify-center flex-col">
                            <span className="text-2xl font-bold">{user.sleepScore}%</span>
                        </div>
                        <div className="absolute top-0 right-0 bg-[var(--secondary)] text-[var(--bg)] text-[10px] font-bold px-2 py-0.5 rounded-full">
                            Sleep
                        </div>
                    </div>

                    <h4 className="font-bold text-lg mb-1">Good Morning {user.name} 🔥</h4>
                    <p className="text-xs opacity-60 mb-6">Continue your routine to achieve your target!</p>

                    {/* Bar Chart Placeholder */}
                    <div className="flex items-end justify-between w-full h-24 gap-2 px-2">
                        {[40, 65, 45, 90, 30].map((h, i) => (
                            <div key={i} className="flex flex-col items-center gap-1 flex-1">
                                <div
                                    className="w-full rounded-t-md bg-[var(--primary)] opacity-20 hover:opacity-100 transition-opacity"
                                    style={{ height: `${h}%` }}
                                />
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Mentors / Agents List */}
            <div className="flex-1">
                <div className="flex items-center justify-between mb-4">
                    <h3 className="font-bold text-lg">Your Mentors</h3>
                    <button className="p-1 rounded-full border border-[var(--border)] hover:bg-[var(--muted)]">
                        <Plus size={16} />
                    </button>
                </div>

                <div className="space-y-4">
                    {agents.map((agent, idx) => (
                        <motion.div
                            key={agent.name}
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: idx * 0.1 }}
                            className="bg-[var(--card)] border border-[var(--border)] p-4 rounded-2xl flex items-center justify-between group hover:shadow-md transition-all"
                        >
                            <div className="flex items-center gap-3">
                                <div className="w-10 h-10 rounded-full bg-[var(--muted)] flex items-center justify-center text-[var(--fg)] group-hover:bg-[var(--primary)] group-hover:text-[var(--bg)] transition-colors">
                                    <agent.icon size={18} />
                                </div>
                                <div>
                                    <h5 className="font-bold text-sm">{agent.name}</h5>
                                    <p className="text-xs opacity-60">{agent.role}</p>
                                </div>
                            </div>
                            <button className="text-xs font-medium text-[var(--primary)] border border-[var(--primary)] px-3 py-1.5 rounded-full hover:bg-[var(--primary)] hover:text-[var(--bg)] transition-colors">
                                Chat
                            </button>
                        </motion.div>
                    ))}
                </div>

                <button className="w-full mt-6 py-3 rounded-xl bg-[var(--primary)]/10 text-[var(--primary)] font-bold text-sm hover:bg-[var(--primary)]/20 transition-colors">
                    See All
                </button>
            </div>
        </aside>
    );
}
