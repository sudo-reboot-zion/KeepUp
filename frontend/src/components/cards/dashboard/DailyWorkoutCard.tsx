/**
 * DailyWorkoutCard - Redesigned with Solana aesthetic
 */

import React from 'react';
import { DailyWorkout } from '@/types/dashboard.types';
import { Check, X, AlertCircle, Edit3, Clock, Activity } from 'lucide-react';
import { format } from 'date-fns';

interface DailyWorkoutCardProps {
  workout: DailyWorkout;
  onSelect?: () => void;
}

export default function DailyWorkoutCard({
  workout,
  onSelect,
}: DailyWorkoutCardProps) {
  const isCompleted = workout.status === 'completed';
  const isSkipped = workout.status === 'skipped';

  return (
    <div
      onClick={onSelect}
      className={`p-5 border transition-all duration-300 group ${onSelect ? 'cursor-pointer hover:border-primary/50 hover:bg-foreground/5' : ''
        } ${isCompleted ? 'bg-primary/5 border-primary/20' :
          isSkipped ? 'bg-red-500/5 border-red-500/20' :
            'bg-foreground/5 border-border'
        }`}
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[10px] font-bold uppercase tracking-widest text-primary">
              {workout.day_of_week}
            </span>
            <span className="text-[10px] font-mono text-muted-foreground">
              {format(new Date(workout.date), 'MMM dd')}
            </span>
          </div>
          <h4 className={`text-lg font-black tracking-tight ${isCompleted ? 'text-muted-foreground line-through' : 'text-foreground'}`}>
            {workout.planned_workout_type}
          </h4>
        </div>
        <div className="flex items-center gap-3">
          {isCompleted && <Check size={20} className="text-primary" />}
          {isSkipped && <X size={20} className="text-red-500" />}
          {workout.was_modified && (
            <div className="p-1.5 rounded bg-blue-500/10 border border-blue-500/20">
              <Edit3 size={14} className="text-blue-500" />
            </div>
          )}
        </div>
      </div>

      <div className="flex items-center gap-4 mb-4 text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
        <div className="flex items-center gap-1.5">
          <Clock size={12} />
          <span>{workout.planned_duration_minutes} MIN</span>
        </div>
        <div className="flex items-center gap-1.5">
          <Activity size={12} />
          <span>{workout.planned_intensity}</span>
        </div>
      </div>

      {workout.planned_exercises.length > 0 && (
        <div className="mb-4">
          <div className="flex flex-wrap gap-1.5">
            {workout.planned_exercises.slice(0, 3).map((exercise, idx) => (
              <span
                key={idx}
                className="text-[10px] font-bold uppercase tracking-widest bg-foreground/5 text-muted-foreground px-2 py-1 rounded border border-border"
              >
                {typeof exercise === 'string' ? exercise : exercise.name}
              </span>
            ))}
            {workout.planned_exercises.length > 3 && (
              <span className="text-[10px] font-bold text-muted-foreground mt-1">
                +{workout.planned_exercises.length - 3} MORE
              </span>
            )}
          </div>
        </div>
      )}

      {workout.was_modified && workout.modification_reason && (
        <div className="flex items-start gap-3 p-3 bg-blue-500/5 border border-blue-500/10 rounded">
          <AlertCircle size={14} className="text-blue-500 flex-shrink-0 mt-0.5" />
          <p className="text-[10px] font-medium text-blue-400 leading-relaxed">
            <span className="font-bold uppercase tracking-widest mr-1">Adjusted:</span>
            {workout.modification_reason}
          </p>
        </div>
      )}

      {workout.user_feedback && (
        <div className="mt-4 pt-4 border-t border-border">
          <p className="text-[10px] text-muted-foreground leading-relaxed">
            <span className="font-bold uppercase tracking-widest text-muted-foreground mr-2">Feedback:</span>
            {workout.user_feedback.how_felt}
            {workout.user_feedback.rpe && <span className="ml-2 text-primary">RPE {workout.user_feedback.rpe}/10</span>}
          </p>
        </div>
      )}
    </div>
  );
}
