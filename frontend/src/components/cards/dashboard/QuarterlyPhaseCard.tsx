'use client';

import React from 'react';
import { QuarterlyPhase, WeeklyPlan } from '@/types/dashboard.types';
import {
  ChevronDown,
  ChevronUp,
  AlertCircle,
  Target,
  Zap,
  Shield,
  BarChart3
} from 'lucide-react';

interface QuarterlyPhaseCardProps {
  phase: QuarterlyPhase;
  weeklyPlans: WeeklyPlan[];
  isExpanded?: boolean;
  onExpand?: () => void;
}

/**
 * QuarterlyPhaseCard - Redesigned with Solana aesthetic.
 * High contrast, grid-based, neon accents.
 */
export default function QuarterlyPhaseCard({
  phase,
  isExpanded = false,
  onExpand,
}: QuarterlyPhaseCardProps) {
  const completionPercentage = Math.round(phase.completion_percentage);



  return (
    <div className={`border border-border bg-card/80 backdrop-blur-sm relative group transition-all duration-300 ${isExpanded ? 'ring-1 ring-primary/30' : ''}`}>
      {/* Corner Accents */}
      <div className={`absolute top-0 left-0 w-2 h-2 border-t border-l border-primary/50 transition-opacity ${isExpanded ? 'opacity-100' : 'opacity-0 group-hover:opacity-100'}`} />
      <div className={`absolute top-0 right-0 w-2 h-2 border-t border-r border-primary/50 transition-opacity ${isExpanded ? 'opacity-100' : 'opacity-0 group-hover:opacity-100'}`} />

      <div
        className="flex flex-col md:flex-row md:items-center justify-between cursor-pointer p-6 gap-6"
        onClick={onExpand}
      >
        <div className="flex items-start gap-4 flex-1">
          <div className="mt-1 p-2 rounded bg-foreground/5 border border-foreground/10">
            <BarChart3 size={18} className="text-muted-foreground" />
          </div>
          <div className="flex flex-col gap-1">
            <div className="flex items-center gap-2">
              <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-primary">
                {phase.quarter} Protocol
              </span>
              <span className={`text-[10px] font-bold uppercase tracking-widest px-1.5 py-0.5 rounded border ${phase.status === 'completed' ? 'bg-primary/10 border-primary/20 text-primary' :
                phase.status === 'in-progress' ? 'bg-secondary/10 border-secondary/20 text-secondary' :
                  'bg-foreground/5 border-border text-muted-foreground'
                }`}>
                {phase.status}
              </span>
            </div>
            <h3 className="text-xl font-black text-foreground tracking-tight">
              {phase.phase_name}
            </h3>
            <p className="text-xs text-muted-foreground font-mono">
              WEEK {phase.week_start} — {phase.week_end}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-8">
          {/* Progress Mini-Bar */}
          <div className="flex flex-col gap-2 min-w-[120px]">
            <div className="flex items-center justify-between text-[10px] font-bold uppercase tracking-widest">
              <span className="text-muted-foreground">Adherence</span>
              <span className="text-foreground">{completionPercentage}%</span>
            </div>
            <div className="w-full h-1 bg-foreground/5 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-primary to-secondary transition-all duration-700"
                style={{ width: `${completionPercentage}%` }}
              />
            </div>
          </div>

          <div className="flex items-center gap-4">
            {phase.risk_factors.length > 0 && (
              <div className="flex items-center gap-1.5 px-2 py-1 rounded bg-red-500/10 border border-red-500/20 text-red-500">
                <AlertCircle size={14} />
                <span className="text-[10px] font-bold uppercase tracking-widest">{phase.risk_factors.length} Risks</span>
              </div>
            )}
            <div className="text-muted-foreground group-hover:text-foreground transition-colors">
              {isExpanded ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
            </div>
          </div>
        </div>
      </div>

      {isExpanded && (
        <div className="px-6 pb-6 pt-2 border-t border-border animate-in fade-in slide-in-from-top-2 duration-300">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-4">

            {/* Left Column: Description & Milestones */}
            <div className="space-y-6">
              <div>
                <h4 className="text-[10px] font-bold uppercase tracking-[0.2em] text-muted-foreground mb-3 flex items-center gap-2">
                  <Target size={12} className="text-primary" />
                  Strategic Objectives
                </h4>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {phase.phase_description}
                </p>
              </div>

              {phase.milestones.length > 0 && (
                <div>
                  <h4 className="text-[10px] font-bold uppercase tracking-[0.2em] text-muted-foreground mb-3">
                    Critical Milestones
                  </h4>
                  <div className="space-y-3">
                    {phase.milestones.map((milestone, idx) => (
                      <div
                        key={idx}
                        className="flex items-start gap-3 p-3 rounded bg-foreground/5 border border-border group/milestone hover:border-primary/30 transition-colors"
                      >
                        <div className="mt-0.5 w-5 h-5 rounded-full border border-border flex items-center justify-center text-[10px] font-bold text-muted-foreground group-hover/milestone:border-primary group-hover/milestone:text-primary transition-colors">
                          {milestone.week}
                        </div>
                        <div className="flex-1">
                          <p className="text-sm font-semibold text-foreground mb-0.5">{milestone.goal}</p>
                          {milestone.description && (
                            <p className="text-xs text-muted-foreground">{milestone.description}</p>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Right Column: Strategies & Metrics */}
            <div className="space-y-6">
              {phase.protective_strategies.length > 0 && (
                <div>
                  <h4 className="text-[10px] font-bold uppercase tracking-[0.2em] text-muted-foreground mb-3 flex items-center gap-2">
                    <Shield size={12} className="text-secondary" />
                    Protective Strategies
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {phase.protective_strategies.map((strategy, idx) => (
                      <span
                        key={idx}
                        className="text-[10px] font-bold uppercase tracking-widest px-3 py-1.5 rounded bg-secondary/10 border border-secondary/20 text-secondary"
                      >
                        {strategy}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 rounded bg-foreground/5 border border-border">
                  <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground mb-1">Target Metric</p>
                  <p className="text-sm font-bold text-foreground">{phase.target_metric || 'N/A'}</p>
                </div>
                <div className="p-4 rounded bg-foreground/5 border border-border">
                  <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground mb-1">Workouts</p>
                  <p className="text-sm font-bold text-foreground">{phase.workouts_completed} / {phase.target_workouts}</p>
                </div>
              </div>

              {phase.target_progression && (
                <div className="p-4 rounded bg-gradient-to-r from-primary/10 to-transparent border-l-2 border-primary">
                  <div className="flex items-center gap-2 mb-1">
                    <Zap size={14} className="text-primary" />
                    <span className="text-[10px] font-bold uppercase tracking-widest text-primary">Progression Logic</span>
                  </div>
                  <p className="text-xs text-muted-foreground">{phase.target_progression}</p>
                </div>
              )}
            </div>

          </div>
        </div>
      )}
    </div>
  );
}
