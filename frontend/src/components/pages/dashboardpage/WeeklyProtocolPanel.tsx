'use client';

import React from 'react';
import {
  DailyWorkout,
  WeeklyPlanDetail
} from '@/types/dashboard.types';
import {
  Calendar,
  Zap,
  TrendingUp
} from 'lucide-react';
// import { format } from 'date-fns';

interface WeeklyProtocolPanelProps {
  currentWeek: WeeklyPlanDetail | null;
  onWorkoutSelect: (workout: DailyWorkout) => void;
}

/**
 * WeeklyProtocolPanel - Displays the current week's schedule and daily workouts.
 * Integrated as a panel within the main dashboard content.
 */
export default function WeeklyProtocolPanel({
  currentWeek,
  onWorkoutSelect,
}: WeeklyProtocolPanelProps) {
  const [selectedDay, setSelectedDay] = React.useState<string>(
    new Date().toLocaleDateString('en-US', { weekday: 'long' })
  );

  if (!currentWeek) {
    return (
      <div className="w-full lg:w-96 bg-muted/30 border border-border p-6 flex flex-col items-center justify-center text-center transition-colors duration-300">
        <Calendar size={40} className="text-muted-foreground mb-4" />
        <p className="text-muted-foreground text-sm font-bold uppercase tracking-widest">No Active Protocol</p>
      </div>
    );
  }

  const todayWorkout = currentWeek.daily_workouts.find(
    (w) => w.day_of_week === selectedDay
  );

  return (
    <div className="w-full lg:w-96 bg-background border-l border-border flex flex-col overflow-hidden transition-colors duration-300">
      {/* Panel Header */}
      <div className="p-6 border-b border-border bg-muted/20">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-black text-foreground uppercase tracking-widest">Weekly Protocol</h3>
          <span className="text-[10px] font-bold text-primary bg-primary/10 px-2 py-0.5 rounded border border-primary/20 uppercase tracking-widest">
            Week {currentWeek.week_number}
          </span>
        </div>

        {/* Day Selector */}
        <div className="flex items-center justify-between gap-1">
          {['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].map((day) => {
            const isSelected = day === selectedDay;
            const hasWorkout = currentWeek.daily_workouts.some(w => w.day_of_week === day);
            return (
              <button
                key={day}
                onClick={() => setSelectedDay(day)}
                className={`flex-1 flex flex-col items-center py-2 rounded transition-all ${isSelected ? 'bg-primary text-black' : 'text-muted-foreground hover:bg-foreground/5'
                  }`}
              >
                <span className="text-[10px] font-black uppercase">{day.substring(0, 1)}</span>
                {hasWorkout && !isSelected && <div className="w-1 h-1 rounded-full bg-primary mt-1" />}
              </button>
            );
          })}
        </div>
      </div>

      {/* Selected Day Details */}
      <div className="flex-1 overflow-y-auto custom-scrollbar p-6 space-y-6">
        {todayWorkout ? (
          <>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h4 className="text-xl font-black text-foreground tracking-tight">{todayWorkout.planned_workout_type}</h4>
                <div className="p-2 rounded bg-foreground/5 border border-foreground/10">
                  <Zap size={16} className="text-primary" />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="p-3 rounded bg-foreground/5 border border-foreground/5">
                  <p className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest mb-1">Duration</p>
                  <p className="text-sm font-bold text-foreground">{todayWorkout.planned_duration_minutes}m</p>
                </div>
                <div className="p-3 rounded bg-foreground/5 border border-foreground/5">
                  <p className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest mb-1">Intensity</p>
                  <p className="text-sm font-bold text-foreground">{todayWorkout.planned_intensity}</p>
                </div>
              </div>
            </div>

            <div className="space-y-3">
              <h5 className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest flex items-center gap-2">
                <TrendingUp size={12} className="text-secondary" />
                Protocol Focus
              </h5>
              <p className="text-xs text-muted-foreground leading-relaxed">
                {currentWeek.focus || "Focusing on consistent execution and metabolic adaptation for this phase."}
              </p>
            </div>

            <button
              onClick={() => onWorkoutSelect?.(todayWorkout)}
              className="w-full py-4 bg-foreground/5 border border-foreground/10 text-foreground text-xs font-black uppercase tracking-[0.2em] hover:bg-primary hover:text-black hover:border-primary transition-all"
            >
              Execute Protocol →
            </button>
          </>
        ) : (
          <div className="h-full flex flex-col items-center justify-center text-center opacity-50">
            <div className="w-12 h-12 rounded-full border border-dashed border-border flex items-center justify-center mb-4">
              <Zap size={20} className="text-muted-foreground" />
            </div>
            <p className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest">Rest & Recovery</p>
          </div>
        )}
      </div>

      {/* Weekly Metrics Footer */}
      <div className="p-6 border-t border-border bg-muted/10">
        <div className="flex items-center justify-between mb-4">
          <span className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest">Weekly Adherence</span>
          <span className="text-[10px] font-black text-foreground">{currentWeek.workouts_completed}/{currentWeek.target_workouts}</span>
        </div>
        <div className="w-full h-1 bg-foreground/5 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-primary to-secondary transition-all duration-1000"
            style={{ width: `${(currentWeek.workouts_completed / currentWeek.target_workouts) * 100}%` }}
          />
        </div>
      </div>
    </div>
  );
}
