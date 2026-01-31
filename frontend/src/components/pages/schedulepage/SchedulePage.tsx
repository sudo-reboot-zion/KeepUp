'use client';

import React, { useEffect, useState } from 'react';
import {
    DashboardResponse,
    QuarterlyPhase,
    QuarterlyPhaseDetail,
    DailyWorkout,
} from '@/types/dashboard.types';
import { fetchDashboardHierarchy, fetchQuarterDetail } from '@/lib/dashboardApi';
import QuarterlyPhaseCard from '@/components/cards/dashboard/QuarterlyPhaseCard';
import WorkoutDetailModal from '@/components/cards/dashboard/WorkoutDetailModal';
import AppSidebar from '@/components/layout/AppSidebar';
import TopBar from '@/components/layout/TopBar';
import WeeklyProtocolPanel from '../dashboardpage/WeeklyProtocolPanel';
import { AlertCircle } from 'lucide-react';

/**
 * SchedulePage - Dedicated 52-week Transformation Schedule.
 * Moved from the main Dashboard to provide a focused view of the protocol.
 */
export default function SchedulePage() {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [dashboardData, setDashboardData] = useState<DashboardResponse | null>(null);
    const [expandedQuarter, setExpandedQuarter] = useState<string | null>(null);
    const [quarterDetails, setQuarterDetails] = useState<Record<string, QuarterlyPhaseDetail>>({});
    const [selectedWorkout, setSelectedWorkout] = useState<DailyWorkout | null>(null);

    const handleExpandQuarter = async (quarter: QuarterlyPhase) => {
        if (expandedQuarter === quarter.quarter) {
            setExpandedQuarter(null);
            return;
        }

        setExpandedQuarter(quarter.quarter);

        if (!quarterDetails[quarter.id]) {
            try {
                const detail = await fetchQuarterDetail(quarter.id.toString());
                setQuarterDetails(prev => ({
                    ...prev,
                    [quarter.id]: detail.quarterly_phase
                }));
            } catch (err) {
                console.error("Failed to fetch quarter details:", err);
            }
        }
    };

    useEffect(() => {
        const loadSchedule = async () => {
            try {
                setLoading(true);
                setError(null);
                const data = await fetchDashboardHierarchy();
                setDashboardData(data);

                if (data.current_quarter) {
                    setQuarterDetails(prev => ({
                        ...prev,
                        [data.current_quarter!.id]: data.current_quarter!
                    }));
                    setExpandedQuarter(data.current_quarter.quarter);
                } else {
                    setExpandedQuarter("Q1");
                }
            } catch (err) {
                const errorMessage = err instanceof Error ? err.message : 'Failed to load schedule';
                setError(errorMessage);
            } finally {
                setLoading(false);
            }
        };

        loadSchedule();
    }, []);

    if (loading) {
        return (
            <div className="flex h-screen bg-background transition-colors duration-300">
                <AppSidebar />
                <div className="flex-1 flex flex-col">
                    <TopBar />
                    <div className="flex-1 flex items-center justify-center">
                        <div className="flex flex-col items-center gap-6">
                            <div className="relative">
                                <div className="w-16 h-16 border-4 border-primary/20 border-t-primary rounded-full animate-spin" />
                                <div className="absolute inset-0 flex items-center justify-center">
                                    <div className="w-8 h-8 bg-primary/10 rounded-full animate-pulse" />
                                </div>
                            </div>
                            <p className="text-primary font-bold uppercase tracking-[0.2em] text-sm animate-pulse">
                                Synchronizing Schedule...
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex h-screen bg-background transition-colors duration-300">
                <AppSidebar />
                <div className="flex-1 flex flex-col">
                    <TopBar />
                    <div className="flex-1 flex items-center justify-center p-8">
                        <div className="max-w-md w-full p-8 border border-border bg-card rounded-lg text-center">
                            <AlertCircle size={48} className="text-red-500 mx-auto mb-4" />
                            <h3 className="text-xl font-bold text-foreground mb-2">Protocol Error</h3>
                            <p className="text-muted-foreground mb-6">{error}</p>
                            <button
                                onClick={() => window.location.reload()}
                                className="px-8 py-3 bg-red-500/10 border border-red-500/50 text-red-500 rounded-lg hover:bg-red-500/20 transition-all font-bold uppercase tracking-widest text-xs"
                            >
                                Retry Sync
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    if (!dashboardData) return null;

    const { quarterly_phases, current_week } = dashboardData;

    return (
        <div className="flex h-screen bg-background overflow-hidden transition-colors duration-300">
            <AppSidebar />

            <div className="flex-1 flex flex-col min-w-0">
                <TopBar />

                <main className="flex-1 flex flex-col lg:flex-row overflow-hidden">
                    {/* Left Panel: Quarterly Roadmap */}
                    <div className="flex-1 overflow-y-auto custom-scrollbar p-8">
                        <div className="max-w-4xl mx-auto">
                            <div className="flex items-center justify-between mb-8">
                                <div>
                                    <h2 className="text-2xl font-black text-foreground tracking-tight uppercase">52-Week Protocol</h2>
                                    <p className="text-muted-foreground text-sm">Full vision of your transformation journey.</p>
                                </div>
                                <div className="flex items-center gap-2 px-3 py-1.5 rounded bg-primary/5 border border-primary/20">
                                    <div className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse" />
                                    <span className="text-[10px] font-bold text-primary uppercase tracking-widest">Active Schedule</span>
                                </div>
                            </div>

                            <div className="space-y-6">
                                {quarterly_phases.map((phase) => (
                                    <QuarterlyPhaseCard
                                        key={phase.id}
                                        phase={quarterDetails[phase.id] || phase}
                                        weeklyPlans={quarterDetails[phase.id]?.weekly_plans || []}
                                        isExpanded={expandedQuarter === phase.quarter}
                                        onExpand={() => handleExpandQuarter(phase)}
                                    />
                                ))}
                            </div>
                        </div>
                    </div>

                    {/* Right Panel: Weekly Details */}
                    <WeeklyProtocolPanel
                        currentWeek={current_week ?? null}
                        onWorkoutSelect={setSelectedWorkout}
                    />
                </main>
            </div>

            {selectedWorkout && (
                <WorkoutDetailModal
                    workout={selectedWorkout}
                    isOpen={!!selectedWorkout}
                    onClose={() => setSelectedWorkout(null)}
                    onStatusUpdate={() => {
                        window.location.reload();
                    }}
                />
            )}
        </div>
    );
}
