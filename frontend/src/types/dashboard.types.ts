/**
 * Dashboard Types - Hierarchical Resolution Structure
 * Yearly Goal → Quarters → Weeks → Days
 */

export interface AgentModification {
  agent_name: string;
  modification_type: string;
  reason: string;
  modified_intensity?: string;
  timestamp: string;
}

export interface WorkoutContext {
  sleep_quality?: number;
  stress_level?: string;
  muscle_soreness?: string;
  energy_level?: string;
}

export interface UserFeedback {
  how_felt: string;
  rpe?: number; // Rate of Perceived Exertion (1-10)
  difficulty?: string;
  notes?: string;
}

export interface PlannedExercise {
  name: string;
  [key: string]: unknown;
}

export interface DailyWorkout {
  id: number;
  weekly_plan_id: number;
  resolution_id: number;
  date: string;
  day_of_week: string;
  planned_workout_type: string;
  planned_duration_minutes: number;
  planned_intensity: string;
  planned_target?: string;
  planned_exercises: (string | PlannedExercise)[];
  context?: Record<string, unknown>;
  was_modified: boolean;
  modification_reason?: string;
  modified_workout_type?: string;
  modified_duration_minutes?: number;
  modified_intensity?: string;
  modification_rationale?: string;
  status: string;
  actual_duration_minutes?: number;
  actual_intensity_perceived?: string;
  user_feedback?: UserFeedback;
  notes?: string;
  intensity_change: string;
  created_at: string;
  updated_at: string;
}

export interface Milestone {
  week: number;
  goal: string;
  description?: string;
}

export interface WeeklyPlan {
  id: number;
  quarterly_phase_id: number;
  resolution_id: number;
  week_number: number;
  quarter_week: number;
  week_start_date: string;
  week_end_date: string;
  target_workouts: number;
  target_duration_minutes: number;
  focus?: string;
  estimated_difficulty: string;
  intensity_progression?: string;
  risk_level: string;
  critical_week?: string;
  workouts_completed: number;
  workouts_planned: number;
  adherence_rate: number;
  total_minutes_completed: number;
  status: string;
  completion_percentage: number;
  remaining_workouts: number;
  created_at: string;
  updated_at: string;
}

export interface WeeklyPlanDetail extends WeeklyPlan {
  daily_workouts: DailyWorkout[];
  agent_reasoning?: Record<string, string>;
  protective_measures: string[];
}

export interface QuarterlyPhase {
  id: number;
  resolution_id: number;
  quarter: string; // "Q1", "Q2", "Q3", "Q4"
  week_start: number;
  week_end: number;
  phase_name: string;
  phase_description: string;
  focus_areas: string[];
  target_workouts: number;
  target_metric?: string;
  target_progression?: string;
  workouts_completed: number;
  adherence_rate: number;
  milestones: Milestone[];
  risk_factors: string[];
  protective_strategies: string[];
  status: string;
  completion_percentage: number;
  created_at: string;
  updated_at: string;
}

export interface QuarterlyPhaseDetail extends QuarterlyPhase {
  weekly_plans: WeeklyPlan[];
}

export interface YearlyGoalSummary {
  id: number;
  resolution_id: number;
  resolution_text: string;
  target_completion_date: string;
  current_week: number;
  total_weeks: number;
  progress_percentage: number;
  status: string;
  confidence_score?: number;
  created_at: string;
}

export interface DashboardResponse {
  yearly_goal: YearlyGoalSummary;
  quarterly_phases: QuarterlyPhase[];
  current_quarter?: QuarterlyPhaseDetail;
  current_week?: WeeklyPlanDetail;
  upcoming_weeks: WeeklyPlan[];
}

export interface QuarterDetailResponse {
  quarterly_phase: QuarterlyPhaseDetail;
}

export interface WeekDetailResponse {
  weekly_plan: WeeklyPlanDetail;
}

export interface WorkoutDetailResponse {
  daily_workout: DailyWorkout;
}

/**
 * API Request Types
 */
export interface CompleteWorkoutRequest {
  how_felt: string;
  rpe?: number;
  difficulty?: string;
  notes?: string;
}

export interface SkipWorkoutRequest {
  reason: string;
}
