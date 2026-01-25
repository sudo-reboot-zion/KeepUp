'use client';

import React from 'react';
import { DailyWorkout } from '@/types/dashboard.types';
import {
  X,
  AlertCircle,
  Zap,
  Clock,
  Activity,
  Target,
  Shield,
  MessageSquare,
  CheckCircle2,
  Circle
} from 'lucide-react';
import { format } from 'date-fns';
import { GridCell } from '@/components/layout/SolanaGrid';

interface WorkoutDetailModalProps {
  workout: DailyWorkout;
  isOpen: boolean;
  onClose: () => void;
  onStatusUpdate?: () => void;
}

/**
 * WorkoutDetailModal - Redesigned with Solana aesthetic.
 * High contrast, grid-based, neon accents.
 */
export default function WorkoutDetailModal({
  workout,
  isOpen,
  onClose
}: WorkoutDetailModalProps) {
  if (!isOpen) return null;

  const isCompleted = workout.status === 'completed';
  const isSkipped = workout.status === 'skipped';

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 md:p-8">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/60 backdrop-blur-md"
        onClick={onClose}
      />

      {/* Modal Container */}
      <div className="relative w-full max-w-4xl max-h-[90vh] overflow-hidden border border-border bg-background shadow-[0_0_50px_rgba(0,0,0,0.3)] flex flex-col transition-colors duration-300">

        {/* Decorative Grid Lines */}
        <div className="absolute inset-0 z-0 pointer-events-none opacity-10">
          <div
            className="absolute inset-0"
            style={{
              backgroundImage: `
                linear-gradient(to right, var(--border) 1px, transparent 1px),
                linear-gradient(to bottom, var(--border) 1px, transparent 1px)
              `,
              backgroundSize: '40px 40px'
            }}
          />
        </div>

        {/* Header */}
        <div className="relative z-10 flex items-center justify-between p-6 border-b border-border bg-muted/20">
          <div className="flex items-center gap-4">
            <div className={`p-3 rounded-lg border ${isCompleted ? 'bg-primary/10 border-primary/20 text-primary' :
              isSkipped ? 'bg-red-500/10 border-red-500/20 text-red-500' :
                'bg-foreground/5 border-border text-muted-foreground'
              }`}>
              {isCompleted ? <CheckCircle2 size={24} /> : isSkipped ? <AlertCircle size={24} /> : <Circle size={24} />}
            </div>
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-[10px] font-bold uppercase tracking-[0.3em] text-primary">
                  Protocol Execution
                </span>
                <span className="text-[10px] font-mono text-muted-foreground">
                  ID: {workout.id}
                </span>
              </div>
              <h2 className="text-2xl font-black text-foreground tracking-tight">
                {workout.planned_workout_type}
              </h2>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-foreground/5 rounded-full transition-colors text-muted-foreground hover:text-foreground"
          >
            <X size={24} />
          </button>
        </div>

        {/* Content Area */}
        <div className="relative z-10 flex-1 overflow-y-auto custom-scrollbar p-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

            {/* Left Column: Core Metrics */}
            <div className="lg:col-span-2 space-y-8">

              {/* Status & Timing Grid */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <GridCell title="Date" className="p-0">
                  <div className="p-4">
                    <p className="text-lg font-bold text-foreground">{format(new Date(workout.date), 'MMM dd, yyyy')}</p>
                    <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">{workout.day_of_week}</p>
                  </div>
                </GridCell>
                <GridCell title="Duration" className="p-0">
                  <div className="p-4">
                    <div className="flex items-center gap-2 text-foreground">
                      <Clock size={16} className="text-primary" />
                      <p className="text-lg font-bold">{workout.planned_duration_minutes}m</p>
                    </div>
                    <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">Planned</p>
                  </div>
                </GridCell>
                <GridCell title="Intensity" className="p-0">
                  <div className="p-4">
                    <div className="flex items-center gap-2 text-foreground">
                      <Activity size={16} className="text-secondary" />
                      <p className="text-lg font-bold">{workout.planned_intensity}</p>
                    </div>
                    <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">Target</p>
                  </div>
                </GridCell>
                <GridCell title="Status" className="p-0">
                  <div className="p-4">
                    <p className={`text-lg font-bold uppercase tracking-tight ${isCompleted ? 'text-primary' : isSkipped ? 'text-red-500' : 'text-muted-foreground'
                      }`}>
                      {workout.status}
                    </p>
                    <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">Current</p>
                  </div>
                </GridCell>
              </div>

              {/* Exercises Section */}
              <div>
                <h3 className="text-[10px] font-bold uppercase tracking-[0.2em] text-muted-foreground mb-4 flex items-center gap-2">
                  <Target size={14} className="text-primary" />
                  Planned Exercises
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {workout.planned_exercises.map((exercise, idx) => (
                    <div
                      key={idx}
                      className="p-4 bg-foreground/5 border border-border hover:border-primary/30 transition-colors group/exercise"
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-bold text-foreground">
                          {typeof exercise === 'string' ? exercise : exercise.name}
                        </span>
                        <div className="w-1.5 h-1.5 rounded-full bg-border group-hover/exercise:bg-primary transition-colors" />
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Agent Insights / Rationale */}
              {workout.modification_rationale && (
                <div className="p-6 bg-gradient-to-br from-secondary/10 to-transparent border-l-2 border-secondary">
                  <div className="flex items-center gap-2 mb-3">
                    <Zap size={16} className="text-secondary" />
                    <h4 className="text-[10px] font-bold uppercase tracking-[0.2em] text-secondary">
                      Agent Rationale
                    </h4>
                  </div>
                  <p className="text-sm text-muted-foreground leading-relaxed italic">
                    {workout.modification_rationale}
                  </p>
                </div>
              )}
            </div>

            {/* Right Column: Adjustments & Feedback */}
            <div className="space-y-8">

              {/* Modifications Section */}
              {workout.was_modified && (
                <div className="space-y-4">
                  <h3 className="text-[10px] font-bold uppercase tracking-[0.2em] text-muted-foreground flex items-center gap-2">
                    <Shield size={14} className="text-blue-500" />
                    System Adjustments
                  </h3>
                  <div className="p-5 bg-blue-500/5 border border-blue-500/20 space-y-4">
                    <div>
                      <p className="text-[10px] font-bold uppercase tracking-widest text-blue-400 mb-1">Reason</p>
                      <p className="text-xs text-foreground">{workout.modification_reason}</p>
                    </div>
                    {workout.modified_workout_type && (
                      <div>
                        <p className="text-[10px] font-bold uppercase tracking-widest text-blue-400 mb-1">New Protocol</p>
                        <p className="text-xs text-foreground">{workout.modified_workout_type}</p>
                      </div>
                    )}
                    <div className="flex items-center gap-4">
                      {workout.modified_duration_minutes && (
                        <div>
                          <p className="text-[10px] font-bold uppercase tracking-widest text-blue-400 mb-1">Duration</p>
                          <p className="text-xs text-foreground">{workout.modified_duration_minutes}m</p>
                        </div>
                      )}
                      {workout.modified_intensity && (
                        <div>
                          <p className="text-[10px] font-bold uppercase tracking-widest text-blue-400 mb-1">Intensity</p>
                          <p className="text-xs text-foreground">{workout.modified_intensity}</p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* User Feedback Section */}
              {workout.user_feedback && (
                <div className="space-y-4">
                  <h3 className="text-[10px] font-bold uppercase tracking-[0.2em] text-muted-foreground flex items-center gap-2">
                    <MessageSquare size={14} className="text-primary" />
                    Post-Session Data
                  </h3>
                  <div className="p-5 bg-primary/5 border border-primary/20 space-y-4">
                    <div>
                      <p className="text-[10px] font-bold uppercase tracking-widest text-primary mb-1">How You Felt</p>
                      <p className="text-xs text-foreground">{workout.user_feedback.how_felt}</p>
                    </div>
                    <div className="flex items-center gap-8">
                      <div>
                        <p className="text-[10px] font-bold uppercase tracking-widest text-primary mb-1">RPE</p>
                        <p className="text-lg font-black text-foreground font-mono">{workout.user_feedback.rpe}/10</p>
                      </div>
                      <div>
                        <p className="text-[10px] font-bold uppercase tracking-widest text-primary mb-1">Difficulty</p>
                        <p className="text-xs font-bold text-foreground uppercase">{workout.user_feedback.difficulty}</p>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Action Buttons */}
              {!isCompleted && !isSkipped && (
                <div className="space-y-3 pt-4">
                  <button className="w-full py-4 bg-primary text-black font-black uppercase tracking-widest text-xs hover:bg-primary/90 transition-all shadow-[0_0_20px_rgba(20,241,149,0.2)]">
                    Complete Session
                  </button>
                  <button className="w-full py-4 bg-foreground/5 border border-border text-foreground font-bold uppercase tracking-widest text-xs hover:bg-foreground/10 transition-all">
                    Skip Protocol
                  </button>
                </div>
              )}

            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="relative z-10 p-4 border-t border-border bg-muted/20 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-primary" />
              <span className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest">System Online</span>
            </div>
          </div>
          <p className="text-[10px] font-mono text-muted-foreground uppercase tracking-widest">
            KEEP-UP // PROTOCOL_V1.0
          </p>
        </div>

      </div>
    </div>
  );
}
