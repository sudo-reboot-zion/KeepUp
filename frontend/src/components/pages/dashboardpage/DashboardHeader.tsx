'use client';

import React from 'react';
import { YearlyGoalSummary } from '@/types/dashboard.types';
import {
    Trophy,
    Target,
    TrendingUp,
    Clock,
    Share2,
    Settings
} from 'lucide-react';

interface DashboardHeaderProps {
    yearlyGoal: YearlyGoalSummary;
    className?: string;
}

/**
 * DashboardHeader - A glassmorphic header component for the dashboard.
 * Displays the main resolution, overall progress, and key metrics.
 */
export default function DashboardHeader({
    yearlyGoal,
    className = ''
}: DashboardHeaderProps) {
    const progress = Math.round(yearlyGoal.progress_percentage);

    return (
        <header className={`relative z-20 ${className}`}>
            {/* Glassmorphic Container */}
            <div className="bg-[#121212]/40 backdrop-blur-xl border-b border-white/5 px-8 py-6">
                <div className="max-w-[1600px] mx-auto">
                    <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-8">

                        {/* Left Side: Resolution Info */}
                        <div className="flex-1">
                            <div className="flex items-center gap-3 mb-2">
                                <div className="p-2 rounded-lg bg-[#14f195]/10 border border-[#14f195]/20">
                                    <Target size={20} className="text-[#14f195]" />
                                </div>
                                <span className="text-[10px] font-bold uppercase tracking-[0.3em] text-[#14f195]">
                                    Active Protocol
                                </span>
                            </div>
                            <h1 className="text-3xl md:text-4xl font-black text-white tracking-tight leading-tight mb-3">
                                {yearlyGoal.resolution_text}
                            </h1>
                            <div className="flex flex-wrap items-center gap-4 text-sm text-gray-400">
                                <div className="flex items-center gap-1.5">
                                    <Clock size={14} className="text-gray-500" />
                                    <span>Started {new Date(yearlyGoal.created_at).toLocaleDateString()}</span>
                                </div>
                                <div className="w-1 h-1 rounded-full bg-gray-700" />
                                <div className="flex items-center gap-1.5">
                                    <Trophy size={14} className="text-yellow-500/70" />
                                    <span>Target: Dec 31, 2026</span>
                                </div>
                            </div>
                        </div>

                        {/* Middle: Progress Visualization */}
                        <div className="flex-1 max-w-md w-full">
                            <div className="bg-white/5 rounded-2xl p-5 border border-white/5 relative overflow-hidden group">
                                {/* Background Glow */}
                                <div className="absolute top-0 right-0 w-32 h-32 bg-[#9945ff]/10 blur-3xl rounded-full -mr-16 -mt-16 group-hover:bg-[#9945ff]/20 transition-colors" />

                                <div className="relative z-10">
                                    <div className="flex items-center justify-between mb-3">
                                        <div className="flex items-center gap-2">
                                            <TrendingUp size={16} className="text-[#9945ff]" />
                                            <span className="text-xs font-bold uppercase tracking-wider text-gray-300">Overall Progress</span>
                                        </div>
                                        <span className="text-2xl font-black text-white font-mono">{progress}%</span>
                                    </div>

                                    {/* Progress Bar */}
                                    <div className="w-full h-2 bg-black/40 rounded-full overflow-hidden mb-3">
                                        <div
                                            className="h-full bg-gradient-to-r from-[#14f195] via-[#9945ff] to-[#9945ff] shadow-[0_0_15px_rgba(153,69,255,0.5)] transition-all duration-1000 ease-out"
                                            style={{ width: `${progress}%` }}
                                        />
                                    </div>

                                    <div className="flex items-center justify-between text-[10px] font-bold uppercase tracking-widest text-gray-500">
                                        <span>Week {yearlyGoal.current_week}</span>
                                        <span>Week {yearlyGoal.total_weeks}</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Right Side: Actions */}
                        <div className="flex items-center gap-3">
                            <button className="p-3 rounded-xl bg-white/5 border border-white/10 text-gray-400 hover:text-white hover:bg-white/10 transition-all">
                                <Share2 size={20} />
                            </button>
                            <button className="p-3 rounded-xl bg-white/5 border border-white/10 text-gray-400 hover:text-white hover:bg-white/10 transition-all">
                                <Settings size={20} />
                            </button>
                            <button className="px-6 py-3 rounded-xl bg-[#14f195] text-black font-bold text-sm hover:bg-[#14f195]/90 transition-all shadow-[0_0_20px_rgba(20,241,149,0.3)]">
                                Log Activity
                            </button>
                        </div>

                    </div>
                </div>
            </div>

            {/* Sub-header / Stats Bar */}
            <div className="bg-black/20 border-b border-white/5 px-8 py-3">
                <div className="max-w-[1600px] mx-auto flex items-center gap-8 overflow-x-auto no-scrollbar">
                    <div className="flex items-center gap-2 whitespace-nowrap">
                        <span className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">Status:</span>
                        <span className="text-[10px] font-bold text-[#14f195] uppercase tracking-widest px-2 py-0.5 rounded bg-[#14f195]/10 border border-[#14f195]/20">
                            {yearlyGoal.status}
                        </span>
                    </div>
                    <div className="w-[1px] h-3 bg-white/10" />
                    <div className="flex items-center gap-2 whitespace-nowrap">
                        <span className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">Confidence:</span>
                        <span className="text-[10px] font-bold text-white uppercase tracking-widest">
                            {yearlyGoal.confidence_score ? `${Math.round(yearlyGoal.confidence_score * 100)}%` : 'N/A'}
                        </span>
                    </div>
                    <div className="w-[1px] h-3 bg-white/10" />
                    <div className="flex items-center gap-2 whitespace-nowrap">
                        <span className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">Streak:</span>
                        <span className="text-[10px] font-bold text-[#9945ff] uppercase tracking-widest">
                            12 Days
                        </span>
                    </div>
                </div>
            </div>
        </header>
    );
}
