/**
 * WeeklyPlanCard - Redesigned with Solana aesthetic
 */

import React from 'react';
import { WeeklyPlan } from '@/types/dashboard.types';
import { AlertTriangle, Zap, Calendar } from 'lucide-react';
import { format } from 'date-fns';

interface WeeklyPlanCardProps {
  plan: WeeklyPlan;
  onSelect?: () => void;
}

export default function WeeklyPlanCard({
  plan,
  onSelect,
}: WeeklyPlanCardProps) {
  const progressPercentage = Math.round(plan.completion_percentage);

  const getRiskBadge = () => {
    if (plan.critical_week) {
      return (
        <div className="flex items-center gap-1 px-2 py-0.5 rounded bg-red-500/10 border border-red-500/20 text-red-500 text-[10px] font-bold uppercase tracking-widest">
          <AlertTriangle size={10} />
          Critical
        </div>
      );
    }

    if (plan.risk_level === 'high') {
      return (
        <div className="flex items-center gap-1 px-2 py-0.5 rounded bg-orange-500/10 border border-orange-500/20 text-orange-500 text-[10px] font-bold uppercase tracking-widest">
          <Zap size={10} />
          High Risk
        </div>
      );
    }

    return null;
  };

  return (
    <div
      onClick={onSelect}
      className={`p-4 border transition-all duration-300 group ${onSelect
        ? 'cursor-pointer hover:border-primary/50 hover:bg-foreground/5'
        : ''
        } bg-foreground/5 border-border`}
    >
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded bg-foreground/5 border border-foreground/10">
            <Calendar size={14} className="text-muted-foreground" />
          </div>
          <h5 className="font-bold text-foreground text-sm">
            Week {plan.week_number}
          </h5>
        </div>
        {getRiskBadge()}
      </div>

      <div className="space-y-2 mb-3">
        <div className="flex items-center justify-between text-[10px] font-bold uppercase tracking-widest">
          <span className="text-muted-foreground">Progress</span>
          <span className="text-foreground">{plan.workouts_completed}/{plan.target_workouts}</span>
        </div>
        <div className="w-full h-1 bg-foreground/5 rounded-full overflow-hidden">
          <div
            className={`h-full transition-all duration-500 ${progressPercentage === 100
              ? 'bg-primary'
              : 'bg-secondary'
              }`}
            style={{ width: `${progressPercentage}%` }}
          />
        </div>
      </div>

      <div className="flex items-center justify-between">
        <p className="text-[10px] text-muted-foreground font-mono uppercase">
          {format(new Date(plan.week_start_date), 'MMM dd')} — {format(new Date(plan.week_end_date), 'MMM dd')}
        </p>
        <span className="text-[10px] font-bold text-primary opacity-0 group-hover:opacity-100 transition-opacity">
          VIEW DETAILS →
        </span>
      </div>
    </div>
  );
}
