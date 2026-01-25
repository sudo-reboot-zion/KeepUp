/**
 * Centralized safety-related TypeScript types
 */

export interface BiometricCheckRequest {
    bp_systolic?: number;
    bp_diastolic?: number;
    resting_hr?: number;
    weight_kg?: number;
    // compatibility aliases used by components
    systolic?: number;
    diastolic?: number;
    heart_rate?: number;
    weight?: number;
    // allow indexing by string for analytics/logging helpers
    [key: string]: number | string | undefined;
}

export interface SafetyAlert {
    level: 'critical' | 'warning' | 'info' | 'low' | 'medium' | 'high';
    category?: string;
    message: string;
    action_required?: boolean;
    timestamp?: string;
    id?: string;
    type?: string;
    severity?: string;
}

export interface SafetyCheckResponse {
    resolution_id: number;
    alerts: SafetyAlert[];
    is_safe: boolean;
    confidence_score?: number;
    last_checked?: string;
}

export interface ConfidenceCheckRequest {
    score: number;
    recommendation_type?: string;
}

export interface ConfidenceCheckResponse {
    is_safe: boolean;
    confidence_score: number;
    alert_level?: string;
    message?: string;
    requires_disclaimer?: boolean;
}

export interface OverttrainingRiskRequest {
    proposed_workout_minutes?: number;
    proposed_intensity?: string;
    weekly_minutes_so_far?: number;
    high_intensity_this_week?: number;
    recovery_days_this_week?: number;
    // compatibility alias used in some places
    weekly_volume?: number;
}

export interface OverttrainingRiskResponse {
    risk_level: 'low' | 'medium' | 'high';
    is_safe: boolean;
    alerts: SafetyAlert[];
    recommendations?: string[];
    message?: string;
}

export interface MedicalThresholdsResponse {
    bp_critical_high: { systolic: number; diastolic: number };
    hr_critical_low: number;
    hr_critical_high: number;
    weight_weekly_change_max: number;
    vo2_max_reduction_threshold: number;
    recovery_score_minimum: number;
    blood_pressure_critical?: { systolic: number; diastolic: number };
    heart_rate_critical?: { min: number; max: number };
    weight_change_per_week?: number;
}

export interface AlertAcknowledgmentRequest {
    alert_type: string;
    category: string;
    message: string;
    action_taken: string;
    // some callers use alert_id instead of this shape
    alert_id?: number | string;
}

export interface AlertAcknowledgmentResponse {
    id: number;
    user_id: number;
    alert_type: string;
    acknowledged_at: string;
}

export interface SafetyReportResponse {
    resolution_id: number;
    timestamp: string;
    biometric_alerts: SafetyAlert[];
    confidence_alerts: SafetyAlert[];
    overtraining_alerts: SafetyAlert[];
    overall_safety_score: number;
    recommendations: string[];
}

// SafetyAlert already exported above
