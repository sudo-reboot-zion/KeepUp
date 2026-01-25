import React from 'react';
import { Flame, CheckCircle2, Dumbbell, Trophy, Target } from 'lucide-react';

interface ProfileStatsProps {
    stats: {
        currentStreak: number;
        totalCheckIns: number;
        milestonesEarned: number;
    };
}

export default function ProfileStats({ stats }: ProfileStatsProps) {
    return (
        <div className="p-8 md:p-12 space-y-12 border-b md:border-b-0 md:border-r border-[var(--border)]">
            {/* Stats Row */}
            <div className="flex flex-col sm:flex-row gap-8 sm:gap-12">
                <div className="flex items-center gap-4">
                    <div className="p-3 bg-yellow-500/10 rounded-xl shrink-0">
                        <Flame className="w-6 h-6 text-yellow-500" />
                    </div>
                    <div>
                        <p className="text-[10px] tracking-[0.2em] text-[var(--fg)]/50 font-bold uppercase whitespace-nowrap">Current Streak</p>
                        <p className="text-3xl font-black">{stats.currentStreak} DAYS</p>
                    </div>
                </div>
                <div className="flex items-center gap-4">
                    <div className="p-3 bg-blue-500/10 rounded-xl shrink-0">
                        <CheckCircle2 className="w-6 h-6 text-blue-500" />
                    </div>
                    <div>
                        <p className="text-[10px] tracking-[0.2em] text-[var(--fg)]/50 font-bold uppercase whitespace-nowrap">Check-ins</p>
                        <p className="text-3xl font-black">{stats.totalCheckIns}</p>
                    </div>
                </div>
            </div>

            {/* Achievements Section */}
            <div className="space-y-6">
                <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-2">
                    <h3 className="text-sm font-bold uppercase tracking-widest text-[var(--fg)]/50">Achievements</h3>
                    <p className="text-[var(--primary)] font-bold text-sm">
                        <span className="text-[var(--fg)] mr-1">{stats.milestonesEarned}</span>
                        Unlocked
                    </p>
                </div>
                <div className="grid grid-cols-4 gap-3 sm:gap-4">
                    <AchievementBox icon={<Flame className="w-5 h-5 sm:w-6 sm:h-6" />} active={true} />
                    <AchievementBox icon={<Dumbbell className="w-5 h-5 sm:w-6 sm:h-6" />} active={true} />
                    <AchievementBox icon={<Trophy className="w-5 h-5 sm:w-6 sm:h-6" />} active={false} />
                    <AchievementBox icon={<Target className="w-5 h-5 sm:w-6 sm:h-6" />} active={false} />
                </div>
            </div>
        </div>
    );
}

function AchievementBox({ icon, active }: { icon: React.ReactNode; active: boolean }) {
    return (
        <div className={`aspect-square rounded-2xl flex items-center justify-center border transition-all ${active
            ? 'bg-[var(--primary)]/10 border-[var(--primary)]/30 shadow-[0_0_20px_rgba(201,252,110,0.1)] text-[var(--primary)]'
            : 'bg-[var(--fg)]/5 border-[var(--border)] text-[var(--fg)]/30 grayscale opacity-30'
            }`}>
            {icon}
        </div>
    );
}
