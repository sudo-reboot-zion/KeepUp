import React from 'react';
import { Flame, CheckCircle2, Dumbbell, Trophy, Target, Award } from 'lucide-react';

interface ProfileStatsProps {
    stats: {
        currentStreak: number;
        totalCheckIns: number;
        milestonesEarned: number;
    };
}

export default function ProfileStats({ stats }: ProfileStatsProps) {
    return (
        <div className="space-y-10">
            <div className="flex items-center gap-3 border-b border-border pb-4">
                <Target size={18} className="text-primary" />
                <h3 className="text-xs font-black uppercase tracking-widest text-foreground">Performance Metrics</h3>
            </div>

            {/* Stats Row */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div className="flex items-center gap-5 p-4 bg-foreground/5 rounded-2xl border border-border/50">
                    <div className="p-4 bg-primary/10 rounded-xl shrink-0">
                        <Flame className="w-6 h-6 text-primary" />
                    </div>
                    <div>
                        <p className="text-[10px] tracking-[0.2em] text-muted-foreground font-black uppercase whitespace-nowrap">Current Streak</p>
                        <p className="text-2xl font-black text-foreground uppercase">{stats.currentStreak} Days</p>
                    </div>
                </div>
                <div className="flex items-center gap-5 p-4 bg-foreground/5 rounded-2xl border border-border/50">
                    <div className="p-4 bg-secondary/10 rounded-xl shrink-0">
                        <CheckCircle2 className="w-6 h-6 text-secondary" />
                    </div>
                    <div>
                        <p className="text-[10px] tracking-[0.2em] text-muted-foreground font-black uppercase whitespace-nowrap">Protocol Check-ins</p>
                        <p className="text-2xl font-black text-foreground uppercase">{stats.totalCheckIns}</p>
                    </div>
                </div>
            </div>

            {/* Achievements Section */}
            <div className="space-y-6 pt-4">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <Award size={14} className="text-muted-foreground" />
                        <h3 className="text-[10px] font-black uppercase tracking-widest text-muted-foreground">Unlocked Achievements</h3>
                    </div>
                    <p className="text-primary font-black text-[10px] uppercase tracking-widest bg-primary/10 px-3 py-1 rounded-full">
                        {stats.milestonesEarned} Milestones
                    </p>
                </div>
                <div className="grid grid-cols-4 gap-4">
                    <AchievementBox icon={<Flame className="w-6 h-6" />} active={true} label="Consistency" />
                    <AchievementBox icon={<Dumbbell className="w-6 h-6" />} active={true} label="Power" />
                    <AchievementBox icon={<Trophy className="w-6 h-6" />} active={false} label="Elite" />
                    <AchievementBox icon={<Target className="w-6 h-6" />} active={false} label="Precision" />
                </div>
            </div>
        </div>
    );
}

function AchievementBox({ icon, active, label }: { icon: React.ReactNode; active: boolean; label: string }) {
    return (
        <div className="flex flex-col items-center gap-2 group cursor-help">
            <div className={`aspect-square w-full rounded-2xl flex items-center justify-center border transition-all duration-300 ${active
                ? 'bg-primary/5 border-primary/30 text-primary shadow-lg shadow-primary/5'
                : 'bg-foreground/2 border-border text-muted-foreground/30 grayscale opacity-40 group-hover:opacity-60'
                }`}>
                {icon}
            </div>
            <span className={`text-[8px] font-black uppercase tracking-[0.15em] transition-colors ${active ? 'text-foreground' : 'text-muted-foreground/30'}`}>
                {label}
            </span>
        </div>
    );
}
