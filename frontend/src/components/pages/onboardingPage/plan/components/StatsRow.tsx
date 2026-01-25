import type { FinalPlan } from '@/types/onboarding.types';

interface StatsRowProps {
    confidenceScore: number | null;
    finalPlan: FinalPlan;
}

export default function StatsRow({ confidenceScore, finalPlan }: StatsRowProps) {
    return (
        <div className="w-full border-t border-b border-[var(--border)] py-20 mb-32 plan-cta" style={{ fontFamily: 'var(--font-ppMontreal)' }}>
            <div className="grid grid-cols-1 md:grid-cols-4 divide-y md:divide-y-0 md:divide-x divide-[var(--border)]">
                <div className="px-8 py-6 md:py-0 text-center">
                    <div className="text-4xl md:text-6xl font-black mb-2 tracking-tighter">
                        {Math.round((confidenceScore || 0) * 100)}%
                    </div>
                    <div className="text-[var(--fg)] opacity-50 text-xs uppercase tracking-[0.2em] font-bold">AI Confidence</div>
                </div>

                <div className="px-8 py-6 md:py-0 text-center">
                    <div className="text-4xl md:text-6xl font-black mb-2 tracking-tighter">
                        {finalPlan.timeline_weeks || 12}W
                    </div>
                    <div className="text-[var(--fg)] opacity-50 text-xs uppercase tracking-[0.2em] font-bold">Plan Duration</div>
                </div>

                <div className="px-8 py-6 md:py-0 text-center">
                    <div className="text-4xl md:text-6xl font-black mb-2 tracking-tighter">
                        {finalPlan.weekly_schedule?.[0]?.workouts_per_week || 3}x
                    </div>
                    <div className="text-[var(--fg)] opacity-50 text-xs uppercase tracking-[0.2em] font-bold">Weekly Sessions</div>
                </div>

                <div className="px-8 py-6 md:py-0 text-center">
                    <div className="text-4xl md:text-6xl font-black mb-2 tracking-tighter text-[var(--primary)]">
                        READY
                    </div>
                    <div className="text-[var(--fg)] opacity-50 text-xs uppercase tracking-[0.2em] font-bold">Strategy Status</div>
                </div>
            </div>
        </div>
    );
}
